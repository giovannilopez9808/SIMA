from os import listdir
import pandas as pd
import numpy as np
dir_data = "../Archivos/"
dir_stations = "../Stations/"
stations = listdir(dir_stations)
stations = [station.upper() for station in stations]
files = ["2015", "2016", "2017", "2018", "2019", "2020"]
measurements = ["SR"]
station = "SUR"
hour_i, hour_f = 8, 19
for file in files:
    names = []
    datas = []
    print("Año\t\t"+file)
    data = pd.read_csv(dir_data+file+".csv", low_memory=False)
    titles = data[:][0:2]
    data = data.drop([0, 1])
    data["Dates"] = pd.to_datetime(data["Dates"])
    keys = data.keys()
    for index in data.index:
        if not hour_i <= data["Dates"][index].hour <= hour_f:
            data = data.drop(index)
    total = np.array([data["Dates"].count()])
    print(total)
    data = data.fillna(0)
    for key in keys:
        if titles[key][0] in measurements:
            n = 0
            for index in data.index:
                if float(data[key][index]) > 0:
                    n += 1
            names.append([key.split(".")[0], titles[key][0]])
            datas.append(n)
    datas = np.round((datas/total)*100, 2)
    for data, name in zip(datas, names):
        print(name[0], "\t", name[1], "\t\t", data)
