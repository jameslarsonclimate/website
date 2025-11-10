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
(IMAGES := ROOT / "images" / "wxchallenge").mkdir(parents=True, exist_ok=True)
(DATA := ROOT / "data" / "wxchallenge").mkdir(parents=True, exist_ok=True)

# Single point to summarize (longitude, latitude)
cityName = "Loveland, CO (KFNL)"
points = pd.DataFrame({"longitude": [-105.004186], "latitude": [40.451685]})
cityName = 'Juneau, AK (PAJN)'
points = pd.DataFrame({"longitude": [-134.576622], "latitude": [58.356023]})

# ISO timestamp (UTC) for metadata and git commit message
now_iso = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

now = datetime.now(timezone.utc)
print(f"Starting forecast for {cityName} at {now.strftime('%Y-%m-%dT%H:%MZ')}")


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
    H_hrrr = FastHerbie([init_hrrr], model="hrrrak", product="sfc", fxx=fxx_hrrr)

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
    init_times_hrrr = None
    valid_times_hrrr = None
    tmax_hrrr = None
    tmin_hrrr = None
    wind_max_hrrr = None
    precip_hrrr = None
    si10_hrrr = None
    tp_hrrr = None
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
    init_times_ifs = None
    valid_times_ifs = None
    tmax_ifs = None
    tmin_ifs = None
    wind_max_ifs = None
    precip_ifs = None
    u10_ifs = None
    v10_ifs = None
    tp_ifs = None
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
    init_times_aifs = None
    valid_times_aifs = None
    tmax_aifs = None
    tmin_aifs = None
    wind_max_aifs = None
    precip_aifs = None
    u10_aifs = None
    v10_aifs = None
    tp_aifs = None
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
    init_times_gfs = None
    valid_times_gfs = None
    tmax_gfs = None
    tmin_gfs = None
    wind_max_gfs = None
    precip_gfs = None
    u10_gfs = None
    v10_gfs = None
    tp_gfs = None
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
try:
    title = f"Forecasting for {cityName} \nValid: {str(valid_times_hrrr[0])} - {str(valid_times_hrrr[-1])} UTC"
except Exception:
    title = f"Forecasting for {cityName} \nValid: {str(valid_times_gfs[0])} - {str(valid_times_gfs[-1])} UTC"
models = [
    ("HRRR", init_times_hrrr, tmax_hrrr, tmin_hrrr, wind_max_hrrr, precip_hrrr),
    ("ECMWF",  init_times_ifs,  tmax_ifs,  tmin_ifs,  wind_max_ifs,  precip_ifs),
    ("GFS",  init_times_gfs,  tmax_gfs,  tmin_gfs,  wind_max_gfs,  precip_gfs),
    ("AIFS", init_times_aifs, tmax_aifs, tmin_aifs, wind_max_aifs, precip_aifs),
]

for name, init, tmax, tmin, wind, prec in models:
    run = run_hour(init)
    print(f"{name} - {run}")
    print(f'{fmt(tmax,'t')}°F   {fmt(tmin,'t')}°F   {fmt(wind,'w')} kt   {fmt(prec,'p')}"')
    print()


# Print the title and table without row numbers
print(title)
# print(df_forecast.to_string(index=False))


# -------------------------------------------------------------------
# Build JSON payload consumed by the website
# -------------------------------------------------------------------
payload = {
    "generated_at_utc": now_iso,
    "meta": {
        "page": "wxchallenge",
        "site": cityName,
        "models": ["HRRR", "IFS", "GFS", "AIFS"],
        "note": "temperatures in °F, winds in kt, precip in inches",
    },
    "models": {"HRRR": hrrr_metrics, "IFS": ifs_metrics, "GFS": gfs_metrics, "AIFS": aifs_metrics},
}

# Write "current" JSON payload (keeps existing behavior for the website)
json_path = DATA / "forecast.json"
json_path.write_text(json.dumps(payload, indent=2))
print(f"Wrote {json_path}")

# --- NEW: maintain a daily history (one JSON object per line). If the same day is run
# --- multiple times, overwrite that day's entry.
history_path = DATA / "forecast_history.jsonl"
date_key = now_iso[:10]  # YYYY-MM-DD

# build a compact history entry that includes the date key
history_entry = {
    "date": date_key,
    "generated_at_utc": now_iso,
    "meta": payload["meta"],
    "models": payload["models"],
}

# read existing lines (if any), filter out today's entry, and append new entry
existing_lines = []
if history_path.exists():
    try:
        with history_path.open("r", encoding="utf8") as fh:
            for ln in fh:
                ln = ln.strip()
                if not ln:
                    continue
                try:
                    obj = json.loads(ln)
                except Exception:
                    # skip malformed lines
                    continue
                # keep lines that are not today's date
                if obj.get("date") != date_key:
                    existing_lines.append(obj)
    except Exception as e:
        print("Warning: could not read existing history file, starting fresh:", e)

