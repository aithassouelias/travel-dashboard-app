import folium

# Créer une carte centrée sur une latitude et une longitude spécifiques
m = folium.Map(zoom_start=13, tiles='cartodbdark_matter')

locations = [
    ("Tour Eiffel, Paris", [48.8584, 2.2945]),
    ("Londres", [51.5074, -0.1278]),
    ("Marrakech", [31.6295, -7.9811]),
    ("Stade Vélodrome, Marseille", [43.2699, 5.3958]),
    ("Bordeaux", [44.8378, -0.5792])
]

for location in locations: 
    # Ajouter un marqueur
    folium.Marker(
        location=location[1],
        popup=location[0],
        icon=folium.Icon(icon="glyphicon glyphicon-heart", color="black", icon_color="#FFD700"),
    ).add_to(m)

# Enregistrer la carte en tant que fichier HTML
m.save('map.html')


import openrouteservice
from openrouteservice import convert

# Remplace par ta propre clé API OpenRouteService
client = openrouteservice.Client(key='5b3ce3597851110001cf624859eadc08586440cca8901585be5744ea')

# Définir deux points pour un test simple (Tour Eiffel -> Musée du Louvre)
start = [6.1751, 49.1193]  # Metz
end = [-6.9147, 30.9280]   # Ouarzazate


# Calculer l'itinéraire entre ces deux points
try:
    route = client.directions(coordinates=[start, end], profile='foot-walking', format='geojson')
    print(route)  # Affiche la réponse de l'API pour diagnostic
except openrouteservice.exceptions.ApiError as e:
    print(f"API Error: {e}")
except Exception as e:
    print(f"Unexpected Error: {e}")

# Si la réponse contient bien 'routes', continuer
if 'routes' in route:
    # Décoder l'itinéraire pour folium
    geometry = route['routes'][0]['geometry']
    route_coords = convert.decode_polyline(geometry)

    # Créer la carte
    map_details = folium.Map(location=[48.8584, 2.2945], zoom_start=13, tiles='cartodbdark_matter')

    # Ajouter des marqueurs pour les deux points
    folium.Marker(location=[48.8584, 2.2945], popup='Tour Eiffel').add_to(map_details)
    folium.Marker(location=[48.8606, 2.3376], popup='Musée du Louvre').add_to(map_details)

    # Tracer l'itinéraire
    folium.PolyLine(route_coords['coordinates'], color="blue", weight=5, opacity=0.7).add_to(map_details)

    # Enregistrer la carte
    map_details.save('map_details.html')
else:
    print("No routes found in API response.")
