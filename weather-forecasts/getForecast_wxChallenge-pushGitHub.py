"""
WxChallenge forecast helper.

For the current station (see wxc_stations.py, or pass an ICAO id on the command line):
  1. pulls observations for the last few completed days (IEM METARs + NWS CLI wind)
  2. verifies earlier runs against those observations (data/wxchallenge/verification.json)
  3. fetches HRRR, RRFS, ECMWF IFS and GFS grids (Herbie; AIFS left out for now), ECMWF IFS HRES at 9 km
     (Open-Meteo single runs, wxc_ifs_hres.py; not in the consensus yet) plus GFS MOS and
     NBM text guidance (AWS, every hourly cycle), each summarised for the next WxChallenge day (06Z-06Z),
     the ECMWF and GEFS ensembles (Open-Meteo; GEFS not in the consensus), the 3 km
     precip ensembles REFS and HRRRCast (wxc_cam_ens.py) and NBM QMD probabilistic precip
     (wxc_nbm_qmd.py); precip-only sources are not part of the consensus. Every source with a
     probability of precipitation carries a "pop" record (wxc_pop.py; display/verification only)
  4. builds a bias-corrected, skill-weighted CONSENSUS from the verified models
  5. writes data/wxchallenge/forecast.json, appends data/wxchallenge/runs.jsonl,
     draws images/wxchallenge/latest.png and verification.png (local only, not pushed), refreshes the page's
     forecast-evolution link config (wxc_links.py) and writes data/wxchallenge/brief.md,
     a plain-text summary for AI assistants (wxc_brief.py; linked only from llms.txt and a
     visually hidden link on the page), and data/wxchallenge/timeline.json for the page's
     scrollable forecasts-and-observations timeline (wxc_timeline.py, wxchallenge/timeline.js;
     display only). A model that fails this run (e.g. the laptop offline)
     keeps its last good forecast for the day on the page, flagged as stale (wxc_carryover.py)
  6. commits and pushes the data/images (GitHub Pages), best effort

Usage:
  python getForecast_wxChallenge-pushGitHub.py [ICAO] [--target-date YYYY-MM-DD]
                                               [--obs-days N] [--no-push] [--skip-grib]
"""

import argparse
import json
import logging
import subprocess
import warnings
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

import numpy as np
import pandas as pd

from functions import (convert_time_to_datetime64, forecast_hours_for_day, fmt,
                       get_latest_forecast_cycle, previous_forecast_cycle, run_hour)
import wxc_brief
import wxc_cache
import wxc_cam_ens
import wxc_carryover
import wxc_clouds
import wxc_ens
import wxc_goes
import wxc_ifs_hres
import wxc_links
import wxc_mos
import wxc_nbm_qmd
import wxc_obs
import wxc_pop
import wxc_timeline
import wxc_today
import wxc_usl
import wxc_verify
from wxc_stations import get_station

warnings.filterwarnings("ignore", message="In*", category=FutureWarning)
warnings.filterwarnings("ignore", message="Engine 'gini' loading failed.*", category=RuntimeWarning)


class _OneLineHerbieErrors(logging.Filter):
    """FastHerbie logs a full traceback for every forecast hour it can't reach (hundreds of
    lines per model when offline). Keep its one-line "Exception has occured" message only."""
    def filter(self, record):
        msg = str(record.msg)
        return not (msg.startswith("Traceback") or msg.startswith("Exception details"))


logging.getLogger("herbie.fast").addFilter(_OneLineHerbieErrors())

ROOT = Path(__file__).resolve().parent
(IMAGES := ROOT / "images" / "wxchallenge").mkdir(parents=True, exist_ok=True)
(DATA := ROOT / "data" / "wxchallenge").mkdir(parents=True, exist_ok=True)

MS_TO_KT = 1.94384
HINDCAST_HOUR = 23        # hindcasts use the runs available at 23Z the day before (just before the 00Z
                          # deadline, like a real submission: includes the 22Z USL, 18Z GFS and GFS MOS)
MAX_FALLBACK = 1          # also try this many older cycles if the newest isn't posted yet
TODAY_LATEST = ["HRRR", "GFS_MOS", "NBM"]   # newest runs drawn on the "today so far" figure
# newest runs fetched for today (grid models: once per cycle, cached): the page's timeline and
# the AI brief show all of them; the today figure (PNG) draws only TODAY_LATEST
TODAY_LATEST_FETCH = TODAY_LATEST + ["RRFS", "GFS", "IFS"]
# grid models: the GRIB_MODELS below plus IFS_HRES (IFS at 9 km, hourly, from Open-Meteo)
# AIFS is left out for now (2026-10-28): its open data is 6-hourly, so its highs and lows run
# low. ECMWF may make it hourly. To bring it back, uncomment it here and in GRIB_MODELS, take it
# out of wxc_verify.RETIRED (and restore PROXY_TRACK_RECORD) and uncomment it in the page's
# GROUPS and timeline.js ORDER / PRESETS.
GRIB_ORDER = ["HRRR", "RRFS", "IFS", wxc_ifs_hres.LABEL, "GFS"]
# GRIB_ORDER = ["HRRR", "RRFS", "IFS", wxc_ifs_hres.LABEL, "GFS", "AIFS"]
MOS_ORDER = list(wxc_mos.MOS_PRODUCTS) + ["USL"]   # GFS_MOS (IEM), NBM (AWS NBS text) + USL (microclimates.org)
ENS_ORDER = list(wxc_ens.MODELS)                    # ENS, AIFS_ENS, GEFS (Open-Meteo)
CAM_ORDER = list(wxc_cam_ens.MODELS)                # HRRRCAST, REFS (3 km precip-only ensembles)
# Herbie sources for HRRR. Azure's URL-signing API answers without an "href" for files that
# aren't there, which Herbie doesn't catch (a KeyError traceback per missing hour), so it's left out.
HRRR_SOURCES = ["aws", "nomads", "google"]


# -------------------------------------------------------------------
# small helpers
# -------------------------------------------------------------------
def k_to_f(da):
    return (da - 273.15) * 1.8 + 32


MAX_POINT_DISTANCE_KM = 40   # nearest grid point must be this close (0.25 deg grid: <= ~20 km)


def _grid_id(ds):
    """Fingerprint of a grid, used to name Herbie's cached BallTree. Grids with the same
    shape but different longitude conventions (GFS 0..360, IFS -180..180) must never
    share a tree, or the point lookup lands on the wrong side of the globe."""
    lat, lon = ds["latitude"].values, ds["longitude"].values
    return (f"wxc2_{'x'.join(map(str, lat.shape))}_{'x'.join(map(str, lon.shape))}_"
            f"{float(lat.flat[0]):.3f}_{float(lon.flat[0]):.3f}_{float(lat.flat[-1]):.3f}_{float(lon.flat[-1]):.3f}")


GRIB_THREADS = 8             # forecast hours downloaded/read at once (Herbie's default is one by one)


def _read_grib(H, search):
    """H.xarray(search) with the forecast hours fetched in parallel. Herbie warns its threaded
    read "only works sometimes" (cfgrib/xarray races), so such a failure is retried one hour
    at a time. Network errors and a search with no match (ValueError) fail as before."""
    import requests
    import xarray as xr
    xr.backends.list_engines()      # load xarray's engine plugins once, before the threads race to
    try:
        return H.xarray(search, max_threads=GRIB_THREADS, backend_kwargs={"decode_times": False})
    except (requests.RequestException, ValueError):
        raise
    except Exception as exc:
        print(f"  (parallel read of {search!r} failed: {type(exc).__name__}; retrying one hour at a time)")
        return H.xarray(search, backend_kwargs={"decode_times": False})


def pick(H, search, points, prefer=None):
    """H.xarray(search) at the station point -> 1-D DataArray over forecast steps."""
    ds = _pick_ds(H, search, points)
    name = prefer if prefer in ds.data_vars else list(ds.data_vars)[0]
    da = ds[name]
    return da.sel(point=0) if "point" in da.dims else da


def pick_vars(H, search, points, names):
    """Like pick, for a search matching several fields of one level type (e.g. 10 m U and V):
    one download per forecast hour instead of one per field. Returns a DataArray per name."""
    ds = _pick_ds(H, search, points)
    missing = [n for n in names if n not in ds.data_vars]
    if missing:
        raise ValueError(f"{search!r} gave {list(ds.data_vars)}, not {missing}")
    return [ds[n].sel(point=0) if "point" in ds[n].dims else ds[n] for n in names]


def wind_10m(H, search, points):
    """10 m wind speed (kt) from U and V, read in one request per forecast hour."""
    u, v = pick_vars(H, search, points, ["u10", "v10"])
    return np.sqrt(u ** 2 + v ** 2) * MS_TO_KT


def without_first_hour(H):
    """FastHerbie H minus its first forecast hour, for interval max/min fields (which the first
    step doesn't have). Shares H's per-hour objects, so the file checks and .idx downloads
    already done for H aren't repeated (a new FastHerbie would redo both for every hour)."""
    import copy
    first = H.fxx[0]
    H2 = copy.copy(H)
    H2.fxx = H.fxx[1:]
    H2.objects = [h for h in H.objects if h.fxx != first]
    H2.file_exists = [h for h in H.file_exists if h.fxx != first]
    H2.file_not_exists = [h for h in getattr(H, "file_not_exists", []) if h.fxx != first]
    H2.tasks = len(H2.objects)
    return H2


def _pick_ds(H, search, points):
    """The fields matching `search` at the station's nearest grid point (Dataset, 'point' dim)."""
    ds = _read_grib(H, search)
    try:
        # a named tree is cached by Herbie, so repeat runs skip rebuilding it
        ds = ds.herbie.pick_points(points, method="nearest", tree_name=_grid_id(ds))
    except TypeError:        # older Herbie without tree_name
        ds = ds.herbie.pick_points(points, method="nearest")
    if "point_grid_distance" in ds.coords:
        dist = float(np.asarray(ds["point_grid_distance"]).ravel()[0])
        if dist > MAX_POINT_DISTANCE_KM:
            raise ValueError(f"nearest grid point for {search!r} is {dist:.0f} km away "
                             f"(bad grid lookup?)")
    return ds


def precip_factor(da, default):
    """Inches per unit of a precip DataArray, read from its GRIB units when present."""
    units = str(da.attrs.get("units", da.attrs.get("GRIB_units", ""))).lower().strip()
    if units in ("m", "m of water equivalent"):
        return 39.3701
    if "kg" in units or units == "mm":
        return 0.0393701
    return default


