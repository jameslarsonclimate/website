"""
Observed WxChallenge verification values (06Z-06Z day) from METARs.

Method follows what the WxChallenge manager (Brad Illston) described:
  * routine METARs from the Iowa State (IEM) ASOS service (report_type=3)
  * per hour: temperature (T-group tenths when present), sustained wind, hourly precip (Pxxxx)
  * 6-hour max/min groups (1snTTT / 2snTTT) also feed the daily max/min
  * daily: Tmax / Tmin, max sustained wind, precip sum
  * the NWS climate report (CLI) max wind speed, read a few hours after the day ends,
    is used as the official wind when available

Day convention: the day labelled D covers routine reports whose time rounded to the
nearest hour is in (D 06Z, D+1 06Z], i.e. the 0653Z ... 0553Z(+1 day) reports. The
xx53Z report nominally belongs to the next top of the hour, and the ~0553Z synoptic
report carries the 6-hr max/min and precip for 00-06Z.
"""

import io
import re
import time
from datetime import date, datetime, timedelta, timezone
from typing import Optional

import pandas as pd

IEM_ASOS = "https://mesonet.agron.iastate.edu/cgi-bin/request/asos.py"
IEM_AFOS = "https://mesonet.agron.iastate.edu/cgi-bin/afos/retrieve.py"
MPH_TO_KT = 0.868976

_RE_WIND = re.compile(r"\b(\d{3}|VRB)(\d{2,3})(?:G(\d{2,3}))?KT\b")
_RE_TGROUP = re.compile(r"\bT([01])(\d{3})([01])(\d{3})\b")
_RE_TEMP_BODY = re.compile(r"(?<![\w/])(M?\d{2})/(M?\d{2})?(?![\w/])")
_RE_P = re.compile(r"\bP(\d{4}|////)\b")
_RE_6 = re.compile(r"\b6(\d{4}|////)\b")
_RE_MAX6 = re.compile(r"\b1([01])(\d{3})\b")
_RE_MIN6 = re.compile(r"\b2([01])(\d{3})\b")


def c_to_f(c):
    return None if c is None else c * 9.0 / 5.0 + 32.0


def round_half_up(x):
    """Round like the verifiers do (0.5 -> away from zero), not banker's rounding."""
    if x is None or pd.isna(x):
        return None
    return int(x + 0.5) if x >= 0 else -int(-x + 0.5)


def _signed_tenths(sign, digits):
    v = int(digits) / 10.0
    return -v if sign == "1" else v


# ----------------------------------------------------------------------------
# METAR parsing
# ----------------------------------------------------------------------------
def parse_metar(metar: str) -> dict:
    """Pull out the fields WxChallenge needs from one METAR string."""
    out = {"temp_f": None, "wind_kt": None, "gust_kt": None, "precip_1h": None,
           "precip_6grp": None, "max6_f": None, "min6_f": None, "has_rmk": False}
    if not isinstance(metar, str):
        return out
    body, _, rmk = metar.partition(" RMK ")
    out["has_rmk"] = bool(rmk)

    m = _RE_WIND.search(body)
    if m:
        out["wind_kt"] = int(m.group(2))
        out["gust_kt"] = int(m.group(3)) if m.group(3) else None

    m = _RE_TGROUP.search(rmk)
    if m:
        out["temp_f"] = c_to_f(_signed_tenths(m.group(1), m.group(2)))
    else:
        m = _RE_TEMP_BODY.search(body)
        if m:
            t = m.group(1)
            out["temp_f"] = c_to_f(-int(t[1:]) if t.startswith("M") else int(t))

    # Hourly precip (hundredths). P0000 = trace. No P group in a routine ob = no precip.
    m = _RE_P.search(rmk)
    if m and m.group(1) != "////":
        v = int(m.group(1)) / 100.0
        out["precip_1h"] = v
        out["trace"] = (v == 0.0)
    m = _RE_6.search(rmk)
    if m and m.group(1) != "////":
        out["precip_6grp"] = int(m.group(1)) / 100.0

    m = _RE_MAX6.search(rmk)
    if m:
        out["max6_f"] = c_to_f(_signed_tenths(m.group(1), m.group(2)))
    m = _RE_MIN6.search(rmk)
    if m:
        out["min6_f"] = c_to_f(_signed_tenths(m.group(1), m.group(2)))
    return out


def day_label(ts: pd.Timestamp) -> date:
    """WxChallenge day for a report time (see module docstring)."""
    rounded = ts.round("h")
    return (rounded - timedelta(hours=6, minutes=1)).date()


def routine_only(df: pd.DataFrame) -> pd.DataFrame:
    """
    Keep one routine report per hour. IEM's report_type=3 already does this, but
    specials (SPECI) sneak in from other sources and their P groups are cumulative
    since the last routine ob, so summing them double counts precip. The routine
    minute is the site's most common minute (e.g. :53); per hour keep the report
    closest to it (within 10 minutes).
    """
    if df.empty:
        return df
    minutes = df["valid"].dt.minute
    routine_min = int(minutes.mode().iloc[0])
    target = df["valid"].dt.floor("h") + pd.to_timedelta(routine_min, unit="m")
    dist = (df["valid"] - target).abs()
    df = df.assign(_dist=dist, _slot=target)
    df = df[df["_dist"] <= pd.Timedelta(minutes=10)]
    df = df.sort_values("_dist").drop_duplicates("_slot").sort_values("valid")
    return df.drop(columns=["_dist", "_slot"])


