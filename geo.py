import pandas as pd
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter

data = pd.read_excel('players.xlsx', sheet_name='players')

geolocator = Nominatim(user_agent="geoapiExercises")
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)

def get_coordinates(city, country):
    try:
        location = geolocator.geocode(f"{city}, {country}")
        if location:
            return location.latitude, location.longitude
        else:
            return None, None
    except:
        return None, None

data[['latitude', 'longitude']] = data.apply(lambda row: pd.Series(get_coordinates(row['City'], row['Country'])), axis=1)

data.to_excel('players_with_coordinates.xlsx', sheet_name='players.csv', index=False)

"""
If still not complete due to GeoAPI limitation, run this again:

import pandas as pd
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter

data = pd.read_excel('players_with_coordinates.xlsx', sheet_name='players')

geolocator = Nominatim(user_agent="geoapiExercises")
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)

def get_coordinates(city, country):
    try:
        location = geolocator.geocode(f"{city}, {country}")
        if location:
            return location.latitude, location.longitude
        else:
            return None, None
    except:
        return None, None

data[['latitude', 'longitude']] = data.apply(
    lambda row: pd.Series(get_coordinates(row['City'], row['Country'])) 
    if pd.isnull(row['latitude']) or pd.isnull(row['longitude']) else pd.Series([row['latitude'], row['longitude']]), 
    axis=1
)

data.to_excel('players_with_coordinates_updated.xlsx', sheet_name='players', index=False)

"""
