import numpy as np
import matplotlib.pyplot as plt
import os
#<----------------------------Lectura de los datos de entrada--------------------------------------->
car="../../Stations/"
stations=["noreste","noroeste"]
for station in stations:
    carp=car+station
    dates=np.loadtxt(carp+"/DataAOD.txt",usecols=0,dtype=str)
    os.mkdir(carp+"/Graphics")
    for date in dates:
        med=np.loadtxt(carp+"/Mediciones/"+date+".txt")
        mod=np.loadtxt(carp+"/ResultsSMARTS/"+date+".txt")
        plt.plot(med[:,0],med[:,1],label="Measurement",lw=3)
        plt.plot(mod[:,0],mod[:,1],label="SMARTS Model",lw=3)
        plt.ylabel("Irradianca VIS-NIR-MIR (W/m$^2$)")
        plt.xlabel("Local hour (h)")
        plt.title(date)
        plt.legend(ncol=2,frameon=False)
        plt.savefig(carp+"/Graphics/"+date+".png")
        plt.clf()