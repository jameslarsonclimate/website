"""
MOS / NBM text guidance.

  GFS  -> GFS MOS (MAV), 00/06/12/18Z, 3-hourly, from the Iowa State Mesonet MOS API
              https://mesonet.agron.iastate.edu/api/1/mos.json?station=KTPA&model=GFS
  NBS  -> National Blend of Models short-range text (NBS), every hourly cycle, 3-hourly rows,
          read from the NBM bucket on AWS (wxc_nbm_text.py; IEM keeps only 00/06/12/18Z)

Daily (06Z-06Z) summary for WxChallenge day D:
  tmax  = max(X from the D+1 00Z row, hourly-ish TMP in the window)
  tmin  = min(N from the D 12Z row, TMP in the window)
  wind  = max WSP (kt) in the window
  precip:
    NBS  Q06 is a QPF amount in hundredths of an inch -> summed
    MOS  Q06 is a QPF *category*; converted with category midpoints (rough; the
         verification bias correction will learn how this behaves at each site)
"""

import functools
from datetime import date, datetime, timedelta, timezone
from typing import Optional

import pandas as pd

import wxc_cache
import wxc_nbm_text
import wxc_pop

IEM_MOS = "https://mesonet.agron.iastate.edu/api/1/mos.json"

# MOS 6-h / 12-h QPF categories -> representative amount (inches)
# 0: none, 1: 0.01-0.09, 2: 0.10-0.24, 3: 0.25-0.49, 4: 0.50-0.99, 5: 1.00-1.99, 6: >=2.00
QPF_CATEGORY_IN = {0: 0.0, 1: 0.05, 2: 0.17, 3: 0.37, 4: 0.75, 5: 1.25, 6: 2.25}

MOS_PRODUCTS = {
    # label in payload : IEM model name
    "GFS_MOS": "GFS",
    "NBM": "NBS",
}


@functools.lru_cache(maxsize=32)
def fetch_mos(station: str, model: str, runtime: Optional[datetime] = None) -> pd.DataFrame:
    """One run's rows (runtime None: the newest). Kept for the rest of the script run, so the target
    day and the today-so-far figure share one request (callers must not modify the frame:
    summarize_mos copies). NBS comes from AWS in the same shape as IEM's rows."""
    if model == "NBS":
        return (wxc_nbm_text.newest(station, "nbs") if runtime is None
                else wxc_nbm_text.fetch(station, "nbs", runtime))
    import requests
    params = {"station": station, "model": model}
    if runtime is not None:
        params["runtime"] = runtime.strftime("%Y-%m-%dT%H:%MZ")
    r = requests.get(IEM_MOS, params=params, timeout=60)
    r.raise_for_status()
    rows = r.json().get("data", [])
    return pd.DataFrame(rows)


def _ts(col):
    t = pd.to_datetime(col)
    return t.dt.tz_localize("UTC") if t.dt.tz is None else t.dt.tz_convert("UTC")


