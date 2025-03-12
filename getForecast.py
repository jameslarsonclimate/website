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
cityName = "Medford, OR"
points = pd.DataFrame({"longitude": [-122.873062], # [Medford, OR]
                       "latitude":  [42.368191],  # [Medford, OR]
                       })
# points = pd.DataFrame({"longitude": [-105.082396, -122.873062], # [Fort Collins, Medford, OR]
#                        "latitude":  [40.548843,    42.368191],  # [Fort Collins, Medford, OR]
#                        })

forecastInit = get_latest_forecast_cycle()
# forecastInit = pd.Timestamp(2025, 3, 5, 18, 0)

# Use the function to calculate forecast range
forecastRange = calculate_forecast_range(forecastInit)

##################################################


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

model_init = convert_time_to_datetime64(t2m_HRRR.time.values)
model_valid_times = convert_time_to_datetime64(t2m_HRRR.valid_time.values)

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

### Print the table

# Create the title
title = f"Forecasting for {cityName} - Model initialized {str(model_init)} UTC\nValid: {str(model_valid_times[0])} - {str(model_valid_times[-1])}"
# {tomorrow.strftime('%B %d')} 06UTC - {day_after_tomorrow.strftime('%B %d')} 06UTC"

# Create the table
data = {
    "Model": ["HRRR"],  # "NBM"],
    "High (°F)": [t2m_max_HRRR],  # np.nan],
    "Low (°F)": [t2m_min_HRRR],  # np.nan],   
    "Precipitation (in)": [tp_max_HRRR],  # np.nan],  
    "Wind Speed (kt)": [si10_max_HRRR],  # np.nan]  
}

df_forecast = pd.DataFrame(data).round(2)

# Print the title and table without row numbers
print(title)
print(df_forecast.to_string(index=False))