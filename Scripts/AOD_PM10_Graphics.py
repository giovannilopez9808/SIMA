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
def value_conse_day(date_list,yy,mm,dd):
    dates=[]
    for date in date_list:
        dates=np.append(dates,yymmdd(date,yy,mm,dd))
    return dates
#---------------Funcion que obtiene el PM de la medicion SIMA-------------------->
def PM_array(array_date,array_data):
    array_conse_day,array_data_value=[],[]
    for PM,date in zip(array_data,array_date):
        conse_day=yymmdd(date,[2,4],[5,7],[8,10])
        hour=int(date[11:13])
        if hour==13:
            if PM!="":
                array_data_value=save_values(array_data_value,float(PM))
                array_conse_day=save_values(array_conse_day,conse_day)
    return array_conse_day,array_data_value
def save_values(array,value):
    array=np.append(array,value)
    return array
stations=["noroeste","noreste"]
file_PM10="PM10_2020.csv";file_SMARTS="DataAOD_moderate.txt";dir_arc="../Archivos/"
for station in stations:
    #<-----------------------------------Localizacion de los archivos de datos-------------------------->
    dir_station="../Stations/"+station+"/"
    #<---------------------------------------Lectur
    date_PM10,data_PM10=np.loadtxt(dir_arc+file_PM10,skiprows=1,usecols=[0,2],dtype=str,delimiter=",",unpack=True)
    dates_PM10,data_PM10=PM_array(date_PM10,data_PM10)
    date_SMARTS=np.loadtxt(dir_station+file_SMARTS,usecols=0,dtype=str)
    data_SMARTS=np.loadtxt(dir_station+file_SMARTS,usecols=5)
    dates_SMARTS=value_conse_day(date_SMARTS,[0,2],[2,4],[4,6])
    del date_SMARTS,date_PM10
    x_PM10,y_SMARTS=[],[]
    for date_SMARTS,aod_SMARTS in zip(dates_SMARTS,data_SMARTS):
        if date_SMARTS in dates_PM10:
            pos=np.where(date_SMARTS==dates_PM10)[0]
            if data_PM10[pos]>=0:
                x_PM10=np.append(x_PM10,data_PM10[pos])
                y_SMARTS=np.append(y_SMARTS,aod_SMARTS)
    plt.xlabel("PM10");plt.ylabel("AOD SMARTS")
    plt.scatter(x_PM10,y_SMARTS)
    plt.savefig(dir_station+"Graphics/AOD_PM10.png")
    plt.clf()