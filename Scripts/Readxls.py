# <-----------Libreria para leer el archivo xls---------------->
import xlrd
import numpy as np
# <-------------Librerias para leer archivos y crear carpetas------------>
from os import listdir
from os.path import isfile, join
import os
import math
import datetime
# <----------Libreria para ubicar los errores------------>
import errno
#


def xlsxdate(xldate):
    return (datetime.datetime(1899, 12, 30) + datetime.timedelta(days=xldate))
#


def dateformat(date):
    if date < 10:
        date = "0"+str(date)
    else:
        date = str(date)
    return date
# <--------Funcion que lee los nombres de los archivos que hay en una carpeta--------->


def ls(ruta):
    return [arch for arch in listdir(ruta) if isfile(join(ruta, arch))]


def CreateFolder(path, name):
    # Creacion de la carpeta
    try:  # Direccion y nombre de la carpeta
        os.mkdir(path+name)
    # Verificacion si la carpeta ya existe o no
    except OSError as e:  # Si no se produce error realizar nada
        if e.errno != errno.EEXIST:
            raise


# <--------Localizacion de la carpeta--------->
dir, stadir = "../Archivos/", "../Stations/"
arc = ["2015", "2016-2018", "2016-2019"]
cont = "SR"
# <--------------Ciclo para analizar todos los archivos----------->
for arch in arc:
    print("Analizando archivo "+arch)
    # Apertura del archivo de excel
    data = xlrd.open_workbook(dir+arch+".xlsx")
    # Lectura del sheet
    sheet = data.sheet_by_index(0)
    # Ciclo para leer las columnas
    for j in range(sheet.ncols-2):
        # Lectura del nombre de la estacion
        station = str(sheet.cell_value(0, j+2)).lower()
        param = str(sheet.cell_value(1, j+2))
        if param == cont:
            # Creacion de la carpeta
            CreateFolder(path=stadir, name=station)
            CreateFolder(path=stadir+station, name="/Mediciones")
            # Ciclo para variar los dias de las mediciones
            for k in range(int((sheet.nrows-3)/24)):
                # Apertura del archivo donde se guardara la medicion de un día
                date = xlsxdate(int(sheet.cell_value(k*24+3, 0)))
                day, month, year = date.day, date.month, date.year
                day, month, year = dateformat(day), dateformat(
                    month), (dateformat(year))[2:4]
                file = open(stadir+station+"/Mediciones/" +
                            year+month+day+".txt", "w")
                # Ciclo que varia las horas
                for n in range(24):  # Lectura de la medicion
                    med = sheet.cell_value(k*24+n+3, j+2)
                    if med == "":
                        med = 0
                    if math.isnan(med) == True:
                        med = 0
                    else:
                        med = float(med)
                    if med < 0:  # Si la medicion es menor a 0, dar el valor de 0
                        med = 0  # Cambios de medicion a W/m^2
                    med = med*1000
                    # Escritura del archivo
                    file.write(str(n+0.5)+" "+str(med)+"\n")
                # Cierre del archivo
                file.close()
