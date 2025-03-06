#!/bin/bash

conda init

# Activate the environment
conda activate weather-output

python getForecast.py
