from utils.functions import get_coordinates, get_location_info, get_pretty_location_infos, create_map_with_multiple_routes


pois = [
    {
        'name': 'Tour Eiffel',
        'coords': [2.2945, 48.8584],  # longitude, latitude
        'date_time': '2024-10-12 09:00'
    },
    {
        'name': 'Musée du Louvre',
        'coords': [2.3364, 48.8606],  # longitude, latitude
        'date_time': '2024-10-12 11:00'
    },
    {
        'name': 'Stade de France',
        'coords': [2.3601, 48.9245],  # longitude, latitude
        'date_time': '2024-10-12 13:00'
    },
    {
        'name': 'Parc des Princes',
        'coords': [2.252, 48.8414],  # longitude, latitude
        'date_time': '2024-10-12 16:00'
    }
]
api_key = '5b3ce3597851110001cf624859eadc08586440cca8901585be5744ea'
create_map_with_multiple_routes(pois,api_key)