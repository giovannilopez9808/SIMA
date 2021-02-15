from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
from functions import *
import pandas as pd
import numpy as np
import datetime


def f(x, m):
    return m*x

def dates2conse_days(dates,year_i):
    conse_days=[yy_mm_dd2consecutiveday(date,year_i) for date in dates]
    return conse_days

stations_name = ["Northwest", "Northeast"]
stations = ["noroeste", "noreste"]
dir_data = "../Archivos/"
dir_stations="../Stations/"
file_MODIS = "MODIS_AOD.csv"
file_SMARTS = "DataAOD_moderate"
year_i=2015
data_MODIS=pd.read_csv(dir_data+file_MODIS)
dates_MODIS = dates2conse_days(data_MODIS["Date"],year_i)
plt.plot(dates_MODIS,data_MODIS["AOD Land Ocean Mean"])
plt.plot(dates_MODIS,data_MODIS["AOD Deep Blue"])
plt.show()
# # <-----------------------------------Localizacion de los archivos de datos-------------------------->
# for station, station_name in zip(stations, stations_name):
#     dir_station = dir_stations+station+"/",")
    
#     date_SMARTS = np.loadtxt(dir_station+file_SMARTS, usecols=0, dtype=str)
#     data_SMARTS = np.loadtxt(dir_station+file_SMARTS, usecols=5)
#     dates_SMARTS = array_conse_day(date_SMARTS, [0, 2], [2, 4], [4, 6])
#     del date_SMARTS, date_MODIS
#     x_MODIS, y_SMARTS, dates = [], [], []
#     for date_SMARTS, aod_SMARTS in zip(dates_SMARTS, data_SMARTS):
#         if date_SMARTS in dates_MODIS:
#             pos = np.where(date_SMARTS == dates_MODIS)[0]
#             if data_MODIS[pos] >= 0:
#                 dates = np.append(dates, date_SMARTS)
#                 x_MODIS = np.append(x_MODIS, data_MODIS[pos])
#                 y_SMARTS = np.append(y_SMARTS, aod_SMARTS)
#     plt.ylabel("AOD$_{550nm}$")
#     plt.xticks(np.arange(0, 365*6, 365), np.arange(2015, 2021))
#     plt.plot(dates, x_MODIS, label="MODIS")
#     plt.plot(dates, y_SMARTS, label="SMARTS")
#     plt.xlim(0, 365*5)
#     plt.ylim(0, 1)
#     plt.legend(frameon=False, mode="expand", ncol=2)
#     plt.savefig(dir_station+"Graphics/AOD_MODIS_SMARTS.png")
#     plt.clf()
#     # <------------------------MODIS vs SMARTS------------------------------>
#     pars, cov = curve_fit(f=f, xdata=x_MODIS, ydata=y_SMARTS, p0=[0])
#     print(pars)
#     fit = x_MODIS*pars[0]
#     plt.title(station_name+" station")
#     plt.xlabel("MODIS AOD$_{550nm}$")
#     plt.ylabel("SMARTS AOD$_{550nm}$")
#     plt.xlim(0, 0.5)
#     plt.ylim(0, 1)
#     plt.plot(x_MODIS, fit, color="red")
#     plt.xticks(np.arange(0, 0.55, 0.05))
#     plt.yticks(np.arange(0, 1.1, 0.1))
#     plt.scatter(x_MODIS, y_SMARTS, color="black")
#     plt.savefig(dir_station+"Graphics/MODIS_SMARTS.png")
#     plt.clf()
