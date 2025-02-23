import folium
import tkinter as tk
import webbrowser
from floodsystem.stationdata import build_station_list, update_water_levels

def classify_station(station):
    if station.latest_level is None:
        return 'No data'
    elif station.relative_water_level() is None:
        return 'No data'
    elif station.relative_water_level() < station.typical_range[0]:
        return 'Below typical range'
    elif station.relative_water_level() > station.typical_range[1]:
        return 'Above typical range'
    else:
        return 'Within typical range'

def plot_stations_on_map():
    
    stations = build_station_list()
    update_water_levels(stations)
    
    ##Base mao
    map_center = [52.205281, 0.109238]
    map_ = folium.Map(location=map_center, zoom_start=6)

    ##Loop through stations and plot with colours
    for station in stations:
        status = classify_station(station)
        if status == 'Below typical range':
            color = 'green'
        elif status == 'Within typical range':
            color = 'blue'
        elif status == 'Above typical range':
            color = 'red'
        else:
            color = 'grey'

        ##Add the station marker
        folium.CircleMarker(
            location=station.coord,
            radius=6,
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.7,
            popup=f"{station.name} ({station.town or 'Unknown Town'})\n{status}"
        ).add_to(map_)

    ##Save the map to an HTML file, then open it in the browser
    map_.save("stations_map.html")
    print("Map saved as 'stations_map.html'")

    return "stations_map.html"

def display_map_in_browser():
    map_file = plot_stations_on_map()
    webbrowser.open(map_file)

display_map_in_browser()
