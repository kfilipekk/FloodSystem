""" Unit test for the geo module """

from floodsystem.geo import stations_by_distance
from haversine import haversine
from floodsystem.utils import sorted_by_key

class MockStation:
    def __init__(self, name, coord):
        self.name = name
        self.coord = coord

def test_stations_by_distance():
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


