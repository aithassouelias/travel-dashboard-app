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