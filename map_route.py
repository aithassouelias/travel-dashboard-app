import folium
import openrouteservice
from datetime import datetime

# Function to create a map with routes between multiple points, sorted by date and time
def create_map_with_multiple_routes(pois, api_key):
    # Initialize the client with your API key
    client = openrouteservice.Client(key=api_key)
    
    # Convert POIs dates to datetime objects for sorting
    for poi in pois:
        poi['date_time'] = datetime.strptime(poi['date_time'], '%Y-%m-%d %H:%M')

    # Sort POIs by date and time
    pois_sorted = sorted(pois, key=lambda x: x['date_time'])

    total_distance = 0

    # Create a folium map centered at the first POI
    start_coords = pois_sorted[0]['coords']
    m = folium.Map(location=start_coords, zoom_start=6, tiles='cartodbdark_matter')

    # Iterate over POIs to create routes between consecutive points
    for i in range(len(pois_sorted) - 1):
        start_coords = pois_sorted[i]['coords']
        end_coords = pois_sorted[i + 1]['coords']
        try:
            # Request the route using the 'foot-walking' profile
            route = client.directions(coordinates=[start_coords, end_coords], profile='foot-walking', format='geojson')
            
            # Check if the 'features' key is in the response and contains data
            if 'features' in route and len(route['features']) > 0:
                geometry = route['features'][0]['geometry']
                coordinates = geometry['coordinates']
                
                # Extract the distance for this segment
                distance_meters = route['features'][0]['properties']['segments'][0]['distance']
                distance_kilometers = distance_meters / 1000
                total_distance += distance_kilometers

                # Add the route to the map
                folium.PolyLine(locations=[(coord[1], coord[0]) for coord in coordinates], color="#FFD700", weight=2.5, opacity=1, smooth_factor=3).add_to(m)

                # Add markers for start and end points with custom circle icons and numbered labels
                folium.Marker(
                    location=[start_coords[1], start_coords[0]],
                    popup=f"{pois_sorted[i]['name']}<br>{pois_sorted[i]['date_time'].strftime('%Y-%m-%d %H:%M')}",
                    icon=folium.DivIcon(html=f"""
                        <div style="
                            display: flex;
                            justify-content: center;
                            align-items: center;
                            width: 24px;
                            height: 24px;
                            border-radius: 50%;
                            background-color: black;
                            color: gold;
                            font-weight: bold;
                            font-size: 14px;">
                            {i + 1}
                        </div>
                    """)
                ).add_to(m)

                folium.Marker(
                    location=[end_coords[1], end_coords[0]],
                    popup=f"{pois_sorted[i + 1]['name']}<br>{pois_sorted[i + 1]['date_time'].strftime('%Y-%m-%d %H:%M')}",
                    icon=folium.DivIcon(html=f"""
                        <div style="
                            display: flex;
                            justify-content: center;
                            align-items: center;
                            width: 24px;
                            height: 24px;
                            border-radius: 50%;
                            background-color: black;
                            color: gold;
                            font-weight: bold;
                            font-size: 14px;">
                            {i + 2}
                        </div>
                    """)
                ).add_to(m)

            else:
                print(f"No features found for route from {pois_sorted[i]['name']} to {pois_sorted[i + 1]['name']}.")

        except openrouteservice.exceptions.ApiError as e:
            print(f"API error: {e}")

    # Save the map to an HTML file
    m.save('./static/route_map.html')

    # Print the total distance in kilometers
    print(f"Total distance between the points: {total_distance:.2f} km")

# Example usage
pois = [
    {'name': 'Tour Eiffel', 'coords': (2.2945, 48.8584), 'date_time': '2024-08-13 10:00'},
    {'name': 'Musée du Louvre', 'coords': (2.3376, 48.8606), 'date_time': '2024-08-13 14:00'},
    {'name': 'Cathédrale Notre-Dame', 'coords': (2.3499, 48.8529), 'date_time': '2024-08-14 10:00'},
    {'name': 'Champs-Élysées', 'coords': (2.3076, 48.8738), 'date_time': '2024-08-15 10:00'},
    {'name': 'Montmartre', 'coords': (2.3430, 48.8867), 'date_time': '2024-08-15 16:00'},
    {'name': 'Musée d\'Orsay', 'coords': (2.3250, 48.8599), 'date_time': '2024-08-16 10:00'},
    {'name': 'Palais Garnier', 'coords': (2.3319, 48.8719), 'date_time': '2024-08-17 10:00'},
    {'name': 'Jardin du Luxembourg', 'coords': (2.3372, 48.8462), 'date_time': '2024-08-18 10:00'}
]

api_key = '5b3ce3597851110001cf624859eadc08586440cca8901585be5744ea'  # Replace with your OpenRouteService API key

create_map_with_multiple_routes(pois, api_key)
