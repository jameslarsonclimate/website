"""
Cloud cover (0-100 %) for the forecast and "today so far" figures. DISPLAY ONLY.

Nothing here feeds the scored values, the consensus, verification, runs.jsonl,
observations.jsonl or the series files. Model cloud cover lives in its own cache files,
    cache/{ICAO}/_cloud_{MODEL}_{YYYYMMDDHH}.json      (one per model run)
next to (never inside) the point-forecast results, so MODEL_VERSIONS is untouched and
older cached forecasts stay valid; a run without a cloud file is extracted separately.

Sources:
  HRRR, RRFS, GFS  TCDC, entire atmosphere (GRIB, see fetch_cloud_grib in the main script)
  IFS, AIFS        tcc (0-1 fraction -> %)
  ENS, AIFS_ENS,   Open-Meteo ensemble members' mean cloud_cover (%), saved with the run by
  GEFS             wxc_ens (only from when it was kept: Open-Meteo serves only the latest run)
  NBM              NBS SKY row (%)
  GFS_MOS          MAV CLD categories -> % (drawn as steps)
  USL              the run page's "Sky Cover" column (%)
  METAR            highest-coverage layer -> %
  GOES             ABI Clear Sky Mask fraction near the station (wxc_goes.py)
"""

import json
import re
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from typing import Optional

import numpy as np
import pandas as pd

import wxc_cache

CLOUDS_ENABLED = True      # set False to leave the cloud panels (and all cloud downloads) out
GOES_ENABLED = True        # set False to skip the GOES Clear Sky Mask (today-so-far figure)

# METAR layer cover -> % (VV = sky obscured). CLR/SKC are flagged so the figure can
# draw them differently: an automated CLR only means nothing below 12,000 ft.
METAR_COVER_PCT = {"CLR": 0, "SKC": 0, "NCD": 0, "NSC": 0,
                   "FEW": 19, "SCT": 44, "BKN": 75, "OVC": 100, "VV": 100}
METAR_CLEAR = {"CLR", "SKC"}
# GFS MOS (MAV) CLD categories -> %
MOS_CLD_PCT = {"CL": 0, "FW": 19, "SC": 44, "BK": 75, "OV": 100}

TEXT_MODELS = {"GFS_MOS": "GFS", "NBM": "NBS", "USL": None}   # our label -> IEM MOS model
_RE_SKY = re.compile(r"(?<![\w/])(CLR|SKC|NCD|NSC|FEW|SCT|BKN|OVC|VV)(\d{3}|///)?(?:CB|TCU)?(?![\w])")


def _t(x) -> str:
    return pd.Timestamp(x).strftime("%Y-%m-%dT%H:%M")


# ----------------------------------------------------------------------------
# conversions
# ----------------------------------------------------------------------------
def sky_pct(codes) -> tuple:
    """Layer codes of one METAR (e.g. ['FEW', 'BKN', 'M']) -> (% from the highest-coverage
    layer, clear flag). (None, False) when no layer is reported."""
    best, clear = None, False
    for c in codes:
        if not isinstance(c, str):
            continue
        c = c.strip().upper()
        if c not in METAR_COVER_PCT:
            continue
        pct = METAR_COVER_PCT[c]
        if best is None or pct > best:
            best = pct
        clear = clear or c in METAR_CLEAR
    return best, bool(clear and best == 0)


def metar_sky_codes(metar: str) -> list:
    """Layer codes from the body of a METAR string (used when IEM's skyc columns are absent)."""
    if not isinstance(metar, str):
        return []
    body = metar.partition(" RMK ")[0]
    return [m.group(1) for m in _RE_SKY.finditer(body)]


def sky_series(raw: pd.DataFrame) -> pd.DataFrame:
    """IEM reports (valid, skyc1-4 and/or metar) -> valid, sky_pct, clear. Reports that
    carry no sky condition are dropped."""
    cols = ["valid", "sky_pct", "clear"]
    if raw is None or raw.empty:
        return pd.DataFrame(columns=cols)
    df = raw.copy()
    df["valid"] = pd.to_datetime(df["valid"], utc=True)
    df = df.drop_duplicates("valid").sort_values("valid")
    sky_cols = [c for c in ("skyc1", "skyc2", "skyc3", "skyc4") if c in df]
    rows = []
    for _, r in df.iterrows():
        codes = [r[c] for c in sky_cols] if sky_cols else []
        if not any(isinstance(c, str) and c.strip().upper() in METAR_COVER_PCT for c in codes):
            codes = metar_sky_codes(r.get("metar"))
        pct, clear = sky_pct(codes)
        if pct is not None:
            rows.append((r["valid"], float(pct), clear))
    return pd.DataFrame(rows, columns=cols)


