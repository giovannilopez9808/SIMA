from functions_OMI import *
from functions import *
from os import listdir
import pandas as pd
import numpy as np
dir_data = "../Archivos/"
input = {
    "path data": dir_data+"OMI_AOD_1/",
    # Path for HDF Files with 1 deg
    "path HDF": "/HDFEOS/GRIDS/Aerosol NearUV Grid/Data Fields/FinalAerosolOpticalDepth",
    "div": 1,
    "scale": 1,
    "lat": 25+40/60,
    "lon": -(100+18/60),
    "year initial": 2015,
    "year final": 2020,
}
AOD_list = ["354", "388", "500"]
total_days = (input["year final"]-input["year initial"]+1)*365+2
dates = []
for day in range(total_days):
    date = str(consecutiveday2date(day, input["year initial"]))
    if date[5:10] != "02-29":
        dates.append(date)
data_AOD = pd.DataFrame(index=dates, columns=[AOD+"nm" for AOD in AOD_list])
for AOD in AOD_list:
    print("Analizando longitud de onda "+AOD)
    data = OMI_data(
        input["year initial"],
        input["year final"],
        input["lon"],
        input["lat"],
        input["div"],
        input["scale"],
        input["path HDF"]+AOD)
    files = sorted(listdir(input["path data"]))
    data.read_files_he5(files,
                        path=input["path data"])
    data.calculate_mensual_mean()
    data.fill_empty_data()
    data.reshape()
    data_AOD[AOD+"nm"] = pd.DataFrame(data.data, index=dates)
data_AOD = data_AOD.replace(0, np.nan)
data_AOD.to_csv(dir_data+"AOD_OMI_1.csv")
