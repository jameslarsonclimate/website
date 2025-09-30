"""
Fetch HRRR and IFS forecasts for a point, save a JSON summary and a small PNG,
and attempt to commit & push the changes to the repository (for GitHub Pages).

This script:
 - uses helper functions from functions.py (get_latest_forecast_cycle,
   calculate_forecast_range, convert_time_to_datetime64)
 - downloads model fields with FastHerbie
 - summarizes tmax/tmin, peak wind, and precipitation for a single point
 - writes a JSON payload under data/wxchallenge/forecast.json
 - writes a small image under images/wxchallenge/latest.png
 - runs 'git add/commit/push' as a best-effort step
"""

# Standard & third-party imports
from functions import *  # get_latest_forecast_cycle, calculate_forecast_range, convert_time_to_datetime64
from herbie import FastHerbie
import pandas as pd
import xarray as xr
import numpy as np
import warnings
import json
import subprocess
from pathlib import Path
from datetime import datetime, timezone
from PIL import Image, ImageDraw
import warnings

# Suppress the specific FutureWarning message from cfgrib
warnings.filterwarnings(
    "ignore",
    # message="In a future version of xarray the default value for compat will change",
    message="In*",
    category=FutureWarning
)

# Silence a specific non-actionable warning emitted by xarray plugins
warnings.filterwarnings("ignore", message="Engine 'gini' loading failed.*", category=RuntimeWarning)

# -------------------------------------------------------------------
# Paths and constants
# -------------------------------------------------------------------
ROOT = Path(__file__).resolve().parent
(IMAGES := ROOT / "images" / "ats640").mkdir(parents=True, exist_ok=True)
(DATA := ROOT / "data" / "ats640").mkdir(parents=True, exist_ok=True)

# Single point to summarize (longitude, latitude)
# cityName = "Loveland, CO (KFNL)"
# points = pd.DataFrame({"longitude": [-105.004186], "latitude": [40.451685]})
cityName = 'Boston, MA (KBOS)'
points = pd.DataFrame({"longitude": [-71.010], "latitude": [42.365]})
cityName = 'Seattle, WA (KSEA)'
points = pd.DataFrame({"longitude": [-122.311468], "latitude": [47.451]})

now = datetime.now(timezone.utc)
print(f"Starting forecast for {cityName} at {now.strftime('%Y-%m-%dT%H:%MZ')}")

# ISO timestamp (UTC) for metadata and git commit message
now_iso = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

# -------------------------
# HRRR (inline)
# -------------------------
try:
    print("Fetching HRRR data...")

    # Determine the latest model cycle (uses functions.get_latest_forecast_cycle)
    init_hrrr = get_latest_forecast_cycle(model="HRRR")

    # Determine forecast steps to request (uses functions.calculate_forecast_range)
    fxx_hrrr = calculate_forecast_range(init_hrrr, model="HRRR")

    # Request fields from Herbie
    H_hrrr = FastHerbie([init_hrrr], model="hrrr", product="sfc", fxx=fxx_hrrr)

    # 2 m temperature: extract, convert K->F, compute max/min for the point
    t2m_hrrr = H_hrrr.xarray("TMP:2 m above", backend_kwargs={'decode_times': False}
                            ).herbie.pick_points(points, method="nearest")['t2m'].sel(point=0)
    t2m_hrrr = (t2m_hrrr - 273.15) * 1.8 + 32
    tmax_hrrr = float(t2m_hrrr.max().values)
    tmin_hrrr = float(t2m_hrrr.min().values)
    init_times_hrrr = convert_time_to_datetime64(t2m_hrrr.time.values)
    valid_times_hrrr = convert_time_to_datetime64(t2m_hrrr.valid_time.values)

    # 10 m wind speed (HRRR exposes :WIND / si10)
    si10_hrrr = H_hrrr.xarray(":WIND", backend_kwargs={'decode_times': False}
                              ).herbie.pick_points(points, method="nearest")['max_10si'].sel(point=0)
    wind_max_hrrr = float(si10_hrrr.max().values) * 1.94384

    # Total precipitation from APCP (convert mm -> in); compute 24h accumulation as in prior script
    tp_hrrr = H_hrrr.xarray("APCP", backend_kwargs={'decode_times': False}
                            ).herbie.pick_points(points, method="nearest")['tp'].sel(point=0)
    tp_hrrr = tp_hrrr * 0.0393701   # mm -> inches (1 mm -> 0.0393701 in)

    # Subtract first timestep to get accumulation over the requested period (as in original)
    tp_hrrr = tp_hrrr - tp_hrrr[0]
    precip_hrrr = float(tp_hrrr.max().values)

    # Pack HRRR metrics
    hrrr_metrics = {
        "tmax_f": round(tmax_hrrr, 1),
        "tmin_f": round(tmin_hrrr, 1),
        "wind_max_kt": round(wind_max_hrrr, 1),
        "precip_in": round(precip_hrrr, 2),
        "init_time_utc": pd.Timestamp(init_times_hrrr[0]).isoformat() if hasattr(init_times_hrrr, "__len__") else str(init_times_hrrr),
        "valid_range_utc": [str(valid_times_hrrr[0]), str(valid_times_hrrr[-1])]
    }
