from utils.functions import get_coordinates, get_location_info

coordinates = get_coordinates("hotel argana agadir")

print(get_location_info(coordinates[0], coordinates[1]))