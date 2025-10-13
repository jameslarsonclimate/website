#!/usr/bin/env python3
# coding: utf-8

import xarray as xr
import pandas as pd


# Dictionary of commonly forecasted locations
forecast_locations = {
    "Fort Collins, CO": {"longitude": -105.0844, "latitude": 40.5853},
    "ARDEC South, CO": {"longitude": -104.996890, "latitude": 40.611019},
    "Steamboat Ski Resort, CO": {"longitude": -106.743743, "latitude": 40.457346},
    "Cameron Pass, CO": {"longitude": -105.902831, "latitude": 40.520283},
    "Winter Park, CO": {"longitude": -105.779869, "latitude": 39.850607},
    "Jackson Hole Ski Resort, WY": {"longitude": -110.856876, "latitude": 43.598331},
    "Medford, OR": {"longitude": -122.873062, "latitude": 42.368191},
}


# Plotting utility functions
def detrend_dim(da, dim, deg=1):
    """
    Linearly detrend data along a specified dimension.

    Parameters:
    da (xarray.DataArray): The input data array to be detrended.
    dim (str): The dimension along which to detrend the data.
    deg (int): The degree of the polynomial fit. Default is 1 (linear detrending).

    Returns:
    xarray.DataArray: The detrended data array.

    Adapted from: https://gist.github.com/rabernat/1ea82bb067c3273a6166d1b1f77d490f
    """
    # Perform polynomial fit along the specified dimension
    p = da.polyfit(dim=dim, deg=deg)

    # Evaluate the polynomial fit along the dimension to get the trend
    fit = xr.polyval(da[dim], p.polyfit_coefficients)

    # Subtract the trend from the original data to obtain the detrended data
    detrended_da = da - fit

    # Maintain the same attributes and variable name
    detrended_da.attrs = da.attrs
    detrended_da.name = da.name

    # Add the 'methodology' attribute
    detrended_da.attrs['methodology: detrend'] = f"{deg} degree detrended performed as a function of grid cell"

    return detrended_da


def remove_seasonal_cycle(data):
    """
    Remove the seasonal cycle from a dataset to create monthly anomalies.

    Parameters:
    data (xarray.DataArray or xarray.Dataset): The input data with a 'time' dimension.

    Returns:
    xarray.DataArray or xarray.Dataset: The data with the seasonal cycle removed, resulting in monthly anomalies.
    """
    # Compute the monthly mean climatology
    monthly_climatology = data.groupby('time.month').mean()

    # Compute the monthly anomalies by subtracting the monthly climatology
    data_anom = data.groupby('time.month') - monthly_climatology

    # Maintain the same attributes and variable name
    data_anom.attrs = data.attrs
    data_anom.name = data.name

    # Add the 'methodology' attribute
    data_anom.attrs['methodology: anomalies'] = "Seasonal cycle removed to create monthly anomalies by using xr.DataArray.groupby('time.month')"

    return data_anom


def stand(da):
    """
    Standardizes the input data array by removing the mean and dividing by the standard deviation along the time dimension.

    Parameters:
    da (xarray.DataArray): The data array to be standardized.

    Returns:
    xarray.DataArray: Standardized data array.
    """
    return (da - da.mean('time')) / da.std('time')


