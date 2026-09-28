"""
WxChallenge forecast helper.

For the current station (see wxc_stations.py, or pass an ICAO id on the command line):
  1. pulls observations for the last few completed days (IEM METARs + NWS CLI wind)
  2. verifies earlier runs against those observations (data/wxchallenge/verification.json)
  3. fetches HRRR, ECMWF IFS, GFS and AIFS grids (Herbie) plus GFS MOS, NAM MOS and
     NBM text guidance (IEM), each summarised for the next WxChallenge day (06Z-06Z)
  4. builds a bias-corrected, skill-weighted CONSENSUS from the verified models
  5. writes data/wxchallenge/forecast.json, appends data/wxchallenge/runs.jsonl,
     draws images/wxchallenge/latest.png and verification.png
  6. commits and pushes the data/images (GitHub Pages), best effort

Usage:
  python getForecast_wxChallenge-pushGitHub.py [ICAO] [--target-date YYYY-MM-DD]
                                               [--obs-days N] [--no-push] [--skip-grib]
"""

import argparse
import json
import subprocess
import warnings
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

import numpy as np
import pandas as pd

from functions import (convert_time_to_datetime64, forecast_hours_for_day, fmt,
                       get_latest_forecast_cycle, previous_forecast_cycle, run_hour)
import wxc_mos
import wxc_obs
import wxc_verify
from wxc_stations import get_station

warnings.filterwarnings("ignore", message="In*", category=FutureWarning)
warnings.filterwarnings("ignore", message="Engine 'gini' loading failed.*", category=RuntimeWarning)

ROOT = Path(__file__).resolve().parent
(IMAGES := ROOT / "images" / "wxchallenge").mkdir(parents=True, exist_ok=True)
(DATA := ROOT / "data" / "wxchallenge").mkdir(parents=True, exist_ok=True)

MS_TO_KT = 1.94384
HINDCAST_HOUR = 21        # hindcasts use the runs available at 21Z the day before (your usual run time)
MAX_FALLBACK = 1          # also try this many older cycles if the newest isn't posted yet
GRIB_ORDER = ["HRRR", "IFS", "GFS", "AIFS"]
MOS_ORDER = list(wxc_mos.MOS_PRODUCTS)   # GFS_MOS, NAM_MOS, NBM


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


def pick(H, search, points, prefer=None):
    """H.xarray(search) at the station point -> 1-D DataArray over forecast steps."""
    ds = H.xarray(search, backend_kwargs={"decode_times": False})
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
    name = prefer if prefer in ds.data_vars else list(ds.data_vars)[0]
    da = ds[name]
    return da.sel(point=0) if "point" in da.dims else da


def precip_factor(da, default):
    """Inches per unit of a precip DataArray, read from its GRIB units when present."""
    units = str(da.attrs.get("units", da.attrs.get("GRIB_units", ""))).lower().strip()
    if units in ("m", "m of water equivalent"):
        return 39.3701
    if "kg" in units or units == "mm":
        return 0.0393701
    return default


def iso_hour(t):
    return pd.Timestamp(t).strftime("%Y-%m-%dT%H")


def summarize(label, init, times, temp_f, wind_kt, precip_in, tmax_extra=None,
              tmin_extra=None, truncated=False, notes=None):
    """Standard result dict: JSON metrics + series for plotting."""
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
                       "wind_kt": np.asarray(wind_kt, float), "precip_in": np.asarray(precip_in, float)}}


# -------------------------------------------------------------------
# GRIB models (Herbie)
# -------------------------------------------------------------------
def fetch_hrrr(init, day, points, station):
    from herbie import FastHerbie
    fxx, trunc = forecast_hours_for_day(init, day, step=1, max_fxx=48)
    H = FastHerbie([init], model=station.hrrr_model, product="sfc", fxx=fxx)
    t2m = k_to_f(pick(H, "TMP:2 m above", points, "t2m"))
    times = convert_time_to_datetime64(t2m.valid_time.values)
    wind = pick(H, ":WIND", points, "max_10si") * MS_TO_KT      # hourly max 10 m wind
    tp = pick(H, "APCP", points, "tp")
    tp = (tp - tp[0]) * precip_factor(tp, 0.0393701)
    notes = ["00Z HRRR stops at f48: window truncated"] if trunc else None
    return summarize("HRRR", init, times, t2m.values, wind.values, tp.values,
                     truncated=trunc, notes=notes)


