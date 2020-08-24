import numpy as np
import math 
import os
#<----------Libreria para ubicar los errores------------>
import errno
#<-------------------------Funcion que le da el formato a SMARTS------------------------>
def escribir(lon_i,lon_f,day,month,year,hour,ozono,aod):
    file=open("data.inp.txt","w")
    file.write(" 'AOD="+str(aod)+"'\n")
    file.write(" 2\n")
    file.write(" 25.750 0.512 0\n")
    file.write(" 1\n")
    file.write(" 'USSA'\n")
    file.write(" 1\n")
    file.write(" 0\n")
    file.write(" 1 "+str(round(ozono/1000,4))+"\n")
    file.write(" 1\n")
    file.write(" 390\n")
    file.write(" 0\n")
    file.write(" 'S&F_URBAN'\n")
    file.write(" 5\n")
    file.write(" "+str(aod)+" 2\n")
    file.write(" 18\n")
    file.write(" 1\n")
    file.write(" 51 37. 180.\n")
    file.write(" "+str(lon_i)+" "+str(lon_f)+" 1 1366.1\n")
    file.write(" 2\n")
    file.write(" "+str(lon_i)+" "+str(lon_f)+" 1\n")
    file.write(" 1\n")
    file.write(" 4\n")
    file.write(" 1\n")
    file.write(" 0 2.9 0\n")
    file.write(" 0\n")
    file.write(" 0\n")
    file.write(" 1\n")
    file.write(" 3\n")
    file.write(" "+str(year)+" "+str(month)+" "+str(day)+" "+str(hour)+" 25.75 -100.25 -6\n")
    file.close()
#<----------------------------Lectura de los datos de entrada--------------------------------------->
car="../../Stations/"
stations=["noreste"]
#<------------------------Hora inicial y final del calculo-------------------------->
hour_i,hour_f=8,17
#<---------------------Longitud inicial y final del calculo---------------------->
lon_i,lon_f=285,2800
#<---------------------------Diferencia de horas y longitudes de onda------------------->
dl_i=lon_i-280+1;dh=(hour_f-hour_i);n_min=dh*60
for station in stations:
    carp=car+station
    try: #Direccion y nombre de la carpeta
        os.mkdir(carp+"/ResultsSMARTS")
    #Verificacion si la carpeta ya existe o no
    except OSError as e: #Si no se produce error realizar nada
        if e.errno!=errno.EEXIST:
            raise
    dates,year,month,day,o3,aod,dr=np.loadtxt(carp+"/DataAOD_moderate.txt",unpack=True)
    n=np.size(year)
    carp+="/ResultsSMARTS/"
    #<-----------------------------Ciclo para variar los dias--------------------------------------->
    for date,year_i,month_i,day_i,o3_i,aod_i in zip(dates,year,month,day,o3,aod):
        date,year_i,month_i,day_i,o3_i=str(int(date)),int(year_i),int(month_i),int(day_i),float(o3_i)
        if year_i!=2014:
            print("Calculando el dia ",year_i,month_i,day_i)
            file_date=open(carp+date+".txt","w")
            for min in range(n_min):
                escribir(lon_i,lon_f,day_i,month_i,year_i,round(hour_i+min/60,4),o3_i,aod_i)
                os.system("./smarts.out")
                mod=np.loadtxt("data.ext.txt",skiprows=dl_i)
                sum=0
                size=np.size(mod[:,0])
                for lon in range(size):
                    if lon==0:
                        sum+=mod[lon,1]
                    else:
                        sum+=mod[lon,1]*(mod[lon,0]-mod[lon-1,0])
                os.system("rm data*")
                file_date.write(str(round(hour_i+min/60,4))+" "+str(round(sum))+"\n")
            file_date.close()