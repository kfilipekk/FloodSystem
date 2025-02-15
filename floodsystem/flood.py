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

