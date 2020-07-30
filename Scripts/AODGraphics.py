import numpy as np
import matplotlib.pyplot as plt
import datetime
car="../Stations/noroeste/"
data=np.loadtxt(car+"AOD2.txt",dtype=str,usecols=[0,1])
n=np.size(data[:,0])
date=np.zeros(n)
dat=np.zeros(n)
for i in range(n):
    year=int("20"+data[i,0][0:2])
    month=int(data[i,0][2:4])
    day=int(data[i,0][4:6])
    date[i]=(datetime.date(year,month,day)-datetime.date(2015,1,1)).days
    dat[i]=round(float(data[i,1]),3)
plt.ylim(0,1)
#plt.xlim((2019-2015)*365,365+(2019-2015)*365)
plt.xticks(np.arange(0,365*5,365),np.arange(2015,2020,1))
plt.title("2019")
plt.plot(date,dat)
plt.show()