def _extra_failed(fields, exc):
    """Note for a failed optional max/min download; the full traceback goes to the console
    (not for a connection failure, where it says nothing new)."""
    import traceback
    print(f"  {fields} failed ({type(exc).__name__}): {exc}")
    if not wxc_carryover.is_network_error(f"{type(exc).__name__}: {exc}"):
        traceback.print_exc()
    return f"{fields} unavailable ({type(exc).__name__}: {str(exc)[:120]})"


def iso_hour(t):
    return pd.Timestamp(t).strftime("%Y-%m-%dT%H")


class IncompleteCycle(RuntimeError):
    """A model cycle whose later forecast hours aren't posted yet."""


def fast_herbie(init, fxx, **kw):
    """
    FastHerbie that insists every requested forecast hour is posted. A cycle is posted hour
    by hour (HRRR's f30-f48 come ~1.5-2 h after init), and summarizing whatever had arrived
    gave e.g. a 00Z HRRR covering only 06-16Z: high missed, precip 0.00. Raising instead lets
    fetch_with_fallback use the previous, complete cycle, and nothing partial gets cached.
    """
    from herbie import FastHerbie
    H = FastHerbie([init], fxx=fxx, **kw)
    have = {h.fxx for h in H.file_exists}
    missing = [f for f in fxx if f not in have]
    if missing:
        raise IncompleteCycle(f"{len(missing)} of {len(fxx)} forecast hours not posted yet "
                              f"(f{missing[0]:03d}-f{missing[-1]:03d})")
    return H


def summarize(label, init, times, temp_f, wind_kt, precip_in, tmax_extra=None,
              tmin_extra=None, truncated=False, notes=None, dewpt_f=None):
    """Standard result dict: JSON metrics + series for plotting. dewpt_f (display only) is
    stored even when None, so a run whose dewpoint failed isn't asked for it again."""
    tmax = float(np.nanmax(temp_f))
    tmin = float(np.nanmin(temp_f))
    src = "instantaneous 2 m T"
    if tmax_extra is not None and np.isfinite(tmax_extra):
        tmax, src = max(tmax, tmax_extra), "2 m T + interval max/min fields"
    if tmin_extra is not None and np.isfinite(tmin_extra):
        tmin = min(tmin, tmin_extra)
    metrics = {
        "tmax_f": round(tmax, 1),
        "tmin_f": round(tmin, 1),
        "wind_max_kt": round(float(np.nanmax(wind_kt)), 1),
        "precip_in": round(float(np.nanmax(precip_in)), 2),
        "init_time_utc": iso_hour(init),
        "valid_range_utc": [str(times[0]), str(times[-1])],
        "n_steps": int(len(times)),
        "temp_source": src,
    }
    if truncated:
        metrics["partial_window"] = True
    if notes:
        metrics["note"] = "; ".join(notes)
    if metrics["precip_in"] > 15:
        metrics["note"] = (metrics.get("note", "") + " precip looks unphysical, check units").strip()
    return {"metrics": metrics,
            "series": {"times": pd.to_datetime(times), "temp_f": np.asarray(temp_f, float),
                       "wind_kt": np.asarray(wind_kt, float), "precip_in": np.asarray(precip_in, float),
                       "dewpt_f": None if dewpt_f is None else np.asarray(dewpt_f, float)}}


# 2 m dewpoint of each GRIB model (search, cfgrib name). DISPLAY ONLY (the page's dewpoint and
# RH panels): never in the metrics, the consensus or the scores, and never fails a model.
DEWPT_SEARCH = {"HRRR": ("DPT:2 m above", "d2m"), "RRFS": ("DPT:2 m above", "d2m"),
                "GFS": ("DPT:2 m above", "d2m"), "IFS": (":2d:", "d2m"), "AIFS": (":2d:", "d2m")}


def grib_dewpoint(label, H, points, n):
    """2 m dewpoint (degF) at the station from Herbie object H (the run's n forecast steps),
    or None if it can't be had."""
    try:
        search, name = DEWPT_SEARCH[label]
        vals = np.atleast_1d(np.asarray(k_to_f(pick(H, search, points, name)).values, float))
        if len(vals) != n:
            raise ValueError(f"{len(vals)} dewpoint steps for {n} temperature steps")
        return vals
    except Exception as exc:
        print(f"  warning: {label} dewpoint skipped ({type(exc).__name__}: {str(exc)[:150]})")
        return None


def add_dewpoint(label, res, points, station):
    """Dewpoint for a run saved before dewpoints were kept: downloads that one field for the
    run's stored steps. Returns True if `res` changed (then it should be saved again)."""
    s, m = res.get("series"), res.get("metrics") or {}
    if label not in DEWPT_SEARCH or not s or "dewpt_f" in s or not m.get("init_time_utc"):
        return False
    from herbie import FastHerbie
    init = pd.Timestamp(m["init_time_utc"] + ":00")
    fxx = [int(round((pd.Timestamp(t) - init).total_seconds() / 3600)) for t in s["times"]]
    try:
        H = FastHerbie([init], fxx=fxx, **cloud_grib_setup(label, init, station)[0])
    except Exception as exc:
        print(f"  warning: {label} dewpoint skipped ({type(exc).__name__}: {str(exc)[:150]})")
        H = None
    s["dewpt_f"] = None if H is None else grib_dewpoint(label, H, points, len(fxx))
    return True


# -------------------------------------------------------------------
# GRIB models (Herbie)
# -------------------------------------------------------------------
# 10 m U and V in one search (one download per forecast hour)
WIND_10M_NCEP = ":[UV]GRD:10 m above ground:"
WIND_10M_ECMWF = ":10[uv]:"


def fetch_hrrr(init, day, points, station, partial=False):
    fxx, trunc = forecast_hours_for_day(init, day, step=1, max_fxx=48, partial=partial)
    H = fast_herbie(init, fxx, model=station.hrrr_model, product="sfc", priority=HRRR_SOURCES)
    t2m = k_to_f(pick(H, "TMP:2 m above", points, "t2m"))
    times = convert_time_to_datetime64(t2m.valid_time.values)
    wind = pick(H, ":WIND", points, "max_10si") * MS_TO_KT      # hourly max 10 m wind
    tp = pick(H, "APCP", points, "tp")
    tp = (tp - tp[0]) * precip_factor(tp, 0.0393701)
    notes = [f"{pd.Timestamp(init):%HZ} HRRR stops at f48: window truncated"] if trunc else None
    return summarize("HRRR", init, times, t2m.values, wind.values, tp.values,
                     truncated=trunc, notes=notes, dewpt_f=grib_dewpoint("HRRR", H, points, len(times)))


def fetch_rrfs(init, day, points, station, partial=False):
    """RRFS v1 (operational 14 Oct 2026; parallel data on AWS since Aug 2026), 2D fields."""
    fxx, trunc = forecast_hours_for_day(init, day, step=1, max_fxx=84, partial=partial)
    kw = dict(model="rrfs", product="2dfld", domain=station.rrfs_domain)
    H = fast_herbie(init, fxx, **kw)
    t2m = k_to_f(pick(H, "TMP:2 m above", points, "t2m"))
    times = convert_time_to_datetime64(t2m.valid_time.values)
    wind = wind_10m(H, WIND_10M_NCEP, points)
    tp = pick(H, ":APCP:surface:0-", points, "tp")        # accumulated from init
    tp = (tp - tp[0]) * precip_factor(tp, 0.0393701)
    # hourly TMAX/TMIN (max/min over the hour ending at each step), first step excluded
    tmax_x = tmin_x = None
    notes = []
    try:
        H2 = without_first_hour(H)
        tmax_x = float(k_to_f(pick(H2, ":TMAX:2 m above", points, "tmax")).max())
        tmin_x = float(k_to_f(pick(H2, ":TMIN:2 m above", points, "tmin")).min())
    except Exception as exc:
        notes.append(_extra_failed("TMAX/TMIN", exc))
    return summarize("RRFS", init, times, t2m.values, wind.values, tp.values,
                     tmax_x, tmin_x, trunc, notes, grib_dewpoint("RRFS", H, points, len(times)))


def fetch_ifs(init, day, points, station=None, partial=False):
    max_fxx = 144 if pd.Timestamp(init).hour in (0, 12) else 90
    fxx, trunc = forecast_hours_for_day(init, day, step=3, max_fxx=max_fxx, partial=partial)
    H = fast_herbie(init, fxx, model="ifs", product="oper")
    t2m = k_to_f(pick(H, ":2t:", points, "t2m"))
    times = convert_time_to_datetime64(t2m.valid_time.values)
    wind = wind_10m(H, WIND_10M_ECMWF, points)
    tp = pick(H, ":tp:", points, "tp")
    tp = (tp - tp[0]) * precip_factor(tp, 39.3701)

    # 3-hourly max/min 2 m T catch the peaks between output times. These fields
    # describe the 3 h *ending* at each step, so the first step is excluded.
    tmax_x = tmin_x = None
    notes = []
    try:
        H2 = without_first_hour(H)
        tmax_x = float(k_to_f(pick(H2, ":mx2t3:", points, "mx2t3")).max())
        tmin_x = float(k_to_f(pick(H2, ":mn2t3:", points, "mn2t3")).min())
    except Exception as exc:
        notes.append(_extra_failed("mx2t3/mn2t3", exc))
    return summarize("IFS", init, times, t2m.values, wind.values, tp.values,
                     tmax_x, tmin_x, trunc, notes, grib_dewpoint("IFS", H, points, len(times)))


def fetch_gfs(init, day, points, station=None, partial=False):
    fxx, trunc = forecast_hours_for_day(init, day, step=3, max_fxx=384, partial=partial)
    H = fast_herbie(init, fxx, model="gfs", product="pgrb2.0p25")
    t2m = k_to_f(pick(H, "TMP:2 m above", points, "t2m"))
    times = convert_time_to_datetime64(t2m.valid_time.values)
    wind = wind_10m(H, WIND_10M_NCEP, points)
    tp = pick(H, ":APCP:surface:0-*", points, "tp")
    tp = (tp - tp[0]) * precip_factor(tp, 0.0393701)

    # GFS TMAX/TMIN: max/min 2 m T over the interval ending at each step
    tmax_x = tmin_x = None
    notes = []
    try:
        H2 = without_first_hour(H)
        tmax_x = float(k_to_f(pick(H2, ":TMAX:2 m above", points, "tmax")).max())
        tmin_x = float(k_to_f(pick(H2, ":TMIN:2 m above", points, "tmin")).min())
    except Exception as exc:
        notes.append(_extra_failed("TMAX/TMIN", exc))
    return summarize("GFS", init, times, t2m.values, wind.values, tp.values,
                     tmax_x, tmin_x, trunc, notes, grib_dewpoint("GFS", H, points, len(times)))


