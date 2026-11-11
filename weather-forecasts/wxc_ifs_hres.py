"""
ECMWF IFS HRES at its native 9 km resolution, hourly, from Open-Meteo's Single Runs API
(model "ecmwf_ifs"), which keeps every run (archived from 2024-03), so it can be hindcast:

  https://single-runs-api.open-meteo.com/v1/forecast?models=ecmwf_ifs&run=YYYY-MM-DDTHH:00&...

"IFS" (the main script's fetch_ifs) is the same HRES run from ECMWF open data: a 0.25 deg grid,
3-hourly, and posted ~2 h later. On the 10/19 12Z run for KOLM 10/20 the two gave the same high
(62.4) but lows of 45.6 (9 km) and 43.8 (open data).

Treated like a GRIB model (results[LABEL] = {"metrics", "series"} in the main script): high,
low, max wind and precip over the 06Z-06Z day from the hourly values, the hourly series (temp,
wind, precip since 06Z, dewpoint) and total cloud cover in the run's cloud file (wxc_clouds;
display only). Results are cached per run (wxc_cache).

Which run: live, the newest complete run in Open-Meteo's meta.json; a hindcast (as_of), the
newest run that was out at as_of (PUBLISH_DELAY_HOURS after its init). A run still being written
answers with nulls past the hours done so far, so a run without every hour of the day is
skipped for the run before it. Shown and scored, but kept out of the consensus
(wxc_verify.NOT_IN_CONSENSUS) until it has a track record.
"""

from datetime import date, datetime, timedelta, timezone
from typing import Optional

import numpy as np
import pandas as pd

import wxc_cache
import wxc_clouds

LABEL = "IFS_HRES"
MODEL = "ecmwf_ifs"
API = "https://single-runs-api.open-meteo.com/v1/forecast"
META = "https://single-runs-api.open-meteo.com/data/ecmwf_ifs/static/meta.json"
HOURLY = "temperature_2m,wind_speed_10m,precipitation,dew_point_2m,relative_humidity_2m,cloud_cover"
INIT_HOURS = (0, 6, 12, 18)
# A run counts as out this long after its init (hindcasts). On 2026-10-21 meta.json had the
# 06Z run complete at 12:04Z, and the 12Z run's first 72 h written by 19:33Z.
PUBLISH_DELAY_HOURS = 8
MAX_FALLBACK = 1           # also try this many older runs if the chosen one isn't usable


class IncompleteRun(ValueError):
    """A run whose hours for the day aren't all there (still being written, or too short)."""


def _get_json(url, params=None):
    import requests
    r = requests.get(url, params=params, timeout=45)
    if r.status_code >= 400:
        try:          # Open-Meteo says why in the body, e.g. "The requested model run is not available"
            reason = r.json().get("reason")
        except ValueError:
            reason = None
        if reason:
            raise ValueError(f"Open-Meteo: {reason}")
    r.raise_for_status()
    return r.json()


def floor_cycle(t: datetime) -> datetime:
    """The latest init time (00/06/12/18Z) at or before t (naive UTC)."""
    t = t.replace(tzinfo=None, minute=0, second=0, microsecond=0)
    return t - timedelta(hours=t.hour % 6)


def init_for(as_of: Optional[datetime]) -> datetime:
    """Newest run to use: from meta.json when live (as_of None), else the newest run out at
    as_of. Naive UTC."""
    if as_of is not None:
        return floor_cycle(as_of - timedelta(hours=PUBLISH_DELAY_HOURS))
    meta = _get_json(META)
    t = meta.get("last_run_initialisation_time")
    if not t:
        raise ValueError("Open-Meteo meta.json has no last_run_initialisation_time")
    return datetime.fromtimestamp(t, tz=timezone.utc).replace(tzinfo=None)