def get_latest_forecast_cycle(model='HRRR'):
    """Get the most recent forecast initialization time (00, 06, 12, or 18 UTC).

    This function determines which of the daily forecast initialization times
    was most recently passed, accounting for each model's specific processing delay
    and initialization schedule.
    
    Parameters:
        model (str): The forecast model to use. Options include:
            - 'HRRR': High-Resolution Rapid Refresh (1.5 hour delay, runs at 00/06/12/18z)
            - 'IFS': ECMWF Integrated Forecasting System (8.7 hour delay, runs at 00/12z only)
            - Other models can be added to the model_configs dictionary

    Returns:
        pd.Timestamp: The most recent past forecast initialization time as a 
            timezone-naive timestamp. For HRRR, possible hours are 00, 06, 12, or 18 UTC.
            For IFS, possible hours are 00 or 12 UTC only.
            If no valid initialization time is found, returns the latest possible time from previous day.

    Example:
        >>> # If current time is 2024-03-15 14:30 UTC
        >>> get_latest_forecast_cycle()  # HRRR model (default)
        Timestamp('2024-03-15 12:00:00')
        >>> get_latest_forecast_cycle('IFS')  # IFS model 
        Timestamp('2024-03-15 00:00:00')
    """
    # Model configuration dictionary with processing delays and initialization hours
    model_configs = {
        'HRRR': {
            'delay': 1.5,        # HRRR has ~1.5 hour processing delay
            'init_hours': [0, 6, 12, 18]  # HRRR runs 4 times daily
        },
        'IFS': {
            'delay': 7.75,        # IFS has ~7.75 hour processing delay
            'init_hours': [0, 12]  # IFS runs 2 times daily
        },
        'AIFS': {
            'delay': 7,        # AIFS has ~7 hour processing delay
            'init_hours': [0, 6, 12, 18]  # AIFS runs 4 times daily
        },
        'GFS': {
            'delay': 5.0,        # GFS has ~5 hour processing delay
            'init_hours': [0, 6, 12, 18]  # GFS runs 4 times daily
        },
        'NBM': {
            'delay': 1.5,        # NBM has ~1.5 hour processing delay
            'init_hours': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24]  # NBM runs hourly
        }

        # Add other models as needed
    }
    
    # Check if the model exists in the configurations
    if model not in model_configs:
        valid_models = list(model_configs.keys())
        raise ValueError(f"Invalid model name: '{model}'. Please use one of the following: {', '.join(valid_models)}")
    
    # Get model configuration
    config = model_configs[model]
    delay_hours = config['delay']
    init_hours = config['init_hours']
    
    # Get current time and adjust for processing delay
    now = pd.Timestamp.now(tz='UTC')
    effective_time = now - pd.Timedelta(hours=delay_hours)
    
    # Find the most recent initialization time
    today = effective_time.floor('D')  # Start of today
    init_times = [today + pd.Timedelta(hours=h) for h in init_hours]
    
    # Add yesterday's last init time to handle early hours
    yesterday = today - pd.Timedelta(days=1)
    yesterday_init_times = [yesterday + pd.Timedelta(hours=h) for h in init_hours]
    init_times = yesterday_init_times + init_times
    
    # Find the most recent initialization time before the effective time
    for init_time in reversed(init_times):
        if effective_time >= init_time:
            return init_time.tz_localize(None)
    
    # Fallback (should rarely happen) - return the latest init time from 2 days ago
    two_days_ago = yesterday - pd.Timedelta(days=1)
    return (two_days_ago + pd.Timedelta(hours=max(init_hours))).tz_localize(None)

def sel_region(da, center, width): 
    half_width = width / 2
    lon = (center[0] + 360) % 360
    da = da.where(da['latitude'] > center[1] - half_width, drop=True)
    da = da.where(da['latitude'] < center[1] + half_width, drop=True)
    da = da.where(da['longitude'] > lon - half_width, drop=True)
    return da.where(da['longitude'] < lon + half_width, drop=True)


def convert_time_to_datetime64(data, units="seconds since 1970-01-01T00:00:00", 
                               calendar="proleptic_gregorian"):
    """
    Convert time values from 'seconds since epoch' format to np.datetime64.
    
    Parameters
    ----------
    data : xarray.Dataset, xarray.DataArray or numpy.ndarray
        Dataset containing time values or array of time values directly
    units : str, optional
        The time units string, default "seconds since 1970-01-01T00:00:00"
    calendar : str, optional
        The calendar type, default "proleptic_gregorian"
    
    Returns
    -------
    numpy.ndarray
        Array of np.datetime64 values
    """
    import numpy as np
    import cftime
    
    # Extract time values if this is an xarray object
    if hasattr(data, 'time'):
        seconds_since_epoch = data.time.values
    else:
        seconds_since_epoch = data
    
    # Convert to cftime objects
    cftime_dates = cftime.num2date(seconds_since_epoch, units=units, calendar=calendar)
    
    # Convert to np.datetime64
    if data.size == 1:
        datetime64_values = np.datetime64(cftime_dates.strftime('%Y-%m-%dT%H'))
    else:
        datetime64_values = np.array([np.datetime64(date.strftime('%Y-%m-%dT%H')) 
                                    for date in cftime_dates])
    
    return datetime64_values

