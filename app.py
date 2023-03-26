import requests
import time
from geopy.geocoders import Nominatim
import folium

def get_iss_location():
    response = requests.get("http://api.open-notify.org/iss-now.json")
    data = response.json()
    lat, lon = float(data["iss_position"]["latitude"]), float(data["iss_position"]["longitude"])
    return lat, lon

def lat_lon_to_address(lat, lon):
    geolocator = Nominatim(user_agent="iss_tracker")
    location = geolocator.reverse(f"{lat}, {lon}")
    return location.address

def display_iss_location(lat, lon, address):
    iss_map = folium.Map(location=[lat, lon], zoom_start=5)
    folium.Marker([lat, lon], popup=f"ISS\n{address}").add_to(iss_map)
    return iss_map

update_interval = 10  # seconds

while True:
    lat, lon = get_iss_location()
    address = lat_lon_to_address(lat, lon)
    iss_map = display_iss_location(lat, lon, address)
    iss_map.save("iss_tracker.html")
    time.sleep(update_interval)
