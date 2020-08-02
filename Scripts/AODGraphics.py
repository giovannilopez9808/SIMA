import numpy as np
import matplotlib.pyplot as plt
import datetime
car="../Stations/noreste/"
dates=np.loadtxt(car+"DataAOD.txt",dtype=str,usecols=0)
aod=np.loadtxt(car+"DataAOD.txt",usecols=5)
n=np.size(dates)
days=np.ones(n)
for i in range(n):
    year=int("20"+dates[i][0:2])
    month=int(dates[i][2:4])
    day=int(dates[i][4:6])
    days[i]=(datetime.date(year,month,day)-datetime.date(2015,1,1)).days
plt.ylim(0,1)
#plt.xlim((2019-2015)*365,365+(2019-2015)*365)
plt.xticks(np.arange(0,365*5,365),np.arange(2015,2020,1))
plt.title("Noreste")
plt.plot(days,aod)
plt.plot([0,365*5],[0.8,0.8],color="red",ls="--")
plt.show()