def _snap_hour_for_model(target_hour, model):
    """
    Snap a requested target_hour to the nearest model output hour based on model frequency.
    Returns an int in 0-23. Uses nearest rounding (e.g., 2 -> 3 for 3-hour models).
    """
    freq_map = {'HRRR': 1, 'IFS': 3, 'GFS': 3, 'AIFS': 6, 'NBM': 1}
    freq = freq_map.get(model, 1)
    if freq == 1:
        return int(target_hour) % 24
    # Round to nearest multiple of freq
    snapped = int(round(target_hour / freq) * freq) % 24
    return snapped

# ...existing code...
def calculate_forecast_range(timestamp, model="HRRR", target_hour=6):
    """
    Calculate forecast range based on model type.

    Args:
        timestamp: pd.Timestamp of the forecast initialization
        model: str, model type ('HRRR', 'IFS', 'GFS', 'AIFS')
        target_hour: int, target "anchor" hour (UTC) to align the forecast window.
                     Default 6 preserves original 06-06z behavior.

    Returns:
        list: Range of forecast hours

    Notes:
    - HRRR unchanged by default (hourly increments).
    - IFS/GFS/AIFS unchanged by default (3- or 6-hour increments as before).
    - Supplying target_hour=2 will produce a 02-02z window instead of 06-06z when possible;
      if the model does not produce hourly outputs the requested hour is snapped to the
      nearest model output hour (e.g., 02 -> 03 for 3-hour models using nearest rounding).
    """
    if not isinstance(target_hour, int) or not (0 <= target_hour <= 23):
        raise ValueError("target_hour must be an integer between 0 and 23 (inclusive)")

    # Snap the requested target_hour to the model's native output frequency so we don't
    # request an anchor hour that the model never produces (e.g., 02 for a 3-hour model).
    freq_map = {'HRRR': 1, 'IFS': 3, 'GFS': 3, 'AIFS': 6, 'NBM': 1}
    freq = freq_map.get(model, 1)
    snapped_target = _snap_hour_for_model(target_hour, model)
    if snapped_target != target_hour:
        # lightweight notice for logs; safe to keep for cron/CI logs
        print(f"Note: target_hour {target_hour} snapped to {snapped_target} for model {model} (interval={freq}h)")

    target = snapped_target

    if model == "HRRR":
        # Original behavior for HRRR but anchored to target (HRRR is hourly)
        hours_to_target = (24 - timestamp.hour + target) % 24
        if hours_to_target == 0:
            hours_to_target = 24  # If already at target_hour, target the next day's hour

        # For 0z model run, add 24 hours to target the following day (preserve original special-case)
        if timestamp.hour == 0:
            return list(range(hours_to_target + 24, hours_to_target + 49))
        else:
            return list(range(hours_to_target, hours_to_target + 25))

    elif model == "IFS":
        # Behavior for IFS anchored to target (3-hour outputs)
        hours_to_target = (24 - timestamp.hour + target) % 24
        if hours_to_target == 0:
            hours_to_target = 24

        if timestamp.hour == 0:
            start = hours_to_target + 24
        else:
            start = hours_to_target

        # Generate exactly 9 time steps with 3-hour increments (preserve original behavior)
        return list(range(start, start + (9 * 3), 3))

    elif model == "AIFS":
        # Behavior for AIFS anchored to target (6-hour outputs)
        hours_to_target = (24 - timestamp.hour + target) % 24
        if hours_to_target == 0:
            hours_to_target = 24

        if timestamp.hour == 0:
            start = hours_to_target + 24
        else:
            start = hours_to_target

        # Generate exactly 5 time steps with 6-hour increments (preserve original behavior)
        return list(range(start, start + (5 * 6), 6))

    elif model == "GFS":
        # Behavior for GFS anchored to target (3-hour outputs)
        hours_to_target = (24 - timestamp.hour + target) % 24
        if hours_to_target == 0:
            hours_to_target = 24

        if timestamp.hour == 0:
            start = hours_to_target + 24
        else:
            start = hours_to_target

        # Generate exactly 9 time steps with 3-hour increments (preserve original behavior)
        return list(range(start, start + (9 * 3), 3))

    else:
        raise ValueError(f"Unsupported model: {model}. Supported models: 'HRRR', 'IFS', 'GFS', 'AIFS'")


