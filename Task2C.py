from floodsystem.stationdata import build_station_list, update_water_levels
from floodsystem.flood import stations_highest_rel_level

def run():
    """Requirements for Task2C 
    Outputs a sorted list of the N stations (objects) at which the water level, relative to the typical range, is highest"""

    # Build station list
    stations = build_station_list()

    # Update water levels to current levels
    update_water_levels(stations)

    stations = stations_highest_rel_level(stations, 10)

    for station in stations:
        print(station.name, station.relative_water_level())

if __name__ == "__main__":
    run()
