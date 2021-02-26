import matplotlib.pyplot as plt
from functions_AOD_OMI import *
from functions_MODIS import *
from functions_SIMA import *
from functions_AOD import *
import pandas as pd


def read_data(PM, MODIS, OMI, path):
    MODIS.read_data(path)
    OMI.read_data(path)
    PM.read_data(path)


def calc_month_mean_of_data(PM, AOD, MODIS, OMI):
    AOD.calc_month_mean_AOD_list()
    PM.calc_month_hour_mean()
    MODIS.calc_month_mean()
    OMI.calc_month_mean()


inputs = {
    "year initial": 2015,
    "year final": 2020,
    "path data": "../Archivos/",
    "station": "NORESTE",
    "path stations": "../Stations/",
    "particle type": "PM10",
    "AOD MODIS file": "MODIS_AOD",
    "AOD MODIS type": "AOD Deep Blue",
    "AOD OMI scale": "1",
    "AOD OMI wavelength": "500"
}
PM_data = SIMA_data(
    inputs["year initial"],
    inputs["year final"],
    inputs["station"],
    inputs["particle type"],
)
AOD_data_list = AOD_list(
    inputs["path stations"],
    inputs["station"],
    inputs["year initial"],
    inputs["year final"]
)
MODIS_data_list = MODIS_data(
    inputs["AOD MODIS file"],
    inputs["year initial"],
    inputs["year final"],
    inputs["AOD MODIS type"],
)
OMI_data_list = AOD_OMI_data(
    inputs["year initial"],
    inputs["year final"],
    inputs["AOD OMI wavelength"],
    inputs["AOD OMI scale"],
)
read_data(PM_data, MODIS_data_list, OMI_data_list, inputs["path data"])
calc_month_mean_of_data(PM_data, AOD_data_list, MODIS_data_list, OMI_data_list)
print(PM_data.month_hour_mean.head())
PM_data.plot_month_means_AOD([
    [AOD_data_list.pristine.month_mean, "Pristine", "#f46188"],
    [AOD_data_list.moderate.month_mean, "Moderate", "#505bda"],
    [AOD_data_list.SSAAER_pristine.month_mean, "SSA Pristine", "#ffaac3"],
    [AOD_data_list.SSAAER_moderate.month_mean, "SSA Moderate", "#1a2849"], ],
    [[MODIS_data_list.month_mean, "MODIS", "red"],
     [OMI_data_list.month_mean, "OMI", "green"]],)
# PM_data.calc_season_hour_mean("NORESTE")
# PM_data.plot_season_means()
