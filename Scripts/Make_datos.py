import numpy as np
import datetime
o3data = np.loadtxt("../Archivos/OzonoMty.csv", skiprows=1,
                    usecols=np.arange(1, 16), dtype=str, delimiter=",")
stations = ["noroeste"]
dir_stations = "../Stations/"
for station in stations:
    dir_station = dir_stations+station+"/"
    dates = np.loadtxt(dir_station+"days.txt", dtype=str)
    file = open(dir_station+"datos.txt", "w")
    for date in dates:
        year, month, day = int("20"+date[0:2]), int(date[2:4]), int(date[4:6])
        day2 = (datetime.date(year, month, day)-datetime.date(year, 1, 1)).days
        o3 = o3data[day2, year-2005]
        file.write(date+" "+o3+" "+str(year) +
                   " "+str(month)+" "+str(day)+"\n")
    file.close()
