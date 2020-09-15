import numpy as np 
import matplotlib.pyplot as plt
#<------------------------------Funcion que realiza el conteo de las mediciones----------------->
def hist(data,divs):
    data_hist=[]
    zeros_i=np.size(np.where(data<0)[0])
    zeros=zeros_i
    for div in divs:
        count=np.size(np.where(data<=div)[0])-zeros
        zeros+=count
        data_hist=np.append(data_hist,count)
    n_data=zeros-zeros_i
    data_hist=data_hist/n_data*100
    return data_hist
#<---------------------------------Funcion que grafica las barras------------------->
def hist_plot(data1,data2,path,title):
    fig, ax = plt.subplots()
    ax.set_ylabel("Frequency (%)")
    x=np.arange(np.size(data1))
    width =0.75 
    ax.plot(x,data2,width,c="green",ls="--")
    ax.set_ylim(0,70)
    ax.set_xlim(-1,10)
    plot_grid(ax)
    ax.set_xlabel("AOD$_{550nm}$")
    rects1=ax.bar(x,data1,width,label='SMARTS',facecolor="purple",alpha=0.5)
    autolabel(ax,rects1)    
    plt.xticks(x+0.5,div)
    plt.title(title+" 2015-2019")
    ax.scatter(x,data2,c="green",label="MODIS")
    plt.legend(frameon=False,ncol=2,mode='expand')
    plt.savefig(path+'Graphics/AOD_hist.png')
def plot_grid(ax):
    y_levels=np.arange(5,75,5)
    for y_level in y_levels:
        if y_level%10==0:
            alpha=0.5
        else:
            alpha=1
        ax.plot([-1,10],[y_level,y_level],ls="--",c="grey",alpha=alpha)
#<------------------------Funcion que grafica los valores de cada barra------------->
def autolabel(ax,rects):
    for rect in rects:
        height =round(rect.get_height(),2)
        ax.annotate('{}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0,3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom',)
#<-------------------------------Direccion de los archivos------------------------>
dir="../Archivos/"
#<----------Numero de divisiones, cota inferior y superior del conteo-------------->
n_bins=10;bin_i=0.1;bin_f=1.1
#<---------------------------Numero de divisiones-------------------------->
n_div=(bin_f-bin_i)/n_bins
div=np.round(np.arange(bin_i,bin_f,n_div),2)
#<--------------------------Estaciones por analizar---------------------------->
stations=['noroeste','noreste']
stations_english=["NW","NE"]
#<---------------------------Direcciones y nombres de los archivos de AOD-SMARTS----------------->
dir_stations='../Stations/';arc_data_SMARTS='DataAOD_moderate.txt'
data_MODIS=np.loadtxt(dir+"MODIS-AOD.csv",delimiter=",",skiprows=1,usecols=2)
MODIS_hist=hist(data_MODIS,div)
for station,station_english in zip(stations,stations_english):
    folder=dir_stations+station+'/'
    data_SMARTS=np.loadtxt(folder+arc_data_SMARTS,usecols=5)
    SMARTS_hist=hist(data_SMARTS,div)
    hist_plot(SMARTS_hist,MODIS_hist,folder,station_english)