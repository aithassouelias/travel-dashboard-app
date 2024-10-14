from utils.functions import get_coordinates, get_location_info, get_pretty_location_infos, create_map_with_multiple_routes

lat, lon = get_coordinates("Parc des princes")
print(get_location_info(lat, lon))