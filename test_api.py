import requests
import pandas as pd
from utils.functions import get_coordinates
# URL de l'API Overpass
overpass_url = "http://overpass-api.de/api/interpreter"

lat, lon = get_coordinates("Londres")

overpass_query = f"""
[out:json];
node
  [tourism=attraction]
  (around:6000,{lat},{lon});
out body;
"""

# Faire la requête GET
response = requests.get(overpass_url, params={'data': overpass_query})

# Vérifier le statut de la réponse
if response.status_code == 200:
    data = response.json()
    print(data)
    
    # Analyser les résultats
    if 'elements' in data and len(data['elements']) > 0:
        for element in data['elements']:
            if 'tags' in element:
                tags = element['tags']
                print(f"Nom : {tags.get('name', 'Inconnu')} - Accessibilité : {tags.get('wheelchair', 'Pas d\'information sur l\'accessibilité.')}")
    else:
        print("Aucun élément trouvé pour ce lieu.")
else:
    print(f"Erreur lors de la requête : {response.status_code}, Message : {response.text}")