except Exception as exc:
    print("Warning: failed to fetch HRRR metrics:", exc)
    hrrr_metrics = {
        "tmax_f": None,
        "tmin_f": None,
        "wind_max_kt": None,
        "precip_in": None,
        "init_time_utc": None,
        "valid_range_utc": None,
        "error": str(exc)
    }

# -------------------------
# IFS (inline)
# -------------------------
try:
    print("Fetching IFS data...")

    init_ifs = get_latest_forecast_cycle(model="IFS")
    fxx_ifs = calculate_forecast_range(init_ifs, model="IFS")
    H_ifs = FastHerbie([init_ifs], model="ifs", product="oper", fxx=fxx_ifs)

    # 2 m temperature: extract and convert
    t2m_ifs = H_ifs.xarray(":2t:", backend_kwargs={'decode_times': False}
                          ).herbie.pick_points(points, method="nearest")['t2m'].sel(point=0)  
    t2m_ifs = (t2m_ifs - 273.15) * 1.8 + 32
    tmax_ifs = float(t2m_ifs.max().values)
    tmin_ifs = float(t2m_ifs.min().values)
    init_times_ifs = convert_time_to_datetime64(t2m_ifs.time.values)
    valid_times_ifs = convert_time_to_datetime64(t2m_ifs.valid_time.values)

    # Wind from components -> magnitude
    u10_ifs = H_ifs.xarray(":10u:", backend_kwargs={'decode_times': False}
                          ).herbie.pick_points(points, method="nearest")['u10'].sel(point=0)  
    v10_ifs = H_ifs.xarray(":10v:", backend_kwargs={'decode_times': False}
                          ).herbie.pick_points(points, method="nearest")['v10'].sel(point=0)
    wind_max_ifs = float((np.sqrt(u10_ifs**2 + v10_ifs**2)).max().values) * 1.94384 # Convert m/s to knots

    # Total precipitation (sum over requested steps) and convert to inches
    tp_ifs = H_ifs.xarray(":tp:", backend_kwargs={'decode_times': False}
                         ).herbie.pick_points(points, method="nearest")['tp'].sel(point=0)
    tp_ifs = tp_ifs - tp_ifs[0] # Subtract first timestep to get accumulation over the requested period

    precip_ifs = float(tp_ifs.max().values) * 39.3701 # Convert meters to inches (1 m -> 39.3701 in)

    # Pack IFS metrics
    ifs_metrics = {
        "tmax_f": round(tmax_ifs, 1),
        "tmin_f": round(tmin_ifs, 1),
        "wind_max_kt": round(wind_max_ifs, 1),
        "precip_in": round(precip_ifs, 2),
        "init_time_utc": pd.Timestamp(init_times_ifs[0]).isoformat() if hasattr(init_times_ifs, "__len__") else str(init_times_ifs),
        "valid_range_utc": [str(valid_times_ifs[0]), str(valid_times_ifs[-1])]
    }
except Exception as exc:
    print("Warning: failed to fetch IFS metrics:", exc)
    ifs_metrics = {
        "tmax_f": None,
        "tmin_f": None,
        "wind_max_kt": None,
        "precip_in": None,
        "init_time_utc": None,
        "valid_range_utc": None,
        "error": str(exc)
    }

