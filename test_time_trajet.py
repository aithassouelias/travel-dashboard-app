import openrouteservice
from datetime import datetime

def get_route_time(start_coords, end_coords, profile, api_key):
    # Initialize the client with your API key
    client = openrouteservice.Client(key=api_key)
    
    try:
        # Request the route using the specified profile
        route = client.directions(coordinates=[start_coords, end_coords], profile=profile, format='geojson')
        
        # Extract the duration for this segment (in seconds)
        duration_seconds = route['features'][0]['properties']['segments'][0]['duration']
        duration_minutes = duration_seconds / 60
        duration_hours = duration_minutes / 60
        return duration_hours
    
    except openrouteservice.exceptions.ApiError as e:
        print(f"API error: {e}")
        return None

# Example usage
start_coords = (6.1751, 49.1193)  # Metz
end_coords = (2.1734, 41.3851)    # Barcelone
api_key = '5b3ce3597851110001cf624859eadc08586440cca8901585be5744ea'  # Replace with your OpenRouteService API key

profiles = ['driving-car', 'cycling-regular', 'foot-walking']

for profile in profiles:
    duration = get_route_time(start_coords, end_coords, profile, api_key)
    if duration is not None:
        print(f"Time of travel by {profile.replace('-', ' ')}: {duration:.2f} minutes")
