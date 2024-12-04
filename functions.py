#!/usr/bin/env python3
# coding: utf-8

import xarray as xr
import pandas as pd

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
