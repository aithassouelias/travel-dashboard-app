import folium

# Créer une carte centrée sur une latitude et une longitude spécifiques
m = folium.Map(location=[45.5236, -122.6750], zoom_start=13, tiles='cartodbdark_matter')

# Ajouter un marqueur
folium.Marker(
    location=[45.5236, -122.6750],
    icon=folium.Icon(icon="glyphicon glyphicon-heart", color="black", icon_color="#FFD700"),
).add_to(m)

# Enregistrer la carte en tant que fichier HTML
m.save('map.html')