#!/bin/bash
# Script to run getForecast.py with the weather-output conda environment

# Set error handling
set -e

# Define file path
FORECAST_SCRIPT="/Users/jglarson/Documents/Website/weather-forecasts/getForecast_ATS640-pushGitHub.py"

# Check if the Python file exists
if [ ! -f "$FORECAST_SCRIPT" ]; then
    echo "Error: $FORECAST_SCRIPT not found."
    exit 1
fi

# Output execution information
echo "Running weather forecast script..."
echo "$(date)"
echo "------------------------------"

# Activate conda environment and execute the Python script
# Using 'eval' with $() to ensure conda initialization works in non-interactive shell
eval "$(conda shell.bash hook)"
conda activate weather-output

# Check if environment activation was successful
if [ $? -ne 0 ]; then
    echo "Error: Failed to activate conda environment 'weather-output'"
    exit 1
fi

# Run the Python script
python "$FORECAST_SCRIPT"

# Run the KFNL forecast script immediately after
SECOND_SCRIPT="/Users/jglarson/Documents/Website/weather-forecasts/getForecast_KFNL-pushGitHub.py"
if [ -f "$SECOND_SCRIPT" ]; then
    echo "Running KFNL forecast script..."
    python "$SECOND_SCRIPT"
else
    echo "Warning: $SECOND_SCRIPT not found, skipping."
fi

# Deactivate the environment
conda deactivate

echo "------------------------------"
echo "Forecast script execution completed."
