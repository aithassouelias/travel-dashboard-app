import folium
import openrouteservice
from datetime import datetime
from io import BytesIO
import requests

def create_map_with_multiple_routes(pois : list, api_key : str):
    """
    Returns the HTML code of a folium map displaying POIs from POIs and api_key
    """
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

   # Create a BytesIO object to hold the map HTML
    map_io = BytesIO()
    m.save(map_io, close_file=False)
    map_html = map_io.getvalue().decode()

    return map_html

def create_empty_map():
    """
    Returns the HTML code of an empty Map
    """
    # Créer une carte sans spécifier de coordonnées initiales
    m = folium.Map(zoom_start=4, tiles='cartodbdark_matter', min_zoom=3, max_bounds=True)

    map_io = BytesIO()
    m.save(map_io, close_file=False)
    map_html = map_io.getvalue().decode()

    return map_html

def get_coordinates(place_name : str):
    """
    Returns latitude and longitude from a place name by calling OSM API
    """
    url = f"https://nominatim.openstreetmap.org/search?q={place_name}&format=json"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Referer": "http://www.yourwebsite.com",
        "Accept-Language": "en-US,en;q=0.5"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        if data:
            latitude = float(data[0]['lat'])
            longitude = float(data[0]['lon'])
            return [latitude, longitude]
        else:
            return [None, None]
    return [None, None]

def get_location_info(lat : float, lon : float):
    """
    Returns Country & City names from latitude and longitude by calling OSM Reverse API
    """
    url = f"https://nominatim.openstreetmap.org/reverse?format=json&lat={lat}&lon={lon}&zoom=10&addressdetails=1"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Referer": "http://www.yourwebsite.com",
        "Accept-Language": "en-US,en;q=0.5"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        address = data.get('address', {})
        city = address.get('city', address.get('town', address.get('village', '')))
        country = address.get('country', '')
        return [city, country]
    else:
        return [None, None]