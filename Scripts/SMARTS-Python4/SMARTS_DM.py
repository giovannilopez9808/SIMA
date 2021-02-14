from SMARTS_algorithm import *
from numpy import loadtxt
from functions import *
"""
Parametros para interactuar con el modelo, esto esta modificado para el uso
de las estaciones noroeste y noreste del SIMA en el periodo 2015-2020
"""
input_parameters = {
    "file data": "DataAOD_moderate.csv",
    "folder results": "Results_SMARTS_DM",
    "path stations": "../../Stations/",
    "stations": ["noroeste"],
    "hour initial": 8,
    "hour final": 17,
    "lon initial": 285,
    "lon final": 2800,
}
# Inicialización del objeto que contiene a la clase SMARTS con sus parametros de entrada
SMARTS_Model = SMARTS(input_parameters["hour initial"],
                      input_parameters["hour final"],
                      input_parameters["lon initial"],
                      input_parameters["lon final"],
                      )

for station in input_parameters["stations"]:
    # Direccion donde se encuentran los datos de cada estacion
    dir_station = input_parameters["path stations"]+station+"/"
    # Creacion de la carpeta resultados si es que no existe, si existe no hace nada
    mkdir(input_parameters["folder results"], path=dir_station)
    # Lectura de los parametros de entrada de cada dia
    dates, years, months, days, o3_list, aod_list, dr_list = loadtxt(
        dir_station+input_parameters["file data"], unpack=True)
    # Direccion de los resultados
    dir_results = dir_station + input_parameters["file data"]
    # <-----------------------------Ciclo para variar los dias--------------------------------------->
    for date, year, month, day, o3, aod in zip(dates, years, months, days, o3_list, aod_list):
        date = str(int(date))
        # Formato de los dias
        year, month, day = int_dates(year, month, day)
        print("Calculando el dia ", year, month, day)
        # Ejecucion del modelo SMARTS
        SMARTS_Model.run_SMARTS(day, month, year, o3,
                                aod, date, path=dir_results)