# unused while AIFS is left out (see GRIB_ORDER)
def fetch_aifs(init, day, points, station=None, partial=False):
    fxx, trunc = forecast_hours_for_day(init, day, step=6, max_fxx=360, partial=partial)
    H = fast_herbie(init, fxx, model="aifs", product="oper")
    t2m = k_to_f(pick(H, ":2t:", points, "t2m"))
    times = convert_time_to_datetime64(t2m.valid_time.values)
    wind = wind_10m(H, WIND_10M_ECMWF, points)
    tp = pick(H, ":tp:", points, "tp")
    factor = precip_factor(tp, 0.0393701)
    tp = (tp - tp[0]) * factor
    notes = ["6-hourly output: high/low likely underdone"]
    if factor != 0.0393701:
        notes.append("AIFS tp reported in metres")
    return summarize("AIFS", init, times, t2m.values, wind.values, tp.values,
                     truncated=trunc, notes=notes, dewpt_f=grib_dewpoint("AIFS", H, points, len(times)))


GRIB_MODELS = {
    # label: (cycle key in functions.get_latest_forecast_cycle, fetch function)
    "HRRR": ("HRRR", fetch_hrrr),
    "IFS": ("IFS", fetch_ifs),
    "GFS": ("GFS", fetch_gfs),
    # "AIFS": ("AIFS", fetch_aifs),     # left out for now, see GRIB_ORDER
    "RRFS": ("RRFS", fetch_rrfs),
}


def fetch_with_fallback(label, cycle_key, fn, day, points, station, as_of=None, partial=False):
    init = get_latest_forecast_cycle(model=cycle_key, now=as_of)
    last = None
    for attempt in range(MAX_FALLBACK + 1):
        cached = wxc_cache.load(station.icao, label, init, day, partial)
        if cached is not None:
            print(f"Using saved {label} {init:%Y-%m-%d %HZ} (already downloaded)")
            if add_dewpoint(label, cached, points, station):     # saved before dewpoints were kept
                wxc_cache.save(station.icao, label, init, day, cached, partial)
            return cached
        try:
            print(f"Fetching {label} {init:%Y-%m-%d %HZ}...")
            res = fn(init, day, points, station, partial=partial)
            # keep the station values so later runs don't download this model run again
            # (skip if an optional field was missing: a later run may find it posted)
            if "unavailable" not in (res["metrics"].get("note") or ""):
                wxc_cache.save(station.icao, label, init, day, res, partial)
            if attempt:
                res["metrics"]["note"] = (res["metrics"].get("note", "") +
                                          "; newest cycle unavailable, used previous").lstrip("; ")
            return res
        except Exception as exc:
            last = exc
            print(f"  {label} {init:%HZ} failed: {type(exc).__name__}: {exc}")
            init = previous_forecast_cycle(init, cycle_key)
    return {"metrics": {"tmax_f": None, "tmin_f": None, "wind_max_kt": None, "precip_in": None,
                        "init_time_utc": None, "valid_range_utc": None, "error": str(last)},
            "series": None}


# -------------------------------------------------------------------
# cloud cover: DISPLAY ONLY. Never part of the results above, the consensus, runs.jsonl
# or the series files; kept per run in cache/{ICAO}/_cloud_{MODEL}_{init}.json (wxc_clouds)
# -------------------------------------------------------------------
TCDC_NOW = r":TCDC:entire atmosphere[^:]*:\d+ hour fcst:"           # instantaneous
TCDC_AVE = r":TCDC:entire atmosphere[^:]*:\d+-\d+ hour ave fcst:"   # interval average


def cloud_grib_setup(label, init, station):
    """Herbie arguments, output interval and last forecast hour (as in the fetch_* functions)."""
    ifs_max = 144 if pd.Timestamp(init).hour in (0, 12) else 90
    return {"HRRR": (dict(model=station.hrrr_model, product="sfc", priority=HRRR_SOURCES), 1, 48),
            "RRFS": (dict(model="rrfs", product="2dfld", domain=station.rrfs_domain), 1, 84),
            "IFS": (dict(model="ifs", product="oper"), 3, ifs_max),
            "GFS": (dict(model="gfs", product="pgrb2.0p25"), 3, 384),
            "AIFS": (dict(model="aifs", product="oper"), 6, 360)}[label]


def _cloud_values(da):
    vals = np.atleast_1d(np.asarray(da.values, float))
    vt = da.coords.get("valid_time")
    try:
        times = np.atleast_1d(convert_time_to_datetime64(vt.values))
    except Exception:          # absent, or a single step (then the caller knows the time)
        times = None
    return vals, times


def fetch_cloud_grib(label, init, fxx, points, station):
    """Total cloud cover (%) of one GRIB run at the station for forecast hours `fxx`.
    GFS/RRFS files hold an instantaneous and an interval-average TCDC; the instantaneous one
    is used, and a step that only has the average is marked averaged."""
    from herbie import FastHerbie
    kw = cloud_grib_setup(label, init, station)[0]
    init = pd.Timestamp(init)
    if label in ("IFS", "AIFS"):
        da = pick(FastHerbie([init], fxx=fxx, **kw), ":tcc:", points, "tcc")
        vals, times = _cloud_values(da)
        units = str(da.attrs.get("units", da.attrs.get("GRIB_units", ""))).strip()
        if units != "%" and (units in ("(0 - 1)", "0-1", "1", "fraction") or np.nanmax(vals) <= 1.0):
            vals = vals * 100.0                                  # tcc is a 0-1 fraction
        averaged = [False] * len(vals)
    else:
        try:
            vals, times = _cloud_values(pick(FastHerbie([init], fxx=fxx, **kw), TCDC_NOW, points, "tcc"))
            averaged = [False] * len(vals)
        except Exception:
            vals, times, averaged = [], [], []
            for f in fxx:                                        # step by step, average as fallback
                H1 = FastHerbie([init], fxx=[f], **kw)
                for search, ave in ((TCDC_NOW, False), (TCDC_AVE, True)):
                    try:
                        v, _ = _cloud_values(pick(H1, search, points, "tcc"))
                    except Exception:
                        continue
                    vals.append(float(v[0]))
                    times.append(init + pd.Timedelta(hours=f))
                    averaged.append(ave)
                    break
            if not vals:
                raise ValueError(f"no TCDC entire-atmosphere record in f{fxx[0]}-f{fxx[-1]}")
    if times is None or len(times) != len(vals):
        times = [init + pd.Timedelta(hours=f) for f in fxx]
    return {"times": [pd.Timestamp(t).strftime("%Y-%m-%dT%H:%M") for t in times],
            "cloud_pct": [float(v) for v in vals], "averaged": averaged}


def model_cloud(station, label, init_iso, day, points, fetch_grib=True):
    """Cloud cover of one run over WxChallenge day `day`: from its cloud file, or extracted
    now (GRIB hours the file lacks; text products fetched again by run time) and saved."""
    init = pd.Timestamp(init_iso)
    rec = wxc_clouds.load_cloud(station.icao, label, init)
    if label in wxc_ens.MODELS:
        pass             # written with the run by wxc_ens (Open-Meteo keeps only the latest run)
    elif label == wxc_ifs_hres.LABEL:
        if rec is None and fetch_grib:   # written with the run; every run is archived, so ask again
            rec = wxc_ifs_hres.fetch_cloud(station, init)
    elif label in GRIB_MODELS:
        _, step, max_fxx = cloud_grib_setup(label, init, station)
        start = pd.Timestamp(datetime(day.year, day.month, day.day, 6))
        fxx, _ = forecast_hours_for_day(init, day, step, max_fxx, partial=init >= start)
        have = set((rec or {}).get("times", []))
        missing = [f for f in fxx if (init + pd.Timedelta(hours=f)).strftime("%Y-%m-%dT%H:%M") not in have]
        if missing and fetch_grib:
            new = fetch_cloud_grib(label, init, missing, points, station)
            rec = wxc_clouds.merge(rec, {"model": label, "init_time_utc": iso_hour(init), **new})
            wxc_clouds.save_cloud(station.icao, label, init, rec)
    elif label in wxc_clouds.TEXT_MODELS and rec is None:
        new = wxc_clouds.fetch_text_cloud(station.icao, label, init)
        if new:
            rec = wxc_clouds.merge(None, {"model": label, **new})
            wxc_clouds.save_cloud(station.icao, label, init, rec)
    return wxc_clouds.for_day(rec, day)


def collect_clouds(station, day, runs, points, fetch_grib=True):
    """{label: cloud series over `day`} for the runs {label: init_time_utc}. A model
    without cloud data is left out with a warning; this never raises."""
    out = {}
    for label, init in runs.items():
        if not init or (label not in GRIB_ORDER and label not in wxc_clouds.TEXT_MODELS
                        and label not in wxc_ens.MODELS):
            continue                     # CAM ensembles: no cloud cover
        try:
            rec = model_cloud(station, label, init, day, points, fetch_grib)
        except Exception as exc:
            if label == "AIFS":          # tcc may not be in the AIFS open data: skip quietly
                print(f"  (no AIFS cloud cover: {type(exc).__name__})")
            else:
                print(f"  warning: {label} cloud cover skipped ({type(exc).__name__}: {str(exc)[:150]})")
            continue
        if rec and rec.get("times"):
            out[label] = rec
    avg = [k for k, v in out.items() if any(v.get("averaged") or [])]
    print(f"  cloud cover for {day}: {', '.join(out) or 'none'}"
          + (f" (time-averaged steps in {', '.join(avg)})" if avg else ""))
    return out


