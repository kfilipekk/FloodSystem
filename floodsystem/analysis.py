import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def polyfit(dates, levels, p):
    ##Convert dates to numerical format
    dates_num = mdates.date2num(dates)
    
    ##Shift the time axis to start from 0 as calculation of polynomial coefficients is more accurate
    d0 = dates_num[0]
    shifted_dates = dates_num - d0
    
    ##Calculate polynomial coefficients and create poly() function
    p_coeff = np.polyfit(shifted_dates, levels, p)
    poly = np.poly1d(p_coeff)
    
    return poly, d0
