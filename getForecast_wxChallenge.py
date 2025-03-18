# Reference: https://herbie.readthedocs.io/en/stable/gallery/bonus_notebooks/time-height.html
from functions import *
from herbie import FastHerbie, HerbieLatest
import matplotlib.pyplot as plt
import pandas as pd
import xarray as xr
import numpy as np
from datetime import datetime, timedelta
import warnings
# Silence the specific RuntimeWarning about the 'gini' engine
warnings.filterwarnings("ignore", message="Engine 'gini' loading failed.*", category=RuntimeWarning)



# Define the points of interest
cityName = "Louisville, KY (KSDF)"
points = pd.DataFrame({"longitude": [-85.735122], # 
                       "latitude":  [38.171471],  # Louisville, KY (KSDF)
                       })

##################################################

forecastInit = get_latest_forecast_cycle(model='HRRR')
# forecastInit = pd.Timestamp(2025, 3, 5, 18, 0)

# Use the function to calculate forecast range
forecastRange = calculate_forecast_range(forecastInit)

H = FastHerbie(
    [forecastInit],
    model="hrrr",
    product="sfc",
    fxx=forecastRange,
)

# 2m temperature
t2m_HRRR = H.xarray("TMP:2 m above", backend_kwargs={'decode_times':False}
                  ).herbie.pick_points(points, method="nearest"
                                       )['t2m'].sel(point=0)[1:]

t2m_HRRR = (t2m_HRRR - 273.15) * 1.8 + 32
t2m_max_HRRR = float(t2m_HRRR.max().values)
t2m_min_HRRR = float(t2m_HRRR.min().values)

model_init_HRRR = convert_time_to_datetime64(t2m_HRRR.time.values)
model_valid_times_HRRR = convert_time_to_datetime64(t2m_HRRR.valid_time.values)

# 10m wind speed
si10_HRRR = H.xarray(":WIND", backend_kwargs={'decode_times':False}
                     ).herbie.pick_points(points, method="nearest"
                                          )['si10'].sel(point=0)[1:]
si10_max_HRRR = float(si10_HRRR.max().values)
si10_max_HRRR = si10_max_HRRR * 1.94384  # Convert m/s to knots

# Total precipitation
tp_HRRR = H.xarray("APCP", backend_kwargs={'decode_times':False}
              ).herbie.pick_points(points, method="nearest"
                                   )['tp'].sel(point=0)
tp_HRRR = tp_HRRR * 0.0393701  # Convert mm (1 kg m^-2 = 1 mm) to inches
tp_HRRR = tp_HRRR[1:] - tp_HRRR[0]  # Subtract the total precipitation that falls before 06UTC
tp_max_HRRR = float(tp_HRRR.max().values)



# ECMWF IFS

forecastInit = get_latest_forecast_cycle(model='ECMWF')

# Use the function to calculate forecast range
forecastRange = calculate_forecast_range(forecastInit)

H = FastHerbie(
    [forecastInit],
    model="ifs",
    product="oper",
    fxx=forecastRange,
)

# 2m temperature
t2m_IFS = H.xarray(":2t:", backend_kwargs={'decode_times':False}
                  ).herbie.pick_points(points, method="nearest"
                                       )['t2m'].sel(point=0)

t2m_IFS = (t2m_IFS - 273.15) * 1.8 + 32
t2m_max_IFS = float(t2m_IFS.max().values)
t2m_min_IFS = float(t2m_IFS.min().values)

model_init_IFS = convert_time_to_datetime64(t2m_IFS.time.values)
model_valid_times_IFS = convert_time_to_datetime64(t2m_IFS.valid_time.values)

# 10m wind speed
u10_IFS = H.xarray(":10u:", backend_kwargs={'decode_times':False}
                     ).herbie.pick_points(points, method="nearest"
                                          )['u10'].sel(point=0)
v10_IFS = H.xarray(":10v:", backend_kwargs={'decode_times':False}
                     ).herbie.pick_points(points, method="nearest"
                                          )['v10'].sel(point=0)
# Calculate max wind speed from u and v components
si10_max_IFS = float((np.sqrt(u10_IFS**2 + v10_IFS**2)).max().values)
si10_max_IFS = si10_max_IFS * 1.94384  # Convert m/s to knots

# Total precipitation
tp_IFS = H.xarray(":tp:", backend_kwargs={'decode_times':False}
                     ).herbie.pick_points(points, method="nearest"
                                          )['tp'].sel(point=0)
tp_sum_IFS = float(tp_IFS.sum().values)



### Print the table

# Create the title
title = f"Forecasting for {cityName} \nValid: {str(model_valid_times_HRRR[0])} - {str(model_valid_times_HRRR[-1])} UTC"

# Create the table combining both models
data = {
    "Model": ["HRRR", "ECMWF IFS"],
    "High (°F)": [t2m_max_HRRR, t2m_max_IFS],
    "Low (°F)": [t2m_min_HRRR, t2m_min_IFS],
    "Precipitation (in)": [tp_max_HRRR, tp_sum_IFS],
    "Wind Speed (kt)": [si10_max_HRRR, si10_max_IFS],
    "Model Init": [f" {str(model_init_HRRR)} UTC", f" {str(model_init_IFS)} UTC"]
}

df_forecast = pd.DataFrame(data).round(2)

# Print the title and table without row numbers
print(title)
print(df_forecast.to_string(index=False))
