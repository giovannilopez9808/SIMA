# <-----------Libreria para leer el archivo xls---------------->
from functions import *
import xlrd


# <--------Localizacion de la carpeta--------->
dir_archivos = "../Archivos/"
dir_stations = "../Stations/"
files_data = ["2015", "2016-2018", "2016-2019","2020"]
type_data = "SR"
# <--------------Ciclo para analizar todos los archivos----------->
for file_data in files_data:
    print("Analizando archivo "+file_data)
    # Apertura del archivo de excel
    data = xlrd.open_workbook(dir_archivos+file_data+".xlsx")
    # Lectura del sheet
    data_sheet = data.sheet_by_index(0)
    # Ciclo para leer las columnas
    for col in range(2, data_sheet.ncols):
        # Lectura del nombre de la estacion
        station = str(data_sheet.cell_value(0, col)).lower()
        param = str(data_sheet.cell_value(1, col))
        if param == type_data:
            dir_station = dir_stations+station+"/"
            # Creacion de la carpeta
            mkdir(name=station, path=dir_stations)
            mkdir(name="Mediciones", path=dir_station)
            # Ciclo para variar los dias de las mediciones
            n_rows = int((data_sheet.nrows-3)/24)
            for row in range(n_rows):
                # Apertura del archivo donde se guardara la medicion de un día
                date = int(data_sheet.cell_value(row*24+3, 0))
                date = xlsxdate2date(date)
                file = open(dir_station+"Mediciones/" +
                            date+".txt", "w")
                # Ciclo que varia las horas
                for hour in range(24):  # Lectura de la medicion
                    med_loc = row*24+hour+3
                    data = data_sheet.cell_value(med_loc, col)
                    data = save_measurement(data)
                    # Escritura del archivo
                    file.write(str(hour+0.5)+" "+data+"\hour")
                # Cierre del archivo
                file.close()
