import numpy as np 
import matplotlib.pyplot as plt
dir="../Archivos/"
data_MODIS=np.loadtxt(dir+"MODIS-AOD.csv",delimiter=",",skiprows=1,usecols=2)
n_data=np.size(data_MODIS)
plt.scatter(np.arange(n_data),data_MODIS,marker=".")
plt.ylim(0,)
plt.xlim(0,365*5)
plt.xticks(np.arange(0,365*6,365),np.arange(2015,2021,1))
plt.savefig("../Graphics/AOD_MODIS_Full.png")