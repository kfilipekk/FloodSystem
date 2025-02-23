import numpy as np
import matplotlib.dates as mdates
from datetime import date
from floodsystem.analysis import polyfit

def test_polyfit():

    ##Sample dates and levels
    dates = np.array([date(2025, 2, 2),date(2025, 2, 3),date(2025, 2, 4),date(2025, 2, 5),])
    levels = np.array([0.4,3.5,6.7,2.3])

    p = len(dates) - 1 ##Minimum degree of polynomial to fit the data
    poly, d0 = polyfit(dates, levels, p)

    ##Compare the actual level to the estimate value from poly
    for i, d in enumerate(dates):
        d_num = mdates.date2num(d)
        predicted_level = poly(d_num - d0) 
        actual_level = levels[i]

        assert np.isclose(predicted_level, actual_level)
        print(f"Date: {d}, Predicted level: {predicted_level}, Actual level: {actual_level}")
        
