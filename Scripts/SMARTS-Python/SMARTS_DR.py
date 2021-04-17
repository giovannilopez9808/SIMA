from SMARTS_algorithm import *
from functions import *
import numpy as np
"""
Parametros para interactuar con el modelo, esto esta modificado
para el uso de las estaciones SIMA en el periodo 2015-2020
"""
input_parameters = {
    "path stations": "../../Stations/",
    "path results": "Results_SMARTS_DR_pristine/",
    #    "path results": "Results_SMARTS_DR_moderate/",
    "file results": "Data_found_pristine.csv",
    #    "file results": "Data_found_moderate.csv",
    "file data": "datos.txt",
    "stations": ["sureste2"],
    "hour initial": 9,
    "hour final": 16,
    "lon initial": 285,
    "lon final": 2800,
    "AOD inicial": 0.01,
    "AOD limite": 1,
    "RD limite": 10,
    "RD delta": 1,
    "Igas": 1,
    #    "Igas": 3,
}

for station in input_parameters["stations"]:
    # Inicialización del objeto que contiene a la clase SMARTS con sus parametros de entrada
    SMARTS_Model = SMARTS_DR(station,
                             input_parameters["hour initial"],
                             input_parameters["hour final"],
                             input_parameters["lon initial"],
                             input_parameters["lon final"],
                             input_parameters["RD limite"],
                             input_parameters["RD delta"],
                             input_parameters["Igas"])
    print("Calculando estacion "+station)
    # Direccion donde se encuentran los datos de cada estacion
    dir_station = input_parameters["path stations"]+station+"/"
    # Creacion de la carpeta resultados si es que no existe, si existe no hace nada
    mkdir(input_parameters["path results"], path=dir_station)
    dir_results = dir_station+input_parameters["path results"]
    # Archivo de resultados donde se guardara el AOD y la RD de cada dia
    AOD_file = open(dir_station+input_parameters["file results"], "w")
    AOD_file.write("Date,year,month,day,ozone,AOD,RD\n")
    # Lectura de los parametros de entrada de cada dia
    dates, o3_list, years, months, days = np.loadtxt(
        dir_station+input_parameters["file data"], unpack=True)
    for date, o3, year, month, day in zip(dates, o3_list, years, months, days):
        date = str(int(date))
        # Inicializacion de los limites del AOD
        SMARTS_Model.initialize_aod(input_parameters["AOD inicial"],
                                    input_parameters["AOD limite"])
        year, month, day = int_dates(year, month, day)
        # Lectura de lñas mediciones
        hour, data = np.loadtxt(dir_station+"/Mediciones/" +
                                date+".txt", skiprows=SMARTS_Model.hour_i, unpack=True)
        # Valor maximo de medicion, esta se usara para el calculo de la RD
        data_max = np.max(data[0:SMARTS_Model.delta_hour+1])
        print("\tCalculando el dia ", year, month, day)
        var = False
        # Primer valor de AOD por intentar, se puede cambiar por cualquier otro siempre y cuando
        # este entre aod_i y aod_lim
        aod = (SMARTS_Model.aod_i+SMARTS_Model.aod_lim)/2
        # Control de iteracciones por si no encuentra algun valor
        iter = 0
        while not(var):
            # Inicio del calculo del AOD
            if iter < 10:
                # Ejecucion del modelo SMARTS con los parametros de cada dia
                SMARTS_Model.run_SMARTS(day, month, year, o3, aod,
                                        date, path=dir_results)
                # Valor maximo de los resultados del modelo SMARTS
                data_model = find_max(date, path=dir_results)
                # Calculo del RD y verificación si se cumple la condicion
                var, RD = SMARTS_Model.RD_decision(data_model, data_max)
                if var:
                    # Si se cumple entonces se escribiran los parametros, el AOD y
                    # la RD en el archivo de resultados
                    print(SMARTS_Model.aod_i, "\t",
                          aod, "\t", SMARTS_Model.aod_lim, "\t", RD)
                    writeAOD(AOD_file, date, year, month, day, o3, aod, RD)
                else:
                    # Si no calculara un nuevo AOD siguiendo el algoritmo del
                    # de busqueda binaria
                    print(SMARTS_Model.aod_i, "\t", aod,
                          "\t", SMARTS_Model.aod_lim, "\t", RD)
                    aod = SMARTS_Model.aod_binary_search(aod, RD)
                    """
                    Si se queda en un intervalo muy pequeño se verificara que cumpla la condicion
                    si lo hace entonces escribira en el archivo el resultado, esto llega a pasar 
                    si se pone un delta_RD menor a 1
                    """
                    if SMARTS_Model.aod_lim == aod and abs(RD-SMARTS_Model.RD_lim) < 2:
                        writeAOD(AOD_file, date, year, month, day, o3, aod, RD)
                        var = True
                    iter += 1
            else:
                var = True
    AOD_file.close()
