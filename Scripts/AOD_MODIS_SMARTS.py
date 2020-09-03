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
stations=["noroeste","noreste"];dir_arc="../Archivos/"
file_MODIS="MODIS-AOD.csv";file_SMARTS="DataAOD_moderate.txt"
#<-----------------------------------Localizacion de los archivos de datos-------------------------->
for station in stations:
    dir_station="../Stations/"+station+"/"
    #<---------------------------------------Lectur
    date_MODIS=np.loadtxt(dir_arc+file_MODIS,skiprows=1,usecols=0,dtype=str,delimiter=",")
    data_MODIS=np.loadtxt(dir_arc+file_MODIS,skiprows=1,usecols=2,delimiter=",")
    dates_MODIS=array_conse_day (date_MODIS,[2,4],[5,7],[8,10])
    date_SMARTS=np.loadtxt(dir_station+file_SMARTS,usecols=0,dtype=str)
    data_SMARTS=np.loadtxt(dir_station+file_SMARTS,usecols=5)
    dates_SMARTS=array_conse_day(date_SMARTS,[0,2],[2,4],[4,6])
    del date_SMARTS,date_MODIS
    x_MODIS,y_SMARTS,dates=[],[],[]
    for date_SMARTS,aod_SMARTS in zip(dates_SMARTS,data_SMARTS):
        if date_SMARTS in dates_MODIS:
            pos=np.where(date_SMARTS==dates_MODIS)[0]
            if data_MODIS[pos]>=0:
                dates=np.append(dates,date_SMARTS)
                x_MODIS=np.append(x_MODIS,data_MODIS[pos])
                y_SMARTS=np.append(y_SMARTS,aod_SMARTS)
    plt.ylabel("AOD$_{550nm}$")
    plt.xticks(np.arange(0,365*6,365),np.arange(2015,2021))
    plt.plot(dates,x_MODIS,label="MODIS")
    plt.plot(dates,y_SMARTS,label="SMARTS")
    plt.xlim(0,365*5)
    plt.ylim(0,1)
    plt.legend(frameon=False,mode="expand",ncol=2)
    plt.savefig(dir_station+"Graphics/AOD_MODIS_SMARTS.png")
    plt.clf()
    plt.xlabel("AOD$_{550nm}$ MODIS");plt.ylabel("AOD$_{550nm}$ SMARTS")
    plt.scatter(x_MODIS,y_SMARTS)
    plt.savefig(dir_station+"Graphics/MODIS_SMARTS.png")
    plt.clf()