def request_run(station, init: datetime) -> dict:
    return _get_json(API, {
        "latitude": station.lat, "longitude": station.lon, "models": MODEL,
        "run": init.strftime("%Y-%m-%dT%H:00"), "hourly": HOURLY,
        "temperature_unit": "fahrenheit", "wind_speed_unit": "kn", "precipitation_unit": "inch",
        "timezone": "GMT",
    })


def _vals(hourly: dict, var: str) -> np.ndarray:
    return np.array([np.nan if v is None else v for v in hourly.get(var) or []], float)


def summarize_run(hourly: dict, init: datetime, day: date, lst_offset: Optional[float] = None) -> dict:
    """{"metrics", "series"} for WxChallenge day `day` (06Z-06Z) from one run's hourly values.
    Temperature and wind at 06Z..06Z inclusive; precipitation is the hour ending at each time,
    so the day's total is the 24 hours after 06Z. Raises IncompleteRun when any is missing."""
    times = pd.to_datetime(hourly["time"])
    start = pd.Timestamp(datetime(day.year, day.month, day.day, 6))
    end = start + pd.Timedelta(hours=24)
    if pd.Timestamp(init) > start:
        raise ValueError(f"run {init:%Y-%m-%d %HZ} starts after the {day} window")
    inst = np.asarray((times >= start) & (times <= end))
    accum = np.asarray((times > start) & (times <= end))
    T, W, P = (_vals(hourly, v) for v in ("temperature_2m", "wind_speed_10m", "precipitation"))
    if len(T) != len(times) or len(W) != len(times) or len(P) != len(times):
        raise ValueError("Open-Meteo response is missing a variable")
    n_have = min(np.isfinite(T[inst]).sum(), np.isfinite(W[inst]).sum())
    if inst.sum() != 25 or accum.sum() != 24 or n_have < 25 or np.isfinite(P[accum]).sum() < 24:
        raise IncompleteRun(f"run {init:%Y-%m-%d %HZ} has {n_have} of 25 hours of {day} 06Z-06Z "
                            "(still being written, or too short)")
    temp, wind = T[inst], W[inst]
    precip = np.concatenate([[0.0], np.cumsum(P[accum])])          # since 06Z, at 06Z..06Z
    td = _vals(hourly, "dew_point_2m")
    dewpt = td[inst] if len(td) == len(times) and np.isfinite(td[inst]).any() else None
    st = times[inst]
    wmax = float(wind.max())
    extra = {}
    if lst_offset is not None:    # WxChallenge verifies wind over the CLI's LST day (rule 15.5)
        from functions import lst_window_utc
        ws, we = lst_window_utc(day, lst_offset)
        lw = W[np.asarray((times >= ws) & (times <= we))]
        if np.isfinite(lw).sum() >= 24:
            extra = {"wind_max_kt_06z": round(wmax, 1), "wind_window": "LST",
                     "wind_window_utc": [ws.strftime("%Y-%m-%dT%H"), we.strftime("%Y-%m-%dT%H")]}
            wmax = float(np.nanmax(lw))
    metrics = {
        "tmax_f": round(float(temp.max()), 1),
        "tmin_f": round(float(temp.min()), 1),
        "wind_max_kt": round(wmax, 1),
        **extra,
        "precip_in": round(float(precip[-1]), 2),
        "init_time_utc": pd.Timestamp(init).strftime("%Y-%m-%dT%H"),
        "valid_range_utc": [st[0].strftime("%Y-%m-%dT%H"), st[-1].strftime("%Y-%m-%dT%H")],
        "n_steps": int(inst.sum()),
        "temp_source": "hourly 2 m T (Open-Meteo ecmwf_ifs, 9 km)",
    }
    return {"metrics": metrics,
            "series": {"times": st, "temp_f": temp, "wind_kt": wind, "precip_in": precip, "dewpt_f": dewpt}}


