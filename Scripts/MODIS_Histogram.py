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
def hist_plot(data1,data2,path):
    fig, ax = plt.subplots(figsize=(9,7))
    x=np.arange(np.size(data1))
    width =0.5 
    plt.ylim(0,100)
    plt.xticks(x,div)
    rects1=ax.bar(x-width/2,data1,width,label='SMARTS',facecolor="purple")
    rects2=ax.bar(x+width/2,data2,width,label='MODIS',facecolor="green")
    plt.legend(frameon=False,ncol=2,mode='expand')
    autolabel(ax,rects1)
    autolabel(ax,rects2)
    plt.savefig(path+'Graphics/AOD_hist.png')
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
n_bins=5;bin_i=0.2;bin_f=1.2
#<---------------------------Numero de divisiones-------------------------->
n_div=(bin_f-bin_i)/n_bins
div=np.round(np.arange(bin_i,bin_f,n_div),2)
#<--------------------------Estaciones por analizar---------------------------->
stations=['noroeste','noreste']
#<---------------------------Direcciones y nombres de los archivos de AOD-SMARTS----------------->
dir_stations='../Stations/';arc_data_SMARTS='DataAOD_moderate.txt'
data_MODIS=np.loadtxt(dir+"MODIS-AOD.csv",delimiter=",",skiprows=1,usecols=2)
MODIS_hist=hist(data_MODIS,div)
for station in stations:
    folder=dir_stations+station+'/'
    data_SMARTS=np.loadtxt(folder+arc_data_SMARTS,usecols=5)
    SMARTS_hist=hist(data_SMARTS,div)
    hist_plot(SMARTS_hist,MODIS_hist,folder)