def mos_cld_pct(cat) -> Optional[float]:
    if not isinstance(cat, str):
        return None
    v = MOS_CLD_PCT.get(cat.strip().upper())
    return None if v is None else float(v)


def mos_cloud(df: pd.DataFrame, model: str) -> Optional[dict]:
    """Cloud series of the newest run in IEM MOS rows: GFS MOS CLD categories (steps),
    NBS SKY percentages (line)."""
    if df is None or df.empty:
        return None
    from wxc_mos import _ts
    df = df.copy()
    df["ft"] = _ts(df["ftime_utc"] if "ftime_utc" in df else df["ftime"])
    df["rt"] = _ts(df["runtime_utc"] if "runtime_utc" in df else df["runtime"])
    df = df[df["rt"] == df["rt"].max()].sort_values("ft")
    if model == "GFS":
        vals = [mos_cld_pct(c) for c in df.get("cld", pd.Series([None] * len(df)))]
    else:
        vals = [None if pd.isna(v) else float(v)
                for v in pd.to_numeric(df.get("sky", pd.Series([None] * len(df))), errors="coerce")]
    if all(v is None for v in vals):
        return None
    return {"init_time_utc": df["rt"].iloc[0].strftime("%Y-%m-%dT%H"),
            "times": [_t(t) for t in df["ft"]], "cloud_pct": vals,
            "step": model == "GFS", "source": "MOS CLD" if model == "GFS" else "NBS SKY"}


# ----------------------------------------------------------------------------
# cloud cache (separate from the point-forecast results)
# ----------------------------------------------------------------------------
def cloud_path(station: str, model: str, init) -> Path:
    return wxc_cache.CACHE_DIR / station.upper() / f"_cloud_{model}_{pd.Timestamp(init):%Y%m%d%H}.json"


def load_cloud(station: str, model: str, init) -> Optional[dict]:
    if not wxc_cache.ENABLED:
        return None
    try:
        return json.loads(cloud_path(station, model, init).read_text())
    except (FileNotFoundError, json.JSONDecodeError):
        return None


def save_cloud(station: str, model: str, init, rec: dict):
    if not wxc_cache.ENABLED:
        return
    p = cloud_path(station, model, init)
    p.parent.mkdir(parents=True, exist_ok=True)
    tmp = p.with_suffix(".tmp")
    tmp.write_text(json.dumps(rec))
    tmp.replace(p)


def merge(old: Optional[dict], new: dict) -> dict:
    """Union of two cloud records of one run, by valid time (new values win). Only finite
    values are kept, so hours that failed are tried again next time."""
    rows = {}
    for rec in (old or {}), new:
        avg = rec.get("averaged") or [False] * len(rec.get("times", []))
        for t, v, a in zip(rec.get("times", []), rec.get("cloud_pct", []), avg):
            if v is not None and np.isfinite(v):
                rows[t] = (round(float(min(max(v, 0.0), 100.0)), 1), bool(a))
    out = {k: v for k, v in {**(old or {}), **new}.items() if k not in ("times", "cloud_pct", "averaged")}
    ts = sorted(rows)
    out.update(times=ts, cloud_pct=[rows[t][0] for t in ts])
    if any(rows[t][1] for t in ts):
        out["averaged"] = [rows[t][1] for t in ts]
    return out


def for_day(rec: Optional[dict], day: date) -> Optional[dict]:
    """The part of a cloud record inside the WxChallenge day (06Z-06Z)."""
    if not rec or not rec.get("times"):
        return None
    start = pd.Timestamp(datetime(day.year, day.month, day.day, 6))
    t = pd.to_datetime(rec["times"])
    keep = [i for i in range(len(t)) if start <= t[i] <= start + pd.Timedelta(hours=24)]
    if not keep:
        return None
    out = {k: v for k, v in rec.items() if not isinstance(v, list)}
    for k in ("times", "cloud_pct", "averaged"):
        if rec.get(k):
            out[k] = [rec[k][i] for i in keep]
    return out


