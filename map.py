import folium

# Créer une carte sans spécifier de coordonnées initiales
m = folium.Map(zoom_start=4, min_zoom=3, max_bounds=True)

locations = [
    ("Tour Eiffel, Paris", [48.8584, 2.2945]),
    ("Londres", [51.5074, -0.1278]),
    ("Marrakech", [31.6295, -7.9811]),
    ("Stade Vélodrome, Marseille", [43.2699, 5.3958]),
    ("Bordeaux", [44.8378, -0.5792])
]

# Extraire les coordonnées de toutes les localisations
coordinates = [loc[1] for loc in locations]

# Ajouter les marqueurs à la carte
for i, location in enumerate(locations):
    folium.Marker(
        location=location[1],
        popup=location[0],
        icon=folium.DivIcon(html=f"""
            <div style="
                display: flex;
                justify-content: center;
                align-items: center;
                width: 24px;
                height: 24px;
                border-radius: 50%;
                background-color: white;
                color: purple;
                font-weight: bold;
                font-size: 14px;">
                {i + 1}
            </div>
        """)
    ).add_to(m)

# Calculer les limites (bounds) pour ajuster automatiquement la carte
bounds = [
    [min(lat for lat, lon in coordinates), min(lon for lat, lon in coordinates)],
    [max(lat for lat, lon in coordinates), max(lon for lat, lon in coordinates)]
]

# Ajuster la carte pour qu'elle corresponde aux limites des marqueurs
m.fit_bounds(bounds)

# Enregistrer la carte en tant que fichier HTML
m.save('map.html')
