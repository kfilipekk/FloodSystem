import folium
import tkinter as tk
from tkinter import ttk, messagebox
import webbrowser
from floodsystem.stationdata import build_station_list, update_water_levels
import folium.plugins
import threading

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

def plot_stations_on_map(radius=8, show_heatmap=False, tiles="OpenStreetMap"):
    stations = build_station_list()
    update_water_levels(stations)
    
    ##Base map
    map_center = [52.205281, 0.109238]
    map_ = folium.Map(location=map_center, zoom_start=6, tiles=tiles)
    
    ## Feature groups for layer control
    marker_group = folium.FeatureGroup(name="Station Markers")
    heatmap_group = folium.FeatureGroup(name="Water Level Heatmap")

    ##Loop through stations and plot with colours
    coordinates = []
    for station in stations:
        status = classify_station(station)
        if status == 'Below typical range':
            color, weight = 'green', 0.5
        elif status == 'Within typical range':
            color, weight = 'blue', 1
        elif status == 'Above typical range':
            color, weight = 'orange', 1.5
        elif status == 'Severely above typical':
            color, weight = 'red', 2
        else:
            color, weight = 'grey', 0.1

        ##Add the station marker
        folium.CircleMarker(
            location=station.coord,
            radius=radius,
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.7,
            popup=folium.Popup(f"""
                <b>{station.name}</b><br>
                Town: {station.town or 'Unknown'}<br>
                Status: {status}<br>
                Level: {station.latest_level or 'N/A'} m<br>
                Typical: {station.typical_range or 'N/A'}
            """, max_width=250)
        ).add_to(marker_group)
        
        if station.latest_level:
            coordinates.append([station.coord[0], station.coord[1], weight])

    ## Add heatmap if selected
    if show_heatmap and coordinates:
        folium.plugins.HeatMap(
            coordinates,
            radius=15,
            blur=20
        ).add_to(heatmap_group)

    ##Add groups to map
    marker_group.add_to(map_)
    heatmap_group.add_to(map_)
    
    ##Adding a larger legend with more info
    legend_html = '''
    <div style="position: fixed; 
                bottom: 50px; left: 50px; width: 280px; height: 180px; 
                background-color: rgba(255, 255, 255, 0.9); z-index:9999; padding: 15px;
                font-size: 14px; border: 2px solid grey; border-radius: 5px; box-shadow: 2px 2px 5px rgba(0,0,0,0.3);">
        <b>Water Level Status Legend</b><br><br>
        <i class="fa fa-circle" style="color:green"></i> Below typical range<br>
        <i class="fa fa-circle" style="color:blue"></i> Within typical range<br>
        <i class="fa fa-circle" style="color:orange"></i> Above typical range<br>
        <i class="fa fa-circle" style="color:red"></i> Severely above typical<br>
        <i class="fa fa-circle" style="color:grey"></i> No data available
    </div>
    '''
    map_.get_root().html.add_child(folium.Element(legend_html))
    
    ## Add layer control
    folium.LayerControl().add_to(map_)
    
    ## Add minimap
    folium.plugins.MiniMap().add_to(map_)
    
    ## Add measurement tool
    folium.plugins.MeasureControl().add_to(map_)
    
    ##Save the map to an HTML file
    map_.save("stations_map.html")
    print("Map saved as 'stations_map.html'")
    
    return "stations_map.html"

def display_map_in_browser():
    map_file = plot_stations_on_map(
        radius=radius_scale.get(),
        show_heatmap=heatmap_var.get(),
        tiles=tiles_var.get()
    )
    webbrowser.open(map_file)

def create_gui():
    root = tk.Tk()
    root.title("Flood Monitoring System")
    root.geometry("400x600")
    root.configure(bg="#f0f0f0")

    ##Title Frame
    title_frame = tk.Frame(root, bg="#f0f0f0")
    title_frame.pack(pady=10)
    tk.Label(title_frame, text="Flood Monitoring System", 
             font=("Arial", 16, "bold"), bg="#f0f0f0").pack()

    ##Main Buttons Frame
    btn_frame = tk.Frame(root, bg="#f0f0f0")
    btn_frame.pack(pady=20)
    
    btn_display = tk.Button(btn_frame, text="Show Map", 
                           command=lambda: threading.Thread(target=display_map_in_browser).start(),
                           height=2, width=20, bg="#4CAF50", fg="white", 
                           font=("Arial", 10, "bold"))
    btn_display.pack(pady=10)

    btn_refresh = tk.Button(btn_frame, text="Refresh Data", 
                           command=lambda: threading.Thread(target=plot_stations_on_map).start(),
                           height=2, width=20, bg="#2196F3", fg="white",
                           font=("Arial", 10, "bold"))
    btn_refresh.pack(pady=10)

    ##Customization Frame
    custom_frame = tk.LabelFrame(root, text="Map Customization", 
                               font=("Arial", 11), bg="#f0f0f0", padx=10, pady=10)
    custom_frame.pack(pady=10, padx=10, fill="x")

    ##Marker Size Slider
    global radius_scale
    tk.Label(custom_frame, text="Marker Size:", bg="#f0f0f0").pack()
    radius_scale = tk.Scale(custom_frame, from_=5, to=15, orient="horizontal",
                           bg="#f0f0f0", length=200)
    radius_scale.set(8)
    radius_scale.pack(pady=5)

    ##Heatmap Toggle
    global heatmap_var
    heatmap_var = tk.BooleanVar()
    tk.Checkbutton(custom_frame, text="Show Heatmap", variable=heatmap_var,
                  bg="#f0f0f0").pack(pady=5)

    #Map Style Dropdown
    global tiles_var
    tk.Label(custom_frame, text="Map Style:", bg="#f0f0f0").pack()
    tiles_var = tk.StringVar(value="OpenStreetMap")
    tiles_options = ["OpenStreetMap", "Stamen Terrain", "CartoDB Positron"]
    ttk.Combobox(custom_frame, textvariable=tiles_var, 
                values=tiles_options, state="readonly").pack(pady=5)

    ##Status Frame
    status_frame = tk.Frame(root, bg="#f0f0f0")
    status_frame.pack(pady=10)
    status_label = tk.Label(status_frame, text="Ready", bg="#f0f0f0",
                           font=("Arial", 10))
    status_label.pack()

    ##Exit Button
    btn_exit = tk.Button(root, text="Exit", command=root.quit,
                        height=2, width=20, bg="#f44336", fg="white",
                        font=("Arial", 10, "bold"))
    btn_exit.pack(pady=20)

    ##Menu Bar
    menubar = tk.Menu(root)
    root.config(menu=menubar)
    file_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="File", menu=file_menu)
    file_menu.add_command(label="Save Map", command=lambda: messagebox.showinfo("Save", "Map saved as stations_map.html"))
    file_menu.add_separator()
    file_menu.add_command(label="Exit", command=root.quit)

    help_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Help", menu=help_menu)
    help_menu.add_command(label="About", command=lambda: messagebox.showinfo(
        "About", "Flood Monitoring System\nVersion 2.0\nBuilt with Python & Folium"))

    root.mainloop()
    
if __name__ == "__main__":
    create_gui()