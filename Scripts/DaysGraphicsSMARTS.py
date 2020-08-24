import numpy as np
import matplotlib.pyplot as plt
import os
#<----------Libreria para ubicar los errores------------>
import errno
#<----------------------------Lectura de los datos de entrada--------------------------------------->
car="../Stations/"
stations=["noreste"]
for station in stations:
    print("Graficando estacion "+station)
    carp=car+station
    dates,aods=np.loadtxt(carp+"/DataAOD_moderate.txt",usecols=[0,5],dtype=str,unpack=True)
    try: #Direccion y nombre de la carpeta
        os.mkdir(carp+"/Graphics")
    #Verificacion si la carpeta ya existe o no
    except OSError as e: #Si no se produce error realizar nada
        if e.errno!=errno.EEXIST:
            raise
    for date,aod in zip(dates,aods):
        med=np.loadtxt(carp+"/Mediciones/"+date+".txt")
        mod=np.loadtxt(carp+"/ResultsSMARTS/"+date+".txt")
        plt.plot(med[:,0],med[:,1],label="Measurement",lw=3)
        plt.plot(mod[:,0],mod[:,1],label="SMARTS Model",lw=3)
        plt.ylabel("UV-VIS-NIR irradiance (W/m$^2$)")
        plt.xlabel("Local hour (h)")
        plt.xlim(8,17)
        plt.ylim(0,1200)
        plt.title("Day "+date+"\n AOD: "+aod)
        plt.legend(ncol=2,frameon=False,mode="expand")
        plt.savefig(carp+"/Graphics/"+date+".png")
        plt.clf()