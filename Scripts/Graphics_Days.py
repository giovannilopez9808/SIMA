import matplotlib.pyplot as plt
from functions import *
import numpy as np
import os
# <----------------------------Lectura de los datos de entrada--------------------------------------->
dir_stations = "../Stations/"
stations = ["noroeste", "noreste"]
for station in stations:
    print("Graficando estacion "+station)
    dir_station = dir_stations+station+"/"
    dates, aods = np.loadtxt(dir_station+"DataAOD_moderate.txt",
                             usecols=[0, 5], dtype=str, unpack=True)
    mkdir("Graphics/", path=dir_station)
    for date, aod in zip(dates, aods):
        med = np.loadtxt(dir_station+"Mediciones/"+date+".txt")
        mod = np.loadtxt(dir_station+"Results_SMARTS/"+date+".txt")
        plt.plot(med[:, 0], med[:, 1],
                 label="Measurement", lw=3, color="black")
        plt.plot(mod[:, 0], mod[:, 1],
                 label="SMARTS Model", lw=3, color="green")
        plt.ylabel("UV-VIS-NIR irradiance (W/m$^2$)")
        plt.xlabel("Local hour (h)")
        plt.xlim(8, 17)
        plt.ylim(0, 1200)
        plt.title("Day "+date+"\n AOD$_{550nm}$: "+aod)
        plt.legend(ncol=2, frameon=False, mode="expand")
        plt.savefig(dir_station+"Graphics/"+date+".png")
        plt.clf()
