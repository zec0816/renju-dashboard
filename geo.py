import pandas as pd
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter

# Read Excel
data = pd.read_excel('players_20250803.xlsx', sheet_name='players_20250803')

# Use a unique user_agent with contact info
geolocator = Nominatim(user_agent="renju_rating_geocoder (trash5896@gmail.com)")

# Add delay to respect rate limits
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=2)

# Cache results to avoid duplicate lookups
cache = {}

def get_coordinates(city, country):
    key = (city, country)
    if key in cache:
        return cache[key]
    try:
        location = geolocator.geocode(f"{city}, {country}")
        if location:
            coords = (location.latitude, location.longitude)
        else:
            coords = (None, None)
    except Exception:
        coords = (None, None)
    cache[key] = coords
    return coords

# Apply coordinate fetching
data[['latitude', 'longitude']] = data.apply(
    lambda row: pd.Series(get_coordinates(row['City'], row['Country'])), axis=1
)

# Save result
data.to_excel('players_with_coordinates_20250803.xlsx', sheet_name='players_20250803', index=False)
