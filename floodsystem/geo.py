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
    rivers = set([s.river for s in stations if s.river])
    return rivers

def stations_by_river(stations: list[MonitoringStation]) -> dict[str,list]:
    """ Returns a dictionary of the rivers with the river as the key and the stations it has as a list value """
    river_dict = {}
    for s in stations:
        river_dict.setdefault(s.river, []).append(s)
    return river_dict
