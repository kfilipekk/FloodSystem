from floodsystem.stationdata import build_station_list
from floodsystem.geo import stations_by_distance


# assing coordinates of Cambridge town centre
p = (52.2053, 0.1218)


def run():
    """ requirements for task 1B.
    Outputs a list of (station name, town, distance) tuples for the 
    ten closest and ten furthest monitoring stations from p. 
    
    """

    stations = build_station_list()
    stations = stations_by_distance(stations, p)

    closest_10_stations = [(station.name, station.town, distance) for station, distance in stations[:10]]
    furthest_10_stations = [(station.name, station.town, distance) for station, distance in stations[-10:]]

    print(closest_10_stations)
    print(furthest_10_stations)

if __name__ == "__main__":
    run()
