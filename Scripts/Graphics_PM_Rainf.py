import matplotlib.pyplot as plt
from functions_SIMA import *
import pandas as pd


def calc_month_mean_of_data(PM, Rain):
    PM.calc_month_mean()
    Rain.calc_month_sum()


inputs = {
    "year initial": 2015,
    "year final": 2020,
    "path data": "../Archivos/",
    "station": "NORESTE",
}

PM_10 = SIMA_data(inputs["year initial"],
                  inputs["year final"],
                  inputs["station"],
                  "PM10",)
RAINF = SIMA_data(inputs["year initial"],
                  inputs["year final"],
                  inputs["station"],
                  "RAINF",)
PM_10.read_data(inputs["path data"])
RAINF.read_data(inputs["path data"])
calc_month_mean_of_data(PM_10, RAINF)
PM_10.plot_month_means_Rainfall([RAINF.month_mean, "Rainfall"])
