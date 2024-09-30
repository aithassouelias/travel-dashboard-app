import folium

# Create a map without specifying initial coordinates
m = folium.Map(zoom_start=4, min_zoom=3, max_bounds=True)

locations = [
    ("Tour Eiffel, Paris", [48.8584, 2.2945], './static/images/destinations/Paris.jpg'),  # Image of Paris
    ("Londres", [51.5074, -0.1278], None),
    ("Marrakech", [31.6295, -7.9811], None),
    ("Stade Vélodrome, Marseille", [43.2699, 5.3958], None),
    ("Bordeaux", [44.8378, -0.5792], None)
]

# Extract coordinates of all locations
coordinates = [loc[1] for loc in locations]

# Add markers to the map
for i, (name, coord, image_url) in enumerate(locations):
    if image_url:
        # Add image and custom HTML for Paris marker
        popup_content = f"""
        <div style="text-align: center;">
            <img src="{image_url}" width="150" height="100"><br>
            <strong>Tour Eiffel</strong><br>
            <span style="color: gray;">Paris, France</span>
        </div>
        """
    else:
        # Default popup content without image
        popup_content = name
    
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
                background-color: white;
                color: purple;
                font-weight: bold;
                font-size: 14px;">
                {i + 1}
            </div>
        """)
    ).add_to(m)

# Calculate bounds to adjust the map automatically to fit all markers
bounds = [
    [min(lat for lat, lon in coordinates), min(lon for lat, lon in coordinates)],
    [max(lat for lat, lon in coordinates), max(lon for lat, lon in coordinates)]
]

# Fit the map to the bounds of the markers
m.fit_bounds(bounds)

# Save the map to an HTML file
m.save('map.html')
