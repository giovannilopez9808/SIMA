import numpy as np
import matplotlib.pyplot as plt
import datetime
from math import ceil
from scipy.optimize import curve_fit
#<----------------------------Funcion de linea recta----------------------------------->
def f(x,m):
    return m*x
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
    arrary_conse_day_all,array_data_value_all=[],[]
    for PM,date in zip(array_data,array_date):
        conse_day=yymmdd(date,[2,4],[5,7],[8,10])
        hour=int(date[11:13])
        if hour==13:
            if PM!="":
                array_data_value=np.append(array_data_value,float(PM))
                array_conse_day=np.append(array_conse_day,conse_day)
    return array_conse_day,array_data_value

stations=["noroeste","noreste"];titles=["Noroeste","Noreste"];alturas=[0.52,0.95]
dir_arc="../Archivos/";dir_Graphics="Graphics/"
file_PM10="PM10_2020.csv";
file_SMARTS="DataAOD_moderate.txt"
fig,axs=plt.subplots(2)
for station,title,ax,altura in zip(stations,titles,axs,alturas):
    #<-----------------------------------Localizacion de los archivos de datos-------------------------->
    dir_station="../Stations/"+station+"/"
    #<---------------------------------------Lectur
    date_PM10,data_PM10=np.loadtxt(dir_arc+file_PM10,skiprows=1,usecols=[0,2],dtype=str,delimiter=",",unpack=True)
    #<-----------------------------------------Datos y dias del SIMA------------------------------------>
    dates_PM10,data_PM10=PM_array(date_PM10,data_PM10)
    #<----------------------------------------------Datos SMARTS------------------------------------->
    date_SMARTS=np.loadtxt(dir_station+file_SMARTS,usecols=0,dtype=str)
    data_SMARTS=np.loadtxt(dir_station+file_SMARTS,usecols=5)
    dates_SMARTS=value_conse_day(date_SMARTS,[0,2],[2,4],[4,6])
    del date_SMARTS,date_PM10
    x_PM10,y_SMARTS_clear,y_SMARTS,dates,dates_n=[],[],[],[],[]
    for date_SMARTS,aod_SMARTS in zip(dates_SMARTS,data_SMARTS):
        if date_SMARTS in dates_PM10:
            pos=np.where(date_SMARTS==dates_PM10)[0]
            if data_PM10[pos]>=0:
                x_PM10=np.append(x_PM10,data_PM10[pos])
                y_SMARTS=np.append(y_SMARTS,aod_SMARTS)
                dates_n=np.append(dates_n,date_SMARTS)
    ax2=ax.twinx()
    ax.scatter(dates_n,x_PM10,color="#114B5F",label="SIMA PM$_{10}$",marker=".",alpha=0.5)
    ax.set_xlim(0,365*5);ax.set_ylim(0,350)
    ax2.set_ylim(0,0.1)
    ax2.set_yticks(np.arange(0,1,0.2));ax.set_yticks(np.arange(0,400,50))
    if ax==axs[1]:
        ax.set_xticks(np.arange(0,365*6,365))
        ax.set_xticklabels(np.arange(2015,2021),rotation=60)
    else:
        ax.set_xticks([])
    ax2.scatter(dates_n,y_SMARTS,color="#DDA15E",label="AOD",marker=".",alpha=0.5)
    if ax==axs[0]:
        ax.legend(frameon=False,loc=1,bbox_to_anchor=(0., 1.15,1,0.02))
        ax2.legend(frameon=False,loc=2,bbox_to_anchor=(0., 1.15,1,0.02))
    fig.text(0.40,altura,"Estación "+title,va="center",fontsize="large")
#<-----------------------------------------Shared ylabel---------------------------------->
fig.text(0.035, 0.5, 'PM$_{10}$', va='center', rotation='vertical',fontsize="large")
fig.text(0.95, 0.5, 'AOD$_{550nm}$', va='center', rotation=-90,fontsize="large")
axs[1].set_xlabel("Año",fontsize="large")
plt.subplots_adjust(left=0.125, bottom=0.167, right=0.879, top=0.88, wspace=0.2, hspace=0.188)
plt.savefig("../"+dir_Graphics+"AODsandPM10.png",dpi=400)
plt.show()
plt.clf()