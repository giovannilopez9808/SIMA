from functions_OMI import *
from functions import *
from os import listdir
import pandas as pd
import numpy as np
dir_data = "../Archivos/"
input = {
    "path data": dir_data+"OMI_AOD_025/",
    # Path for HDF Files with 0.25 deg
    "path HDF": "/HDFEOS/GRIDS/ColumnAmountAerosol/Data Fields/AerosolOpticalThicknessMW",
    "lon": 25+40/60,
    "lat": -(100+18/60),
    "year initial": 2015,
    "year final": 2020,
}
wavelength_dict = {
    "342.5nm": 0,
    "388nm": 1,
    "442nm": 2,
    "463nm": 3,
    "483.5nm": 4,
}
total_days = (input["year final"]-input["year initial"]+1)*365+2
dates = [consecutiveday2yymmdd(day, input["year initial"])
         for day in range(total_days) if not "0229" in consecutiveday2yymmdd(day, input["year initial"])]
data_AOD = pd.DataFrame(index=dates, columns=wavelength_dict.keys())
for key in wavelength_dict.keys():
    print("Analizando longitud de onda "+key)
    data = OMI_data_AOD_025Deg(
        input["year initial"],
        input["year final"],
        input["lon"],
        input["lat"],
        wavelength_dict[key])
    files = sorted(listdir(input["path data"]))
    data.read_files_he5(
        files, path=input["path data"], path_HDF=input["path HDF"])
    data.calculate_mensual_mean()
    data.fill_empty_data()
    data.reshape()
    data_AOD[key] = pd.DataFrame(data.data, index=dates)
data_AOD = data_AOD.replace(0, np.nan)
data_AOD.to_csv(dir_data+"AOD_OMI_025.csv")
