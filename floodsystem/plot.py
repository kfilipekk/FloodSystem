import matplotlib.pyplot as plt
import datetime
from .datafetcher import fetch_measure_levels

def plot_water_levels(station,dates,levels):
    plt.plot(dates,levels)
    plt.xlabel('date')
    plt.ylabel('water level (m)')
    plt.xticks(rotation=45)
    plt.title({station.name})

    plt.tight_layout()
    plt.show()



#fig, axes = plt.subplots(1, 2, figsize=(10, 4))  # 1 row, 2 columns




