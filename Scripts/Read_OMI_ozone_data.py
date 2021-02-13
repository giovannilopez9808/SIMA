from functions_OMI import *
from os import listdir
dir_data="../Archivos/"
input = {
    "path HDF": "HDFEOS/GRIDS/ColumnAmountO3/Data Fields/ColumnAmountO3",
    "path data": dir_data+"OMI_Ozone/",
    "lon": 25+40/60,
    "lat": -(100+18/60),
    "year initial": 2015,
    "year final": 2020,
}
data = OMI_data_ozone(
    input["year initial"],
    input["year final"],
    input["lon"],
    input["lat"],)
files = sorted(listdir(input["path data"]))
data.read_files_he5(files,input["path data"],input["path HDF"])
# data.calculate_mensual_mean()
# data.fill_empty_data()
data.write_data("Ozono_OMI_clean",path=dir_data)