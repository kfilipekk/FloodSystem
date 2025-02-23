import pytest
from floodsystem.station import MonitoringStation
from floodsystem.risk import determine_numerical_risk, stations_by_risk_level

@pytest.fixture
def mock_stations():
    station1 = MonitoringStation("ID1", "Station1", "River1", (0, 0), "Town1", (0, 10), "measure1")
    station1.latest_level = 1.0
    station1.relative_water_level = lambda: 1.5

    station2 = MonitoringStation("ID2", "Station2", "River1", (1, 1), "Town1", (0, 10), "measure2")
    station2.latest_level = 0.5
    station2.relative_water_level = lambda: 0.7

    station3 = MonitoringStation("ID3", "Station3", "River2", (2, 2), "Town2", (0, 10), "measure3")
    station3.latest_level = None
    station3.relative_water_level = lambda: 0.0

    return [station1, station2, station3]

def test_determine_numerical_risk(mock_stations):
    stations = mock_stations
    determine_numerical_risk(stations)

    assert stations[0].flood_risk_factor > 0
    assert stations[1].flood_risk_factor > 0
    assert stations[2].flood_risk_factor == 0

