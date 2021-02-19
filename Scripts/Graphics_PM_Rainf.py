import matplotlib.pyplot as plt
from functions_SIMA import *
import pandas as pd


def calc_month_mean_of_data(PM, Rain, station):
    PM.calc_month_mean(station)
    Rain.calc_month_mean(station)


inputs = {
    "year initial": 2015,
    "year final": 2020,
    "path data": "../Archivos/",
    "stations": ["NOROESTE", "NORESTE"],
}

station = "NORESTE"
PM_10 = SIMA_data(inputs["year initial"],
                  inputs["year final"], inputs["stations"])
RAINF = SIMA_data(inputs["year initial"],
                  inputs["year final"], inputs["stations"])
PM_10.read_data("PM10_SIMA.csv", inputs["path data"])
RAINF.read_data("RAINF_SIMA.csv", inputs["path data"])
calc_month_mean_of_data(PM_10, RAINF, station)
PM_10.plot_month_means_Rain([RAINF.month_mean, "Rainfall"])
