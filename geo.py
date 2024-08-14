import pandas as pd
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter

# Load the data
# Load the data
data = pd.read_excel('players.xlsx', sheet_name='players')

# Initialize the geolocator
geolocator = Nominatim(user_agent="geoapiExercises")
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)

# Function to get coordinates
def get_coordinates(city, country):
    try:
        location = geolocator.geocode(f"{city}, {country}")
        if location:
            return location.latitude, location.longitude
        else:
            return None, None
    except:
        return None, None

# Add latitude and longitude to the dataframe
data[['latitude', 'longitude']] = data.apply(lambda row: pd.Series(get_coordinates(row['City'], row['Country'])), axis=1)

# Save the updated data to a new Excel file
data.to_excel('players_with_coordinates.xlsx', sheet_name='players.csv', index=False)
