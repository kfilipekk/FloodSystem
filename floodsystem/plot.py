import matplotlib.pyplot as plt
from .datafetcher import fetch_measure_levels
from .analysis import polyfit
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


def plot_water_levels(station,dates,levels):
    plt.plot(dates,levels)
    plt.xlabel('date')
    plt.ylabel('water level (m)')
    plt.xticks(rotation=45)
    plt.title({station.name})

    plt.legend()
    plt.tight_layout()
    plt.show()


def plot_water_level_with_fit(station, dates, levels, p):

    dates_num = mdates.date2num(dates)
    ##Calculate the polynomial fit from analysis.py
    poly, d0 = polyfit(dates, levels, p)

    ##Plot the actual data
    plt.plot(dates, levels, '.', label="Actual Levels")

    ##Plot the polynomial fit
    x1 = np.linspace(dates_num[0], dates_num[-1], 100)
    ##poly() evaluates the polynomial at the given x values
    plt.plot(mdates.num2date(x1), poly(x1 - d0), label=f"Degree {p} Fit")

    plt.xlabel('date')
    plt.ylabel('water level (m)')
    plt.xticks(rotation=45)
    plt.title({station.name})
    
    plt.legend()
    plt.tight_layout()
    plt.show()



#fig, axes = plt.subplots(1, 2, figsize=(10, 4))  # 1 row, 2 columns