# -------------------------
# EPS
# -------------------------
try:
    print("Fetching EPS data...")

    init_eps = get_latest_forecast_cycle(model="IFS")
    fxx_eps = calculate_forecast_range(init_eps, model="IFS")
    # H_eps = FastHerbie([init_eps], model="eps", product="enfo", fxx=fxx_eps)
    H_eps_init = FastHerbie([init_eps], model="ifs", product="enfo", fxx=[fxx_eps[0]])
    H_eps_end = FastHerbie([init_eps], model="ifs", product="enfo", fxx=[fxx_eps[-1]])


    # # 2 m temperature: extract and convert
    # t2m_aifs = H_aifs.xarray(":2t:", backend_kwargs={'decode_times': False}
    #                         ).herbie.pick_points(points, method="nearest")['t2m'].sel(point=0)
    # t2m_aifs = (t2m_aifs - 273.15) * 1.8 + 32
    # tmax_aifs = float(t2m_aifs.max().values)
    # tmin_aifs = float(t2m_aifs.min().values)
    init_times_aifs = convert_time_to_datetime64(t2m_aifs.time.values)
    valid_times_aifs = convert_time_to_datetime64(t2m_aifs.valid_time.values)

    # # Wind from components -> magnitude
    # u10_aifs = H_aifs.xarray(":10u:", backend_kwargs={'decode_times': False}
    #                         ).herbie.pick_points(points, method="nearest")['u10'].sel(point=0)
    # v10_aifs = H_aifs.xarray(":10v:", backend_kwargs={'decode_times': False}
    #                         ).herbie.pick_points(points, method="nearest")['v10'].sel(point=0)
    # wind_max_aifs = float((np.sqrt(u10_aifs**2 + v10_aifs**2)).max().values) * 1.94384 # Convert m/s to knots

    # Total precipitation (sum over requested steps) and convert to inches
    # tp_eps = H_aifs.xarray(":tp:sfc:[1-9][0-9]?:g:", backend_kwargs={'decode_times': False}
    #                         ).herbie.pick_points(points, method="nearest")['tp'].sel(point=0)
    # tp_eps = tp_eps - tp_eps[0] # Subtract first timestep to get accumulation over the requested period
    # precip_eps = float(tp_eps.max().values) * 0.0393701 # Convert millimeters to inches (1 m -> 39.3701 in)
    tp_init = H_eps_init.xarray(":tp:sfc:[1-9][0-9]?:g:", backend_kwargs={'decode_times': False}
                  ).herbie.pick_points(points, method="nearest")['tp'].sel(point=0)
    tp_end = H_eps_end.xarray(":tp:sfc:[1-9][0-9]?:g:", backend_kwargs={'decode_times': False}
                  ).herbie.pick_points(points, method="nearest")['tp'].sel(point=0)
    precip_eps = (tp_end - tp_init) * 39.3701

    init_times_eps = convert_time_to_datetime64(tp_init.time.values)
    valid_time_init_eps = convert_time_to_datetime64(tp_init.valid_time.values)
    valid_time_end_eps = convert_time_to_datetime64(tp_end.valid_time.values)


    # Pack EPS metrics
    eps_metrics = {
        "tmax_f": np.nan,  # round(tmax_eps, 1),
        "tmin_f": np.nan,  # round(tmin_eps, 1),
        "wind_max_kt": np.nan,  # round(wind_max_eps, 1),
        "precip_in": round(precip_eps, 2),
        "init_time_utc": pd.Timestamp(init_times_eps[0]).isoformat() if hasattr(init_times_eps, "__len__") else str(init_times_eps),
        "valid_range_utc": [str(valid_time_init_eps), str(valid_time_end_eps)]
    }
except Exception as exc:
    print("Warning: failed to fetch EPS metrics:", exc)
    eps_metrics = {
        "tmax_f": None,
        "tmin_f": None,
        "wind_max_kt": None,
        "precip_in": None,
        "init_time_utc": None,
        "valid_range_utc": None,
        "error": str(exc)
    }

