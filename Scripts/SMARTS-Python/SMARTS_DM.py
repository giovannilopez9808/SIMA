from SMARTS_algorithm import *
from numpy import loadtxt
from functions import *


input_parameters = {
    "path stations": "../../Stations/",
    "stations": ["noroeste"],
    "hour initial": 8,
    "hour final": 17,
    "lon initial": 285,
    "lon final": 2800,
}

input = SMARTS(input_parameters["hour initial"],
               input_parameters["hour final"],
               input_parameters["lon initial"],
               input_parameters["lon final"],
               )

for station in input_parameters["stations"]:
    dir_station = input_parameters["path stations"]+station+"/"
    mkdir("Results_SMARTS_DM", path=dir_station)
    dates, years, months, days, o3_list, aod_list, dr_list = loadtxt(
        dir_station+"/DataAOD_moderate.txt", unpack=True)
    dir_results = dir_station + "/Results_SMARTS/"
    # <-----------------------------Ciclo para variar los dias--------------------------------------->
    for date, year, month, day, o3, aod in zip(dates, years, months, days, o3_list, aod_list):
        date = str(int(date))
        year, month, day = int_dates(year, month, day)
        print("Calculando el dia ", year, month, day)
        input.run_SMARTS(day, month, year, o3, aod, date, path=dir_results)
