# Copyright (C) 2018 Garth N. Wells
#
# SPDX-License-Identifier: MIT
"""Unit test for the station module"""

from floodsystem.station import MonitoringStation
from floodsystem.station import inconsistent_typical_range_stations
import pytest


def test_create_monitoring_station():

    # Create a station
    s_id = "test-s-id"
    m_id = "test-m-id"
    label = "some station"
    coord = (-2.0, 4.0)
    trange = (-2.3, 3.4445)
    river = "River X"
    town = "My Town"
    s = MonitoringStation(s_id, m_id, label, coord, trange, river, town)

    assert s.station_id == s_id
    assert s.measure_id == m_id
    assert s.name == label
    assert s.coord == coord
    assert s.typical_range == trange
    assert s.river == river
    assert s.town == town

@pytest.fixture
def sample_stations():
    """ Fixture that creates test stations """
    station_1 = MonitoringStation("station1", "measure1", "Station A", (1.1, 1.1), (1.0, 2.0), "River A", "Town A")
    station_2 = MonitoringStation("station2", "measure2", "Station B", (2.2, 2.2), (3.0, 2.0), "River B", "Town B")
    station_3 = MonitoringStation("station3", "measure3", "Station C", (3.3, 3.3), None, "River C", "Town C")
    return [station_1, station_2, station_3]


def test_typical_range_consistent(sample_stations) -> None:
    """ Ensures the function detects inconsistent ranges """
    station_1, station_2, station_3 = sample_stations

    assert station_1.typical_range_consistent()
    assert not station_2.typical_range_consistent()
    assert not station_3.typical_range_consistent()


def test_inconsistent_typical_range_stations(sample_stations) -> None:
    """ Test for finding inconsistent typical range stations """
    station_1, station_2, station_3 = sample_stations

    inconsistent_stations = inconsistent_typical_range_stations([station_1, station_2, station_3])
    assert inconsistent_stations == [station_2, station_3]
