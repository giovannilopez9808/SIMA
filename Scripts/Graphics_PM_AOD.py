import matplotlib.pyplot as plt
from functions_AOD import *
from functions_SIMA import *
import pandas as pd


def calc_month_mean_of_data(PM, AOD):
    PM.calc_month_mean("NORESTE")
    AOD.calc_month_mean_AOD_list()


inputs = {
    "year initial": 2015,
    "year final": 2020,
    "path data": "../Archivos/",
    "stations": ["NOROESTE", "NORESTE"],
    "path stations": "../Stations/",
    "particle type": "PM10",
}
PM_data = SIMA_data(
    inputs["year initial"],
    inputs["year final"],
    inputs["stations"],
    inputs["particle type"],
)
AOD_data_list = AOD_list(
    inputs["path stations"],
    "NOROESTE",
    inputs["year initial"],
    inputs["year final"]
)
PM_data.read_data(inputs["path data"])
# PM_data.calc_year_mean()
calc_month_mean_of_data(PM_data, AOD_data_list)
# PM_data.calc_day_mean("NORESTE")
PM_data.plot_month_means_AOD([
    [AOD_data_list.pristine.month_mean, "Pristine", "#f46188"],
    [AOD_data_list.moderate.month_mean, "Moderate", "#505bda"],
    [AOD_data_list.SSAAER_pristine.month_mean, "SSAAER Pristine", "#ffaac3"],
    [AOD_data_list.SSAAER_moderate.month_mean, "SSAAER Moderate", "#1a2849"],
])
# PM_data.calc_season_hour_mean("NORESTE")
# PM_data.plot_season_means()
