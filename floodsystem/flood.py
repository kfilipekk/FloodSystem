""" This module contains functionality related to stations with high water levels"""

def stations_level_over_threshold(stations, tol):
    """Returns a list of (station, relative water level tuples) 
    for which the relative water level is over tolerance"""

    stations_over_threshold = []

    for station in stations:
        if station.typical_range_consistent():
            try:
                if station.relative_water_level() > tol:
                    stations_over_threshold.append((station, station.relative_water_level()))
            except TypeError:
                pass

    return sorted(stations_over_threshold, key=lambda x: x[1], reverse=True)


def stations_highest_rel_level(stations, N):
    """Returns a list of the N stations at which the relative water level is highest"""

    stations_list = []

    for station in stations:
        if station.typical_range_consistent():
            rel_level = station.relative_water_level()
            if rel_level is not None and isinstance(rel_level, float):
                stations_list.append(station)

    

    stations_list = sorted(stations_list, key=lambda x: x.relative_water_level(), reverse=True)

    return stations_list[:N]


    

    
    

