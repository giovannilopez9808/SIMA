from SMARTS_algorithm import *
from pandas import read_csv
from functions import *
"""
Parametros para interactuar con el modelo, esto esta modificado para el uso
de las estaciones noroeste y noreste del SIMA en el periodo 2015-2020
"""
parameters = {
    "file data": "Data_found_pristine.csv",
    "folder results": "Results_SMARTS_DM",
    "path stations": "../../Stations/",
    "igas": 1,
    "stations": ["noreste"],
    "hour initial": 8,
    "hour final": 17,
    "wavelength initial": 285,
    "wavelength final": 2800,
}
for station in parameters["stations"]:
    # Inicialización del objeto que contiene a la clase SMARTS con sus parametros de entrada
    SMARTS_Model = SMARTS(parameters,
                          station
                          )
    # Direccion donde se encuentran los datos de cada estacion
    station_path = "{}{}/".format(parameters["path stations"],
                                  station)
    # Creacion de la carpeta resultados si es que no existe, si existe no hace nada
    mkdir(parameters["folder results"],
          path=station_path)
    # Lectura de los parametros de entrada de cada dia
    data = read_csv("{}{}".format(station_path,
                                  parameters["file data"]))
    # Direccion de los resultados
    path_results = "{}{}/".format(station_path,
                                  parameters["folder results"])
    # Ciclo para variar los dias
    for index in data.index:
        print("Calculando el dia {}-{}-{}".format(data["year"][index],
                                                  str(data["month"]
                                                      [index]).zfill(2),
                                                  str(data["day"][index]).zfill(2)))
        # Ejecucion del modelo SMARTS
        SMARTS_Model.run(data["day"][index],
                         data["month"][index],
                         data["year"][index],
                         data["ozone"][index],
                         data["AOD"][index],
                         data["Date"][index],
                         path=path_results)
