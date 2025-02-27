from floodsystem.stationdata import build_station_list, update_water_levels
from floodsystem.flood import stations_level_over_threshold

def run():
    """Requirements for Task2B 
    Outputs stations for which current relative level is over 0.8"""

    # Build station list
    stations = build_station_list()

    # Update water levels to current levels
    update_water_levels(stations)

    stations_over_threshold = stations_level_over_threshold(stations, 0.8)
    
    for station in stations_over_threshold:
        print(station[0].name, station[1])
    
if __name__ == "__main__":
    run()