def fetch_ifs(init, day, points, station=None):
    from herbie import FastHerbie
    max_fxx = 144 if pd.Timestamp(init).hour in (0, 12) else 90
    fxx, trunc = forecast_hours_for_day(init, day, step=3, max_fxx=max_fxx)
    H = FastHerbie([init], model="ifs", product="oper", fxx=fxx)
    t2m = k_to_f(pick(H, ":2t:", points, "t2m"))
    times = convert_time_to_datetime64(t2m.valid_time.values)
    u = pick(H, ":10u:", points, "u10")
    v = pick(H, ":10v:", points, "v10")
    wind = np.sqrt(u ** 2 + v ** 2) * MS_TO_KT
    tp = pick(H, ":tp:", points, "tp")
    tp = (tp - tp[0]) * precip_factor(tp, 39.3701)

    # 3-hourly max/min 2 m T catch the peaks between output times. These fields
    # describe the 3 h *ending* at each step, so the first step is excluded.
    tmax_x = tmin_x = None
    notes = []
    try:
        H2 = FastHerbie([init], model="ifs", product="oper", fxx=fxx[1:])
        tmax_x = float(k_to_f(pick(H2, ":mx2t3:", points, "mx2t3")).max())
        tmin_x = float(k_to_f(pick(H2, ":mn2t3:", points, "mn2t3")).min())
    except Exception as exc:
        notes.append(f"mx2t3/mn2t3 unavailable ({type(exc).__name__})")
    return summarize("IFS", init, times, t2m.values, wind.values, tp.values,
                     tmax_x, tmin_x, trunc, notes)


def fetch_gfs(init, day, points, station=None):
    from herbie import FastHerbie
    fxx, trunc = forecast_hours_for_day(init, day, step=3, max_fxx=384)
    H = FastHerbie([init], model="gfs", product="pgrb2.0p25", fxx=fxx)
    t2m = k_to_f(pick(H, "TMP:2 m above", points, "t2m"))
    times = convert_time_to_datetime64(t2m.valid_time.values)
    u = pick(H, "UGRD:10 m above ground", points, "u10")
    v = pick(H, "VGRD:10 m above ground", points, "v10")
    wind = np.sqrt(u ** 2 + v ** 2) * MS_TO_KT
    tp = pick(H, ":APCP:surface:0-*", points, "tp")
    tp = (tp - tp[0]) * precip_factor(tp, 0.0393701)

    # GFS TMAX/TMIN: max/min 2 m T over the interval ending at each step
    tmax_x = tmin_x = None
    notes = []
    try:
        H2 = FastHerbie([init], model="gfs", product="pgrb2.0p25", fxx=fxx[1:])
        tmax_x = float(k_to_f(pick(H2, ":TMAX:2 m above", points, "tmax")).max())
        tmin_x = float(k_to_f(pick(H2, ":TMIN:2 m above", points, "tmin")).min())
    except Exception as exc:
        notes.append(f"TMAX/TMIN unavailable ({type(exc).__name__})")
    return summarize("GFS", init, times, t2m.values, wind.values, tp.values,
                     tmax_x, tmin_x, trunc, notes)


def fetch_aifs(init, day, points, station=None):
    from herbie import FastHerbie
    fxx, trunc = forecast_hours_for_day(init, day, step=6, max_fxx=360)
    H = FastHerbie([init], model="aifs", product="oper", fxx=fxx)
    t2m = k_to_f(pick(H, ":2t:", points, "t2m"))
    times = convert_time_to_datetime64(t2m.valid_time.values)
    u = pick(H, ":10u:", points, "u10")
    v = pick(H, ":10v:", points, "v10")
    wind = np.sqrt(u ** 2 + v ** 2) * MS_TO_KT
    tp = pick(H, ":tp:", points, "tp")
    factor = precip_factor(tp, 0.0393701)
    tp = (tp - tp[0]) * factor
    notes = ["6-hourly output: only 5 temperature samples, high/low likely underdone"]
    if factor != 0.0393701:
        notes.append("AIFS tp reported in metres")
    return summarize("AIFS", init, times, t2m.values, wind.values, tp.values,
                     truncated=trunc, notes=notes)


GRIB_MODELS = {
    # label: (cycle key in functions.get_latest_forecast_cycle, fetch function)
    "HRRR": ("HRRR", fetch_hrrr),
    "IFS": ("IFS", fetch_ifs),
    "GFS": ("GFS", fetch_gfs),
    "AIFS": ("AIFS", fetch_aifs),
}