def run_hour(init):
    if init is None:
        return "n/a"
    try:
        val = init[0] if hasattr(init, "__len__") and not isinstance(init, (str, bytes)) else init
        ts = pd.Timestamp(val)
        return f"{ts.hour:02d}z"
    except Exception:
        return "n/a"

def fmt(val, kind):
    if val is None:
        return "n/a"
    try:
        if kind == "t":
            return f"{val:.1f}"
        if kind == "w":
            return f"{int(round(val))}"
        if kind == "p":
            return f"{val:.2f}"
    except Exception:
        return "n/a"


# def calculate_forecast_range(timestamp, model="HRRR"):
#     """
#     Calculate forecast range based on model type.
    
#     Args:
#         timestamp: pd.Timestamp of the forecast initialization
#         model: str, model type ('HRRR' or 'IFS')
        
#     Returns:
#         list: Range of forecast hours
    
#     For HRRR:
#         Calculate forecast range from the timestamp to 5:00 the next day plus 24 hours
#         in 1-hour increments
        
#     For IFS:
#         Calculate forecast range from the timestamp to 6:00 the next day plus 24 hours
#         in 3-hour increments

#     For GFS:
#         Calculate forecast range from the timestamp to 3:00 the next day plus 24 hours
#         in 3-hour increments
#     """
#     if model == "HRRR":
#         # Original behavior for HRRR (target 6:00 AM)
#         hours_to_target = (24 - timestamp.hour + 6) % 24
#         if hours_to_target == 0:
#             hours_to_target = 24  # If already at 6am, we want the next day's 6am

#         # For 0z model run, add 24 hours to target the following day
#         if timestamp.hour == 0:
#             return list(range(hours_to_target + 24, hours_to_target + 49))
#         else:
#             return list(range(hours_to_target, hours_to_target + 25))
    
#     elif model == "IFS":
#         # Modified behavior for IFS (target 6:00 AM)
#         hours_to_target = (24 - timestamp.hour + 6) % 24
#         if hours_to_target == 0:
#             hours_to_target = 24  # If already at 6am, we want the next day's 6am

#         # Calculate start point
#         if timestamp.hour == 0:
#             start = hours_to_target + 24
#         else:
#             start = hours_to_target

#         # Generate exactly 9 time steps with 3-hour increments (covering 06:00 to 06:00)
#         return list(range(start, start + (9 * 3), 3))
    
#     elif model == "AIFS":
#         # Modified behavior for AIFS (target 6:00 AM)
#         hours_to_target = (24 - timestamp.hour + 6) % 24
#         if hours_to_target == 0:
#             hours_to_target = 24  # If already at 6am, we want the next day's 6am

#         # Calculate start point
#         if timestamp.hour == 0:
#             start = hours_to_target + 24
#         else:
#             start = hours_to_target

#         # Generate exactly 5 time steps with 6-hour increments (covering 06:00 to 06:00)
#         return list(range(start, start + (5 * 6), 6))

#     elif model == "GFS":
#         # Modified behavior for GFS (target 6:00 AM)
#         hours_to_target = (24 - timestamp.hour + 6) % 24
#         if hours_to_target == 0:
#             hours_to_target = 24  # If already at 6am, we want the next day's 6am

#         # Calculate start point
#         if timestamp.hour == 0:
#             start = hours_to_target + 24
#         else:
#             start = hours_to_target

#         # Generate exactly 8 time steps with 3-hour increments (covering 06:00 to 06:00)
#         return list(range(start, start + (9 * 3), 3))

#     else:
#         raise ValueError(f"Unsupported model: {model}. Supported models: 'HRRR', 'IFS', 'GFS'")