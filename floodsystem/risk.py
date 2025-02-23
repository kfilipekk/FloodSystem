from floodsystem.station import inconsistent_typical_range_stations
from floodsystem.geo import stations_by_river, stations_within_radius

##Constants for risk calculation
initial_water_level_weight = 0.5
river_level_weight = 0.3
normal_water_level = 0.0
radius = 50.0


def determine_numerical_risk(stations):
    ##Filter out stations with inconsistent data or no level
    good_stations = [s for s in stations if s.latest_level is not None and s not in inconsistent_typical_range_stations(stations)]
    bad_stations = [s for s in stations if s not in good_stations]

    ##Assign initial risk based on relative water level
    for station in good_stations:
        station.flood_risk_factor = (station.relative_water_level() or 0) * initial_water_level_weight

    ##Adjust risk factor based on river average
    for river, river_stations in stations_by_river(good_stations).items():
        avg_water_level = sum(s.relative_water_level() for s in river_stations if s.relative_water_level()) / len(river_stations)
        for station in river_stations:
            station.flood_risk_factor += (avg_water_level - normal_water_level) * river_level_weight

    ##Estimate risk for stations with missing data from nearby stations
    for station in bad_stations:
        nearby_stations = stations_within_radius(good_stations, station.coord, radius)
        station.flood_risk_factor = (sum(s.flood_risk_factor for s in nearby_stations) / len(nearby_stations)) if nearby_stations else 0


def stations_by_risk_level(stations):
    """Returns a list of stations sorted by their flood risk factor."""
    determine_numerical_risk(stations)
    valid_stations = [s for s in stations if getattr(s, 'flood_risk_factor', None) is not None]
    return sorted(valid_stations, key=lambda s: s.flood_risk_factor, reverse=True) if valid_stations else []
