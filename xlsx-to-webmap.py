# Python-Skript zur Visualisierung von Milpa-Standorte auf einer Deutschlandkarte
# Pipeline von Excel-Datei zu interaktiver HTML-Karte
# Basiert auf dem folgenden Tutorial: https://melaniewalsh.github.io/Intro-Cultural-Analytics/07-Mapping/01-Mapping.html

from geopy.geocoders import Nominatim
import folium
import pandas as pd

# Einlesen der Excel-Datei mit Milpa-Standorten in einen DataFrame 'milpa_df'
milpa_df = pd.read_excel("files/milpa-netzwerk.xlsx", sheet_name="Standorte")

# Initialisierung des Geolocators mit Nominatim (https://geopy.readthedocs.io/en/stable/)
geolocator = Nominatim(user_agent="Milpa Netzwerk", timeout=2)

# Funktion zur Geokodierung der Adressen
def find_location(row):
    address = row['Adresse']
    location = geolocator.geocode(address)
    if location != None:
        return location.latitude, location.longitude, location.address, location.raw['importance']
    else:
        return "Not Found", "Not Found", "Not Found", "Not Found"

# Anwenden der Geokodierungsfunktion auf den DataFrame 'milpa_df'
milpa_df[['Länge', 'Breite', 'Nominatim Adresse', 'Nominatim Wichtigkeit']] = milpa_df.apply(find_location, axis="columns", result_type="expand")
print(milpa_df[['Ort', 'Adresse', 'Länge', 'Breite']]) # Ausgabe der gefundenen Standorte

# Erstellen einer Deutschlandkarte mit Folium
germany_map = folium.Map(
    location=[51.1657, 10.4515], # Geographische Mitte Deutschlands
    tiles="Stadia.Outdoors", # Weitere verfügbare Tiles auf https://leaflet-extras.github.io/leaflet-providers/preview/
    zoom_start=6,
    min_zoom=6,
    min_lat=47.2, # Südgrenze Deutschlands
    max_lat=55.1, # Nordgrenze Deutschlands
    min_lon=5.8, # Westgrenze Deutschlands
    max_lon=15.1, # Ostgrenze Deutschlands
    max_bounds=True # Verhindert das Verschieben der Karte über die Grenzen hinaus
)

# Funktion zum Hinzufügen von Markern auf der Karte
def create_map_markers(row, map_name):
    folium.Marker(
        location=[row['Länge'], row['Breite']],
        tooltip=row['Ort'],
        popup=row['Adresse'],
        icon=folium.Icon(color="darkgreen", icon="seedling", prefix='fa') # Icons aus: https://fontawesome.com/icons
    ).add_to(map_name)

# Anwenden der Marker-Erstellungsfunktion auf die gefundene Standorte
marker_locations = milpa_df[milpa_df['Nominatim Adresse'] != "Not Found"]
marker_locations.apply(create_map_markers, axis="columns", map_name=germany_map)

# Speichern der interaktiven Karte als HTML-Datei
germany_map.save("website/germany_map.html")


"""
Unused code for reference:
milpa_df = pd.read_csv("C:/Users/Luis0/Documents/milpa-netzwerk.csv", delimiter=",")
location = geolocator.geocode(milpa_df.at[1, 'Adresse'])

Pro tip: print(location) == print(location.address)!!
"""