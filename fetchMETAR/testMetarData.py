# ---- Simple config (edit these or override via CLI) ----
STATIONS_DEFAULT = ["KDEN", "KATL", "KLAX", "KORD", "KSEA", "KBOS"]
DAYS_DEFAULT = 14

IEM_BASE = "https://mesonet.agron.iastate.edu/cgi-bin/request/asos.py"
FIELDS = ["tmpf", "sknt", "p01i", "precip_in"]  # temp F, wind kt, precip inches (hourly or total/fallback)


def parse_args_no_argparse(argv: List[str]) -> tuple[List[str], int]:
    """Minimal CLI: positional args => stations; --days N or --days=N to set days."""
    stations = []
    days = DAYS_DEFAULT
    i = 0
    while i < len(argv):
        tok = argv[i]
        if tok.startswith("--days="):
            try:
                days = int(tok.split("=", 1)[1])
            except ValueError:
                print("Ignoring invalid --days value.", file=sys.stderr)
        elif tok == "--days":
            if i + 1 < len(argv):
                try:
                    days = int(argv[i + 1])
                    i += 1
                except ValueError:
                    print("Ignoring invalid --days value.", file=sys.stderr)
            else:
                print("Ignoring --days with no value.", file=sys.stderr)
        elif tok.startswith("-"):
            print(f"Ignoring unknown option {tok}", file=sys.stderr)
        else:
            stations.append(tok.upper())
        i += 1
    if not stations:
        stations = [s.upper() for s in STATIONS_DEFAULT]
    return stations, days


def fetch_station_dataframe(station: str, start_utc: datetime, end_utc: datetime) -> pd.DataFrame:
    params = {
        "station": station.upper(),
        "data": ";".join(FIELDS),
        "tz": "Etc/UTC",
        "format": "onlycomma",
        "latlon": "no",
        "year1": start_utc.year,
        "month1": start_utc.month,
        "day1": start_utc.day,
        "hour1": start_utc.hour,
        "minute1": start_utc.minute,
        "year2": end_utc.year,
        "month2": end_utc.month,
        "day2": end_utc.day,
        "hour2": end_utc.hour,
        "minute2": end_utc.minute,
    }
    r = requests.get(IEM_BASE, params=params, timeout=60)
    r.raise_for_status()
    if not r.text.strip():
        return pd.DataFrame()
    df = pd.read_csv(io.StringIO(r.text))
    if df.empty or "valid" not in df.columns:
        return pd.DataFrame()
    df["valid"] = pd.to_datetime(df["valid"], utc=True)
    for col in FIELDS:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    if "p01i" in df.columns and df["p01i"].notna().any():
        df["precip_in_used"] = df["p01i"]
    elif "precip_in" in df.columns:
        df["precip_in_used"] = df["precip_in"]
    else:
        df["precip_in_used"] = pd.NA
    keep = ["valid", "tmpf", "sknt", "precip_in_used"]
    df = df[keep]
    df.rename(columns={"valid": "time_utc"}, inplace=True)
    df["station"] = station.upper()
    return df


def aggregate_06z_days(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return pd.DataFrame(columns=["station", "climate_day", "tmax_f", "tmin_f", "precip_in", "windmax_mph"])
    df = df.copy()
    df["climate_day"] = (df["time_utc"] - pd.Timedelta(hours=6)).dt.date
    df["wind_mph"] = df["sknt"] * 1.15078  # knots -> mph
    grouped = df.groupby(["station", "climate_day"], as_index=False).agg(
        tmax_f=("tmpf", "max"),
        tmin_f=("tmpf", "min"),
        precip_in=("precip_in_used", "sum"),
        windmax_mph=("wind_mph", "max"),
    )
    mask_all_missing_temp = grouped["tmax_f"].isna() & grouped["tmin_f"].isna()
    grouped = grouped.loc[not mask_all_missing_temp if isinstance(mask_all_missing_temp, bool) else ~mask_all_missing_temp]
    grouped["precip_in"] = grouped["precip_in"].fillna(0.0)
    for c in ("tmax_f", "tmin_f", "windmax_mph"):
        grouped[c] = grouped[c].round(1)
    grouped["precip_in"] = grouped["precip_in"].round(2)
    return grouped.reset_index(drop=True)


def build_output_table(agg: pd.DataFrame, stations: List[str], days: int) -> pd.DataFrame:
    if agg.empty:
        return pd.DataFrame()
    now = datetime.now(timezone.utc)
    current_label = (now - timedelta(hours=6)).date()  # exclude possibly incomplete current climate day
    agg = agg.loc[agg["climate_day"] != current_label].copy()
    recent_days = sorted(agg["climate_day"].unique())[-days:]
    agg = agg[agg["climate_day"].isin(recent_days)].copy()
    tidy = agg.set_index(["climate_day", "station"])[["tmax_f", "tmin_f", "precip_in", "windmax_mph"]]
    wide = tidy.unstack("station").sort_index(ascending=True)
    wide.columns = [f"{st}_{var}" for var, st in wide.columns]
    wide = wide.reset_index().rename(columns={"climate_day": "date_06Z_label"})
    ordered_cols = ["date_06Z_label"]
    var_order = ["tmax_f", "tmin_f", "precip_in", "windmax_mph"]
    for st in stations:
        for v in var_order:
            col = f"{st.upper()}_{v}"
            if col in wide.columns:
                ordered_cols.append(col)
    ordered_cols += [c for c in wide.columns if c not in ordered_cols]
    return wide[ordered_cols]


def main():
    stations, days = parse_args_no_argparse(sys.argv[1:])
    now = datetime.now(timezone.utc)
    # Pull a bit more than needed to ensure we capture all hours for N completed 06Z days
    start_utc = now - timedelta(days=days + 3)
    end_utc = now

    frames = []
    for st in stations:
        try:
            df = fetch_station_dataframe(st, start_utc, end_utc)
            if df.empty:
                print(f"Warning: no data for {st}", file=sys.stderr)
                continue
            frames.append(aggregate_06z_days(df))
        except Exception as e:
            print(f"Error {st}: {e}", file=sys.stderr)

    if not frames:
        print("No data available.")
        sys.exit(2)

    agg_all = pd.concat(frames, ignore_index=True)
    table = build_output_table(agg_all, stations, days)
    if table.empty:
        print("No aggregated results to display (insufficient observations).")
        sys.exit(3)

    pd.set_option("display.width", None)
    pd.set_option("display.max_columns", None)
    pd.set_option("display.max_rows", None)
    print(f"\n06Z–06Z Daily Stats (last completed {days} days)")
    print("Columns are per-station: _tmax_f, _tmin_f, _precip_in, _windmax_mph\n")
    print(table.to_string(index=False))


if __name__ == "__main__":
    main()

