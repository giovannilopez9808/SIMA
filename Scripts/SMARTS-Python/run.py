import numpy as np
import math 
import os
#<-------------------------Funcion que le da el formato a SMARTS------------------------>
def escribir(lon_i,lon_f,day,month,year,hour,ozono,aod):
    file=open("data.inp.txt","w")
    file.write(" 'AOD="+str(aod)+"'\n")
    #<----------------------Card 2------------------>
    file.write(" 2\n")
    #<---------------------Card 2a------------------->
    #<--------------lat,altit,height----------------->
    file.write(" 25.750 0.512 0\n")
    #<----------------------Card 3------------------->
    #<---------------------IATMOS-------------------->
    file.write(" 1\n")
    #<-----------------------Card 3a----------------->
    file.write(" 'USSA'\n")
    #<-----------------------Card 4------------------->
    #<------------------------H2O-------------------->
    file.write(" 1\n")
    #<------------------------Card 4a----------------->
    file.write(" 0\n")
    #<-----------------------Card 5---------------------->
    #<-----------------------Ozono-------------------------->
    file.write(" 1 "+str(round(ozono/1000,4))+"\n")
    #<-------------------------Card 6------------------>
    file.write(" 0\n")
    #<-------------------------Card 6a----------------->
    file.write(" 3\n")
    #<-------------------------Card 7----------------------->
    #<-------------------------Co2------------------------->
    file.write(" 390\n")
    #<------------------------------Card 7a------------------->
    file.write(" 0\n")
    #<------------------------Card 8------------------------->
    file.write(" 'S&F_URBAN'\n")
    #<--------------------------Card 9------------------------>
    file.write(" 5\n")
    #<-----------------------------Card 9a------------------------->
    file.write(" "+str(aod)+" 2\n")
    #<----------------------------Card 10----------------------->
    file.write(" 18\n")
    #<-------------------------Card 10b----------------------->
    file.write(" 1\n")
    #<-------------------------------Card 10d-------------------->
    #<------------------IALBDG, TILT,WAZIM------------------------>
    file.write(" 51 37. 180.\n")
    #<------------------------------Card 11---------------------------->
    #<----------------Wave min, Wave max, suncor, solar cons---------->
    file.write(" "+str(lon_i)+" "+str(lon_f)+" 1 1366.1\n")
    #<-------------------------------Card 12---------------------------->
    file.write(" 2\n")
    #<----------------------------------Card 12a------------------------>
    #<-----------------------Wave min, Wave max, inter wave----------->
    file.write(" "+str(lon_i)+" "+str(lon_f)+" 1\n")
    #<-----------------------------Card 12b----------------------_>
    file.write(" 1\n")
    #<------------------------------Card 12c--------------------------------->
    file.write(" 4\n")
    #<-------------------------------------Card 13----------------------->
    file.write(" 1\n")
    #<---------------------------------------Card 13a-------------------------->
    #<-------------- slope, apert, limit------------------------------------>
    file.write(" 0 2.9 0\n")
    #<---------------------------------------Card 14------------------------>
    file.write(" 0\n")
    #<-------------------------------------------Card 15------------------------->
    file.write(" 0\n")
    #<-------------------------------------------Card 16------------------------->
    file.write(" 1\n")
    #<-------------------------------------------Card 17------------------------->
    file.write(" 3\n")
    #<-------------------------------------------Card 17a------------------------->
    #<--------------------------------Year, month, day, hour, latit, longit, zone------------>
    file.write(" "+str(year)+" "+str(month)+" "+str(day)+" "+str(hour)+" 25.75 -100.25 -6\n")
    file.close()
def writeAOD(date,year,month,day,o3,aod,DR):
    AOD_file.write(str(int(date))+" "+str(year)+" "+str(month)+" "+str(day)+" "+str(o3)+" " 
    +str(round(aod,3))+" "+str(round(DR,2))+"\n")
#<----------------------------Lectura de los datos de entrada--------------------------------------->
car="../../Stations/"
stations=["noroeste"]
DR_lim,aod_i,aod_lim=7,0.01,1
#<------------------------Hora inicial y final del calculo-------------------------->
hour_i,hour_f=11,14
#<---------------------Longitud inicial y final del calculo---------------------->
#lon_i,lon_f=285,2800
lon_i,lon_f=400,1100
#<---------------------------Diferencia de horas y longitudes de onda------------------->
dl_i=lon_i-280+1;dh=(hour_f-hour_i);n_min=dh*60
for station in stations:
    print("Calculando estacion "+station)
    carp=car+station
    AOD_file=open(carp+"/DataAOD.txt","w")
    date,day,month,year,o3=np.loadtxt(carp+"/datos.txt",unpack=True)
    n=np.size(year)
    #<-----------------------------Ciclo para variar los dias--------------------------------------->
    for i in range(n):
        data=np.loadtxt(carp+"/Mediciones/"+str(int(date[i]))+".txt",skiprows=hour_i)
        data=np.max(data[0:dh,1])
        year_i,month_i,day_i,o3_i=int(year[i]),int(month[i]),int(day[i]),o3[i]
        if year_i!=2014:
            print("           Calculando el dia ",year_i,month_i,day_i)
            #<------------------------------Valores iniciales------------------------------------------->
            aod,var,k=aod_i,False,1
            while var==False and k<math.ceil(aod_lim/aod_i):
                resul=np.zeros(n_min)
                for min in range(n_min):
                    escribir(lon_i,lon_f,day_i,month_i,year_i,round(hour_i+min/60,4),o3_i,aod)
                    os.system("./smarts.out")
                    mod=np.loadtxt("data.ext.txt",skiprows=dl_i)
                    sum=0
                    size=np.size(mod[:,0])
                    for lon in range(size):
                        if lon==0:
                            sum+=mod[lon,1]
                        else:
                            sum+=mod[lon,1]*(mod[lon,0]-mod[lon-1,0])
                    resul[min]=sum
                    os.system("rm data*")
                #<-------------------------Posicion del valor mas alto------------------------------------>
                pos=(np.where(np.max(resul)==resul)[0])[0]
                #<-----------------------Promedio de datos minuto a minuto------------------------------>
                data_mod=np.mean(resul[pos-30:pos+31])
                DR=100*(data_mod-data)/data
                if abs(DR)<DR_lim: 
                    writeAOD(date[i],year_i,month_i,day_i,o3_i,aod,DR)
                    var=True
                else:
                    if DR<0:
                        writeAOD(date[i],year_i,month_i,day_i,o3_i,aod,DR)
                        var=True
                    else:
                        aod+=aod_i
                k+=1