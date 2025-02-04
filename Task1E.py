from floodsystem.geo import rivers_by_station_number
from floodsystem.stationdata import build_station_list

def run():
    """ Requirements for task 1E.
    Returns a list of tuples of the rivers and the number of stations they have. Top N rivers returned
    """

    stations = build_station_list()
    N = 9
    top_rivers = rivers_by_station_number(stations, N)
    print(top_rivers)

if __name__ == "__main__":
    run()
