"""
Fetch HRRR and IFS forecasts for a point, save summary JSON and a small image,
and push results to the git repo (suitable for GitHub Pages).

This version inlines the previous fetch_model_metrics logic for HRRR and IFS
instead of using a helper function.
"""
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

warnings.filterwarnings("ignore", message="Engine 'gini' loading failed.*", category=RuntimeWarning)

ROOT = Path(__file__).resolve().parent
(IMAGES := ROOT / "images" / "wxchallenge").mkdir(parents=True, exist_ok=True)
(DATA := ROOT / "data" / "wxchallenge").mkdir(parents=True, exist_ok=True)

cityName = "San Antonio (KSAT)"
points = pd.DataFrame({"longitude": [-98.469932], "latitude": [29.523753]})

now_iso = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

# -------------------------
# HRRR (inline)
# -------------------------
try:
    print("Fetching HRRR data...")

    init_hrrr = get_latest_forecast_cycle(model="HRRR")
    fxx_hrrr = calculate_forecast_range(init_hrrr, model="HRRR")
    H_hrrr = FastHerbie([init_hrrr], model="hrrr", product="sfc", fxx=fxx_hrrr)

    t2m_hrrr = H_hrrr.xarray("TMP:2 m above", backend_kwargs={'decode_times': False}
                            ).herbie.pick_points(points, method="nearest")['t2m'].sel(point=0)
    t2m_hrrr = (t2m_hrrr - 273.15) * 1.8 + 32
    tmax_hrrr = float(t2m_hrrr.max().values)
    tmin_hrrr = float(t2m_hrrr.min().values)
    init_times_hrrr = convert_time_to_datetime64(t2m_hrrr.time.values)
    valid_times_hrrr = convert_time_to_datetime64(t2m_hrrr.valid_time.values)

    si10_hrrr = H_hrrr.xarray(":WIND", backend_kwargs={'decode_times': False}
                              ).herbie.pick_points(points, method="nearest")['si10'].sel(point=0)
    wind_max_hrrr = float(si10_hrrr.max().values) * 1.94384

    tp_hrrr = H_hrrr.xarray("APCP", backend_kwargs={'decode_times': False}
                            ).herbie.pick_points(points, method="nearest")['tp'].sel(point=0)
    tp_hrrr = tp_hrrr * 0.0393701
    tp_hrrr = tp_hrrr[1:] - tp_hrrr[0]
    precip_hrrr = float(tp_hrrr.max().values)

    hrrr_metrics = {
        "tmax_f": round(tmax_hrrr, 2),
        "tmin_f": round(tmin_hrrr, 2),
        "wind_max_kt": round(wind_max_hrrr, 2),
        "precip_in": round(precip_hrrr, 3),
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

    t2m_ifs = H_ifs.xarray(":2t:", backend_kwargs={'decode_times': False}
                          ).herbie.pick_points(points, method="nearest")['t2m'].sel(point=0)
    t2m_ifs = (t2m_ifs - 273.15) * 1.8 + 32
    tmax_ifs = float(t2m_ifs.max().values)
    tmin_ifs = float(t2m_ifs.min().values)
    init_times_ifs = convert_time_to_datetime64(t2m_ifs.time.values)
    valid_times_ifs = convert_time_to_datetime64(t2m_ifs.valid_time.values)

    u10_ifs = H_ifs.xarray(":10u:", backend_kwargs={'decode_times': False}
                          ).herbie.pick_points(points, method="nearest")['u10'].sel(point=0)
    v10_ifs = H_ifs.xarray(":10v:", backend_kwargs={'decode_times': False}
                          ).herbie.pick_points(points, method="nearest")['v10'].sel(point=0)
    wind_max_ifs = float((np.sqrt(u10_ifs**2 + v10_ifs**2)).max().values) * 1.94384

    tp_ifs = H_ifs.xarray(":tp:", backend_kwargs={'decode_times': False}
                         ).herbie.pick_points(points, method="nearest")['tp'].sel(point=0)
    precip_ifs = float(tp_ifs.sum().values) * 0.0393701

    ifs_metrics = {
        "tmax_f": round(tmax_ifs, 2),
        "tmin_f": round(tmin_ifs, 2),
        "wind_max_kt": round(wind_max_ifs, 2),
        "precip_in": round(precip_ifs, 3),
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

# Create the title
title = f"Forecasting for {cityName} \nValid: {str(valid_times_hrrr[0])} - {str(valid_times_hrrr[-1])} UTC"

# Create the table combining both models (use the current variable names)
data = {
    "Model": ["HRRR", "IFS"],
    "High (°F)": [tmax_hrrr, tmax_ifs],
    "Low (°F)": [tmin_hrrr, tmin_ifs],
    "Precipitation (in)": [precip_hrrr, precip_ifs],
    "Wind Speed (kt)": [wind_max_hrrr, wind_max_ifs],
    "Model Init": [f"{str(init_times_hrrr)} UTC", f"{str(init_times_ifs)} UTC"]
}

df_forecast = pd.DataFrame(data).round(2)

# Print the title and table without row numbers
print(title)
print(df_forecast.to_string(index=False))


# -------------------------
# Build and write payload
# -------------------------
payload = {
    "generated_at_utc": now_iso,
    "meta": {
        "page": "wxchallenge",
        "site": cityName,
        "models": ["HRRR", "IFS"],
        "note": "temperatures in °F, winds in kt, precip in inches"
    },
    "models": {
        "HRRR": hrrr_metrics,
        "IFS": ifs_metrics
    }
}

json_path = DATA / "forecast.json"
json_path.write_text(json.dumps(payload, indent=2))
print(f"Wrote {json_path}")

# -------------------------
# Small image for site
# -------------------------
img_path = IMAGES / "latest.png"
try:
    im = Image.new("RGB", (1000, 300), (245, 247, 250))
    d = ImageDraw.Draw(im)
    txt = f"{cityName}\nUpdated: {now_iso}\nHRRR tmax: {hrrr_metrics.get('tmax_f')}°F  IFS tmax: {ifs_metrics.get('tmax_f')}°F"
    d.text((20, 20), txt, fill=(20, 20, 20))
    im.save(img_path, "PNG")
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