# Copyright (C) 2018 Garth N. Wells
#
# SPDX-License-Identifier: MIT
"""This module contains a collection of functions related to
geographical data.

"""

from haversine import haversine, Unit
from .utils import sorted_by_key  # noqa
from collections import Counter
from .station import MonitoringStation

def stations_by_distance(stations, p):
    """ This function returns a list of (station, distance)
    tuples, sorted by distance, where the distance is 
    calculated from the coordinations of p.
    
    """
    
    stations_by_distance = [(station, haversine(station.coord, p)) for station in stations]
    sorted_stations_by_distance = sorted_by_key(stations_by_distance, 1)
    return sorted_stations_by_distance


def stations_within_radius(stations, centre, r):
    """ This function returns a list of all stations within a radius r of the centre """

    # Handle edge cases
    if r <= 0 or not stations:
        return []
    
    stations = stations_by_distance(stations, centre)

    within_radius = []
    for station, distance in stations:
        if distance < r:
            within_radius.append(station)
        else:
            break
    
    return within_radius




def rivers_with_stations(stations: list[MonitoringStation]) -> set[str]:
    """ Returns a list of all the rivers which have a station as a set """
    rivers = set([s.river for s in stations])
    return rivers

def stations_by_river(stations: list[MonitoringStation]) -> dict[str,list]:
    """ Returns a dictionary of the rivers with the river as the key and the stations it has as a list value """
    river_station_dict = {}
    for s in stations:
        river_station_dict.setdefault(s.river, []).append(s)
    return river_station_dict



def rivers_by_station_number(stations, N):
    """Returns a list of (river name, number of stations) tuples, sorted by number of stations """
    ##Counter creates a dictionary with the rivers as keys and the number of stations in them as values
    river_counts = Counter(s.river for s in stations)
    ##Sorts the dictionary into a list of tuples in descending order
    sorted_rivers = sorted(river_counts.items(), key=lambda x: x[1], reverse=True)

    if N < len(sorted_rivers):
        ##Threshold value for number of stations on a river
        threshold = sorted_rivers[N-1][1]
        sorted_rivers = [(river, count) for river, count in sorted_rivers if count >= threshold]
    return sorted_rivers

