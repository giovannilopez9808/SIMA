import numpy as np
import matplotlib.pyplot as plt
from os import listdir
dir="../Stations/"
stations=["NORESTE","NOROESTE"]
for station in stations:
    car=dir+station+"/"
    dates=listdir(car)
    for date in dates:
        data=np.loadtxt(car+"/"+date)
        plt.scatter(data[:,0],data[:,1])
        plt.xlim(6,19)
        plt.title(station+" "+date)
        plt.show()