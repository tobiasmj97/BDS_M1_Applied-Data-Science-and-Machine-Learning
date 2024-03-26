#Load pandas
import pandas as pd

# Read the file from remote
data = pd.read_json('https://admin.opendata.dk/dataset/44ecd686-5cb5-40f2-8e3f-b5e3607a55ef/resource/eeabb0f8-1b19-4c80-b059-5ba5c4c872d2/download/guidedenmarkaalborgenjson.json')

# The GeoCoordinates are hiding in the Address column
data['Address'][0]['GeoCoordinate']

# You can use list comprehension to pull out GeoCoordinates (also empty values) - try out
# This will allow you to filter for missing data without fancy workarounds
[x['GeoCoordinate'] for x in data['Address']]

# Make a new column based on that to be used for filtering out missing data
data['GeoCoordinate'] = [x['GeoCoordinate'] for x in data['Address']]

# drop, where no GeoCoordinate
data = data.dropna(subset=['GeoCoordinate'])

# Pull out the values
data['latitude'] = [x['Latitude'] for x in data['GeoCoordinate']]
data['longitude'] = [x['Longitude'] for x in data['GeoCoordinate']]