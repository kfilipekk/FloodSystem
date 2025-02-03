from numpy import sort
from floodsystem.geo import rivers_with_stations, stations_by_river
from floodsystem.stationdata import build_station_list

def run():
    """ Requirements for task 1B.
    Prints the number of rivers wih stations and the first 10 in alphabetical order.
    Prints the names of the stations for 3 rivers
    """
        
    stations = build_station_list()


    river_set = rivers_with_stations(stations)
    print(f"{len(river_set)} rivers with at least one monitoring station\n")
    print(f"{sorted(river_set)[0:9]}\n")


    river_dict = stations_by_river(stations)
    for river in ["River Aire", "River Cam", "River Thames"]:
        if river in river_dict:
            station_names = sorted([s.name for s in river_dict[river]])
            print(f"The river {river} has stations\n {station_names}\n")

if __name__ == "__main__":
    run()
