from functions_OMI import *
from os import listdir

input = {
    "path data": "../Archivos/OMIData/",
    "lon": 25+40/60,
    "lat": -(100+18/60),
    "year initial": 2005,
    "year final": 2020,
}
data = OMI_data(
    input["year initial"],
    input["year final"],
    input["lon"],
    input["lat"],)
files = listdir(input["path data"])
data.read_files_he5(files)
data.calculate_mensual_mean()
data.fill_empty_data()
data.write_data("OzonoMty", path=input["path data"])