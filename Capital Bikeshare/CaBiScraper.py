import csv
import requests
from datetime import datetime

# URLs for the GBFS feeds
station_status_url = "https://gbfs.lyft.com/gbfs/2.3/dca-cabi/en/station_status.json"

# Mapping of actual station IDs to preferred names/shorter IDs
station_id_mapping = {
    '08247aa4-1f3f-11e7-bf6b-3863bb334450': '20th & E St NW',
    '8429af9f-3adc-4db6-b96a-7fd9c75fe3a3': '21st St & G st NW',
    '08261b21-1f3f-11e7-bf6b-3863bb334450': '22nd & P ST NW',
    '08249cd3-1f3f-11e7-bf6b-3863bb334450': '21st & E St NW',
}

# Fetch station status
response = requests.get(station_status_url)
status_data = response.json()

# Current time for logging, formatted as a string
now = datetime.now().strftime('%H:%M:%S')

# File to store the data
filename = "CaBiScraper.csv"

# Check if file exists to write headers
try:
    with open(filename, 'x', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["timestamp", "station_id", "num_regular_bikes_available", "num_ebikes_available", "num_bikes_disabled", "num_docks_disabled"])
except FileExistsError:
    pass

# Append data to the CSV, using the mapping for station IDs
with open(filename, 'a', newline='') as csvfile:
    writer = csv.writer(csvfile)
    for status in status_data['data']['stations']:
        if status['station_id'] in station_id_mapping:  # Check if the station_id is in your mapping
            preferred_id = station_id_mapping[status['station_id']]  # Use the preferred ID/name
            writer.writerow([
                now,
                preferred_id,
                status.get('num_bikes_available', 'N/A'),  # Assuming this includes regular bikes
                status.get('num_ebikes_available', 'N/A'),
                status.get('num_bikes_disabled', 'N/A'),
                status.get('num_docks_disabled', 'N/A')
            ])

print(f"Data for {now} written to {filename}")
