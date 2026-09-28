#!/bin/bash
# Run the WxChallenge forecast script in the weather-output conda environment.
# Usage: ./getForecast_wxChallenge.sh [ICAO] [--target-date YYYY-MM-DD] [--no-push] [--skip-grib]

# Set error handling
set -e

# Define file path
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FORECAST_SCRIPT="$SCRIPT_DIR/getForecast_wxChallenge-pushGitHub.py"
cd "$SCRIPT_DIR"

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
# cron/launchd start with a minimal PATH, so look for conda in common install locations
if ! command -v conda >/dev/null 2>&1; then
    for base in "$HOME/miniforge3" "$HOME/mambaforge" "$HOME/miniconda3" "$HOME/anaconda3" \
                "/opt/homebrew/Caskroom/miniforge/base" "/opt/miniconda3" "/opt/anaconda3"; do
        if [ -x "$base/bin/conda" ]; then export PATH="$base/bin:$PATH"; break; fi
    done
fi
if ! command -v conda >/dev/null 2>&1; then
    echo "Error: conda not found on PATH."
    exit 1
fi
eval "$(conda shell.bash hook)"

# (with 'set -e' a separate '$?' check never runs, so test the command directly)
if ! conda activate wxchallenge; then
    echo "Error: Failed to activate conda environment 'wxchallenge'"
    exit 1
fi

# Run the Python script
# Arguments are passed through, e.g. ./getForecast_wxChallenge.sh KTPA --no-push
python "$FORECAST_SCRIPT" "$@"

# Deactivate the environment
conda deactivate

echo "------------------------------"
echo "Forecast script execution completed."
