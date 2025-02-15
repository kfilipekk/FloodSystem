"""Unit tests for flood module"""

from floodsystem.flood import stations_level_over_threshold, stations_highest_rel_level

# Create class of mock station with only required data for testing
class MockStation:
        def __init__(self, name, range_consistent, rel_water_level):
            self.name = name
            self.range_consistent = range_consistent
            self.rel_water_level = rel_water_level

        def typical_range_consistent(self):
            return self.range_consistent
            
        def relative_water_level(self):
            return self.rel_water_level


def test_stations_level_over_threshold():

    # Build station list
    station1 = MockStation("s1", True, 0.7)
    station2 = MockStation("s2", True, 0.5)
    station3 = MockStation("s3", True, -0.75)
    station4 = MockStation("s4", False, None)
    station5 = MockStation("s5", True, 10.7)

    stations = [station1, station2, station3, station4, station5]

    # Testing for different tolerances
    assert stations_level_over_threshold(stations, 0.3) == [(station5, 10.7), (station1, 0.7), (station2, 0.5)]
    assert stations_level_over_threshold(stations, 1.5) == [(station5, 10.7)]
    assert stations_level_over_threshold(stations, 15) == []


def test_stations_highest_rel_level():

     # Build station list
    station1 = MockStation("s1", True, 0.7)
    station2 = MockStation("s2", True, 0.5)
    station3 = MockStation("s3", True, -0.75)
    station4 = MockStation("s4", False, None)
    station5 = MockStation("s5", True, 10.7)

    stations = [station1, station2, station3, station4, station5]

    # Testing for different values of N

    assert stations_highest_rel_level(stations, 3) == [station5, station1, station2]
    assert stations_highest_rel_level(stations, 0) == []
    assert stations_highest_rel_level(stations, 5) == [station5, station1, station2, station3]


    