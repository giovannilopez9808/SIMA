from functions_OMI import *
from os import listdir
dir_data = "../Archivos/"
input = {
    "path HDF": "HDFEOS/GRIDS/ColumnAmountO3/Data Fields/ColumnAmountO3",
    "div": 0.25,
    "scale": 1,
    "path data": dir_data+"OMI_Ozone/",
    "lat": 25+40/60,
    "lon": -(100+18/60),
    "year initial": 2005,
    "year final": 2020,
}
data = OMI_data(
    input["year initial"],
    input["year final"],
    input["lon"],
    input["lat"],
    input["div"],
    input["scale"],
    input["path HDF"])
files = sorted(listdir(input["path data"]))
data.read_files_he5(files, input["path data"])
data.write_data("Ozono_OMI_clean", path=dir_data)
data.calculate_mensual_mean()
data.fill_empty_data()
data.write_data("Ozono_OMI", path=dir_data)
