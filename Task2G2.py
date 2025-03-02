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
    elif station.relative_water_level() > station.typical_range[1] * 1.5:
        return 'Severely above typical'
    else:
        return 'Within typical range'

def plot_stations_on_map():
    
    stations = build_station_list()
    update_water_levels(stations)
    
    ##Base map
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
            color = 'orange'
        elif status == 'Severely above typical':
            color = 'red'
        else:
            color = 'grey'

        ##Add the station marker
        folium.CircleMarker(
            location=station.coord,
            radius=8,
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.7,
            popup=f"{station.name} ({station.town or 'Unknown Town'})\n{status}"
        ).add_to(map_)
    
    ##Adding a legend
    legend_html = '''
    <div style="position: fixed; 
                bottom: 50px; left: 50px; width: 200px; height: 120px; 
                background-color: white; z-index:9999; padding: 10px;
                font-size: 14px; border: 2px solid grey; border-radius: 5px;">
        <b>Water Level Status</b><br>
        <i class="fa fa-circle" style="color:green"></i> Below typical<br>
        <i class="fa fa-circle" style="color:blue"></i> Within typical<br>
        <i class="fa fa-circle" style="color:orange"></i> Above typical<br>
        <i class="fa fa-circle" style="color:red"></i> Severely above<br>
        <i class="fa fa-circle" style="color:grey"></i> No data
    </div>
    '''
    map_.get_root().html.add_child(folium.Element(legend_html))
    
    ##Save the map to an HTML file, then open it in the browser
    map_.save("stations_map.html")
    print("Map saved as 'stations_map.html'")
    
    return "stations_map.html"

def display_map_in_browser():
    map_file = plot_stations_on_map()
    webbrowser.open(map_file)

def create_gui():
    root = tk.Tk()
    root.title("Flood Monitoring System")
    root.geometry("300x200")

    label = tk.Label(root, text="Flood Monitoring System", font=("Arial", 14))
    label.pack(pady=10)

    btn_display = tk.Button(root, text="Show Map", command=display_map_in_browser, height=2, width=15)
    btn_display.pack(pady=10)

    btn_exit = tk.Button(root, text="Exit", command=root.quit, height=2, width=15)
    btn_exit.pack(pady=10)

    root.mainloop()

# Start GUI
create_gui()