# -------------------------------------------------------------------
# plotting
# -------------------------------------------------------------------
def plot_forecast(results, mos, cons, station, day, path, clouds=None):
    """clouds: {model: cloud series} adds a cloud-cover panel at the bottom (None: no panel)."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.dates as mdates
    import matplotlib.pyplot as plt

    colors = {"HRRR": "C0", "RRFS": "C8", "IFS": "C1", "IFS_HRES": wxc_verify.STYLE["IFS_HRES"][0],
              "GFS": "C2", "AIFS": "C3",
              "GFS_MOS": "C2", "NBM": "C5", "USL": "C6", "ENS": "C9", "AIFS_ENS": "C3",
              "GEFS": "C4"}
    n = 3 if clouds is None else 4
    fig, axes = plt.subplots(n, 1, figsize=(12, 10 if n == 3 else 13.3), sharex=True,
                             gridspec_kw={"height_ratios": [1, 1, 1, wxc_clouds.PANEL_RATIO][:n]})
    for name in GRIB_ORDER:
        s = results.get(name, {}).get("series")
        if not s:
            continue
        axes[0].plot(s["times"], s["temp_f"], "o-", color=colors[name], label=name)
        axes[1].plot(s["times"], s["wind_kt"], "o-", color=colors[name], label=name)
        axes[2].plot(s["times"], s["precip_in"], "o-", color=colors[name], label=name, alpha=0.8)
    w0 = pd.Timestamp(datetime(day.year, day.month, day.day, 6))
    w1 = w0 + pd.Timedelta(hours=24)
    for name in MOS_ORDER + ENS_ORDER:
        s = mos.get(name, {}).get("series")
        # GEFS (not in the consensus) is in the tables and box plots; another ensemble
        # band would bury the other lines here
        if not s or not s["times"] or name in wxc_verify.NOT_IN_CONSENSUS:
            continue
        t = pd.to_datetime(s["times"])
        if t.tz is not None:
            t = t.tz_convert(None)
        inside = (t >= w0) & (t <= w1)
        if not inside.all():
            # never draw points from outside the day: a bad timestamp would otherwise pull a
            # line across the whole panel
            print(f"  warning: {name}: {int((~inside).sum())} points outside {w0:%m-%d %HZ}-{w1:%m-%d %HZ} dropped")
        keep = [i for i in np.argsort(t.values) if inside[i]]
        t = t[keep]
        s = {k: ([v[i] for i in keep] if isinstance(v, list) and len(v) == len(inside) else v) for k, v in s.items()}
        if s.get("tmp_p10"):   # ensemble: shade the 10-90% range of the members
            axes[0].fill_between(t, s["tmp_p10"], s["tmp_p90"], color=colors[name], alpha=0.12, lw=0,
                                 label=f"{name} 10-90%")
        axes[0].plot(t, s["tmp_f"], "s--", color=colors[name], label=name, alpha=0.8)
        axes[1].plot(t, s["wsp_kt"], "s--", color=colors[name], label=name, alpha=0.8)
        if s.get("precip_cum_in"):
            axes[2].plot(t, s["precip_cum_in"], "s--", color=colors[name], label=name, alpha=0.8)
    if cons.get("tmax_f") is not None:
        axes[0].axhline(cons["tmax_f"], color="k", ls=":", lw=1.5, label="Consensus high/low")
        axes[0].axhline(cons["tmin_f"], color="k", ls=":", lw=1.5)
    if cons.get("wind_max_kt") is not None:
        axes[1].axhline(cons["wind_max_kt"], color="k", ls=":", lw=1.5, label="Consensus max")
    for ax, lab in zip(axes, ["Temperature (°F)", "Wind speed (kt)", "Accumulated precip (in)"]):
        ax.set_ylabel(lab)
        ax.grid(True, linestyle="--", alpha=0.4)
        ax.legend(loc="best", fontsize=8, ncol=2)
    if clouds is not None:
        try:
            # the same "o-" (grid models) / "s--" alpha 0.8 (text guidance) lines as above
            # GEFS left out, as in the panels above
            clouds = {k: v for k, v in clouds.items() if k not in wxc_verify.NOT_IN_CONSENSUS or k in GRIB_ORDER}
            wxc_clouds.draw_models(axes[3], clouds, lambda n: dict(ls="--", marker="s", alpha=0.8)
                                   if n in MOS_ORDER + ENS_ORDER else dict(ls="-", marker="o"))
        except Exception as exc:          # never lose the figure over the cloud panel
            print(f"  warning: cloud panel left empty ({type(exc).__name__}: {exc})")
        axes[3].xaxis.grid(True, linestyle="--", alpha=0.4)
        wxc_clouds.style_axis(axes[3])
    axes[-1].set_xlabel("Valid time (UTC)")
    axes[-1].set_xlim(w0, w1)          # always the forecast day, even if a series is off
    axes[-1].xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d\n%H:%M"))
    plt.setp(axes[-1].xaxis.get_majorticklabels(), rotation=30, ha="right")
    fig.suptitle(f"{station.label}: forecast for {day:%a %b %d} (06Z-06Z)", y=0.98)
    fig.tight_layout(rect=[0, 0, 1, 0.96])
    wxc_verify.save_png(fig, path, dpi=150)
    plt.close(fig)


# -------------------------------------------------------------------
# main
# -------------------------------------------------------------------
PUSH_HINTS = [
    (("could not read username", "authentication failed", "terminal prompts disabled",
      "permission denied", "403", "invalid username or password"),
     "GitHub rejected or never received credentials on this computer. One-time fix in a terminal:\n"
     "    brew install gh && gh auth login && gh auth setup-git\n"
     "(or sign in with a personal access token and let the macOS keychain store it)."),
    (("rejected", "fetch first", "non-fast-forward"),
     "GitHub has commits this computer doesn't. Run:  git pull --rebase origin main  then re-run."),
    (("could not resolve host", "unable to access", "timed out"),
     "Network problem reaching github.com; the commit is saved locally and will go up next run."),
]


def git_push(now_iso):
    """Commit data/images/page and push. Unpushed commits from earlier failed runs are
    pushed too, and a failed push is reported loudly (it used to fail silently)."""
    import os
    env = {**os.environ, "GIT_TERMINAL_PROMPT": "0"}   # fail fast under cron instead of waiting for a password

    def git(*args, check=True):
        return subprocess.run(["git", *args], cwd=ROOT, env=env, capture_output=True, text=True, check=check)

    try:
        git("add", str(DATA.relative_to(ROOT)), str(IMAGES.relative_to(ROOT)),
            str((ROOT / "wxchallenge" / "index.html").relative_to(ROOT)))
        if git("diff", "--cached", "--quiet", check=False).returncode == 1:
            git("commit", "-m", f"update wxchallenge: {now_iso}")
            print(f"Git: committed update wxchallenge: {now_iso}")
        else:
            print("Git: nothing new to commit")
        branch = git("rev-parse", "--abbrev-ref", "HEAD").stdout.strip()
        if branch != "main":
            print(f"Git: warning, on branch '{branch}'; the website is built from main")
        r = git("push", "origin", branch, check=False)
        if r.returncode == 0:
            print("Git: pushed to GitHub (website updates in a minute or two)")
            return True
        err = (r.stderr or r.stdout).strip()
        hint = next((h for keys, h in PUSH_HINTS if any(k in err.lower() for k in keys)), "")
        bar = "!" * 72
        print(f"\n{bar}\nGIT PUSH FAILED: the website was NOT updated.\n{err}\n\n{hint}\n{bar}\n")
    except subprocess.CalledProcessError as exc:
        print(f"Git step failed: {' '.join(exc.cmd)}\n{(exc.stderr or '').strip()}")
    return False


def run_models(station, day, points, as_of=None, skip_grib=False, only=None, partial=False):
    """All models for WxChallenge day `day`; as_of=None means the latest runs,
    otherwise the runs that were available at `as_of` (hindcast)."""
    results = {}
    for label, (cycle_key, fn) in GRIB_MODELS.items():
        if skip_grib or (only is not None and label not in only):
            continue
        if label == "HRRR" and not station.hrrr_model:
            print("Skipping HRRR (station outside HRRR domains)")
            continue
        if label == "RRFS" and not station.rrfs_domain:
            print("Skipping RRFS (station outside RRFS domains)")
            continue
        results[label] = fetch_with_fallback(label, cycle_key, fn, day, points, station, as_of, partial)
    # IFS HRES 9 km: one small request (so also with skip_grib); every run archived, so hindcast too
    if not partial and (only is None or wxc_ifs_hres.LABEL in only):
        results[wxc_ifs_hres.LABEL] = wxc_ifs_hres.get_forecast(station, day, as_of)
    mos = {}
    if only is None or any(k in only for k in MOS_ORDER):
        print("Fetching MOS / NBM text guidance...")
        mos = wxc_mos.get_mos_forecasts(station.icao, day, as_of, only)
    if only is None or "USL" in only:
        mos["USL"] = wxc_usl.get_usl_forecast(station.icao, day, as_of)
        u = mos["USL"]
        print(f"  {'USL':8s} {u.get('init_time_utc')}: " + (u.get("error") or
              f"{u['tmax_f']}/{u['tmin_f']}F {u['wind_max_kt']}kt {u['precip_in']}in"))
    if not partial and (only is None or any(k in only for k in ENS_ORDER)):
        print("Fetching global ensembles (Open-Meteo)...")
        mos.update(wxc_ens.get_ensembles(station, day, as_of, only))
    # 3 km precip ensembles: live runs only (no hindcasts; HRRRCast is ~1 GB per cycle)
    if as_of is None and not partial and not skip_grib and (only is None or any(k in only for k in CAM_ORDER)):
        print("Fetching 3 km precip ensembles (REFS, HRRRCast)...")
        mos.update(wxc_cam_ens.get_cam_ensembles(station, day, only=only))
    # NBM QMD calibrated PoP + precip percentiles: live runs only (~29 MB per new cycle)
    if as_of is None and not partial and not skip_grib and (only is None or wxc_nbm_qmd.LABEL in only):
        print("Fetching NBM QMD probabilistic precip...")
        try:
            mos[wxc_nbm_qmd.LABEL] = wxc_nbm_qmd.get_qmd(station, day)
        except Exception as exc:
            mos[wxc_nbm_qmd.LABEL] = wxc_nbm_qmd._fail(f"{type(exc).__name__}: {exc}")
        if mos[wxc_nbm_qmd.LABEL].get("error"):
            print(f"  {wxc_nbm_qmd.LABEL:8s} {mos[wxc_nbm_qmd.LABEL].get('init_time_utc')}: "
                  f"{mos[wxc_nbm_qmd.LABEL]['error']}")
    models = {k: results[k]["metrics"] for k in GRIB_ORDER if k in results}
    models.update({k: {kk: vv for kk, vv in v.items() if kk != "series"} for k, v in mos.items()})
    return results, mos, models


def collect_series(results, mos):
    """Hourly/3-hourly series of every model in a compact, JSON-friendly form."""
    out = {}
    for k in GRIB_ORDER:
        r = results.get(k) or {}
        s = r.get("series")
        if s:
            out[k] = {"init_time_utc": r["metrics"].get("init_time_utc"),
                      "tmax_f": r["metrics"].get("tmax_f"), "tmin_f": r["metrics"].get("tmin_f"),
                      "times": [pd.Timestamp(t).strftime("%Y-%m-%dT%H:%M") for t in s["times"]],
                      "temp_f": [round(float(v), 1) for v in s["temp_f"]],
                      "wind_kt": [round(float(v), 1) for v in s["wind_kt"]],
                      "precip_in": [round(float(v), 3) for v in s["precip_in"]]}
            if s.get("dewpt_f") is not None:            # display only
                out[k]["dewpt_f"] = [None if not np.isfinite(v) else round(float(v), 1) for v in s["dewpt_f"]]
    for k in MOS_ORDER + ENS_ORDER:
        m = mos.get(k) or {}
        s = m.get("series")
        if s and s.get("times"):
            out[k] = {"init_time_utc": m.get("init_time_utc"), "times": s["times"],
                      # the scored daily values (e.g. USL/MOS daily summary), which can go
                      # beyond the hourly values
                      "tmax_f": m.get("tmax_f"), "tmin_f": m.get("tmin_f"),
                      "temp_f": s.get("tmp_f"), "wind_kt": s.get("wsp_kt"),
                      "precip_in": s.get("precip_cum_in")}
            if s.get("dpt_f"):                           # MOS / NBM / ensemble dewpoint, display only
                out[k]["dewpt_f"] = s["dpt_f"]
            if s.get("rh_pct"):                          # ensembles: the members' mean RH, display only
                out[k]["rh_pct"] = s["rh_pct"]
            if s.get("tmp_p10") and s.get("tmp_p90"):      # ensembles: members' 10-90% range
                out[k]["temp_p10"], out[k]["temp_p90"] = s["tmp_p10"], s["tmp_p90"]
    return out


def save_hindcast_series(station, day, as_of, results, mos):
    """Hourly series of a hindcast (the runs out at 23Z the day before) as the day's
    'submitted' series, so the page's timeline reaches back over a new city's hindcast days.
    Never replaces a live pre-deadline series; models from an earlier hindcast of the day stay."""
    ser = collect_series(results, mos)
    if not ser:
        return None
    old = wxc_verify.load_series(station.icao, day, "submitted")
    if old is not None and not old.get("hindcast"):
        return None
    models = {**((old or {}).get("models") or {}), **ser}
    return wxc_verify.save_series(station.icao, day, "submitted", as_of.isoformat(), models, hindcast=True)


def today_clouds(station, today, start, now, points, sub, lat, raw, skip_grib=False):
    """Cloud cover for the today-so-far figure (display only; each part fails on its own)."""
    out = {}
    for kind, group in (("submitted", sub), ("latest", lat)):
        runs = {k: m.get("init_time_utc") for k, m in ((group or {}).get("models") or {}).items()}
        out[kind] = collect_clouds(station, today, runs, points, fetch_grib=not skip_grib)
    try:
        out["metar"] = wxc_clouds.sky_series(raw)
    except Exception as exc:
        print(f"  warning: METAR sky cover skipped ({type(exc).__name__}: {exc})")
    if wxc_clouds.GOES_ENABLED:
        try:
            out["goes"] = wxc_goes.hourly_cloud(station, start, now)
        except Exception as exc:
            print(f"  warning: GOES cloud mask skipped ({type(exc).__name__}: {exc})")
    return out


CLOUD_CONTEXT = DATA / "cloud_context.json"
CLOUD_FORECAST = DATA / "cloud_forecast.json"   # the target day's model cloud cover (wxc_brief.py)
CLOUD_TODAY = DATA / "cloud_today.json"         # today's GOES / METAR / model clouds (wxc_brief.py)


def write_cloud_today(station, today, now, clouds):
    """Today's observed clouds (GOES hourly, METAR nearest each hour) and the submitted runs'
    cloud forecasts, for the AI brief. Display only, like cloud_context.json."""
    metar = []
    sky = clouds.get("metar")
    if sky is not None and not sky.empty:
        s = sky.assign(hour=sky["valid"].dt.round("h"),
                       dist=(sky["valid"] - sky["valid"].dt.round("h")).abs())
        s = s.sort_values(["hour", "dist"]).drop_duplicates("hour")
        metar = [{"hour": h.strftime("%Y-%m-%dT%H:%M"), "sky_pct": round(float(p), 1)}
                 for h, p in zip(s["hour"], s["sky_pct"])]
    goes = [{k: r.get(k) for k in ("hour", "cloud_pct", "satellite", "n_pixels")}
            for r in clouds.get("goes") or []]
    CLOUD_TODAY.write_text(wxc_verify.dumps(
        {"station": station.icao, "date": today.isoformat(), "generated_at_utc": now.isoformat(),
         "goes": goes, "metar": metar, "models": clouds.get("submitted") or {}}))
CONTEXT_ATTEMPTS = 3          # runs that may retry a day with missing pieces before it is frozen
CONTEXT_BUDGET_S = 240        # per run: older days still to fill are left for the next runs
TIMELINE_BUDGET_S = 180       # per run, for the timeline's catch-up downloads (GOES, old cloud cover)
TIMELINE_GOES_DAYS = 3        # finished days that get their missing GOES hours (~5 MB each); older
                              # (hindcast) days show METAR sky cover only, unless asked for
                              # (scripts/backfill_timeline.py --goes)


CYCLE_BUDGET_S = 150          # per run, for the 12Z/18Z toggle's backfill downloads
# models the backfill can fetch at a given init (the ensembles can't: Open-Meteo serves only
# the latest run, so their cycle rows come from the live runs alone)
CYCLE_SOURCES = ["HRRR", "RRFS", "GFS", "IFS", wxc_ifs_hres.LABEL, "GFS_MOS", "NBM", "USL"]


def fetch_cycle(station, label, init, day, points):
    """One model's forecast for `day` from the run initialized at `init` (naive UTC), as metrics,
    or {"error": ...}. GRIB models from the saved results or a download; the others by asking
    for the runs out just after `init`, then checking the run that came back is that one."""
    if label in GRIB_MODELS:
        cycle_key, fn = GRIB_MODELS[label]
        cached = wxc_cache.load(station.icao, label, init, day)
        if cached is not None:
            return cached["metrics"]
        try:
            res = fn(pd.Timestamp(init), day, points, station)
        except Exception as exc:
            return {"error": f"{type(exc).__name__}: {exc}"}
        if "unavailable" not in (res["metrics"].get("note") or ""):
            wxc_cache.save(station.icao, label, pd.Timestamp(init), day, res)
        return res["metrics"]
    t = init.replace(tzinfo=timezone.utc)
    if label == wxc_ifs_hres.LABEL:
        m = wxc_ifs_hres.get_forecast(station, day, t + timedelta(hours=wxc_ifs_hres.PUBLISH_DELAY_HOURS))["metrics"]
    elif label == "GFS_MOS":
        m = wxc_mos.get_mos_forecasts(station.icao, day, t + timedelta(hours=wxc_mos.MOS_CYCLES["GFS"][1]),
                                      only=[label])[label]
    elif label == "NBM":
        import wxc_nbm_text
        m = wxc_mos.get_mos_forecasts(station.icao, day, t + timedelta(hours=wxc_nbm_text.posted_delay(init.hour)),
                                      only=[label])[label]
    elif label == "USL":
        m = wxc_usl.get_usl_forecast(station.icao, day, t + timedelta(minutes=30))
    else:
        return {"error": f"no backfill for {label}"}
    if m.get("error"):
        return m
    if wxc_verify._init_time(m) != init:
        return {"error": f"{init:%Y-%m-%d %HZ} run not found (got {m.get('init_time_utc')})"}
    return m


def cycle_backfill(station, verif, points, now, fetch_grib=True, budget_s=CYCLE_BUDGET_S):
    """The 12Z/18Z runs the page's toggle scores separately (wxc_verify.CYCLES; display only),
    for the period's days (hindcast days included) and today, where the live runs didn't keep
    them. Stored in cycle_runs.jsonl, never runs.jsonl. Returns how many were added."""
    import time as _time
    t0 = _time.time()
    days = [d["date"] for d in (verif or {}).get("days") or []]
    days.append((now - timedelta(hours=6)).date().isoformat())     # today's forecasts (made yesterday)
    models = [m for m in CYCLE_SOURCES if (fetch_grib or m not in GRIB_MODELS)
              and (m != "HRRR" or station.hrrr_model) and (m != "RRFS" or station.rrfs_domain)]
    plan = wxc_verify.cycle_plan(wxc_verify.read_runs(), wxc_verify.read_jsonl(wxc_verify.CYCLE_RUNS),
                                 station.icao, sorted(set(days)), models)
    added = 0
    for i, (day, label, init) in enumerate(plan):
        if budget_s is not None and _time.time() - t0 > budget_s:
            print(f"  {len(plan) - i} runs left for the next run (time budget)")
            break
        print(f"  {label} {init:%Y-%m-%d %HZ} for {day}")
        m = fetch_cycle(station, label, init, date.fromisoformat(day), points)
        err = m.get("error") or (None if all(m.get(v) is not None for v in wxc_verify.VARS) else "no values")
        if err and wxc_carryover.is_network_error(err):
            print(f"    not reached (left for the next run): {err[:120]}")
            continue
        if err:
            print(f"    failed: {err[:160]}")
        wxc_verify.append_cycle_run(station.icao, day, label, init, m, now.isoformat(), err)
        added += not err
    return added


def timeline_update(station, now, points, verif, fetch_grib=True, budget_s=TIMELINE_BUDGET_S,
                    goes_days=TIMELINE_GOES_DAYS):
    """The page's scrollable timeline (wxc_timeline.py; display only). Fills in what the runs
    during the day couldn't save: a finished day's last reports (the schedule stops at the 00Z
    deadline, the day ends at 06Z) with its overnight GOES hours, and the cloud cover and
    dewpoints of days from before they were saved. Then writes data/wxchallenge/timeline.json."""
    import time as _time
    t0 = _time.time()
    icao = station.icao
    days = wxc_timeline.timeline_days(DATA, icao, since=(verif or {}).get("period_start"))
    today = (now - timedelta(hours=6)).date()
    goes_from = today - timedelta(days=goes_days) if goes_days is not None else date.min

    # finished days without a complete record of their reports, or saved before dewpoints were
    # (their GOES hours are kept): one METAR request for all
    def needs_obs(rec):
        return not rec.get("complete") or ((rec.get("reports") or {}).get("times") and
                                           "dewpt_f" not in rec["reports"])
    todo = [d for d in days if d < today and wxc_timeline.is_final(d, now)]
    todo = [d for d in todo if needs_obs(wxc_timeline.load_day(DATA, icao, d, "obs") or {})]
    raw = None
    if todo:
        first, last = min(todo), max(todo)
        span = (datetime(first.year, first.month, first.day, 6, tzinfo=timezone.utc),
                datetime(last.year, last.month, last.day, 6, tzinfo=timezone.utc) + timedelta(days=1))
        try:
            raw = (wxc_obs.fetch_metars(icao, *span, specials=True, sky=True) if wxc_clouds.CLOUDS_ENABLED
                   else wxc_obs.fetch_metars(icao, *span, specials=True))
        except Exception as exc:
            print(f"  warning: timeline METARs {first}..{last} failed ({type(exc).__name__}: {exc})")
    for d in sorted(todo, reverse=True) if raw is not None else []:
        old = wxc_timeline.load_day(DATA, icao, d, "obs") or {}
        part = wxc_timeline.day_reports(raw, d)
        reports = wxc_obs.report_series(part) if not part.empty else None
        sky = goes = None
        want_goes = wxc_clouds.CLOUDS_ENABLED and wxc_clouds.GOES_ENABLED and d >= goes_from
        if old.get("complete"):            # only the dewpoints were missing: keep its GOES hours
            g = old.get("goes") or {}
            goes = [{"hour": t, "cloud_pct": v} for t, v in zip(g.get("times") or [], g.get("pct") or [])]
            want_goes = False
        if wxc_clouds.CLOUDS_ENABLED:
            try:
                sky = wxc_clouds.sky_series(part)
            except Exception as exc:
                print(f"  warning: timeline sky cover {d} skipped ({type(exc).__name__}: {exc})")
            if want_goes and _time.time() - t0 < budget_s:
                s = datetime(d.year, d.month, d.day, 6, tzinfo=timezone.utc)
                try:
                    goes = wxc_goes.hourly_cloud(station, s, s + timedelta(hours=24))
                except Exception as exc:
                    print(f"  warning: timeline GOES {d} skipped ({type(exc).__name__}: {exc})")
        attempts = 1 if old.get("complete") else old.get("attempts", 0) + 1
        whole = not want_goes or bool(goes and len(goes) >= 23)
        rec = wxc_timeline.obs_record(icao, d, reports, sky, goes, now,
                                      complete=(reports is not None and whole) or attempts >= CONTEXT_ATTEMPTS)
        rec["attempts"] = attempts
        wxc_timeline.save_day(DATA, icao, d, "obs", rec)
        print(f"  timeline obs {d}: {0 if reports is None else len(reports)} reports, "
              f"{len(goes or [])} GOES hours{'' if rec['complete'] else ' (incomplete, retried next run)'}")

    # cloud cover of the submitted runs of past days (today and the forecast day are written
    # by today_figure and main); mostly from the cloud cache, else downloaded again
    if wxc_clouds.CLOUDS_ENABLED:
        for d in sorted((d for d in days if d < today), reverse=True):
            old = wxc_timeline.load_day(DATA, icao, d, "clouds") or {}
            if old.get("submitted") or old.get("attempts", 0) >= CONTEXT_ATTEMPTS:
                continue
            if _time.time() - t0 > budget_s:
                print("  timeline: time budget used; older cloud cover left for the next run")
                break
            sub = wxc_timeline.load_series(DATA, icao, d, "submitted") or {}
            runs = {k: m.get("init_time_utc") for k, m in (sub.get("models") or {}).items()}
            clouds = collect_clouds(station, d, runs, points, fetch_grib=fetch_grib)
            rec = wxc_timeline.clouds_record(icao, d, clouds, None, now)
            rec["attempts"] = old.get("attempts", 0) + 1
            wxc_timeline.save_day(DATA, icao, d, "clouds", rec)

    # dewpoints of series saved before they were kept (display only; newest days first)
    for d in sorted((d for d in days if d <= today), reverse=True):
        if _time.time() - t0 > budget_s:
            print("  timeline: time budget used; older dewpoints left for the next run")
            break
        n = series_dewpoints(station, d, points, fetch_grib, deadline=t0 + budget_s)
        if n:
            print(f"  timeline dewpoints {d}: {n} model(s)")

    try:
        today_json = json.loads((DATA / "today.json").read_text())
    except (FileNotFoundError, json.JSONDecodeError):
        today_json = None
    bundle = wxc_timeline.build(DATA, icao, now, verif, today_json, station.label,
                                since=(verif or {}).get("period_start"), lat=station.lat, lon=station.lon)
    if bundle:
        path = wxc_timeline.write(DATA, bundle)
        print(f"  timeline: {len(bundle['days'])} days ({bundle['days'][0]['date']}..{bundle['days'][-1]['date']}) "
              f"in {_time.time() - t0:.0f} s -> {path.name}")


def series_dewpoints(station, day, points, fetch_grib=True, deadline=None):
    """Dewpoints (display only) for a day's submitted series saved before they were kept: GRIB
    runs from the model cache or downloaded again (that one field), GFS MOS (IEM) / NBM (AWS) by
    run time, USL from its run page. A model whose dewpoint can't be had gets dewpt_f None, so it isn't asked again.
    Stops at `deadline` (time.time()); returns the number of models filled."""
    import time as _time
    path = wxc_verify.SERIES_DIR / f"{station.icao}_{day.isoformat()}_submitted.json"
    try:
        rec = json.loads(path.read_text())
    except (FileNotFoundError, json.JSONDecodeError):
        return 0
    done = 0
    for name, m in (rec.get("models") or {}).items():
        if "dewpt_f" in m or not m.get("times") or not m.get("init_time_utc"):
            continue
        if name not in DEWPT_SEARCH and name not in wxc_mos.MOS_PRODUCTS and name != "USL":
            continue                     # ensembles: dewpoint only from when it was kept (no rebuild)
        if deadline is not None and _time.time() > deadline:
            break
        td = None
        if name in DEWPT_SEARCH:
            init = pd.Timestamp(m["init_time_utc"] + ":00")
            cached = wxc_cache.load(station.icao, name, init, day) or {}
            cs = cached.get("series") or {}
            if cs.get("dewpt_f") is not None and len(cs["dewpt_f"]) == len(cs["times"]):
                by_t = dict(zip(pd.to_datetime(cs["times"]).strftime("%Y-%m-%dT%H:%M"), cs["dewpt_f"]))
                td = [by_t.get(t) for t in m["times"]]
            elif fetch_grib:
                res = {"series": {"times": pd.to_datetime(m["times"])}, "metrics": {"init_time_utc": m["init_time_utc"]}}
                add_dewpoint(name, res, points, station)
                td = res["series"].get("dewpt_f")
            else:
                continue
            td = None if td is None else [None if v is None or not np.isfinite(v) else round(float(v), 1) for v in td]
        elif name == "USL":
            try:
                by_t = wxc_usl.run_dewpoints(station.icao, m["init_time_utc"], day) or {}
                td = [by_t.get(t) for t in m["times"]]
            except Exception as exc:
                print(f"  warning: USL dewpoint {day} skipped ({type(exc).__name__}: {str(exc)[:150]})")
        else:
            try:
                rt = datetime.strptime(m["init_time_utc"], "%Y-%m-%dT%H").replace(tzinfo=timezone.utc)
                ms = wxc_mos.summarize_mos(wxc_mos.fetch_mos(station.icao, wxc_mos.MOS_PRODUCTS[name], rt),
                                           day, wxc_mos.MOS_PRODUCTS[name]).get("series") or {}
                by_t = dict(zip(ms.get("times") or [], ms.get("dpt_f") or []))
                td = [by_t.get(t) for t in m["times"]]
            except Exception as exc:
                print(f"  warning: {name} dewpoint {day} skipped ({type(exc).__name__}: {str(exc)[:150]})")
        m["dewpt_f"] = td if td and any(v is not None for v in td) else None
        done += 1
    if done:
        tmp = path.with_suffix(".tmp")
        tmp.write_text(wxc_verify.dumps(rec))
        tmp.replace(path)
    return done


def cloud_context(station, verif, points, fetch_grib=True, budget_s=CONTEXT_BUDGET_S):
    """Forecast vs observed cloud (day / night) of every scored run on the scoreboard, in
    data/wxchallenge/cloud_context.json. DISPLAY ONLY: verification.json, the scores and the
    consensus never see it. Days are added once and kept (the cloud cache is pruned, this file
    is not); a day with missing pieces is retried for up to CONTEXT_ATTEMPTS runs."""
    import time as _time
    t0 = _time.time()
    try:
        store = json.loads(CLOUD_CONTEXT.read_text())
    except (FileNotFoundError, json.JSONDecodeError):
        store = {}
    store.setdefault("note", "Display only: cloud cover is not scored. Errors are forecast minus "
                             "observed in percentage points (positive = too cloudy).")
    days_store = store.setdefault("stations", {}).setdefault(station.icao, {})
    eligible = set(GRIB_ORDER) | set(wxc_clouds.TEXT_MODELS) | set(wxc_ens.MODELS)
    todo = []
    for d in verif.get("days", []):
        old = days_store.get(d["date"])
        if old and (old.get("complete") or old.get("attempts", 0) >= CONTEXT_ATTEMPTS):
            continue
        todo.append(d)
    if not todo:
        print("  cloud context: up to date")
        return 0
    todo.sort(key=lambda d: d["date"], reverse=True)        # newest first: what you look at
    first, last = date.fromisoformat(todo[-1]["date"]), date.fromisoformat(todo[0]["date"])
    sky = pd.DataFrame(columns=["valid", "sky_pct", "clear"])
    try:
        raw = wxc_obs.fetch_metars(station.icao, datetime(first.year, first.month, first.day, 5, tzinfo=timezone.utc),
                                   datetime(last.year, last.month, last.day, 6, tzinfo=timezone.utc) + timedelta(days=1),
                                   sky=True)
        sky = wxc_clouds.sky_series(raw)
    except Exception as exc:
        print(f"  warning: METAR sky cover for {first}..{last} failed ({type(exc).__name__}: {exc})")
    runs = wxc_verify.read_runs()
    done = 0
    for d in todo:
        if _time.time() - t0 > budget_s:
            print(f"  cloud context: time budget used; {len(todo) - done} older day(s) left for the next run")
            break
        day = date.fromisoformat(d["date"])
        scored = wxc_verify.forecasts_for_day(runs, station.icao, d["date"])
        models = {}
        for name in d.get("models", {}):
            fc = scored.get(name, (None,))[0]
            init = (fc or {}).get("init_time_utc")
            if name not in eligible or not init:
                continue
            if name in wxc_ens.MODELS and wxc_clouds.load_cloud(station.icao, name, pd.Timestamp(init)) is None:
                continue         # a run from before ensemble cloud cover was kept: can't be had
            try:
                models[name] = (init, model_cloud(station, name, init, day, points, fetch_grib))
            except Exception as exc:
                print(f"  warning: {d['date']} {name} cloud cover unavailable ({type(exc).__name__}: {str(exc)[:120]})")
                models[name] = (init, None)
        goes = {}
        for h in range(25):
            t = datetime(day.year, day.month, day.day, 6) + timedelta(hours=h)
            try:
                goes[t.strftime("%Y-%m-%dT%H:%M")] = json.loads(wxc_goes._cache_path(station.icao, t).read_text())["cloud_pct"]
            except (FileNotFoundError, json.JSONDecodeError, KeyError):
                pass
        ctx = wxc_clouds.day_context(day, station.lat, station.lon, sky, goes, models)
        old = days_store.get(d["date"]) or {}
        # keep what an earlier attempt found if this one could not get it again
        for name, m in (old.get("models") or {}).items():
            if name not in ctx["models"]:
                ctx["models"][name] = m
                ctx["missing"].pop(name, None)
        if ctx["obs"]["day_pct"] is None and (old.get("obs") or {}).get("day_pct") is not None:
            ctx["obs"] = old["obs"]
        ctx["attempts"] = old.get("attempts", 0) + 1
        ctx["complete"] = not ctx["missing"] and ctx["obs"]["day_pct"] is not None \
            and ctx["obs"]["night_pct"] is not None
        days_store[d["date"]] = ctx
        done += 1
    store["generated_at_utc"] = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    CLOUD_CONTEXT.write_text(wxc_verify.dumps(store, indent=1))
    print(f"  cloud context: {done} day(s) updated in {_time.time() - t0:.0f} s -> {CLOUD_CONTEXT.name}")
    return done


def today_figure(station, now, points, skip_grib=False):
    """Observations for the current 06Z-06Z day so far vs. the submitted and latest forecasts."""
    today = (now - timedelta(hours=6)).date()
    start = datetime(today.year, today.month, today.day, 6, tzinfo=timezone.utc)
    print(f"\nToday so far ({today}, 06Z-06Z)")
    sub = wxc_verify.load_series(station.icao, today, "submitted")
    # No stored pre-deadline run (or only an older rebuild made from earlier runs, which
    # may miss e.g. the 22Z USL): rebuild from everything out just before the 00Z deadline.
    as_of = datetime(today.year, today.month, today.day, tzinfo=timezone.utc) - timedelta(minutes=1)
    stale = (sub is not None and sub.get("hindcast")
             and pd.to_datetime(sub.get("generated_at_utc") or 0, utc=True) < pd.Timestamp(as_of))
    if sub is None or stale:
        why = "older rebuild" if stale else "no stored pre-deadline series"
        print(f"  {why} for {today}; rebuilding from runs available at {as_of:%Y-%m-%d %H:%MZ}")
        r, m, _ = run_models(station, today, points, as_of, skip_grib)
        ser = collect_series(r, m)
        if ser:      # nothing fetched (offline): don't store an empty rebuild, try again next run
            wxc_verify.save_series(station.icao, today, "submitted", as_of.isoformat(), ser, hindcast=True)
            sub = wxc_verify.load_series(station.icao, today, "submitted")
    print("  latest runs for the rest of today:")
    r, m, _ = run_models(station, today, points, None, skip_grib, only=TODAY_LATEST_FETCH, partial=True)
    ser = collect_series(r, m)
    prev = (wxc_verify.load_series(station.icao, today, "latest") or {}).get("models") or {}
    # a model that failed this time (e.g. offline) keeps its previous latest run
    ser = {**{k: v for k, v in prev.items() if k in TODAY_LATEST_FETCH}, **ser}
    wxc_verify.save_series(station.icao, today, "latest", now.isoformat(), ser)
    lat = wxc_verify.load_series(station.icao, today, "latest")
    raw = None
    if wxc_clouds.CLOUDS_ENABLED:          # same request plus the sky columns (display only)
        try:
            raw = wxc_obs.fetch_metars(station.icao, start, now, specials=True, sky=True)
        except Exception as exc:
            print(f"  warning: METAR sky request failed ({type(exc).__name__}: {exc}); plain METARs used")
    if raw is None:
        raw = wxc_obs.fetch_metars(station.icao, start, now, specials=True)
    if not raw.empty:   # only this day's reports, so the running precip total starts at 06Z
        t = pd.to_datetime(raw["valid"], utc=True)
        raw = raw[(t > pd.Timestamp(start)) & (t <= pd.Timestamp(now))]
    obs = wxc_obs.report_series(raw)
    clouds = None
    if wxc_clouds.CLOUDS_ENABLED:
        try:
            clouds = today_clouds(station, today, start, now, points, sub, lat, raw, skip_grib)
            write_cloud_today(station, today, now, clouds)
        except Exception as exc:
            print(f"  warning: cloud cover skipped ({type(exc).__name__}: {exc})")
    try:          # today's reports and cloud cover for the page's timeline (display only)
        c = clouds or {}
        wxc_timeline.save_day(DATA, station.icao, today, "obs", wxc_timeline.obs_record(
            station.icao, today, obs, c.get("metar"), c.get("goes"), now, complete=False))
        if c.get("submitted") or c.get("latest"):
            wxc_timeline.save_day(DATA, station.icao, today, "clouds", wxc_timeline.clouds_record(
                station.icao, today, c.get("submitted"), c.get("latest"), now))
    except Exception as exc:
        print(f"  warning: timeline files for today skipped ({type(exc).__name__}: {exc})")
    # the figure draws only TODAY_LATEST's newest runs (the rest are for the AI brief)
    lat_fig = lat and {**lat, "models": {k: v for k, v in (lat.get("models") or {}).items() if k in TODAY_LATEST}}
    clouds_fig = clouds and {**clouds, "latest": {k: v for k, v in (clouds.get("latest") or {}).items()
                                                  if k in TODAY_LATEST}}
    wxc_today.plot_today(station, today, now, obs, sub, lat_fig, IMAGES / "today.png", clouds=clouds_fig)
    print(f"Wrote {IMAGES / 'today.png'}")
    bias = wxc_today.today_bias(obs, sub, today, now)
    bias.update({"station": station.icao, "generated_at_utc": now.isoformat()})
    (DATA / "today.json").write_text(wxc_verify.dumps(bias, indent=2))
    try:          # the scoreboard's provisional "today" column (display only, never in the consensus)
        wxc_verify.write_today_column(station.icao, bias)
    except Exception as exc:
        print(f"  warning: today's verification column skipped ({type(exc).__name__}: {exc})")
    if bias["models"]:
        o = bias["obs"]
        print(f"  So far through {bias['through_utc'][11:16]}Z: obs high {o['high']:.0f} low {o['low']:.0f} "
              f"wind {o['wind']:.0f} kt precip {o['precip']:.2f}")
        print(f"  {'model':10s} {'T bias':>6s} {'T MAE':>6s} {'hi err':>6s} {'lo err':>6s} {'wind':>5s} {'pcp err':>7s}")
        for name, r in sorted(bias["models"].items(), key=lambda kv: kv[1]["temp_mae"]):
            f = lambda v, d=1: "   --" if v is None else f"{v:+.{d}f}"  # noqa: E731
            print(f"  {name:10s} {f(r['temp_bias']):>6s} {r['temp_mae']:6.1f} {f(r.get('high_err')):>6s} "
                  f"{f(r.get('low_err')):>6s} {f(r.get('wind_bias')):>5s} {f(r.get('precip_err'), 2):>7s}")


def print_pop(models):
    """Console PoP table (display only)."""
    rows = [(k, m["pop"]) for k, m in models.items() if m.get("pop")]
    if not rows:
        return
    pc = lambda p: "  --" if p is None else f"{p:4.0%}"  # noqa: E731
    print(f"\nChance of >= 0.01\" (PoP)  {'  '.join(wxc_pop.BLOCK_LABELS)}     24 h")
    for k, p in rows:
        b = p.get("blocks") or {}
        p24 = (pc(p["p24"]) if p.get("p24") is not None else
               (f"{p['p24_range'][0]:.0%}-{p['p24_range'][1]:.0%}" if p.get("p24_range") else "  --"))
        n = f"  ({p['n_members']} members)" if p.get("n_members") else ""
        print(f"  {k:22s} " + "  ".join(f"{pc(b.get(x)):>5s}" for x in wxc_pop.BLOCK_LABELS) + f"   {p24}{n}")


def main():
    ap = argparse.ArgumentParser(description="WxChallenge forecast + verification")
    ap.add_argument("station", nargs="?", help="ICAO id (default: wxc_stations.CURRENT_STATION)")
    ap.add_argument("--target-date", help="forecast day YYYY-MM-DD (default: next day open for submission)")
    ap.add_argument("--obs-days", type=int, default=4, help="completed days of observations to (re)fetch")
    ap.add_argument("--no-push", action="store_true", help="skip git commit/push")
    ap.add_argument("--skip-grib", action="store_true", help="MOS/NBM + verification only (fast)")
    ap.add_argument("--no-today", action="store_true", help="skip the 'today so far' figure")
    ap.add_argument("--hindcast-days", type=int, default=wxc_verify.HINDCAST_DAYS,
                    help="re-create model forecasts for up to N recent days that have no stored run "
                         "(so biases are available from day one of a new city; days already hindcast "
                         "are skipped, so only the first run of a city is slow); 0 disables")
    args = ap.parse_args()

    # Laptop woke without wifi: every source would fail (and log a traceback each), nothing could
    # be pushed, and the page already shows the last good forecasts. Skip; the next run catches up.
    if not wxc_carryover.network_up():
        print(f"No network (none of {', '.join(wxc_carryover.CHECK_HOSTS)} reachable); skipping this run.")
        return

    station = get_station(args.station)
    n_pruned = wxc_cache.prune()
    if n_pruned:
        print(f"Pruned {n_pruned} saved model results older than {wxc_cache.PRUNE_DAYS} days")
    now = datetime.now(timezone.utc).replace(microsecond=0)
    now_iso = now.isoformat()
    # The next day open for submission: forecasts for D (06Z D - 06Z D+1) are due 00Z D
    day = date.fromisoformat(args.target_date) if args.target_date else now.date() + timedelta(days=1)
    points = pd.DataFrame({"longitude": [station.lon], "latitude": [station.lat]})
    print(f"Starting forecast for {station.label}, day {day} (06Z-06Z), at {now:%Y-%m-%dT%H:%MZ}")

    # ---- 1. observations (only days not already final in observations.jsonl) ----
    wxc_verify.migrate_legacy_history()
    last_done = wxc_obs.last_complete_day(now)
    window = [last_done - timedelta(days=i) for i in range(max(args.obs_days, args.hindcast_days))][::-1]
    need = wxc_verify.obs_days_to_fetch(station.icao, window, bool(station.cli_pil), now)
    if not need:
        print(f"Observations {window[0]}..{window[-1]} already stored (final); no fetch needed")
    else:
        try:
            obs = wxc_obs.get_observations(station, now=now, first=min(need), last=max(need))
            obs = [o for o in obs if date.fromisoformat(o["date"]) in need]
            wxc_verify.upsert_observations(obs)
            for o in obs:
                src = o.get("source", {})
                print(f"  obs {o['date']}: {o['tmax_f']}/{o['tmin_f']}F ({src.get('tmax_f')}/{src.get('tmin_f')})  "
                      f"wind {o['wind_max_kt']}kt ({src.get('wind_max_kt')})  precip {o['precip_in']}\""
                      f"{' T' if o.get('precip_trace') else ''} ({src.get('precip_in')})"
                      f"{'' if o['complete'] else '  [incomplete]'}"
                      f"{'  pending: ' + ', '.join(o['pending']) if o.get('pending') else ''}")
                for n in o.get("notes", []):
                    print(f"    note: {n}")
        except Exception as exc:
            print("Warning: observation update failed:", exc)

    # ---- 2. hindcasts: model runs for recent days that were never forecast ----
    if args.hindcast_days > 0:
        runs = wxc_verify.read_jsonl(wxc_verify.RUNS)
        # (ensembles are left out: Open-Meteo only serves the latest run)
        all_models = [k for k in GRIB_ORDER if (k != "HRRR" or station.hrrr_model)
                      and (k != "RRFS" or station.rrfs_domain)] + MOS_ORDER
        for d in window[-args.hindcast_days:]:
            todo = wxc_verify.hindcast_plan(runs, station.icao, d.isoformat(), all_models)
            if not todo:
                continue
            as_of = datetime(d.year, d.month, d.day, tzinfo=timezone.utc) - timedelta(hours=24 - HINDCAST_HOUR)
            print(f"\nHindcast for {d}: {', '.join(todo)} as available at {as_of:%Y-%m-%d %HZ}")
            hres, hmos, hmodels = run_models(station, d, points, as_of, args.skip_grib, only=todo)
            try:          # hourly series for the page's timeline (display only)
                save_hindcast_series(station, d, as_of, hres, hmos)
            except Exception as exc:
                print(f"  warning: hindcast series for {d} not saved ({type(exc).__name__}: {exc})")
            # a source that couldn't be reached (offline) doesn't use up a hindcast attempt
            offline = [k for k, v in hmodels.items() if wxc_carryover.is_network_error(v.get("error"))]
            if offline:
                print(f"  not reached (left for the next run): {', '.join(offline)}")
                hmodels = {k: v for k, v in hmodels.items() if k not in offline}
                if not hmodels:
                    continue
            # consensus from everything now known for that day (earlier hindcast + this one)
            known = {k: fc for k, (fc, _, _) in wxc_verify.forecasts_for_day(runs, station.icao, d.isoformat()).items()
                     if k != "CONSENSUS"}
            known.update({k: v for k, v in hmodels.items() if v.get("tmax_f") is not None})
            if known:
                hmodels["CONSENSUS"] = wxc_verify.consensus(known, {})
            wxc_verify.append_run(as_of.isoformat(), station.icao, d, hmodels, hindcast=True)

    verif = wxc_verify.write_verification(station.icao, now.date())
    wxc_verify.print_summary(verif)

    # ---- 3. models for the day being forecast ----
    results, mos, models = run_models(station, day, points, None, args.skip_grib)
    # a model that failed this run (laptop asleep, bad wifi) keeps its last good forecast for the day
    json_path = DATA / "forecast.json"
    errors = {k: m.get("error") or "no data" for k, m in models.items() if not wxc_carryover.has_values(m)}
    carried = wxc_carryover.carry_over(results, mos, models, wxc_carryover.load_previous(json_path, station.icao, day),
                                       wxc_verify.load_series(station.icao, day, "submitted"), GRIB_ORDER)
    status = wxc_carryover.run_status(errors, list(carried), now_iso)
    if carried:
        print(f"Not refreshed this run, previous forecasts kept: {', '.join(carried)}")
    if status.get("message"):
        print(f"Warning: {status['message']}")

    # ---- 4. consensus ----
    usable = {k: v for k, v in models.items() if v.get("tmax_f") is not None}
    cons = wxc_verify.consensus(usable, verif["summary"], now=now)
    models["CONSENSUS"] = cons
    for v, d in cons.get("method", {}).items():
        if d.get("excluded_outliers"):
            print(f"Consensus {v}: excluded outlier(s) {', '.join(d['excluded_outliers'])}")
        if d.get("excluded_stale"):
            print(f"Consensus {v}: excluded stale run(s) {', '.join(d['excluded_stale'])}")

    # ---- console table ----
    print(f"\nForecast for {station.label}, {day} 06Z - {day + timedelta(days=1)} 06Z")
    print(f"{'model':10s} {'run':>4s}  {'high':>6s} {'low':>6s} {'wind':>5s} {'precip':>6s}")
    for name, m in models.items():
        print(f"{name:10s} {run_hour(m.get('init_time_utc')) if m.get('init_time_utc') else '':>4s}  "
              f"{fmt(m.get('tmax_f'), 't'):>6s} {fmt(m.get('tmin_f'), 't'):>6s} "
              f"{fmt(m.get('wind_max_kt'), 'w'):>5s} {fmt(m.get('precip_in'), 'p'):>6s}"
              f"{'  ' + m['error'][:60] if m.get('error') else ''}")

    print_pop(models)

    # ---- 5. outputs ----
    start = datetime(day.year, day.month, day.day, 6)
    payload = {
        "generated_at_utc": now_iso,
        "meta": {
            "page": "wxchallenge",
            "site": station.label,
            "station": station.icao,
            "wfo": station.wfo,
            "afd_url": station.afd_url,
            "tz": station.tz,
            "target_date": day.isoformat(),
            "valid_range_utc": [start.strftime("%Y-%m-%dT%H"),
                                (start + timedelta(days=1)).strftime("%Y-%m-%dT%H")],
            "models": list(models),
            "note": "temperatures in °F, winds in kt, precip in inches",
        },
        "models": models,
        "run_status": status,
    }
    # nothing at all came through (e.g. offline just after the target day moved on): leave the
    # last forecasts up and only flag the failed update
    usable_any = any(wxc_carryover.has_values(m) for k, m in models.items() if k != "CONSENSUS")
    if not usable_any and json_path.exists():
        payload = json.loads(json_path.read_text())
        payload["run_status"] = status
        print(f"\nNo forecasts fetched; kept the previous {json_path.name} (flagged as not updated)")
    else:
        print(f"\nWrote {json_path}")
    json_path.write_text(wxc_verify.dumps(payload, indent=2))

    # runs.jsonl records what this run actually got (verification falls back to earlier runs itself)
    wxc_verify.append_run(now_iso, station.icao, day,
                          {k: carried.get(k, v) for k, v in models.items()
                           if k != "CONSENSUS" or v.get("tmax_f") is not None})
    print(f"Appended run to {wxc_verify.RUNS}")
    # hourly series of this (pre-deadline) run, for tomorrow's "today so far" figure
    # (carried-over models have their series back; with nothing fetched the saved one stays)
    ser = collect_series(results, mos)
    if ser:
        wxc_verify.save_series(station.icao, day, "submitted", now_iso, ser)

    clouds = None
    if wxc_clouds.CLOUDS_ENABLED:          # display only: after every scored output is written
        try:
            runs = {k: results[k]["metrics"].get("init_time_utc") for k in GRIB_ORDER if k in results}
            runs.update({k: mos[k].get("init_time_utc") for k in [*wxc_clouds.TEXT_MODELS, *ENS_ORDER]
                         if k in mos and not mos[k].get("error")})
            clouds = collect_clouds(station, day, runs, points, fetch_grib=not args.skip_grib)
            if clouds:       # the target day's cloud forecast, for the AI brief (display only)
                CLOUD_FORECAST.write_text(wxc_verify.dumps(
                    {"station": station.icao, "target_date": day.isoformat(),
                     "generated_at_utc": now_iso, "models": clouds}))
                wxc_timeline.save_day(DATA, station.icao, day, "clouds",      # and for the page's timeline
                                      wxc_timeline.clouds_record(station.icao, day, clouds, None, now))
        except Exception as exc:
            print(f"Warning: cloud cover skipped ({type(exc).__name__}: {exc})")
    try:
        if usable_any:       # otherwise the previous figure stays, like forecast.json
            plot_forecast(results, mos, cons, station, day, IMAGES / "latest.png", clouds)
            print(f"Wrote {IMAGES / 'latest.png'}")
    except Exception as exc:
        print("Forecast image skipped:", exc)
    try:
        if wxc_verify.plot_verification(verif, IMAGES / "verification.png"):
            print(f"Wrote {IMAGES / 'verification.png'}")
    except Exception as exc:
        print("Verification image skipped:", exc)
    if not args.no_today:
        try:
            today_figure(station, now, points, args.skip_grib)
        except Exception as exc:
            print("Today-so-far figure skipped:", type(exc).__name__, exc)

    # cloud context for the scoreboard (display only; after the today figure saved its GOES hours)
    if wxc_clouds.CLOUDS_ENABLED:
        try:
            print("\nCloud context for the verified days (not scored):")
            cloud_context(station, verif, points, fetch_grib=not args.skip_grib)
        except Exception as exc:
            print(f"Warning: cloud context skipped ({type(exc).__name__}: {exc})")

    # the page's scrollable timeline (display only; after today.json and the today figure's files)
    try:
        print("\nTimeline for the page (not scored):")
        timeline_update(station, now, points, verif, fetch_grib=not args.skip_grib)
    except Exception as exc:
        print(f"Warning: timeline skipped ({type(exc).__name__}: {exc})")

    # 12Z/18Z runs scored separately on the page's toggle (display only; after everything scored)
    try:
        print("\nPer-cycle runs for the scoreboard's 12Z/18Z toggle (not scored):")
        n = cycle_backfill(station, verif, points, now, fetch_grib=not args.skip_grib)
        wxc_verify.refresh_cycles(station.icao)
        print(f"  {n} run(s) added")
    except Exception as exc:
        print(f"Warning: per-cycle backfill skipped ({type(exc).__name__}: {exc})")

    # forecast-evolution links on the page (station config only; the page builds the run times)
    try:
        page = ROOT / "wxchallenge" / "index.html"
        print(f"{'Updated' if wxc_links.update_page(page, station) else 'Unchanged'}: forecast-evolution links in {page}")
    except Exception as exc:
        print(f"Warning: forecast-evolution links skipped ({type(exc).__name__}: {exc})")

    # plain-text brief for AI assistants (after today.json, which it summarises)
    try:
        print(f"Wrote {wxc_brief.write_brief(DATA)}")
    except Exception as exc:
        print(f"Warning: AI brief skipped ({type(exc).__name__}: {exc})")

    # ---- 6. publish ----
    if not args.no_push:
        git_push(now_iso)


if __name__ == "__main__":
    main()
