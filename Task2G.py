import tkinter as tk
from floodsystem.stationdata import build_station_list, update_water_levels
from floodsystem.risk import towns_by_risk_level

def update_display():
    stations = build_station_list()
    update_water_levels(stations)
    towns_by_risk = towns_by_risk_level(stations)

    listbox.delete(0, tk.END)

    for town, risk_factor in towns_by_risk[:20]:
        risk_label = readable_risk(risk_factor)
        town_info = f"{town} - {risk_label} Risk | Factor: {round(risk_factor, 3)}"

        listbox.insert(tk.END, town_info)

        ## Colour code
        if risk_label == "Very Severe":
            listbox.itemconfig(tk.END, {'fg': 'red'})
        elif risk_label == "Severe":
            listbox.itemconfig(tk.END, {'fg': '#FF8C00'})
        elif risk_label == "High":
            listbox.itemconfig(tk.END, {'fg': 'orange'})
        elif risk_label == "Moderate":
            listbox.itemconfig(tk.END, {'fg': 'blue'})
        elif risk_label == "Low":
            listbox.itemconfig(tk.END, {'fg': 'green'})

def readable_risk(factor):
    """Converts numerical risk factor to a readable category."""
    if factor > 2.5:
        return "Very Severe"
    elif factor > 2.0:
        return "Severe"
    elif factor > 1.5:
        return "High"
    elif factor > 1.0:
        return "Moderate"
    else:
        return "Low"

## Create the main application window
root = tk.Tk()
root.title("Flood Warning System")
title_label = tk.Label(root, text="Top 20 High-Risk Towns", font=("Arial", 14, "bold"))
title_label.pack(pady=10)

## Create a listbox to display town risks
listbox = tk.Listbox(root, width=80, height=20, font=("Arial", 12))
listbox.pack(pady=10)

## Refresh button to update data
refresh_button = tk.Button(root, text="Refresh Data", command=update_display, font=("Arial", 12))
refresh_button.pack(pady=10)

update_display()

root.mainloop()
