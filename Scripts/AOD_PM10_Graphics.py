import numpy as np
import matplotlib.pyplot as plt
import datetime
from math import ceil
from scipy.optimize import curve_fit
# <----------------------------Funcion de linea recta----------------------------------->


def f(x, m):
    return m*x
# <-----------------------------Funcion para obtener el dia consecutivo------------------------------>


def yymmdd(date, yy, mm, dd):
    year = int("20"+date[yy[0]:yy[1]])
    month = int(date[mm[0]:mm[1]])
    day = int(date[dd[0]:dd[1]])
    conse_day = (datetime.date(year, month, day) -
                 datetime.date(2015, 1, 1)).days
    return conse_day
# <---------------------------Funcion para obtenr un array de dias consecutivos------------------->


def value_conse_day(date_list, yy, mm, dd):
    dates = []
    for date in date_list:
        dates = np.append(dates, yymmdd(date, yy, mm, dd))
    return dates
# ---------------Funcion que obtiene el PM de la medicion SIMA-------------------->


def PM_array(array_date, array_data):
    array_conse_day, array_data_value = [], []
    arrary_conse_day_all, array_data_value_all = [], []
    for PM, date in zip(array_data, array_date):
        conse_day = yymmdd(date, [2, 4], [5, 7], [8, 10])
        hour = int(date[11:13])
        if hour == 13:
            if PM != "":
                array_data_value = np.append(array_data_value, float(PM))
                array_conse_day = np.append(array_conse_day, conse_day)
    return array_conse_day, array_data_value


stations = ["noroeste", "noreste"]
titles = ["Noroeste", "Noreste"]
dir_arc = "../Archivos/"
dir_Graphics = "Graphics/"
file_PM10 = "PM10_2020.csv"
file_SMARTS = "DataAOD_moderate.txt"
fig, axs = plt.subplots(1, 2, figsize=(8, 5))
for station, title, ax in zip(stations, titles, axs):
    # <-----------------------------------Localizacion de los archivos de datos-------------------------->
    dir_station = "../Stations/"+station+"/"
    # <---------------------------------------Lectur
    date_PM10, data_PM10 = np.loadtxt(
        dir_arc+file_PM10, skiprows=1, usecols=[0, 2], dtype=str, delimiter=",", unpack=True)
    # <-----------------------------------------Datos y dias del SIMA------------------------------------>
    dates_PM10, data_PM10 = PM_array(date_PM10, data_PM10)
    # <----------------------------------------------Datos SMARTS------------------------------------->
    date_SMARTS = np.loadtxt(dir_station+file_SMARTS, usecols=0, dtype=str)
    data_SMARTS = np.loadtxt(dir_station+file_SMARTS, usecols=5)
    dates_SMARTS = value_conse_day(date_SMARTS, [0, 2], [2, 4], [4, 6])
    del date_SMARTS, date_PM10
    x_PM10, y_SMARTS, dates, dates_n = [], [], [], []
    for date_SMARTS, aod_SMARTS in zip(dates_SMARTS, data_SMARTS):
        if date_SMARTS in dates_PM10:
            pos = np.where(date_SMARTS == dates_PM10)[0]
            if data_PM10[pos] >= 0:
                x_PM10 = np.append(x_PM10, data_PM10[pos])
                y_SMARTS = np.append(y_SMARTS, aod_SMARTS)
                dates_n = np.append(dates_n, date_SMARTS)
# <---------------------------------------Fit------------------------------------------------------>
    pars, cov = curve_fit(f=f, xdata=x_PM10, ydata=y_SMARTS, p0=[0])
# <--------------------------------------linea recta---------------------------------------->
    fit = (np.array([0, 350]))*pars[0]
# <-----------------------------------Limite de los ejes y ticks----------------------------->
    ax.set_xlim(0, 350)
    ax.set_ylim(0, 1)
    if ax == axs[0]:
        ax.set_yticks(np.arange(0, 1.1, 0.1))
        ax.set_ylabel("SMARTS AOD$_{550nm}$", fontsize="large")
    else:
        ax.set_yticks([])
    ax.set_xticks(np.arange(0, 400, 50))
    ax.set_xticklabels(np.arange(0, 400, 50), rotation=45)
# <-----------------------------------Plot del fit-------------------------------------------------->
    ax.plot([0, 350], fit, ls="--", c="#114b5f",
            label="$y="+str(np.round(pars[0], 4))+"x$")
# <----------------------------------Plot de los datos---------------------------------------->
    ax.scatter(x_PM10, y_SMARTS, c="#88d498")
    ax.set_title("Estacion "+title)
    ax.legend(frameon=False)
fig.text(0.5, 0.025, "SIMA PM$_{10}$", va="center", fontsize="large")
plt.subplots_adjust(left=0.1, bottom=0.152, right=0.957,
                    top=0.912, wspace=0.079, hspace=0.2)
plt.savefig("../"+dir_Graphics+"AODvsPM10.png", dpi=400)