# ----------------------------------------------------------------------------
# text products (MOS / NBM from IEM, USL page)
# ----------------------------------------------------------------------------
def fetch_text_cloud(icao: str, label: str, init) -> Optional[dict]:
    """Cloud series of one text-guidance run, fetched again by its run time (the scored
    MOS/USL results are not touched)."""
    init = pd.Timestamp(init)
    runtime = (init.tz_localize("UTC") if init.tzinfo is None else init).to_pydatetime()
    if label == "USL":
        import wxc_usl
        html = wxc_usl._get(wxc_usl.BASE.format(icao=icao.upper()) + runtime.strftime("%Y%m%d_%H") + ".html")
        if html is None:
            return None
        run = wxc_usl.parse_run(html)
        if not run["times"] or not any(v is not None for v in run.get("sky_pct", [])):
            return None
        return {"init_time_utc": runtime.strftime("%Y-%m-%dT%H"), "times": [_t(t) for t in run["times"]],
                "cloud_pct": run["sky_pct"], "step": False, "source": "USL Sky Cover"}
    import wxc_mos
    model = TEXT_MODELS[label]
    rec = mos_cloud(wxc_mos.fetch_mos(icao, model, runtime), model)
    if rec and rec["init_time_utc"] != runtime.strftime("%Y-%m-%dT%H"):
        return None       # IEM answered with a different run
    return rec


# ----------------------------------------------------------------------------
# verification context: forecast vs observed cloud of each scored run, by day and night.
# Written to data/wxchallenge/cloud_context.json (never verification.json) and shown on
# the scoreboard as explanation only: clouds are not scored.
#   day    hours with the sun up (sunrise to sunset): drives the high
#   night  dark hours from 06Z to sunrise: drives the low
# Observed: METAR sky cover (the ASOS ceilometer works day and night, up to 12,000 ft at
# automated sites). GOES is kept beside it from the hourly values already saved by the
# today figure (no extra downloads); at night it misses low stratus and fog.
# ----------------------------------------------------------------------------
CONTEXT_MIN_COVER = 0.5      # a window mean needs at least this share of its hours


def sun_elevation(t, lat: float, lon: float) -> float:
    """Solar elevation (deg) at UTC time t (NOAA general solar position formulas)."""
    t = pd.Timestamp(t)
    hr = t.hour + t.minute / 60
    g = 2 * np.pi / 365 * (t.dayofyear - 1 + (hr - 12) / 24)
    eqtime = 229.18 * (0.000075 + 0.001868 * np.cos(g) - 0.032077 * np.sin(g)
                       - 0.014615 * np.cos(2 * g) - 0.040849 * np.sin(2 * g))
    decl = (0.006918 - 0.399912 * np.cos(g) + 0.070257 * np.sin(g) - 0.006758 * np.cos(2 * g)
            + 0.000907 * np.sin(2 * g) - 0.002697 * np.cos(3 * g) + 0.00148 * np.sin(3 * g))
    ha = np.radians((hr * 60 + eqtime + 4 * lon) / 4 - 180)
    phi = np.radians(lat)
    cos_z = np.sin(phi) * np.sin(decl) + np.cos(phi) * np.cos(decl) * np.cos(ha)
    return float(90 - np.degrees(np.arccos(np.clip(cos_z, -1, 1))))


def day_night_hours(day: date, lat: float, lon: float) -> tuple:
    """(daytime hours, night hours) of WxChallenge day `day`, as naive UTC Timestamps:
    day = sun above the horizon; night = the dark hours from 06Z until sunrise."""
    start = pd.Timestamp(datetime(day.year, day.month, day.day, 6))
    hours = [start + pd.Timedelta(hours=h) for h in range(25)]
    up = [sun_elevation(t, lat, lon) > 0 for t in hours]
    first = up.index(True) if True in up else len(hours)
    return [t for t, u in zip(hours, up) if u], hours[:first]


def window_mean(times, values, hours) -> Optional[float]:
    """Mean of a forecast series over `hours`, linearly interpolated to each hour (so
    3- and 6-hourly models count every hour); None if it covers too few of them."""
    if not hours or not times:
        return None
    t = pd.to_datetime(list(times))
    t = t.tz_convert(None) if t.tz is not None else t
    v = np.array([np.nan if x is None else x for x in values], float)
    ok = np.isfinite(v)
    if ok.sum() < 1:
        return None
    ts = (t[ok] - pd.Timestamp(0)) / pd.Timedelta(hours=1)
    hs = np.array([(h - pd.Timestamp(0)) / pd.Timedelta(hours=1) for h in hours])
    inside = (hs >= ts.min()) & (hs <= ts.max())
    if inside.sum() < CONTEXT_MIN_COVER * len(hours):
        return None
    order = np.argsort(ts)
    return round(float(np.interp(hs[inside], np.asarray(ts)[order], v[ok][order]).mean()), 1)