def cloud_record(hourly: dict, init: datetime) -> Optional[dict]:
    """Total cloud cover (%) at every hour of the run (display only), for wxc_clouds.save_cloud."""
    cc = _vals(hourly, "cloud_cover")
    if len(cc) != len(hourly.get("time") or []) or not np.isfinite(cc).any():
        return None
    return wxc_clouds.merge(None, {
        "model": LABEL, "init_time_utc": pd.Timestamp(init).strftime("%Y-%m-%dT%H"), "step": False,
        "source": "Open-Meteo ecmwf_ifs (9 km)",
        "times": [pd.Timestamp(t).strftime("%Y-%m-%dT%H:%M") for t in pd.to_datetime(hourly["time"])],
        "cloud_pct": [None if not np.isfinite(v) else float(v) for v in cc]})


def _save_cloud(station, init, hourly):
    """Cloud cover in its own file, never in the result; a failure never costs the forecast."""
    try:
        rec = cloud_record(hourly, init)
        if rec and wxc_clouds.CLOUDS_ENABLED:
            wxc_clouds.save_cloud(station.icao, LABEL, init,
                                  wxc_clouds.merge(wxc_clouds.load_cloud(station.icao, LABEL, init), rec))
    except Exception as exc:
        print(f"  warning: {LABEL} cloud cover not saved ({type(exc).__name__}: {exc})")


def fetch_cloud(station, init) -> Optional[dict]:
    """A run's cloud record, from its cloud file or requested again (every run is archived)."""
    init = pd.Timestamp(init).to_pydatetime().replace(tzinfo=None)
    rec = wxc_clouds.load_cloud(station.icao, LABEL, init)
    if rec is None:
        _save_cloud(station, init, request_run(station, init)["hourly"])
        rec = wxc_clouds.load_cloud(station.icao, LABEL, init)
    return rec


def _fail(msg) -> dict:
    return {"metrics": {"tmax_f": None, "tmin_f": None, "wind_max_kt": None, "precip_in": None,
                        "init_time_utc": None, "valid_range_utc": None, "error": msg},
            "series": None}


def get_forecast(station, day: date, as_of: Optional[datetime] = None,
                 now: Optional[datetime] = None) -> dict:
    """IFS HRES 9 km for WxChallenge day `day`: {"metrics", "series"} like the GRIB models,
    or an entry with "error". as_of: hindcast (the runs out at that time)."""
    try:
        init = init_for(as_of)
    except Exception as exc:
        return _fail(f"Open-Meteo meta failed: {exc}")
    last = None
    for attempt in range(MAX_FALLBACK + 1):
        cached = wxc_cache.load(station.icao, LABEL, init, day)
        if cached is not None:
            print(f"Using saved {LABEL} {init:%Y-%m-%d %HZ} (already downloaded)")
            res = cached
            break
        try:
            print(f"Fetching {LABEL} {init:%Y-%m-%d %HZ} (Open-Meteo single run)...")
            hourly = request_run(station, init)["hourly"]
            res = summarize_run(hourly, init, day, getattr(station, "lst_offset_hours", None))
            wxc_cache.save(station.icao, LABEL, init, day, res)
            _save_cloud(station, init, hourly)
            break
        except Exception as exc:
            last = exc
            print(f"  {LABEL} {init:%Y-%m-%d %HZ} failed: {type(exc).__name__}: {exc}")
            init -= timedelta(hours=6)
    else:
        return _fail(f"{type(last).__name__}: {last}")
    from wxc_verify import NOT_IN_CONSENSUS
    notes = [n for n in (res["metrics"].get("note") or "").split("; ") if n]
    if attempt and "newest run unavailable, used previous" not in notes:
        notes.append("newest run unavailable, used previous")
    if LABEL in NOT_IN_CONSENSUS and "not in the consensus" not in notes:
        notes.append("not in the consensus")
    if notes:
        res["metrics"]["note"] = "; ".join(notes)
    if as_of is None:              # Open-Meteo's feed stalling: flag a run older than the limit
        import wxc_ens
        wxc_ens.flag_stale(LABEL, res["metrics"], now or datetime.now(timezone.utc))
    return res