def summarize_mos(df: pd.DataFrame, target_day: date, model: str) -> dict:
    """Summarize one MOS run (rows from the IEM API) for WxChallenge day `target_day`."""
    empty = {"tmax_f": None, "tmin_f": None, "wind_max_kt": None, "precip_in": None,
             "init_time_utc": None, "valid_range_utc": None}
    if df is None or df.empty:
        return {**empty, "error": "no MOS rows"}
    df = df.copy()
    df["ft"] = _ts(df["ftime_utc"] if "ftime_utc" in df else df["ftime"])
    rt = _ts(df["runtime_utc"] if "runtime_utc" in df else df["runtime"])
    df["rt"] = rt
    # keep only the newest run if several are present
    df = df[df["rt"] == df["rt"].max()]
    runtime = df["rt"].iloc[0]

    start = pd.Timestamp(datetime(target_day.year, target_day.month, target_day.day, 6), tz="UTC")
    end = start + pd.Timedelta(hours=24)
    win = df[(df["ft"] >= start) & (df["ft"] <= end)]
    if win.empty or df["ft"].max() < end:
        return {**empty, "init_time_utc": runtime.strftime("%Y-%m-%dT%H"),
                "error": f"run does not cover {start:%Y-%m-%d %HZ}-{end:%Y-%m-%d %HZ}"}

    xn_col = "txn" if model == "NBS" else "n_x"
    def val_at(ts, col):
        row = df[df["ft"] == ts]
        if row.empty or col not in row or pd.isna(row[col].iloc[0]):
            return None
        return float(row[col].iloc[0])

    tmp = pd.to_numeric(win.get("tmp"), errors="coerce").dropna()
    x = val_at(end - pd.Timedelta(hours=6), xn_col)        # D+1 00Z row: daytime max
    n = val_at(start + pd.Timedelta(hours=6), xn_col)      # D 12Z row: overnight min
    tmax_cands = [v for v in [x, tmp.max() if not tmp.empty else None] if v is not None]
    tmin_cands = [v for v in [n, tmp.min() if not tmp.empty else None] if v is not None]

    wsp = pd.to_numeric(win.get("wsp"), errors="coerce").dropna()

    q = win[(win["ft"] > start) & win["ft"].dt.hour.isin([0, 6, 12, 18])]
    q06 = pd.to_numeric(q["q06"], errors="coerce").dropna() if "q06" in q else pd.Series(dtype=float)
    precip, note = None, None
    if len(q06) >= 4:
        if model == "NBS":
            precip = float(q06.sum()) / 100.0
            note = "NBS Q06 amounts"
        else:
            precip = float(sum(QPF_CATEGORY_IN.get(int(c), 0.0) for c in q06))
            note = f"MOS Q06 categories {list(map(int, q06))} -> midpoints"
    p06 = pd.to_numeric(q.get("p06"), errors="coerce").dropna() if "p06" in q else pd.Series(dtype=float)
    # PoP: P06 at 12, 18, 00 and 06Z is the chance of >= 0.01" in the 6 h ending then (display
    # only). No P24, and P12 ends at 00/12Z, so the 24-h PoP is only bounded by the four P06s.
    blocks = {}
    if "p06" in q:
        for ft, v in zip(q["ft"], pd.to_numeric(q["p06"], errors="coerce")):
            if not pd.isna(v):
                blocks[wxc_pop.block_of_hour_ending(ft)] = float(v) / 100.0
    pop = wxc_pop.record(None, blocks, basis=f"{'NBS' if model == 'NBS' else 'GFS MOS'} P06", bounds=True)

    return {
        "tmax_f": round(max(tmax_cands), 1) if tmax_cands else None,
        "tmin_f": round(min(tmin_cands), 1) if tmin_cands else None,
        "wind_max_kt": round(float(wsp.max()), 1) if not wsp.empty else None,
        "precip_in": round(precip, 2) if precip is not None else None,
        "pop06_max_pct": int(p06.max()) if not p06.empty else None,
        "pop": pop,
        "precip_note": note,
        "init_time_utc": runtime.strftime("%Y-%m-%dT%H"),
        "valid_range_utc": [start.strftime("%Y-%m-%dT%H"), end.strftime("%Y-%m-%dT%H")],
        "series": {
            "times": [t.strftime("%Y-%m-%dT%H:%M") for t in win["ft"]],
            "tmp_f": [None if pd.isna(v) else float(v) for v in pd.to_numeric(win.get("tmp"), errors="coerce")],
            "wsp_kt": [None if pd.isna(v) else float(v) for v in pd.to_numeric(win.get("wsp"), errors="coerce")],
            # display only (the page's dewpoint panel)
            "dpt_f": ([None if pd.isna(v) else float(v) for v in pd.to_numeric(win["dpt"], errors="coerce")]
                      if "dpt" in win else None),
        },
    }


# cycle hours and typical availability delay (hours) of each IEM text product
# (NBS: every hourly cycle from AWS, see wxc_nbm_text.candidate_runtimes)
MOS_CYCLES = {"GFS": ([0, 6, 12, 18], 4.5)}   # (NAM MOS removed: retired Oct 2026)


def candidate_runtimes(model: str, as_of: datetime, n: int = 3) -> list:
    """The n newest runs of `model` that were available at `as_of` (newest first)."""
    if model == "NBS":
        return wxc_nbm_text.candidate_runtimes(as_of, n)
    hours, delay = MOS_CYCLES[model]
    t = pd.Timestamp(as_of).tz_convert("UTC") if pd.Timestamp(as_of).tzinfo else pd.Timestamp(as_of, tz="UTC")
    t = (t - pd.Timedelta(hours=delay)).floor("h")
    out = []
    while len(out) < n:
        if t.hour in hours:
            out.append(t.to_pydatetime())
        t -= pd.Timedelta(hours=1)
    return out


def get_mos_forecasts(station: str, target_day: date, as_of: Optional[datetime] = None,
                      only: Optional[list] = None) -> dict:
    """
    GFS MOS and NBM (NBS) summaries for the target day.
    Live (as_of=None): the newest run, falling back to older runs if it doesn't cover
    the day. Hindcast (as_of set): the newest run that was out at `as_of`.
    """
    out = {}
    for label, model in MOS_PRODUCTS.items():
        if only is not None and label not in only:
            continue
        res = None
        try:
            tries = ([None] if as_of is None else []) + candidate_runtimes(
                model, as_of or datetime.now(timezone.utc))
            for rt in tries:
                if rt is not None:              # a specific run: maybe saved by an earlier script run
                    hit = wxc_cache.load(station, label, rt, target_day)
                    if hit is not None:
                        res = hit
                        break
                df = fetch_mos(station, model, rt)
                res = summarize_mos(df, target_day, model)
                if not res.get("error"):
                    wxc_cache.save(station, label, res["init_time_utc"] + ":00", target_day, res)
                    break
        except Exception as exc:
            res = {"tmax_f": None, "tmin_f": None, "wind_max_kt": None, "precip_in": None,
                   "init_time_utc": None, "valid_range_utc": None, "error": str(exc)}
        out[label] = res
        status = res.get("error") or f"{res['tmax_f']}/{res['tmin_f']}F {res['wind_max_kt']}kt {res['precip_in']}in"
        print(f"  {label:8s} {res.get('init_time_utc')}: {status}")
    return out
