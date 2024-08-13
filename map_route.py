import folium
import openrouteservice
from openrouteservice import convert
import json

# Function to create a map with a route between two points
def create_map_with_route(start_coords, end_coords, api_key):
    # Initialize the client with your API key
    client = openrouteservice.Client(key=api_key)

    try:
        # Request the route using the 'foot-walking' profile
        route = client.directions(coordinates=[start_coords, end_coords], profile='foot-walking', format='geojson')

        # Check if the 'features' key is in the response and contains data
        if 'features' in route and len(route['features']) > 0:
            geometry = route['features'][0]['geometry']
            coordinates = geometry['coordinates']

            # Create a folium map centered at the starting point with the custom style
            m = folium.Map(location=start_coords, zoom_start=14, tiles='cartodbdark_matter')

            distance_meters = route['features'][0]['properties']['segments'][0]['distance']
            distance_kilometers = distance_meters / 1000

            # Print the distance in kilometers
            print(f"Distance between the points: {distance_kilometers:.2f} km")
            # Add the route to the map
            folium.PolyLine(locations=[(coord[1], coord[0]) for coord in coordinates], color="#FFD700", weight=2.5, opacity=1, smooth_factor=3).add_to(m)

            # Add markers for start and end points with custom icons
            folium.Marker(
                location=[start_coords[1], start_coords[0]],
                popup="Start",
                icon=folium.Icon(icon="glyphicon glyphicon-heart", color="black", icon_color="#FFD700")
            ).add_to(m)

            folium.Marker(
                location=[end_coords[1], end_coords[0]],
                popup="End",
                icon=folium.Icon(icon="glyphicon glyphicon-heart", color="black", icon_color="#FFD700")
            ).add_to(m)

            # Save the map to an HTML file
            m.save('route_map.html')

            print("Map with route created successfully. Check 'route_map.html'.")

        else:
            print("No features found in API response.")

    except openrouteservice.exceptions.ApiError as e:
        print(f"API error: {e}")

# Example usage
start_coords = (2.2945, 48.8584)  # Example: Eiffel Tower
end_coords = (2.3376, 48.8606)    # Example: Louvre Museum
api_key = '5b3ce3597851110001cf624859eadc08586440cca8901585be5744ea'  # Replace with your OpenRouteService API key

create_map_with_route(start_coords, end_coords, api_key)
