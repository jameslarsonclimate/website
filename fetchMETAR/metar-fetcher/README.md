# Constants
SERVICE = "http://mesonet.agron.iastate.edu/cgi-bin/request/asos.py?"
MAX_ATTEMPTS = 6

def download_data(uri):
    """Fetch the data from the IEM ASOS service."""
    attempt = 0
    while attempt < MAX_ATTEMPTS:
        try:
            data = urlopen(uri, timeout=300).read().decode("utf-8")
            if data is not None and not data.startswith("ERROR"):
                return data
        except Exception as exp:
            print(f"download_data({uri}) failed with {exp}")
            attempt += 1
    print("Exhausted attempts to download, returning empty data")
    return ""

def download_metar_asos_data(airport_code):
    """Download METAR/ASOS data for the specified airport code."""
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(weeks=2)

    # Prepare the URL for downloading data
    service_url = (
        SERVICE + "data=all&tz=Etc/UTC&format=comma&latlon=yes&"
        + start_date.strftime("year1=%Y&month1=%m&day1=%d&")
        + end_date.strftime("year2=%Y&month2=%m&day2=%d&")
        + f"station={airport_code}"
    )

    print(f"Downloading data for {airport_code} from {start_date} to {end_date}...")
    data = download_data(service_url)

    # Save data to CSV
    if data:
        output_file = f"{airport_code}_metar_asos_data.csv"
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(data)
        print(f"Data saved to {output_file}")
    else:
        print("No data downloaded.")

# Specify the airport code
airport_code = "KATL"  # Example: Atlanta Hartsfield-Jackson International Airport
download_metar_asos_data(airport_code)
```

### Instructions to Use:
1. Open a Jupyter Notebook.
2. Copy and paste the above code into a cell.
3. Change the `airport_code` variable to the desired airport code (e.g., "KATL" for Atlanta).
4. Run the cell to download the METAR/ASOS data for the specified airport and save it as a CSV file.

### Note:
- Ensure you have an active internet connection as the script fetches data from an online service.
- The downloaded CSV file will be saved in the current working directory of your Jupyter Notebook.