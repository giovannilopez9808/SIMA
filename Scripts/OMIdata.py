import h5py
from os import listdir
import numpy as np
import math
import datetime
# <------------Funcion que localiza la posicion en la grilla dada la posicion geografica----------------->


def loc(lon_i, lon, div):
    pos = math.ceil((lon_i-lon)/div)
    return pos
# <-----------------Funcion para obtener el numero de mes desde el dia consecutivo----------------------->


def n_month(year, year_i, day):
    month = (datetime.date(year+year_i, 1, 1) +
             datetime.timedelta(days=day)).month-1
    return month


# <--------------------------------------Parametros para variar------------------------------------------>
car = "../Archivos/OMIData/"  # Carpeta donde se encuentran los archivos
div = 0.25  # Division de grilla
lon_i, lat_i = 90, -180  # Longitud y latitud inicial del documento
lon, lat = 25+40/60, -(100+18/60)  # Longitud y latitud de la cuidad (MTY)
year_i, year_f = 2005, 2019  # Primer y ultimo año de datos
# <----------------------------Posiciones en la grilla para la ciudad------------------------------------>
pos_lon, pos_lat = loc(lon_i, lon, div), loc(lat_i, lat, div)
d_year = year_f-year_i+1
o3_annual = np.zeros([365, d_year])
o3_mean_month = np.zeros([12, 2])
files = listdir(car)
name_year = 0
# <------------------------------------Archivo resultante----------------------------------------------->
for file in files:
    carp = car+file
    year, month, day = int(file[19:23]), int(file[24:26]), int(file[26:28])
    if year != name_year:
        print("Analizando año "+str(year))
        name_year = year
    HD5 = h5py.File(carp, "r")
    data_o3 = list(
        HD5["/HDFEOS/GRIDS/OMI Column Amount O3/Data Fields/ColumnAmountO3"])
    data, n = 0, 0
    # <--------------------------------Calculo de los promedios con los vecinos------------------------>
    for i in [-1, 0, 1]:
        for j in [-1, 0, 1]:
            o3 = data_o3[pos_lat+i][pos_lon+j]

            # <--------------------------Si existe el valor, contabilizarlo---------------------------->
            if o3 > 0:
                data += o3
                n += 1
        # <----------------------Asignacion del valor si es que se realizaron mediciones------------------->
    if n != 0:
        o3 = math.ceil(data/n)
        date = (datetime.date(year, month, day)-datetime.date(year, 1, 1)).days
        if date > 364:
            date = 364
        o3_annual[date, year-year_i] = o3
    HD5.close()
# <------------------------Calculo del promedio mensual en el periodo---------------------------------->
for year in range(d_year):
    for day in range(365):
        o3 = o3_annual[day, year]
        # <--------------------------Si hubo mediciones, se contabiliza------------------------------->
        if o3 > 0:
            month = n_month(year, year_i, day)
            # <---------------------------------Registro de los datos--------------------------------->
            o3_mean_month[month, 0] += o3
            o3_mean_month[month, 1] += 1
# <------------------Calculo del promedio mensual----------------------------------------------------->
print("Calculando promedios")
for month in range(12):
    if o3_mean_month[month, 1] != 0:
        o3_mean_month[month, 0] = math.ceil(
            o3_mean_month[month, 0]/o3_mean_month[month, 1])
# <----------------------------Asignacion a los dias en que no hubo medicion-------------------------->
for year in range(d_year):
    for day in range(365):
        if o3_annual[day, year] == 0:
            month = n_month(year, year_i, day)
            o3_annual[day, year] = o3_mean_month[month, 0]
# <------------------------------Escritura del archivo final------------------------------------------>
print("Escribiendo archivo final OzonoMTY.txt")
file = open("OzonoMTY.txt", "w")
for day in range(365):
    for year in range(d_year):
        file.write(str(o3_annual[day, year])+" ")
    file.write("\n")
file.close()
