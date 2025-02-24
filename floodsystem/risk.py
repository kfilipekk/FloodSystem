from collections import defaultdict
from floodsystem.station import inconsistent_typical_range_stations
from floodsystem.geo import stations_by_river, stations_within_radius

## Constants for risk calculation
initial_water_level_weight = 0.5
river_level_weight = 0.3
normal_water_level = 0.0
radius = 50.0

def determine_numerical_risk(stations):
    ##Filter out stations with inconsistent data or no level
    good_stations = [s for s in stations if s.latest_level is not None and s.town and s not in inconsistent_typical_range_stations(stations)]
    
    ##Assign initial risk based on relative water level
    town_risk_factors = defaultdict(list)
    
    for station in good_stations:
        risk_factor = (station.relative_water_level() or 0) * initial_water_level_weight
        town_risk_factors[station.town].append(risk_factor)

    ##Adjust risk factor based on river average
    for river, river_stations in stations_by_river(good_stations).items():
        avg_water_level = sum(s.relative_water_level() for s in river_stations if s.relative_water_level()) / len(river_stations)
        for station in river_stations:
            town_risk_factors[station.town].append((avg_water_level - normal_water_level) * river_level_weight)

    ##Final risk factor calculation
    town_risks = {town: sum(risks) / len(risks) for town, risks in town_risk_factors.items()}
    print(town_risks)
    return town_risks


def towns_by_risk_level(stations):
    """Returns a list of towns sorted by their flood risk factor."""
    town_risks = determine_numerical_risk(stations)
    return sorted(town_risks.items(), key=lambda x: x[1], reverse=True)