# append new entry and write back as newline-delimited JSON (one object per line)
existing_lines.append(history_entry)
try:
    with history_path.open("w", encoding="utf8") as fh:
        for obj in existing_lines:
            fh.write(json.dumps(obj, separators=(",", ":"), ensure_ascii=False) + "\n")
    print(f"Wrote {history_path} ({len(existing_lines)} entries)")
except Exception as e:
    print("Warning: failed to update history file:", e)


# -------------------------
# Small image for site
# -------------------------
img_path = IMAGES / "latest.png"
try:
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates

    def to_1d(x):
        try:
            x = x.sel(point=0)
        except Exception:
            pass
        return np.asarray(x).flatten()

    def make_model_series(times_var, temp_var=None, wind_var=None, precip_var=None,
                          temp_conv=None, wind_conv=None, precip_conv=None):
        """
        Return dict with keys 'times','temps','winds','precs' or None on failure.
        wind_var may be a tuple (u10, v10) or a single DataArray.
        """
        try:
            if times_var is None:
                raise ValueError("missing times")
            times = pd.to_datetime(times_var)

            temps = None
            if temp_var is not None:
                temps = to_1d(temp_var)
                if temp_conv is not None:
                    temps = temp_conv(temps)

            winds = None
            if wind_var is not None:
                if isinstance(wind_var, (list, tuple)):
                    u, v = wind_var
                    u1 = to_1d(u)
                    v1 = to_1d(v)
                    winds = np.sqrt(u1**2 + v1**2)
                else:
                    winds = to_1d(wind_var)
                if wind_conv is not None and winds is not None:
                    winds = wind_conv(winds)

            precs = None
            if precip_var is not None:
                precs = to_1d(precip_var)
                if precip_conv is not None and precs is not None:
                    precs = precip_conv(precs)

            return {"times": times, "temps": temps, "winds": winds, "precs": precs}
        except Exception:
            return None

    # build series for each model, using the same conversions as the rest of the script
    series = {}
    series["HRRR"] = make_model_series(valid_times_hrrr,
                                       temp_var=t2m_hrrr,
                                       wind_var=si10_hrrr,
                                       precip_var=tp_hrrr,
                                       wind_conv=lambda x: x * 1.94384)   # m/s -> kt

    series["IFS"] = make_model_series(valid_times_ifs,
                                      temp_var=t2m_ifs,
                                      wind_var=(u10_ifs, v10_ifs),
                                      precip_var=tp_ifs,
                                      wind_conv=lambda x: x * 1.94384,
                                      precip_conv=lambda x: x * 39.3701)   # m -> in (as used elsewhere)

    series["AIFS"] = make_model_series(valid_times_aifs,
                                       temp_var=t2m_aifs,
                                       wind_var=(u10_aifs, v10_aifs),
                                       precip_var=tp_aifs,
                                       wind_conv=lambda x: x * 1.94384,
                                       precip_conv=lambda x: x * 0.0393701)

    series["GFS"] = make_model_series(valid_times_gfs,
                                      temp_var=t2m_f,
                                      wind_var=(u10, v10),
                                      precip_var=tp_gfs,
                                      wind_conv=lambda x: x * 1.94384)  # tp_gfs already converted earlier

    # if no valid series at all, skip image creation
    if not any(v is not None for v in series.values()):
        raise RuntimeError("No model series available to plot")

    # plotting
    colors = {"HRRR": "C0", "IFS": "C1", "GFS": "C2", "AIFS": "C3"}
    fig, axes = plt.subplots(3, 1, figsize=(12, 10), sharex=True)

    # Temperature
    ax = axes[0]
    for name in ["HRRR", "IFS", "GFS", "AIFS"]:
        s = series.get(name)
        if s and s["times"] is not None and s["temps"] is not None:
            try:
                ax.plot(s["times"], s["temps"], marker="o", linestyle="-", color=colors[name], label=name)
            except Exception:
                pass
    ax.set_ylabel("Temperature (°F)")
    ax.grid(True, linestyle="--", alpha=0.4)
    ax.legend(loc="best")

    # Wind
    ax = axes[1]
    for name in ["HRRR", "IFS", "GFS", "AIFS"]:
        s = series.get(name)
        if s and s["times"] is not None and s["winds"] is not None:
            try:
                ax.plot(s["times"], s["winds"], marker="o", linestyle="-", color=colors[name], label=name)
            except Exception:
                pass
    ax.set_ylabel("Wind Speed (kt)")
    ax.grid(True, linestyle="--", alpha=0.4)
    ax.legend(loc="best")

    # Precipitation (line plot)
    ax = axes[2]
    for name in ["HRRR", "IFS", "GFS", "AIFS"]:
        s = series.get(name)
        if s and s["times"] is not None and s["precs"] is not None:
            try:
                ax.plot(s["times"], s["precs"], marker="o", linestyle="-", color=colors[name], label=name, alpha=0.8)
            except Exception:
                pass
    ax.set_ylabel("Precipitation (in)")
    ax.set_xlabel("Valid time (UTC)")
    ax.grid(True, linestyle="--", alpha=0.4)
    ax.legend(loc="best")

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