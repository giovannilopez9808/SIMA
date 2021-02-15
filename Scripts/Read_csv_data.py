# <-----------Libreria para leer el archivo xls---------------->
from pandas import read_csv
from functions import *


# <--------Localizacion de la carpeta--------->
dir_archivos = "../Archivos/"
dir_stations = "../Stations/"
files_data = ["2015", "2016", "2017", "2018", "2019", "2020"]
type_data = "SR"
# <--------------Ciclo para analizar todos los archivos----------->
for file_data in files_data:
    print("Analizando archivo "+file_data)
    # Apertura del archivo de excel
    data = read_csv(dir_archivos+file_data+".csv",low_memory=False)
    data = data.fillna(0)
    keys=data.keys()
    # Ciclo para leer las columnas
    for key in keys:
        # Lectura del nombre de la estacion
        station = (key.split(".")[0]).lower()
        param = data[key][0]
        if param == type_data:
            dir_station = dir_stations+station+"/"
            # Creacion de la carpeta
            mkdir(name=station, path=dir_stations)
            mkdir(name="Mediciones", path=dir_station)
            # Ciclo para variar los dias de las mediciones
            n_rows = (data[key].size-2)//24
            for row in range(n_rows):
                # Apertura del archivo donde se guardara la medicion de un día
                date = consecutiveday2yymmdd(row,int(file_data))
                file = open(dir_station+"Mediciones/" +
                            date+".txt", "w")
                # Ciclo que varia las horas
                for hour in range(24):  # Lectura de la medicion
                    med_loc = row*24+hour+2
                    values = data[key][med_loc]
                    values = save_measurement(values)
                    # Escritura del archivo
                    file.write(str(hour+0.5)+" "+values+"\n")
                # Cierre del archivo
                file.close()