# -------------------------
# AIFS (inline)
# -------------------------
try:
    print("Fetching AIFS data...")

    init_aifs = get_latest_forecast_cycle(model="AIFS")
    fxx_aifs = calculate_forecast_range(init_aifs, model="AIFS")
    H_aifs = FastHerbie([init_aifs], model="aifs", product="oper", fxx=fxx_aifs)

    # 2 m temperature: extract and convert
    t2m_aifs = H_aifs.xarray(":2t:", backend_kwargs={'decode_times': False}
                            ).herbie.pick_points(points, method="nearest")['t2m'].sel(point=0)
    t2m_aifs = (t2m_aifs - 273.15) * 1.8 + 32
    tmax_aifs = float(t2m_aifs.max().values)
    tmin_aifs = float(t2m_aifs.min().values)
    init_times_aifs = convert_time_to_datetime64(t2m_aifs.time.values)
    valid_times_aifs = convert_time_to_datetime64(t2m_aifs.valid_time.values)

    # Wind from components -> magnitude
    u10_aifs = H_aifs.xarray(":10u:", backend_kwargs={'decode_times': False}
                            ).herbie.pick_points(points, method="nearest")['u10'].sel(point=0)
    v10_aifs = H_aifs.xarray(":10v:", backend_kwargs={'decode_times': False}
                            ).herbie.pick_points(points, method="nearest")['v10'].sel(point=0)
    wind_max_aifs = float((np.sqrt(u10_aifs**2 + v10_aifs**2)).max().values) * 1.94384 # Convert m/s to knots

    # Total precipitation (sum over requested steps) and convert to inches
    tp_aifs = H_aifs.xarray(":tp:", backend_kwargs={'decode_times': False}
                            ).herbie.pick_points(points, method="nearest")['tp'].sel(point=0)
    tp_aifs = tp_aifs - tp_aifs[0] # Subtract first timestep to get accumulation over the requested period
    precip_aifs = float(tp_aifs.max().values) * 0.0393701 # Convert millimeters to inches (1 m -> 39.3701 in)

    # Pack AIFS metrics
    aifs_metrics = {
        "tmax_f": round(tmax_aifs, 1),
        "tmin_f": round(tmin_aifs, 1),
        "wind_max_kt": round(wind_max_aifs, 1),
        "precip_in": round(precip_aifs, 2),
        "init_time_utc": pd.Timestamp(init_times_aifs[0]).isoformat() if hasattr(init_times_aifs, "__len__") else str(init_times_aifs),
        "valid_range_utc": [str(valid_times_aifs[0]), str(valid_times_aifs[-1])]
    }
except Exception as exc:
    print("Warning: failed to fetch AIFS metrics:", exc)
    aifs_metrics = {
        "tmax_f": None,
        "tmin_f": None,
        "wind_max_kt": None,
        "precip_in": None,
        "init_time_utc": None,
        "valid_range_utc": None,
        "error": str(exc)
    }

# -------------------------
# GFS (inline)
# -------------------------
try:
    print("Fetching GFS data...")

    # determine latest cycle & forecast range for GFS
    init_gfs = get_latest_forecast_cycle(model="GFS")
    fxx_gfs = calculate_forecast_range(init_gfs, model="GFS")

    # request fields (product string may vary by deployment; adjust if needed)
    H = FastHerbie([init_gfs], model="gfs", product="pgrb2.0p25", fxx=fxx_gfs)

    # 2 m temperature -> convert K to °F
    t2m_gfs = H.xarray("TMP:2 m above", backend_kwargs={'decode_times': False}
                    ).herbie.pick_points(points, method="nearest")['t2m'].sel(point=0)
    t2m_f = (t2m_gfs - 273.15) * 9.0/5.0 + 32.0
    tmax_gfs = float(t2m_f.max().values)
    tmin_gfs = float(t2m_f.min().values)
    init_times_gfs = convert_time_to_datetime64(t2m_gfs.time.values)
    valid_times_gfs = convert_time_to_datetime64(t2m_gfs.valid_time.values)

    # wind components -> magnitude (m/s -> kt)
    u10 = H.xarray("UGRD:10 m above ground", backend_kwargs={'decode_times': False}
                    ).herbie.pick_points(points, method="nearest")['u10']
    v10 = H.xarray("VGRD:10 m above ground", backend_kwargs={'decode_times': False}
                    ).herbie.pick_points(points, method="nearest")['v10']
    wind_max_gfs = float((np.sqrt(u10**2 + v10**2)).max().values) * 1.94384

    # Total precipitation from APCP (convert mm -> in); compute 24h accumulation as in prior script
    tp_gfs = H.xarray(":APCP:surface:0-*", backend_kwargs={'decode_times': False}
                            ).herbie.pick_points(points, method="nearest")['tp'].sel(point=0)
    tp_gfs = (tp_gfs - tp_gfs[0]) * 0.0393701   # mm -> inches (1 mm -> 0.0393701 in)
    
    precip_gfs = float(tp_gfs.max().values)

    # Pack GFS metrics
    gfs_metrics = {
        "tmax_f": round(tmax_gfs, 1),
        "tmin_f": round(tmin_gfs, 1),
        "wind_max_kt": round(wind_max_gfs, 1),
        "precip_in": round(precip_gfs, 2),
        "init_time_utc": pd.Timestamp(init_times_gfs[0]).isoformat() if hasattr(init_times_gfs, "__len__") else str(init_times_gfs),
        "valid_range_utc": [str(valid_times_gfs[0]), str(valid_times_gfs[-1])]
    }