def summarize_metars(df: pd.DataFrame) -> pd.DataFrame:
    """df has columns 'valid' (UTC) and 'metar'. Returns one row per WxChallenge day."""
    if df.empty:
        return pd.DataFrame()
    df = df.copy()
    df["valid"] = pd.to_datetime(df["valid"], utc=True)
    df = df.drop_duplicates("valid").sort_values("valid")
    # max sustained wind from every report (specials included): used when no CLI exists
    all_wind = pd.Series([parse_metar(m)["wind_kt"] for m in df["metar"]], index=df.index, dtype=float)
    all_day = pd.Series([day_label(t) for t in df["valid"]], index=df.index)
    wind_all = all_wind.groupby(all_day).max()
    df = routine_only(df)
    parsed = pd.DataFrame([parse_metar(m) for m in df["metar"]], index=df.index)
    df = pd.concat([df, parsed], axis=1)
    df["rounded"] = df["valid"].dt.round("h")
    df["day"] = [day_label(t) for t in df["valid"]]
    df["hour"] = df["rounded"].dt.hour

    rows = []
    for d, g in df.groupby("day"):
        # 6-hr groups only from the synoptic reports inside the day (12, 18, 00, 06-end)
        syn = g[g["hour"].isin([0, 6, 12, 18])]
        temps = pd.concat([g["temp_f"], syn["max6_f"], syn["min6_f"]]).dropna()
        tmax = max(g["temp_f"].max(skipna=True), syn["max6_f"].max(skipna=True))
        tmin = min(g["temp_f"].min(skipna=True), syn["min6_f"].min(skipna=True))
        if temps.empty:
            tmax = tmin = None

        precip_hourly = g["precip_1h"].fillna(0.0).sum()
        # 6RRRR groups are only reported when precip fell, so missing = 0
        six = syn["precip_6grp"].dropna()
        precip_six = six.sum() if syn["has_rmk"].sum() >= 4 else None
        n_hours = g["rounded"].nunique()
        precip = precip_hourly
        precip_source = "hourly P groups"
        # A missing hourly ob drops its precip; fall back to the synoptic 6-hr groups
        if n_hours < 24 and precip_six is not None and precip_six > precip_hourly:
            precip, precip_source = precip_six, "6-hr groups"
        trace = bool((g["precip_1h"] == 0.0).any()) and precip == 0.0

        rows.append({
            "date": d.isoformat(),
            "tmax_f_raw": None if tmax is None or pd.isna(tmax) else round(float(tmax), 1),
            "tmin_f_raw": None if tmin is None or pd.isna(tmin) else round(float(tmin), 1),
            "tmax_f": round_half_up(tmax) if tmax is not None else None,
            "tmin_f": round_half_up(tmin) if tmin is not None else None,
            "wind_max_kt_metar": None if g["wind_kt"].isna().all() else int(g["wind_kt"].max()),
            "gust_max_kt_metar": None if g["gust_kt"].isna().all() else int(g["gust_kt"].max()),
            "wind_max_kt_all_reports": None if pd.isna(wind_all.get(d)) else int(wind_all.get(d)),
            "precip_in": round(float(precip), 2),
            "precip_trace": trace,
            "precip_source": precip_source,
            "precip_6hr_groups_in": None if precip_six is None else round(float(precip_six), 2),
            "n_routine_obs": int(n_hours),
            "complete": bool(n_hours >= 20),   # allow a few missing hourly obs
        })
    return pd.DataFrame(rows)


def fetch_metars(station: str, start: datetime, end: datetime, retries: int = 3) -> pd.DataFrame:
    """Routine METARs from IEM in [start, end] (UTC)."""
    import requests
    params = {
        "network": "ASOS", "station": station, "data": "metar",
        "year1": start.year, "month1": start.month, "day1": start.day,
        "hour1": start.hour, "minute1": 0,
        "year2": end.year, "month2": end.month, "day2": end.day,
        "hour2": end.hour, "minute2": 59,
        "tz": "Etc/UTC", "format": "onlycomma", "latlon": "no", "elev": "no",
        "missing": "M", "trace": "T", "direct": "no", "report_type": 3,
    }
    last = None
    for attempt in range(retries):
        try:
            r = requests.get(IEM_ASOS, params=params, timeout=60)
            r.raise_for_status()
            if r.text.startswith("ERROR"):
                raise RuntimeError(r.text[:200])
            df = pd.read_csv(io.StringIO(r.text))
            return df[["valid", "metar"]] if not df.empty else df
        except Exception as exc:
            last = exc
            time.sleep(3 * (attempt + 1))
    raise RuntimeError(f"IEM METAR request failed for {station}: {last}")