def obs_window_mean(sky: pd.DataFrame, hours) -> Optional[float]:
    """Mean observed sky cover over `hours`: per hour, the report nearest the top of the
    hour within 35 minutes (the routine xx:53 ob for the next hour)."""
    if sky is None or sky.empty or not hours:
        return None
    v = pd.to_datetime(sky["valid"], utc=True).dt.tz_convert(None)
    vals = []
    for h in hours:
        d = (v - h).abs()
        i = d.idxmin()
        if d[i] <= pd.Timedelta(minutes=35):
            vals.append(float(sky.loc[i, "sky_pct"]))
    if len(vals) < CONTEXT_MIN_COVER * len(hours):
        return None
    return round(float(np.mean(vals)), 1)


def goes_window_mean(values: dict, hours) -> Optional[float]:
    """values: {'YYYY-mm-ddTHH:MM': cloud %} from the hourly GOES cache."""
    got = [values[h.strftime("%Y-%m-%dT%H:%M")] for h in hours
           if values.get(h.strftime("%Y-%m-%dT%H:%M")) is not None]
    if not hours or len(got) < CONTEXT_MIN_COVER * len(hours):
        return None
    return round(float(np.mean(got)), 1)


def day_context(day: date, lat: float, lon: float, sky: pd.DataFrame, goes: dict, models: dict) -> dict:
    """Cloud context of one verified day. models: {name: (init_time_utc, cloud record or
    None)} for the scored runs. Errors are forecast minus observed, in percentage points
    (positive = too cloudy)."""
    day_h, night_h = day_night_hours(day, lat, lon)
    fmt = "%Y-%m-%dT%H:%M"
    obs = {"day_pct": obs_window_mean(sky, day_h), "night_pct": obs_window_mean(sky, night_h),
           "goes_day_pct": goes_window_mean(goes, day_h), "goes_night_pct": goes_window_mean(goes, night_h)}
    out = {"date": day.isoformat(),
           "day_hours_utc": [day_h[0].strftime(fmt), day_h[-1].strftime(fmt)] if day_h else None,
           "night_hours_utc": [night_h[0].strftime(fmt), night_h[-1].strftime(fmt)] if night_h else None,
           "obs": obs, "models": {}, "missing": {}}
    for name, (init, rec) in models.items():
        if not rec or not rec.get("times"):
            out["missing"][name] = "no cloud data for the scored run"
            continue
        m = {"init_time_utc": init,
             "day_pct": window_mean(rec["times"], rec["cloud_pct"], day_h),
             "night_pct": window_mean(rec["times"], rec["cloud_pct"], night_h)}
        for k in ("day", "night"):
            f, o = m[f"{k}_pct"], obs[f"{k}_pct"]
            m[f"{k}_err"] = None if f is None or o is None else round(f - o)
        out["models"][name] = m
    return out


# ----------------------------------------------------------------------------
# plotting (shared by the forecast and today-so-far figures)
# ----------------------------------------------------------------------------
PANEL_RATIO = 1.0           # cloud panel height relative to the other panels


def style_axis(ax):
    """0-100 % axis with light gridlines at 25/50/75 (0 and 100 sit just inside the frame)."""
    ax.set_ylim(-5, 105)
    ax.set_yticks([0, 25, 50, 75, 100])
    ax.yaxis.grid(False)
    for y in (25, 50, 75):
        ax.axhline(y, color="0.85", lw=0.6, zorder=0)
    ax.set_ylabel("Cloud cover (%)")


def draw_models(ax, clouds: dict, style, utc: bool = False):
    """Model cloud lines in each model's usual colour. style(name) -> the plot kwargs
    (ls, lw, alpha, marker, ms) the figure uses for that model in its other panels, so the
    cloud lines look exactly like the temperature/wind/precip lines. MOS CLD categories are
    drawn as steps; time-averaged GFS steps get open markers. Unlabelled: the colours are
    in the other legends."""
    import matplotlib as mpl
    from wxc_verify import STYLE
    for name, s in (clouds or {}).items():
        if not s or not s.get("times"):
            continue
        color = STYLE.get(name, ("C7", "-"))[0]
        kw = {**style(name), "color": color}
        t = pd.to_datetime(s["times"], utc=utc)
        v = np.array([np.nan if x is None else x for x in s["cloud_pct"]], float)
        ax.plot(t, v, drawstyle="steps-mid" if s.get("step") else "default", **kw)
        avg = np.array(s.get("averaged") or [False] * len(v), bool)
        if avg.any():
            ms = kw.get("ms") or mpl.rcParams["lines.markersize"]
            ax.plot(t[avg], v[avg], "o", mfc="white", mec=color, ms=ms, zorder=4)