except Exception as exc:
    print("Warning: failed to fetch GFS metrics:", exc)
    gfs_metrics = {
        "tmax_f": None,
        "tmin_f": None,
        "wind_max_kt": None,
        "precip_in": None,
        "init_time_utc": None,
        "valid_range_utc": None,
        "error": str(exc)
    }

# Create the title and the table combining both models (use the current variable names)
title = f"Forecasting for {cityName} \nValid: {str(valid_times_hrrr[0])} - {str(valid_times_hrrr[-1])} UTC"

data = {
    "Model": ["HRRR", "IFS", "GFS", "AIFS", "EPS"],
    "High (°F)": [tmax_hrrr, tmax_ifs, tmax_gfs, tmax_aifs, tmax_eps],
    "Low (°F)": [tmin_hrrr, tmin_ifs, tmin_gfs, tmin_aifs, tmin_eps],
    "Precipitation (in)": [precip_hrrr, precip_ifs, precip_gfs, precip_aifs, precip_eps],
    "Wind Speed (kt)": [wind_max_hrrr, wind_max_ifs, wind_max_gfs, wind_max_aifs, wind_max_eps],
    "Model Init": [f"{str(init_times_hrrr)} UTC", f"{str(init_times_ifs)} UTC", f"{str(init_times_gfs)} UTC", f"{str(init_times_aifs)} UTC", f"{str(init_times_eps)} UTC"]
}

df_forecast = pd.DataFrame(data).round(2)

# Print the title and table without row numbers
print(title)
print(df_forecast.to_string(index=False))


# -------------------------------------------------------------------
# Build JSON payload consumed by the website
# - include 'models' object with HRRR and IFS (current schema)
# - also include legacy top-level metrics + meta.model/meta.init_time_utc
#   so the existing index.html (which expects the old schema) continues to work
# -------------------------------------------------------------------
payload = {
    "generated_at_utc": now_iso,
    "meta": {
        "page": "wxchallenge",
        "site": cityName,
        "models": ["HRRR", "IFS", "GFS", "AIFS", "EPS"],
        "note": "temperatures in °F, winds in kt, precip in inches",
    },
    "models": {"HRRR": hrrr_metrics, "IFS": ifs_metrics, "GFS": gfs_metrics, "AIFS": aifs_metrics, "EPS": eps_metrics},
}

# Write JSON payload
json_path = DATA / "forecast-away.json"
json_path.write_text(json.dumps(payload, indent=2))
print(f"Wrote {json_path}")

