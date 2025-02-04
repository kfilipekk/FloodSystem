""" Unit test for the geo module """

from floodsystem.geo import stations_by_distance
from floodsystem.geo import stations_within_radius
from haversine import haversine
from floodsystem.utils import sorted_by_key



def test_stations_by_distance():

    class MockStation:
        def __init__(self, name, coord):
            self.name = name
            self.coord = coord

    # Mock data: create mock stations with coordinates
    station1 = MockStation("Station 1", (52.205, 0.1218))  # Cambridge
    station2 = MockStation("Station 2", (48.8566, 2.3522))  # Paris
    station3 = MockStation("Station 3", (51.5074, -0.1278))  # London
        
    stations = [station1, station2, station3]
    reference_point = (52.205, 0.1218)  # Cambridge

    # Call stations_by_distance function to be tested with test data
    results = stations_by_distance(stations, reference_point)

    # Manually calculate expected outputs
    expected_distances = [(station, haversine(station.coord, reference_point)) for station in stations]

    # Sort manually calculated outputs
    sorted = sorted_by_key(expected_distances, 1)

    assert len(results) == len(sorted)
    for i in range(len(results)):
        assert results[i][0] == sorted[i][0]
        assert results[i][1] == sorted[i][1]


def test_stations_within_radius():

    class MockStation:
        def __init__(self, name):
            self.name = name

    # Mock data
    station1 = MockStation("Station 1")
    station2 = MockStation("Station 2")
    station3 = MockStation("Station 3")

    stations = [(station1, 1.0), (station2, 2.5), (station3, 5.0)]  # Station-Distance pairs
    centre = (0, 0)  # Mock centre

    # Mock function for sorting 
    def stations_by_distance(stations):
        return sorted(stations, key=lambda x: x[1])  # Already sorted in this case

    # Edge cases
    assert stations_within_radius([], centre, 10) == []  # No stations
    assert stations_within_radius(stations, centre, 0) == []  # Radius 0
    assert stations_within_radius(stations, centre, -5) == []  # Negative radius

    # Functional cases
    assert stations_within_radius(stations, centre, 1.5) == [s1]  # Only s1 in range
    assert stations_within_radius(stations, centre, 3) == [s1, s2]  # s1 and s2 in range
    assert stations_within_radius(stations, centre, 10) == [s1, s2, s3]  # All stations in range
    assert stations_within_radius(stations, centre, 5) == [s1, s2]  # Edge case: s3 is at r=5 but excluded




