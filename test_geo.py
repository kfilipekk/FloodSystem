""" Unit test for the geo module """
from floodsystem.geo import stations_by_distance
from floodsystem.geo import stations_within_radius
from floodsystem.geo import rivers_with_stations
from floodsystem.geo import stations_by_river
from floodsystem.geo import rivers_by_station_number
from haversine import haversine
from floodsystem.utils import sorted_by_key
import pytest

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

class MockStation2:
    def __init__(self, name, river):
        self.name = name
        self.river = river

@pytest.fixture
def sample_stations():
    """ Create mock MonitoringStation objects for testing """
    station1 = MockStation2("Station1", "River A")
    station2 = MockStation2("Station2", "River A")
    station3 = MockStation2("Station3", "River B")
    station4 = MockStation2("Station4", "River C")
    station5 = MockStation2("Station5", "River C")
    station6 = MockStation2("Station6", "River C")
    station7 = MockStation2("Station7", "River D")
    station8 = MockStation2("Station8", "River D")
    station9 = MockStation2("Station9", "River E")
    station10 = MockStation2("Station10", "River F")

    return [station1, station2, station3, station4, station5, station6, station7, station8, station9, station10]

def test_rivers_with_stations(sample_stations: list[MockStation2]) -> None:
    """ Test that rivers_with_stations correctly returns a set of unique river names """
    expected_rivers = {"River A", "River B", "River C", "River D", "River E", "River F"}
    assert rivers_with_stations(sample_stations) == expected_rivers

def test_stations_by_river(sample_stations: list[MockStation2]) -> None:
    """ Test that stations_by_river correctly maps rivers to station lists """
    expected_dict = {
    "River A": [sample_stations[0], sample_stations[1]],
    "River B": [sample_stations[2]],
    "River C": [sample_stations[3], sample_stations[4], sample_stations[5]],    
    "River D": [sample_stations[6], sample_stations[7]],
    "River E": [sample_stations[8]],
    "River F": [sample_stations[9]]
    }
    assert stations_by_river(sample_stations) == expected_dict

def test_rivers_by_station_number(sample_stations: list[MockStation2]) -> None:
    """ Test that rivers_by_station_number returns the correct sorted list of river counts """
    expected_list_N4 = [("River C", 3), ("River A", 2), ("River D", 2), ("River B", 1), ("River E", 1), ("River F", 1)]
    assert rivers_by_station_number(sample_stations, 4) == expected_list_N4

    expected_list_N3 = [("River C", 3), ("River A", 2), ("River D", 2)]
    assert rivers_by_station_number(sample_stations, 3) == expected_list_N3
        
    expected_list_N2 = [("River C", 3), ("River A", 2), ("River D", 2)]
    assert rivers_by_station_number(sample_stations, 2) == expected_list_N2
        
    expected_list_N1 = [("River C", 3)]
    assert rivers_by_station_number(sample_stations, 1) == expected_list_N1

def test_stations_within_radius():

    # Mock data
    station1 = MockStation("Station 1", (0, 1)) # distance = 111.19
    station2 = MockStation("Station 2", (2, 2)) # distance = 314.47
    station3 = MockStation("Station 3", (5, 12)) # distance = 1443.96

    stations = [station1, station2, station3]  # Station-Distance pairs
    centre = (0, 0)  # Mock centre

    # Edge cases
    assert stations_within_radius([], centre, 10) == []  # No stations
    assert stations_within_radius(stations, centre, 0) == []  # Radius 0
    assert stations_within_radius(stations, centre, -5) == []  # Negative radius

    # Functional cases
    assert stations_within_radius(stations, centre, 120) == [station1]  
    assert stations_within_radius(stations, centre, 320) == [station1, station2]  
    assert stations_within_radius(stations, centre, 1500) == [station1, station2, station3]  