# -------------------------
# Small image for site
# -------------------------
img_path = IMAGES / "latest-away.png"
try:
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates

    def to_1d(x):
        try:
            x = x.sel(point=0)
        except Exception:
            pass
        return np.asarray(x).flatten()

    # --- prepare time series for each model ---
    times_hrrr = pd.to_datetime(valid_times_hrrr)
    temps_hrrr = to_1d(t2m_hrrr)
    wind_hrrr = to_1d(si10_hrrr) * 1.94384
    precip_hrrr = to_1d(tp_hrrr)  # already converted to inches and processed earlier

    times_ifs = pd.to_datetime(valid_times_ifs)
    temps_ifs = to_1d(t2m_ifs)
    wind_ifs = to_1d(np.sqrt(u10_ifs**2 + v10_ifs**2)) * 1.94384
    # convert IFS tp (mm -> in) and compute accumulation inside the window (match other models)
    precip_ifs = tp_ifs.values * 39.3701

    times_aifs = pd.to_datetime(valid_times_aifs)
    temps_aifs = to_1d(t2m_aifs)
    wind_aifs = to_1d(np.sqrt(u10_aifs**2 + v10_aifs**2)) * 1.94384
    # convert AIFS tp (mm -> in) and compute accumulation inside the window (match other models)
    precip_aifs = tp_aifs.values * 0.0393701

    times_gfs = pd.to_datetime(valid_times_gfs)
    temps_gfs = to_1d(t2m_f)
    wind_gfs = to_1d(np.sqrt(u10**2 + v10**2)) * 1.94384
    precip_gfs = to_1d(tp_gfs)  # already converted to inches and processed earlier

    times_eps = pd.to_datetime(valid_times_eps)
    # temps_eps = to_1d(t2m_eps)
    # wind_eps = to_1d(np.sqrt(u10_eps**2 + v10_eps**2)) * 1.94384
    # convert EPS tp (mm -> in) and compute accumulation inside the window (match other models)
    precip_eps = tp_eps.values * 39.3701

    # --- create combined 3-panel figure ---
    fig, axes = plt.subplots(3, 1, figsize=(12, 10), sharex=True)

    # Temperature
    ax = axes[0]
    ax.plot(times_hrrr, temps_hrrr, marker='o', linestyle='-', color='C0', label='HRRR')
    ax.plot(times_ifs, temps_ifs, marker='o', linestyle='-', color='C1', label='IFS')
    ax.plot(times_gfs, temps_gfs, marker='o', linestyle='-', color='C2', label='GFS')
    ax.plot(times_aifs, temps_aifs, marker='o', linestyle='-', color='C3', label='AIFS')
    ax.set_ylabel("Temperature (°F)")
    ax.grid(True, linestyle='--', alpha=0.4)
    ax.legend(loc='best')

    # Wind
    ax = axes[1]
    ax.plot(times_hrrr, wind_hrrr, marker='o', linestyle='-', color='C0', label='HRRR')
    ax.plot(times_ifs, wind_ifs, marker='o', linestyle='-', color='C1', label='IFS')
    ax.plot(times_gfs, wind_gfs, marker='o', linestyle='-', color='C2', label='GFS')
    ax.plot(times_aifs, wind_aifs, marker='o', linestyle='-', color='C3', label='AIFS')
    ax.set_ylabel("Wind Speed (kt)")
    ax.grid(True, linestyle='--', alpha=0.4)
    ax.legend(loc='best')

    # Precipitation (line plot)
    ax = axes[2]
    ax.plot(times_hrrr, precip_hrrr, marker='o', linestyle='-', color='C0', label='HRRR', alpha=0.8)
    ax.plot(times_ifs, precip_ifs, marker='o', linestyle='-', color='C1', label='IFS', alpha=0.8)
    ax.plot(times_gfs, precip_gfs, marker='o', linestyle='-', color='C2', label='GFS', alpha=0.8)
    ax.plot(times_aifs, precip_aifs, marker='o', linestyle='-', color='C3', label='AIFS', alpha=0.8)
    ax.plot(times_eps, precip_eps, marker='o', linestyle='-', color='C4', label='EPS', alpha=0.8)
    ax.set_ylabel("Precipitation (in)")
    ax.set_xlabel("Valid time (UTC)")
    ax.grid(True, linestyle='--', alpha=0.4)
    ax.legend(loc='best')

    # format x-axis
    axes[-1].xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d\n%H:%M'))
    plt.setp(axes[-1].xaxis.get_majorticklabels(), rotation=30, ha='right')
    plt.suptitle(f"{cityName} — Temperature, Wind, Precip", y=0.98)
    plt.tight_layout(rect=[0, 0, 1, 0.96])

    # save and close
    fig.savefig(img_path, dpi=150)
    plt.close(fig)
    print(f"Wrote {img_path}")
except Exception as e:
    print("Image creation skipped:", e)

# -------------------------
# Commit & push (best-effort)
# -------------------------
def run(cmd):
    print("+", " ".join(cmd))
    subprocess.check_call(cmd)

try:
    run(["git", "add", str(DATA.relative_to(ROOT)), str(IMAGES.relative_to(ROOT))])
    run(["git", "commit", "-m", f"update wxchallenge: {now_iso}"])
    run(["git", "push", "origin", "main"])
except subprocess.CalledProcessError:
    print("Git step skipped or failed (e.g., no changes or auth issue).")