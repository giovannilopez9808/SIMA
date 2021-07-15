from functions import *
import pandas as pd
import numpy as np
import datetime
o3data = pd.read_csv("../Archivos/Ozono_OMI.csv")
stations = ["noreste"]
dir_stations = "../Stations/"
for station in stations:
    dir_station = dir_stations+station+"/"
    dates = np.loadtxt(dir_station+"days.txt", dtype=str)
    file = open(dir_station+"datos.txt", "w")
    file.write("Date,Ozone,Year,Month,Day\n")
    for date in dates:
        year, month, day = int("20"+date[0:2]), int(date[2:4]), int(date[4:6])
        conse_day = date2consecutiveday(year, month, day)
        o3 = o3data[str(year)][conse_day]
        file.write("{},{:.3f},{},{},{}\n".format(date, o3, year, month, day))
    file.close()
