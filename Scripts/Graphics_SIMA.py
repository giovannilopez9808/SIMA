import matplotlib.pyplot as plt
from functions_SIMA import *
import pandas as pd


inputs = {
    "year initial": 2015,
    "year final": 2020,
    "path data": "../Archivos/",
    "stations": ["NOROESTE", "NORESTE"],
}
PM_data = PM10(
    inputs["year initial"],
    inputs["year final"],
    inputs["stations"],
)
PM_data.read_data("PM10_SIMA.csv",inputs["path data"])
PM_data.Clean_data()
PM_data.calc_year_mean()
PM_data.calc_month_mean("NORESTE")
PM_data.calc_day_mean("NORESTE")
PM_data.plot_month_means()
PM_data.calc_season_hour_mean("NORESTE")
PM_data.plot_season_means()