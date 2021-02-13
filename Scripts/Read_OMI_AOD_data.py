from functions_OMI import *
from os import listdir

wavelength = {
    "342.5": 0,
    "388": 1,
    "442": 2,
    "463": 3,
    "483.5": 4,
}
input = {
    "path data": "OMI/",
    "lon": 25+40/60,
    "lat": -(100+18/60),
    "year initial": 2015,
    "year final": 2020,
    "wavelength": wavelength["483.5"],
}
data = OMI_data_AOD(
    input["year initial"],
    input["year final"],
    input["lon"],
    input["lat"],
    input["wavelength"])
files = sorted(listdir(input["path data"]))
data.read_files_he5(files,path=input["path data"])
data.calculate_mensual_mean()
data.fill_empty_data()
data.write_data("AODMty")