def fetch_with_fallback(label, cycle_key, fn, day, points, station, as_of=None):
    init = get_latest_forecast_cycle(model=cycle_key, now=as_of)
    last = None
    for attempt in range(MAX_FALLBACK + 1):
        try:
            print(f"Fetching {label} {init:%Y-%m-%d %HZ}...")
            res = fn(init, day, points, station)
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
# plotting
# -------------------------------------------------------------------
def plot_forecast(results, mos, cons, station, day, path):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.dates as mdates
    import matplotlib.pyplot as plt

    colors = {"HRRR": "C0", "IFS": "C1", "GFS": "C2", "AIFS": "C3",
              "GFS_MOS": "C2", "NAM_MOS": "C4", "NBM": "C5"}
    fig, axes = plt.subplots(3, 1, figsize=(12, 10), sharex=True)
    for name in GRIB_ORDER:
        s = results.get(name, {}).get("series")
        if not s:
            continue
        axes[0].plot(s["times"], s["temp_f"], "o-", color=colors[name], label=name)
        axes[1].plot(s["times"], s["wind_kt"], "o-", color=colors[name], label=name)
        axes[2].plot(s["times"], s["precip_in"], "o-", color=colors[name], label=name, alpha=0.8)
    for name in MOS_ORDER:
        s = mos.get(name, {}).get("series")
        if not s or not s["times"]:
            continue
        t = pd.to_datetime(s["times"])
        axes[0].plot(t, s["tmp_f"], "s--", color=colors[name], label=name, alpha=0.8)
        axes[1].plot(t, s["wsp_kt"], "s--", color=colors[name], label=name, alpha=0.8)
    if cons.get("tmax_f") is not None:
        axes[0].axhline(cons["tmax_f"], color="k", ls=":", lw=1.5, label="Consensus high/low")
        axes[0].axhline(cons["tmin_f"], color="k", ls=":", lw=1.5)
    if cons.get("wind_max_kt") is not None:
        axes[1].axhline(cons["wind_max_kt"], color="k", ls=":", lw=1.5, label="Consensus max")
    for ax, lab in zip(axes, ["Temperature (°F)", "Wind speed (kt)", "Accumulated precip (in)"]):
        ax.set_ylabel(lab)
        ax.grid(True, linestyle="--", alpha=0.4)
        ax.legend(loc="best", fontsize=8, ncol=2)
    axes[-1].set_xlabel("Valid time (UTC)")
    axes[-1].xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d\n%H:%M"))
    plt.setp(axes[-1].xaxis.get_majorticklabels(), rotation=30, ha="right")
    fig.suptitle(f"{station.label}: forecast for {day:%a %b %d} (06Z-06Z)", y=0.98)
    fig.tight_layout(rect=[0, 0, 1, 0.96])
    fig.savefig(path, dpi=150)
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


def run_models(station, day, points, as_of=None, skip_grib=False, only=None):
    """All models for WxChallenge day `day`; as_of=None means the latest runs,
    otherwise the runs that were available at `as_of` (hindcast)."""
    results = {}
    for label, (cycle_key, fn) in GRIB_MODELS.items():
        if skip_grib or (only is not None and label not in only):
            continue
        if label == "HRRR" and not station.hrrr_model:
            print("Skipping HRRR (station outside HRRR domains)")
            continue
        results[label] = fetch_with_fallback(label, cycle_key, fn, day, points, station, as_of)
    mos = {}
    if only is None or any(k in only for k in MOS_ORDER):
        print("Fetching MOS / NBM text guidance...")
        mos = wxc_mos.get_mos_forecasts(station.icao, day, as_of, only)
    models = {k: results[k]["metrics"] for k in GRIB_ORDER if k in results}
    models.update({k: {kk: vv for kk, vv in v.items() if kk != "series"} for k, v in mos.items()})
    return results, mos, models


