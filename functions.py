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


def get_latest_forecast_cycle():
    """Get the most recent forecast initialization time (00, 06, 12, or 18 UTC).

    This function determines which of the four daily forecast initialization times 
    was most recently passed. The function checks if the current time is past 
    19:30, 13:30, 07:30, or 01:30 UTC and returns the corresponding initialization 
    time (18:00, 12:00, 06:00, or 00:00 UTC respectively). These times correspond 
    to when new forecast model runs typically become available, accounting for 
    ~1.5 hour processing delay.

    Returns:
        pd.Timestamp: The most recent past forecast initialization time as a 
            timezone-naive timestamp. Possible hours are 00, 06, 12, or 18 UTC.
            If current time is before 01:00 UTC, returns 18:00 UTC from previous day.

    Example:
        >>> # If current time is 2024-03-15 14:30 UTC
        >>> get_latest_forecast_cycle()
        Timestamp('2024-03-15 12:00:00')
    """

    now = pd.Timestamp.now(tz='UTC')
    
    # Check which time is the most recent past time
    if now >= pd.Timestamp(now.year, now.month, now.day, 19, 30, tz='UTC'):
        recent_time = pd.Timestamp(now.year, now.month, now.day, 18, 0, tz='UTC')
    elif now >= pd.Timestamp(now.year, now.month, now.day, 13, 30, tz='UTC'):
        recent_time = pd.Timestamp(now.year, now.month, now.day, 12, 0, tz='UTC')
    elif now >= pd.Timestamp(now.year, now.month, now.day, 7, 30, tz='UTC'):
        recent_time = pd.Timestamp(now.year, now.month, now.day, 6, 0, tz='UTC')
    elif now >= pd.Timestamp(now.year, now.month, now.day, 1, 30, tz='UTC'):
        recent_time = pd.Timestamp(now.year, now.month, now.day, 0, 0, tz='UTC')
    else:
        recent_time = pd.Timestamp(now.year, now.month, now.day-1, 18, 0, tz='UTC')

    return recent_time.tz_localize(None)


def sel_region(da, center, width): 
    half_width = width / 2
    da = da.where(da['latitude'] > center[0] - half_width, drop=True)
    da = da.where(da['latitude'] < center[0] + half_width, drop=True)
    da = da.where(da['longitude'] > center[1] - half_width, drop=True)
    return da.where(da['longitude'] < center[1] + half_width, drop=True)


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


def calculate_forecast_range(timestamp):
    """
    Calculate forecast range from the timestamp to 5:00 the next day plus 24 hours
    
    Args:
        timestamp: pd.Timestamp of the forecast initialization
        
    Returns:
        np.ndarray: Range of forecast hours
    """
    # Calculate hours from timestamp to 05:00 the next day
    hours_to_5am = (24 - timestamp.hour + 5) % 24
    if hours_to_5am == 0:
        hours_to_5am = 24  # If already at 5am, we want the next day's 5am
        
    # Set the forecast range from hours_to_5am to hours_to_5am + 25
    return list(range(hours_to_5am, hours_to_5am + 25)) 
