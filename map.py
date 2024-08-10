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


# Liste des points d'intérêt à Paris avec leur nom et coordonnées GPS
locations = [
    ("Tour Eiffel", [48.8584, 2.2945]),
    ("Musée du Louvre", [48.8606, 2.3376]),
    ("Cathédrale Notre-Dame", [48.8529, 2.3500]),
    ("Montmartre - Sacré-Cœur", [48.8867, 2.3431]),
    ("Arc de Triomphe", [48.8738, 2.2950])
]

# Extraire les coordonnées de chaque lieu
coordinates = [loc[1] for loc in locations]

# Calculer les limites géographiques des points
bounds = [[min(lat for lat, lon in coordinates), min(lon for lat, lon in coordinates)],
          [max(lat for lat, lon in coordinates), max(lon for lat, lon in coordinates)]]

# Créer la carte avec le fond souhaité
map_details = folium.Map(tiles='cartodbdark_matter')

# Ajouter des marqueurs pour chaque point d'intérêt
for location in locations: 
    folium.Marker(
        location=location[1],
        popup=location[0],
        icon=folium.Icon(icon="glyphicon glyphicon-heart", color="black", icon_color="#FFD700"),
    ).add_to(map_details)

# Ajuster le zoom et le centrage de la carte pour inclure tous les points
map_details.fit_bounds(bounds)

# Optionnel: ajuster manuellement le zoom si nécessaire
map_details.options['zoom'] = 15  # Exemple: augmenter le zoom pour cadrer de plus près

# Enregistrer la carte en tant que fichier HTML
map_details.save('map_details.html')
