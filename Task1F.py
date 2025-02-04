from floodsystem.stationdata import build_station_list
from floodsystem.station import inconsistent_typical_range_stations

def run():
    """Task1F: Find and print stations with inconsistent typical range data."""
    
    stations = build_station_list()
    inconsistent_stations = inconsistent_typical_range_stations(stations)

    station_names = sorted(s.name for s in inconsistent_stations)
    print(f"{len(station_names)} stations with inconsistent range \n {station_names}")

if __name__ == "__main__":
    run()