def main():
    ap = argparse.ArgumentParser(description="WxChallenge forecast + verification")
    ap.add_argument("station", nargs="?", help="ICAO id (default: wxc_stations.CURRENT_STATION)")
    ap.add_argument("--target-date", help="forecast day YYYY-MM-DD (default: next day open for submission)")
    ap.add_argument("--obs-days", type=int, default=4, help="completed days of observations to (re)fetch")
    ap.add_argument("--no-push", action="store_true", help="skip git commit/push")
    ap.add_argument("--skip-grib", action="store_true", help="MOS/NBM + verification only (fast)")
    ap.add_argument("--hindcast-days", type=int, default=4,
                    help="re-create model forecasts for up to N recent days that have no stored run "
                         "(so biases are available from day one of a new city); 0 disables")
    args = ap.parse_args()

    station = get_station(args.station)
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
                print(f"  obs {o['date']}: {o['tmax_f']}/{o['tmin_f']}F  wind {o['wind_max_kt']}kt "
                      f"({o['wind_source']})  precip {o['precip_in']}\"{' T' if o.get('precip_trace') else ''}"
                      f"{'' if o['complete'] else '  [incomplete]'}")
        except Exception as exc:
            print("Warning: observation update failed:", exc)

    # ---- 2. hindcasts: model runs for recent days that were never forecast ----
    if args.hindcast_days > 0:
        runs = wxc_verify.read_jsonl(wxc_verify.RUNS)
        all_models = [k for k in GRIB_ORDER if k != "HRRR" or station.hrrr_model] + MOS_ORDER
        for d in window[-args.hindcast_days:]:
            todo = wxc_verify.hindcast_plan(runs, station.icao, d.isoformat(), all_models)
            if not todo:
                continue
            as_of = datetime(d.year, d.month, d.day, tzinfo=timezone.utc) - timedelta(hours=24 - HINDCAST_HOUR)
            print(f"\nHindcast for {d}: {', '.join(todo)} as available at {as_of:%Y-%m-%d %HZ}")
            _, _, hmodels = run_models(station, d, points, as_of, args.skip_grib, only=todo)
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

    # ---- 4. consensus ----
    usable = {k: v for k, v in models.items() if v.get("tmax_f") is not None}
    cons = wxc_verify.consensus(usable, verif["summary"])
    models["CONSENSUS"] = cons
    for v, d in cons.get("method", {}).items():
        if d.get("excluded_outliers"):
            print(f"Consensus {v}: excluded outlier(s) {', '.join(d['excluded_outliers'])}")

    # ---- console table ----
    print(f"\nForecast for {station.label}, {day} 06Z - {day + timedelta(days=1)} 06Z")
    print(f"{'model':10s} {'run':>4s}  {'high':>6s} {'low':>6s} {'wind':>5s} {'precip':>6s}")
    for name, m in models.items():
        print(f"{name:10s} {run_hour(m.get('init_time_utc')) if m.get('init_time_utc') else '':>4s}  "
              f"{fmt(m.get('tmax_f'), 't'):>6s} {fmt(m.get('tmin_f'), 't'):>6s} "
              f"{fmt(m.get('wind_max_kt'), 'w'):>5s} {fmt(m.get('precip_in'), 'p'):>6s}"
              f"{'  ' + m['error'][:60] if m.get('error') else ''}")

    # ---- 5. outputs ----
    start = datetime(day.year, day.month, day.day, 6)
    payload = {
        "generated_at_utc": now_iso,
        "meta": {
            "page": "wxchallenge",
            "site": station.label,
            "station": station.icao,
            "target_date": day.isoformat(),
            "valid_range_utc": [start.strftime("%Y-%m-%dT%H"),
                                (start + timedelta(days=1)).strftime("%Y-%m-%dT%H")],
            "models": list(models),
            "note": "temperatures in °F, winds in kt, precip in inches",
        },
        "models": models,
    }
    json_path = DATA / "forecast.json"
    json_path.write_text(wxc_verify.dumps(payload, indent=2))
    print(f"\nWrote {json_path}")

    wxc_verify.append_run(now_iso, station.icao, day,
                          {k: v for k, v in models.items() if k != "CONSENSUS" or v.get("tmax_f") is not None})
    print(f"Appended run to {wxc_verify.RUNS}")

    try:
        plot_forecast(results, mos, cons, station, day, IMAGES / "latest.png")
        print(f"Wrote {IMAGES / 'latest.png'}")
    except Exception as exc:
        print("Forecast image skipped:", exc)
    try:
        if wxc_verify.plot_verification(verif, IMAGES / "verification.png"):
            print(f"Wrote {IMAGES / 'verification.png'}")
    except Exception as exc:
        print("Verification image skipped:", exc)

    # ---- 6. publish ----
    if not args.no_push:
        git_push(now_iso)


if __name__ == "__main__":
    main()
