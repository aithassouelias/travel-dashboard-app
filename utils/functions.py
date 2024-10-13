import folium
import openrouteservice
from datetime import datetime
from io import BytesIO
import requests
from utils.models import Users

def create_map_with_multiple_routes(pois: list, api_key: str):
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

    # Create a folium map centered at the first POI (temporary center)
    m = folium.Map(location=pois_sorted[0]['coords'][::-1], zoom_start=6, tiles='cartodbdark_matter', width='100%', height='400px')

    # List to collect all coordinates for fitting the map bounds
    all_coords = []

    # Check if there's only one POI
    if len(pois_sorted) == 1:
        single_poi = pois_sorted[0]
        folium.Marker(
            location=[single_poi['coords'][1], single_poi['coords'][0]],
            popup=f"{single_poi['name']}<br>{single_poi['date_time'].strftime('%Y-%m-%d %H:%M')}",
            icon=folium.DivIcon(html=f"""
                <div style="
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    width: 24px;
                    height: 24px;
                    border-radius: 50%;
                    background-color: #6973dc;
                    color: white;
                    font-weight: bold;
                    font-size: 14px;">1</div>
            """)
        ).add_to(m)
        m.fit_bounds([[single_poi['coords'][1], single_poi['coords'][0]]])
    else:
        # Create routes and markers for multiple POIs
        for i in range(len(pois_sorted) - 1):
            start_coords = pois_sorted[i]['coords']
            end_coords = pois_sorted[i + 1]['coords']
            try:
                # Request the route using the 'foot-walking' profile
                route = client.directions(coordinates=[start_coords, end_coords], profile='foot-walking', format='geojson')
                
                if 'features' in route and len(route['features']) > 0:
                    coordinates = route['features'][0]['geometry']['coordinates']
                    folium.PolyLine(locations=[(coord[1], coord[0]) for coord in coordinates], color="#6973dc", weight=2.5).add_to(m)

                    # Add markers for start and end points
                    for j, coord in enumerate([start_coords, end_coords]):
                        folium.Marker(
                            location=[coord[1], coord[0]],
                            popup=f"{pois_sorted[i + j]['name']}<br>{pois_sorted[i + j]['date_time'].strftime('%Y-%m-%d %H:%M')}",
                            icon=folium.DivIcon(html=f"""
                                <div style="
                                    display: flex;
                                    justify-content: center;
                                    align-items: center;
                                    width: 24px;
                                    height: 24px;
                                    border-radius: 50%;
                                    background-color: #6973dc;
                                    color: white;
                                    font-weight: bold;
                                    font-size: 14px;">{i + j + 1}</div>
                            """)
                        ).add_to(m)

                    # Collect all coordinates for fitting bounds
                    all_coords.extend([[start_coords[1], start_coords[0]], [end_coords[1], end_coords[0]]])

            except openrouteservice.exceptions.ApiError as e:
                print(f"API error: {e}")

        # Adjust the map to fit all the points and routes
        m.fit_bounds(all_coords)

    # Create a BytesIO object to hold the map HTML
    map_html = m._repr_html_()
    return map_html

def create_map_with_multiple_pois(locations: list):
    """
    Returns the HTML code of a folium map displaying POIs from the given locations.
    Each location is expected to be a tuple (name, coord, image_url).
    """

    # Create a map centered around the average of the provided locations
    m = folium.Map(zoom_start=4, min_zoom=3, max_bounds=True, tiles='cartodbdark_matter')

    # Add markers to the map
    for i, (name, coord) in enumerate(locations):
        
        popup_content = popup_content = name
        
        # Add marker with the custom popup
        folium.Marker(
            location=coord,
            popup=folium.Popup(popup_content, max_width=200),
            icon=folium.DivIcon(html=f"""
                <div style="
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    width: 24px;
                    height: 24px;
                    border-radius: 50%;
                    background-color: #6973dc;
                    color: white;
                    font-weight: bold;
                    font-size: 14px;">{i + 1}</div>
            """)
        ).add_to(m)

    # Calculate bounds to adjust the map automatically to fit all markers
    bounds = [
        [min(lat for lat, lon in locations), min(lon for lat, lon in locations)],
        [max(lat for lat, lon in locations), max(lon for lat, lon in locations)]
    ]

    # Fit the map to the bounds of the markers
    m.fit_bounds(bounds)

    # Return the HTML representation of the map
    return m._repr_html_()


def create_empty_map(lat, lon):
    """
    Returns the HTML code of an empty map centered around the given latitude and longitude.
    """
    # Créer une carte centrée sur les coordonnées spécifiées avec un zoom approprié
    m = folium.Map(location=[lat, lon], zoom_start=8, tiles='cartodbdark_matter', min_zoom=3, max_bounds=True)

    # Create a BytesIO object to hold the map HTML
    map_html = m._repr_html_()
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
    Returns location informations from latitude and longitude by calling OSM Reverse API
    """
    url = f"https://nominatim.openstreetmap.org/reverse?format=json&lat={lat}&lon={lon}&zoom=18&addressdetails=1&accept-language=fr"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Referer": "http://www.yourwebsite.com",
        "Accept-Language": "en-US,en;q=0.5"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return response
    
def get_pretty_location_infos(place_name : str):
    """
    Returns city, country and address type from a place name using OSM API and OSM REVERSE API
    """
    # API 
    lat,lon = get_coordinates(place_name)
    infos = get_location_info(lat, lon)

    address_type = infos["addresstype"]
    city = infos["address"]["city"]
    country = infos["address"]["country"]

    return [city, country, address_type, lat,lon]

def generate_username(email):
    # Extract username from email (before @ symbol)
    base_username = email.split('@')[0]

    # Check if the username already exists
    username = base_username
    count = 1

    # Keep appending numbers or random characters until the username is unique
    while Users.query.filter_by(username=username).first() is not None:
        username = f"{base_username}{count}"
        count += 1

    return username