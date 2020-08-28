import numpy as np
import matplotlib.pyplot as plt
import datetime
from math import ceil
#<-----------------------------Funcion para obtener el dia consecutivo------------------------------>
def yymmdd(date,yy,mm,dd):
    year=int("20"+date[yy[0]:yy[1]])
    month=int(date[mm[0]:mm[1]])
    day=int(date[dd[0]:dd[1]])
    conse_day=(datetime.date(year,month,day)-datetime.date(2015,1,1)).days
    return conse_day
#<---------------------------Funcion para obtenr un array de dias consecutivos------------------->
def array_conse_day(date_list,yy,mm,dd):
    dates=[]
    for date in date_list:
        dates=np.append(dates,yymmdd(date,yy,mm,dd))
    return dates
#<-----------------------------------Localizacion de los archivos de datos-------------------------->
dir_arc="../Archivos/";dir_station="../Stations/noroeste/"
file_MODIS="MODIS-AOD.csv";file_SMARTS="DataAOD.txt"
#<---------------------------------------Lectur
date_MODIS=np.loadtxt(dir_arc+file_MODIS,skiprows=1,usecols=0,dtype=str,delimiter=",")
data_MODIS=np.loadtxt(dir_arc+file_MODIS,skiprows=1,usecols=2,delimiter=",")
dates_MODIS=array_conse_day (date_MODIS,[2,4],[5,7],[8,10])
date_SMARTS=np.loadtxt(dir_station+file_SMARTS,usecols=0,dtype=str)
data_SMARTS=np.loadtxt(dir_station+file_SMARTS,usecols=5)
dates_SMARTS=array_conse_day(date_SMARTS,[0,2],[2,4],[4,6])
del date_SMARTS,date_MODIS
x_MODIS,y_SMARTS=[],[]
for date_SMARTS,aod_SMARTS in zip(dates_SMARTS,data_SMARTS):
    if date_SMARTS in dates_MODIS:
        pos=np.where(date_SMARTS==dates_MODIS)[0]
        if data_MODIS[pos]>=0:
            x_MODIS=np.append(x_MODIS,data_MODIS[pos])
            y_SMARTS=np.append(y_SMARTS,aod_SMARTS)
print(np.size(x_MODIS))
check=0
for i in range(np.size(x_MODIS)):
    if x_MODIS[i]<0.05:
        check+=1
print(check)
plt.xlabel("AOD MODIS");plt.ylabel("AOD SMARTS")
plt.scatter(x_MODIS,y_SMARTS)
#plt.show()