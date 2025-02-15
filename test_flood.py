"""Unit tests for flood module"""

from floodsystem.flood import stations_level_over_threshold

# Create class of mock station with only required data for testing
class MockStation:
        def __init__(self, name, typical_range_consistent, relative_water_level):
            self.name = name
            self.typical_range_consistent = typical_range_consistent
            self.relative_water_level = relative_water_level

            def typical_range_consistent(self):
                return self.typical_range_consistent
            
            def relative_water_level(self):
                 return self.relative_water_level


def test_stations_level_over_threshold():

    # Build station list
    station1 = MockStation(station1, True, 0.7)
    station2 = MockStation(station2, True, 0.5)
    station3 = MockStation(station3, True, -0.75)
    station4 = MockStation(station4, False, None)
    station5 = MockStation(station5, True, 10.7)

    stations = [station1, station2, station3, station4, station5]

    