import numpy as np
import datetime
o3data=np.loadtxt("../Archivos/OzonoMTY.txt")
stations=["noroeste"]
dir="../Stations/"
for station in stations:
    car=dir+station
    dates=np.loadtxt(car+"/days.txt",dtype=str)
    n=np.size(dates)
    file=open(car+"/datos.txt","w")
    file.write(str(n)+"\n")
    for date in dates:
        year,month,day=int("20"+date[0:2]),int(date[2:4]),int(date[4:6])
        day2=(datetime.date(year,month,day)-datetime.date(year,1,1)).days
        o3=o3data[day2,year-2005]
        file.write(date+" "+str(day)+" "+str(month)+" "+str(year)+" "+str(o3)+"\n")
    file.close()
