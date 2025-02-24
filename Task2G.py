import tkinter as tk
from floodsystem.stationdata import build_station_list, update_water_levels
from floodsystem.risk import stations_by_risk_level

def update_display():
    stations = build_station_list()
    update_water_levels(stations)
    stations_by_risk = stations_by_risk_level(stations)

    listbox.delete(0, tk.END)

    for station in stations_by_risk[:20]:
        risk_label = station.readable_risk()
        risk_factor = round(station.flood_risk_factor, 3)
        station_info = f"{station.name} ({station.town or 'Unknown Town'}) - {risk_label} Risk | Factor: {risk_factor}"

        listbox.insert(tk.END, station_info)

        ##Colour code 
        if risk_label == "Very Severe":
            listbox.itemconfig(tk.END, {'fg': 'red'})
        if risk_label == "Severe":
            listbox.itemconfig(tk.END, {'fg': '#FF8C00'})
        elif risk_label == "High":
            listbox.itemconfig(tk.END, {'fg': 'orange'})
        elif risk_label == "Moderate":
            listbox.itemconfig(tk.END, {'fg': 'blue'})
        elif risk_label == "Low":
            listbox.itemconfig(tk.END, {'fg': 'green'})

##Create the main application window
root = tk.Tk()
root.title("Flood Warning System")
title_label = tk.Label(root, text="Top 20 High-Risk Flood Stations", font=("Arial", 14, "bold"))
title_label.pack(pady=10)

##Create a listbox to display station risks
listbox = tk.Listbox(root, width=80, height=20, font=("Arial", 12))
listbox.pack(pady=10)

##Refresh button to update data
refresh_button = tk.Button(root, text="Refresh Data", command=update_display, font=("Arial", 12))
refresh_button.pack(pady=10)

update_display()

root.mainloop()
