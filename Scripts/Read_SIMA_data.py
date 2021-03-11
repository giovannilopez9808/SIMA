from functions import *
import pandas as pd
import numpy as np
import os


def keys2names(keys):
    names = []
    for key in keys:
        names.append(key.split(".")[0].upper())
    return names


def comaorfinish(value, values):
    coma = ","
    if value == values[-1]:
        coma = "\n"
    return coma


dir_data = "../Archivos/"
dir_stations = "../Stations/"
stations = [station.upper() for station in sorted(os.listdir(dir_stations))]
files = ["2015", "2016", "2017", "2018", "2019", "2020"]
particle_type = "WSR"
file_data = open(dir_data+particle_type+"_SIMA.csv", "w")
file_data.write("Dates,")
for station in stations:
    coma = comaorfinish(station, stations)
    file_data.write(station+coma)
for file in files:
    print("Analizando año {}".format(file))
    data = pd.read_csv(dir_data+file+".csv", low_memory=False)
    particle_types = data[:][0:2]
    data = data.drop(data.index[0:2])
    data.index = pd.to_datetime(data["Dates"])
    data = data.drop("Dates", 1)
    keys_stations = keys2names(data.keys())
    SIMA_data = pd.DataFrame({"Dates": data.index})
    SIMA_data = SIMA_data.set_index("Dates")
    for station in stations:
        for key, key_station in zip(data.keys(), keys_stations):
            if particle_types[key][0] == particle_type and station == key_station:
                SIMA_data[station] = data[key]
    for date in data.index:
        file_data.write(str(date)+",")
        for station in stations:
            if station in keys_stations:
                value = str(SIMA_data[station][date])
                if value == "nan":
                    value = ""
            else:
                value = ""
            coma = comaorfinish(station, stations)
            file_data.write(value+coma)
file_data.close()
