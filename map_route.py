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
    print(pois_sorted)
    total_distance = 0

    # Create a folium map centered at the first POI (temporary center)
    start_coords = pois_sorted[0]['coords']
    m = folium.Map(location=start_coords, zoom_start=6, tiles='cartodbdark_matter')

    # List to collect all coordinates for fitting the map bounds
    all_coords = []

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

                # Add the start and end coordinates to the list for fitting bounds
                all_coords.append([start_coords[1], start_coords[0]])
                all_coords.append([end_coords[1], end_coords[0]])

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

    # Adjust the map to fit all the points and routes
    m.fit_bounds(all_coords)

    # Save the map to an HTML file
    m.save('./static/route_map.html')

