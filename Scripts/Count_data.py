from os import listdir
import pandas as pd
import numpy as np
dir_data = "../Archivos/"
dir_stations = "../Stations/"
stations = listdir(dir_stations)
stations = [station.upper() for station in stations]
files=["2015","2016","2017","2018","2019","2020"]
measurements=["PM10","PM2.5"]
for file in files:
    names=[]
    datas=[]
    print("Año\t\t"+file+"\n\n")
    data = pd.read_csv(dir_data+file+".csv", low_memory=False)
    keys=data.keys()
    for key in keys:
        if data[key][0] in measurements:
            count=int(data[key].count())
            names.append([key.split(".")[0],data[key][0]])
            datas.append(count)
    total=np.sum(datas)
    datas=np.round((datas/total)*100,2)
    for data,name in zip(datas,names):
        print(name[0],"\t",name[1],"\t\t",data)
