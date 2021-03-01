from os import listdir
import pandas as pd
import numpy as np
dir_data = "../Archivos/"
dir_stations = "../Stations/"
stations = listdir(dir_stations)
stations = [station.upper() for station in stations]
files = ["2015", "2016", "2017", "2018", "2019", "2020"]
measurements = ["PM10"]
for file in files:
    names = []
    datas = []
    print("Año\t\t"+file)
    data = pd.read_csv(dir_data+file+".csv", low_memory=False)
    keys = data.keys()
    total = np.array([data["Dates"].count()])
    for key in keys:
        if data[key][0] in measurements:
            count = int(data[key].count())
            names.append([key.split(".")[0], data[key][0]])
            datas.append(count)
    print(total)
    datas = np.round((datas/total)*100, 1)
    for data, name in zip(datas, names):
        print("{:10} {:4} {:.1f}".format(name[0], name[1], data))
