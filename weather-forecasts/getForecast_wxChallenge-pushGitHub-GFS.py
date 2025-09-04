"""
Minimal script: fetch GFS for a single point and print a small summary table.

- Relies on helper functions in ../functions.py (get_latest_forecast_cycle,
  calculate_forecast_range, convert_time_to_datetime64).
- Uses FastHerbie to request fields.
- Prints a 1-row table (model = GFS) showing High/Low (°F), Precip (in), Wind (kt), Init, Valid range.
"""
import sys
from pathlib import Path
from functions import *   # get_latest_forecast_cycle, calculate_forecast_range, convert_time_to_datetime64
from herbie import FastHerbie
import pandas as pd
import numpy as np

# single point (longitude, latitude)
cityName = "Loveland, CO (KFNL)"
points = pd.DataFrame({"longitude": [-105.004186], "latitude": [40.451685]})

print("Fetching GFS data...")

# determine latest cycle & forecast range for IFS
init_gfs = get_latest_forecast_cycle(model="IFS")
fxx_gfs = calculate_forecast_range(init_gfs, model="IFS")

# request fields (product string may vary by deployment; adjust if needed)
H = FastHerbie([init_gfs], model="gfs", product="pgrb2", fxx=fxx_gfs)

# 2 m temperature -> convert K to °F
t2m = H.xarray("TMP:2 m above", backend_kwargs={'decode_times': False}
                ).herbie.pick_points(points, method="nearest")['t2m'].sel(point=0)
t2m_f = (t2m - 273.15) * 9.0/5.0 + 32.0
tmax_gfs = float(t2m_f.max().values)
tmin_gfs = float(t2m_f.min().values)
init_times_gfs = convert_time_to_datetime64(t2m.time.values)
valid_times_gfs = convert_time_to_datetime64(t2m.valid_time.values)

# wind components -> magnitude (m/s -> kt)
u10 = H.xarray(":10u:", backend_kwargs={'decode_times': False}
                ).herbie.pick_points(points, method="nearest")['u10'].sel(point=0)
v10 = H.xarray(":10v:", backend_kwargs={'decode_times': False}
                ).herbie.pick_points(points, method="nearest")['v10'].sel(point=0)
wind_max_kt = float((np.sqrt(u10**2 + v10**2)).max().values) * 1.94384

# total precipitation (sum over steps) -> convert mm -> inches
tp = H.xarray(":tp:", backend_kwargs={'decode_times': False}
                ).herbie.pick_points(points, method="nearest")['tp'].sel(point=0)
precip_in = float(tp.sum().values) * 0.0393701

# build and print a simple table using pandas for formatting
df = pd.DataFrame({
    "Model": ["GFS"],
    "High (°F)": [round(tmax_gfs,2)],
    "Low (°F)": [round(tmin_gfs,2)],
    "Precipitation (in)": [round(precip_in,3)],
    "Wind Speed (kt)": [round(wind_max_kt,2)],
    "Model Init": [pd.Timestamp(init_times_gfs[0]).isoformat() if hasattr(init_times_gfs, "__len__") else str(init_times_gfs)],
    "Valid Range": [f"{valid_times_gfs[0]} - {valid_times_gfs[-1]}"]
})

title = f"Forecasting for {cityName}"
print(title)
print(df.to_string(index=False))
