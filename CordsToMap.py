import folium
from itertools import product
import math

# Basis-Koordinaten mit Platzhaltern
latitude_base = "50.27214"
longitude_base = "11.XX338"

# Ersetze 'l' durch '1' in der Longitude
longitude_base = longitude_base.replace('l', '1')

# Funktion, um alle möglichen Koordinaten zu generieren
def generate_coordinates(lat_base, lon_base):
    lat_placeholder_count = lat_base.count('X')
    lon_placeholder_count = lon_base.count('X')
    
    # Erzeuge alle möglichen Kombinationen für die Platzhalter
    combinations = product(range(10), repeat=lat_placeholder_count + lon_placeholder_count)
    
    coordinates = []
    for combo in combinations:
        lat_combo = list(lat_base)
        lon_combo = list(lon_base)
        
        # Ersetze die Platzhalter in der Latitude
        for i in range(lat_placeholder_count):
            lat_combo[lat_combo.index('X')] = str(combo[i])
        
        # Ersetze die Platzhalter in der Longitude
        for j in range(lon_placeholder_count):
            lon_combo[lon_combo.index('X')] = str(combo[lat_placeholder_count + j])
        
        # Füge die generierten Koordinaten zur Liste hinzu
        coordinates.append((float("".join(lat_combo)), float("".join(lon_combo))))
    
    return coordinates

# Generiere alle möglichen Koordinaten
coordinates = generate_coordinates(latitude_base, longitude_base)

# Anzahl der Punkte pro Karte
points_per_map = 2000

# Anzahl der benötigten Karten
num_maps = math.ceil(len(coordinates) / points_per_map)

# Erstelle mehrere Karten
for map_index in range(num_maps):
    # Berechne den Start- und Endindex für die Punkte dieser Karte
    start_index = map_index * points_per_map
    end_index = min(start_index + points_per_map, len(coordinates))
    
    # Erstelle eine Karte mit einem Startpunkt
    map_center = (50.27214, 11.13338)  # Grobe Mitte der Koordinaten
    mymap = folium.Map(location=map_center, zoom_start=10)
    
    # Füge die Punkte dieser Karte hinzu
    for coord in coordinates[start_index:end_index]:
        folium.CircleMarker(location=coord, popup=f"{coord[0]},{coord[1]}\n<a href=\"https://maps.google.de/maps?q={coord[0]},{coord[1]}&t=k\">Google</a>", radius=2, color='red').add_to(mymap)
    
    # Speichere die Karte in einer HTML-Datei
    map_filename = f"possible_points_map_{map_index + 1}.html"
    mymap.save(map_filename)
    print(f"Karte {map_index + 1} wurde erstellt und als '{map_filename}' gespeichert.")