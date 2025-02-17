import matplotlib.pyplot as plt
from floodsystem.plot import plot_water_levels
from floodsystem.flood import stations_highest_rel_level
from floodsystem.stationdata import build_station_list, update_water_levels
from floodsystem.datafetcher import fetch_measure_levels
import datetime

def run():
    dt = 10
    stations = build_station_list()
    update_water_levels(stations)
    stationshigh = stations_highest_rel_level(stations, dt)
    for s in stationshigh:
        dates, levels = fetch_measure_levels(s.measure_id, dt=datetime.timedelta(days=dt))
        plot_water_levels(s,dates,levels)
    
if __name__ == "__main__":
    print("*** Task 2E: CUED Part IA Flood Warning System ***")
    run()
