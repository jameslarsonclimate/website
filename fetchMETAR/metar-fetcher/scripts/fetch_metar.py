import pandas as pd
from datetime import datetime, timedelta
from urllib.request import urlopen
import os

# Function to download data from IEM ASOS service
def download_metar_data(station_code, start_date, end_date):
    """
    Download METAR/ASOS data for a specified airport code from the IEM ASOS service.

    Args:
        station_code (str): The airport code (e.g., 'KATL' for Atlanta).
        start_date (datetime): The start date for the data download.
        end_date (datetime): The end date for the data download.

    Returns:
        pd.DataFrame: DataFrame containing the METAR/ASOS data.
    """
    # Base URL for IEM ASOS service
    service_url = "http://mesonet.agron.iastate.edu/cgi-bin/request/asos.py?"

    # Prepare the request URL
    request_url = f"{service_url}data=all&tz=Etc/UTC&format=comma&latlon=yes&"
    request_url += f"year1={start_date.year}&month1={start_date.month}&day1={start_date.day}&"
    request_url += f"year2={end_date.year}&month2={end_date.month}&day2={end_date.day}&"
    request_url += f"station={station_code}"

    # Download the data
    try:
        print(f"Downloading data for {station_code} from {start_date} to {end_date}...")
        data = urlopen(request_url).read().decode("utf-8")
        return data
    except Exception as e:
        print(f"Failed to download data: {e}")
        return None

# Function to save data to CSV
def save_data_to_csv(data, filename):
    """
    Save the downloaded data to a CSV file.

    Args:
        data (str): The raw data as a string.
        filename (str): The filename for the CSV file.
    """
    with open(filename, "w", encoding="utf-8") as f:
        f.write(data)
    print(f"Data saved to {filename}")

# Main function to execute the download and save process
def main(station_code):
    # Define the date range (last two weeks)
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(weeks=2)

    # Download METAR/ASOS data
    raw_data = download_metar_data(station_code, start_date, end_date)

    if raw_data:
        # Save the data to a CSV file
        filename = f"{station_code}_metar_data_{start_date.strftime('%Y%m%d')}_{end_date.strftime('%Y%m%d')}.csv"
        save_data_to_csv(raw_data, filename)

# Specify the airport code (e.g., 'KATL' for Atlanta)
airport_code = 'KATL'  # Change this to your desired airport code
main(airport_code)