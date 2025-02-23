import pytest
from unittest.mock import patch
from floodsystem.plot import plot_water_level_with_fit

def test_plot_water_level_with_fit():
    class MockStation:
        def __init__(self, name):
            self.name = name
    station = MockStation(name="Cambridge")
    dates = ['2025-02-01', '2025-02-02', '2025-02-03']
    levels = [0.5, 1.2, 0.8]
    p = 2

    with patch('matplotlib.pyplot.plot') as mock_plot, patch('matplotlib.pyplot.show') as mock_show:
        plot_water_level_with_fit(station, dates, levels, p)
        mock_plot.assert_called()
        mock_show.assert_called()
