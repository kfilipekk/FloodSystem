# Copyright (C) 2018 Garth N. Wells
#
# SPDX-License-Identifier: MIT
"""This module provides a model for a monitoring station, and tools
for manipulating/modifying station data

"""

class MonitoringStation:
    """This class represents a river level monitoring station"""

    def __init__(self, station_id, measure_id, label, coord, typical_range,
                 river, town):
        """Create a monitoring station."""

        self.station_id = station_id
        self.measure_id = measure_id

        # Handle case of erroneous data where data system returns
        # '[label, label]' rather than 'label'
        self.name = label
        if isinstance(label, list):
            self.name = label[0]

        self.coord = coord
        self.typical_range = typical_range
        self.river = river
        self.town = town

        self.latest_level = None

    def __repr__(self):
        d = "Station name:     {}\n".format(self.name)
        d += "   id:            {}\n".format(self.station_id)
        d += "   measure id:    {}\n".format(self.measure_id)
        d += "   coordinate:    {}\n".format(self.coord)
        d += "   town:          {}\n".format(self.town)
        d += "   river:         {}\n".format(self.river)
        d += "   typical range: {}".format(self.typical_range)
        return d
    
    def typical_range_consistent(self) -> bool:
        """Checks if the typical range exists and high > low """
        return self.typical_range and self.typical_range[0] < self.typical_range[1]
    
    def relative_water_level(self):
        """Returns latest water level as a fraction of typical range"""
        try:
            return (self.latest_level - self.typical_range[0]) / (self.typical_range[1] - self.typical_range[0])
        except AttributeError:
            return None
        except TypeError:
            return None
        
    def readable_risk(self):
        if self.flood_risk_factor >= 5:
            return "Very Severe"
        if self.flood_risk_factor >= 2.5:
            return "Severe"
        elif self.flood_risk_factor >= 2:
            return "High"
        elif self.flood_risk_factor >= 1:
            return "Moderate"
        else:
            return "Low"


def inconsistent_typical_range_stations(stations):
    return [s for s in stations if not s.typical_range_consistent()]
