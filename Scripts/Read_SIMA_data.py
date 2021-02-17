from functions import *
import pandas as pd
import numpy as np
import os


def index2date(index, year):
    n = len(index)
    dates = ["", ""]
    hour = [-1, -1]
    for i in range(n):
        dates.append(str(consecutiveday2date(index[i]//24, year)))
    for i in range(n//24):
        hour = np.append(hour, np.arange(24))
    return dates, hour


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
particle_type = "PM2.5"
file_data = open(dir_data+particle_type+"_SIMA.csv", "w")
file_data.write("Dates,Hours,")
for station in stations:
    coma = comaorfinish(station, stations)
    file_data.write(station+coma)
for file in files:
    data = pd.read_csv(dir_data+file+".csv", low_memory=False)
    keys_stations = keys2names(data.keys())
    index = data.index[2:]-2
    dates, hours = index2date(index, int(file))
    len_data = len(dates)-2
    SIMA_data = pd.DataFrame({"Dates": dates})
    for station in stations:
        for key, key_station in zip(data.keys(), keys_stations):
            if data[key][0] == particle_type and station == key_station:
                SIMA_data[station] = data[key]
    SIMA_data = SIMA_data.drop([0, 1])
    SIMA_data = SIMA_data.set_index("Dates")
    for date in range(len_data):
        file_data.write(dates[date+2]+",")
        file_data.write(str(hours[date+2])+",")
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