# ----------------------------------------------------------------------------
# NWS daily climate report (CLI)
# ----------------------------------------------------------------------------
_MONTHS = {m: i for i, m in enumerate(
    ["JANUARY", "FEBRUARY", "MARCH", "APRIL", "MAY", "JUNE", "JULY", "AUGUST",
     "SEPTEMBER", "OCTOBER", "NOVEMBER", "DECEMBER"], start=1)}
_RE_CLI_DATE = re.compile(r"CLIMATE SUMMARY FOR\s+([A-Z]+)\s+(\d{1,2})\s+(\d{4})")
_RE_CLI_WIND = re.compile(r"HIGHEST WIND SPEED\s+(\d+|MM)")
_RE_CLI_GUST = re.compile(r"HIGHEST GUST SPEED\s+(\d+|MM)")
_RE_CLI_MAX = re.compile(r"^\s*MAXIMUM\s+(-?\d+|MM)", re.M)
_RE_CLI_MIN = re.compile(r"^\s*MINIMUM\s+(-?\d+|MM)", re.M)


def parse_cli(text: str) -> dict:
    """Parse one or more CLI products. Returns {date_iso: {...}} preferring final reports."""
    out = {}
    starts = [m.start() for m in _RE_CLI_DATE.finditer(text)]
    for i, s in enumerate(starts):
        seg = text[s: starts[i + 1] if i + 1 < len(starts) else len(text)]
        m = _RE_CLI_DATE.search(seg)
        month = _MONTHS.get(m.group(1))
        if not month:
            continue
        d = date(int(m.group(3)), month, int(m.group(2))).isoformat()
        prelim = "VALID TODAY AS OF" in seg
        def num(rx):
            mm = rx.search(seg)
            return None if not mm or mm.group(1) == "MM" else int(mm.group(1))
        rec = {"cli_wind_mph": num(_RE_CLI_WIND), "cli_gust_mph": num(_RE_CLI_GUST),
               "cli_tmax_f": num(_RE_CLI_MAX), "cli_tmin_f": num(_RE_CLI_MIN),
               "cli_preliminary": prelim}
        if rec["cli_wind_mph"] is not None:
            rec["cli_wind_kt"] = round_half_up(rec["cli_wind_mph"] * MPH_TO_KT)
        # IEM lists newest first: keep the first final report; a prelim only if nothing else
        if d not in out or (out[d]["cli_preliminary"] and not prelim):
            out[d] = rec
    return out


def fetch_cli(pil: str, limit: int = 30) -> dict:
    import requests
    if not pil:
        return {}
    r = requests.get(IEM_AFOS, params={"pil": pil, "fmt": "text", "limit": limit}, timeout=60)
    r.raise_for_status()
    return parse_cli(r.text)


# ----------------------------------------------------------------------------
# Public entry point
# ----------------------------------------------------------------------------
def last_complete_day(now: datetime) -> date:
    """Most recent WxChallenge day whose 06Z end (+10 min for the 0553Z ob) has passed."""
    return (now - timedelta(hours=6, minutes=10)).date() - timedelta(days=1)


def get_observations(station, days_back: int = 3, now: Optional[datetime] = None,
                     first: Optional[date] = None, last: Optional[date] = None) -> list:
    """
    Observed values for completed WxChallenge days, either the last `days_back`
    days or the explicit range [first, last]. `station` is a wxc_stations.Station.
    Returns a list of dicts (one per day).
    """
    now = now or datetime.now(timezone.utc)
    last_complete = min(last or last_complete_day(now), last_complete_day(now))
    first = first or last_complete - timedelta(days=days_back - 1)
    if first > last_complete:
        return []
    days_back = (last_complete - first).days + 1
    start = datetime(first.year, first.month, first.day, 6, tzinfo=timezone.utc)
    end = min(now, datetime(last_complete.year, last_complete.month, last_complete.day,
                            6, tzinfo=timezone.utc) + timedelta(days=1, minutes=30))
    daily = summarize_metars(fetch_metars(station.icao, start, end))
    if daily.empty:
        return []
    daily = daily[(daily["date"] >= first.isoformat()) & (daily["date"] <= last_complete.isoformat())]

    cli = {}
    try:
        # IEM returns the newest CLI products first; ~2-3 per day (prelim + final + corrections)
        age = (last_complete_day(now) - first).days + 1
        cli = fetch_cli(station.cli_pil, limit=max(10, 3 * age + 3))
    except Exception as exc:
        print(f"CLI fetch failed ({station.cli_pil}): {exc}")

    fetched = now.replace(microsecond=0).isoformat()
    records = []
    for rec in daily.to_dict("records"):
        rec.update({"station": station.icao, "fetched_at_utc": fetched})
        c = cli.get(rec["date"], {})
        rec.update(c)
        # Official-style wind: CLI max sustained wind when available, else METAR max
        if c.get("cli_wind_kt") is not None:
            rec["wind_max_kt"], rec["wind_source"] = c["cli_wind_kt"], "CLI"
        else:
            w = rec.get("wind_max_kt_all_reports")
            w = rec["wind_max_kt_metar"] if w is None else max(w, rec["wind_max_kt_metar"] or 0)
            rec["wind_max_kt"], rec["wind_source"] = w, "METAR (no CLI)"
        records.append(rec)
    return records
