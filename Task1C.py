from floodsystem.geo import stations_within_radius
from floodsystem.stationdata import build_station_list

# assigning coordinates of Cambridge town centre
p = (52.2053, 0.1218)

# 10km radius
r = 10

def run():
    """ Requirements for task 1C.
    Outputs a list of all stations within a 10km of Cambridge"""
    
    all_stations = build_station_list()
    station_list = stations_within_radius(all_stations, p, r)

    station_names = [station.name for station in station_list]

    print(sorted(station_names))

if __name__ == "__main__":
    run()