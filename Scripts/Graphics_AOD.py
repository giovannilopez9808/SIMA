import numpy as np
import matplotlib.pyplot as plt
import datetime
from math import ceil
# ---------------Funcion que obtiene el PM de la medicion SIMA-------------------->


def PM_SIMA(file_data, ncol, car, n, station):
    print("     Imprimiendo "+file_data+" del SIMA")
    dir = "../Archivos/"
    PM_measurement = np.zeros(n)
    date_sima, PM_sima = np.loadtxt(
        dir+file_data+"_2020.csv", delimiter=",", usecols=[0, ncol], skiprows=1, dtype=str, unpack=True)
    n = np.size(date_sima)
    j = 0
    for i in range(n):
        conse_day = yymmdd(date_sima, i, [2, 4], [5, 7], [8, 10])
        if conse_day in days:
            hour = int(date_sima[i][11:13])
            if hour == 13:
                if PM_sima[i] != "":
                    PM_measurement[j] = float(PM_sima[i])
                elif PM_sima[i+1] != "":
                    PM_measurement[j] = float(PM_sima[i+1])
                j += 1
    plot_data(x=days, y=PM_measurement, ylim=ceil(np.max(PM_measurement)/50)*50,
              title=station, name=file_data+"_SIMA.png", carp=car+"Graphics/", line=False)
# <--------------------Funcion que grafica del AOD y del PM------------------------------->


def plot_data(x, y, ylim, title, name, carp, line):
    plt.xlim(0, 365*5)
    plt.xticks(np.arange(0, 365*6, 365), np.arange(2015, 2021, 1))
    plt.scatter(x, y, c="#4287f5", marker=".")
    if line == True:
        plt.plot([0, 365*5], [1, 1], color="red", ls="--")
    plt.ylim(0, ylim)
    plt.savefig(carp+name)
    plt.clf()
# <-----------------------------Funcion para obtener el dia consecutivo------------------------------>


def yymmdd(date_sima, i, yy, mm, dd):
    year = int("20"+date_sima[i][yy[0]:yy[1]])
    month = int(date_sima[i][mm[0]:mm[1]])
    day = int(date_sima[i][dd[0]:dd[1]])
    conse_day = (datetime.date(year, month, day) -
                 datetime.date(2015, 1, 1)).days
    return conse_day


# <-------------------Nombre de las estaciones por graficar----------------------->
stations = ["noreste", "noroeste"]
# <-------------------Numero de columnas de los archivos del SIMA------------------>
stations_sima = [2, 4]
days_total = []
for station, station_sima in zip(stations, stations_sima):
    print("Analizando estacion "+station)
    print("     Imprimiendo AOD del SMARTS")
    car = "../Stations/"+station+"/"
    # <--------------------Dias de cielo despejado antes seleccionado------------------->
    dates = np.loadtxt(car+"DataAOD_moderate.txt", dtype=str, usecols=0)
    # <--------------------------AOD Calculado----------------------------------->
    aod = np.loadtxt(car+"DataAOD_moderate.txt", usecols=5)
    n = np.size(dates)
    days = np.ones(n)
    for i in range(n):
        days[i] = yymmdd(dates, i, [0, 2], [2, 4], [4, 6])
    days_total = np.union1d(days, days_total)
    # <------------------------------Grafia del AOD calculado por el SMARTS-------------------------->
    plot_data(x=days, y=aod, ylim=1, name="AOD_SMARTS.png",
              carp=car+"Graphics/", title=station, line=True)
    # <-------------------AOD medido por el SIMA---------------------------------------->
    PM_SIMA(file_data="PM10", ncol=station_sima, car=car, n=n, station=station)
    PM_SIMA(file_data="PM25", ncol=station_sima, car=car, n=n, station=station)
# <---------------------------Analizando datos de MODIS----------------------------->
print("Analizando AOD de MODIS")
# <------------------------------------Datos de las mediciones------------------------------->
dates_MODIS, datas_MODIS = np.loadtxt(
    "../Archivos/MODIS-AOD.csv", skiprows=1, usecols=[0, 2], unpack=True, delimiter=",", dtype=str)
AOD_MODIS = []
for date_MODIS, data_MODIS in zip(dates_MODIS, datas_MODIS):
    conse_day = yymmdd([date_MODIS], 0, [2, 4], [5, 7], [8, 10])
    if conse_day in days_total:
        AOD_MODIS = np.append(AOD_MODIS, float(data_MODIS))
# <------------------------------------------Ploteo del AOD------------------------------------------>
plot_data(x=days_total, y=AOD_MODIS, ylim=1, name="AOD_MODIS.png",
          carp="../Graphics/", title="MODIS", line=False)
