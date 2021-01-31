import numpy as np
import datetime
data=np.loadtxt("OzonoMTY.txt",dtype=str)
years=np.arange(2005,2020)
file=open("Ozono.csv","w")
file.write(",")
for i in range(14):
    file.write(str(years[i])+",")
file.write(str(years[-1])+"\n")
day_i=datetime.date(2019,1,1)
for j in range(365):
    date=day_i+datetime.timedelta(days=j)
    day=str(date.day)
    day="0"*(2-len(day))+day
    month=str(date.month)
    month="0"*(2-len(month))+month
    date=month+"/"+day
    file.write(date+",")
    for i in range(15):
        if i<14:
            file.write(data[j,i]+",")
        else:
            file.write(data[j,i]+"\n")
file.close()