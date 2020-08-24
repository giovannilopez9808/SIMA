import numpy as np
import matplotlib.pyplot as plt
import datetime
#---------------Funcion que obtiene el PM de la medicion SIMA-------------------->
def AODGraphics(file_data,label):
    dir="../Stations/noreste/"
    date_sima=np.loadtxt(dir+file_data,usecols=0,dtype=str)
    AOD=np.loadtxt(dir+file_data,usecols=5)
    n=np.size(date_sima)
    days=np.zeros(n)
    for i in range(n):
        days[i]=yymmdd(date_sima,i,[0,2],[2,4],[4,6])
    plot_data(x=days,y=AOD,label=label)
#<--------------------Funcion que grafica del AOD y del PM------------------------------->
def plot_data(x,y,label):
    plt.xlim(0,365*5)
    plt.xticks(np.arange(0,365*6,365),np.arange(2015,2021,1))
    plt.scatter(x,y,marker=".",label=label)
    plt.plot([0,365*5],[0.8,0.8],color="red",ls="--")
    plt.ylim(0,1)
#<-----------------------------Funcion para obtener el dia consecutivo------------------------------>
def yymmdd(date_sima,i,yy,mm,dd):
    year=int("20"+date_sima[i][yy[0]:yy[1]])
    month=int(date_sima[i][mm[0]:mm[1]])
    day=int(date_sima[i][dd[0]:dd[1]])
    conse_day=(datetime.date(year,month,day)-datetime.date(2015,1,1)).days
    return conse_day
files=["DataAOD.txt","DataAOD_0.txt"]
labels=["Clear","Moderate"]
for file,label in zip(files,labels):
    AODGraphics(file_data=file,label=label)
plt.legend(frameon=False,mode="expand",ncol=2)
plt.show()