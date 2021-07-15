from functions import *
import pandas as pd
import numpy as np
import os


class SMARTS:
    """
    Clase que contiene las funciones que interactuaran con el modelo SMARTS
    """

    def __init__(self, parameters={}, station=""):
        """
        Valores con los cuales se inicializa el modelo SMARTS
        ### inputs
        + station      ----> Estacion que se analizara
        + hour_i       ----> Hora inicial para correr el modelo
        + hour_f       ----> Hora final para correr el modelo
        + lon_ i       ----> Longitud de onda inicial para el modelo
        + lon_ f       ----> Longitud de onda final para el modelo
        + igas         ----> Card 6a del Modelo SMARTS
        + delta_lon    ----> Número de longitudes de onda que se saltara el resultado del modelo
        + total_minute ----> Total minutos que correra el modelo
        """
        self.parameters = parameters
        self.delta_lon = parameters["wavelength initial"]-280+1
        self.total_minute = int(
            (parameters["hour final"]-parameters["hour initial"])*60)
        self.define_location(station)

    def define_location(self, station):
        stations = {
            "centro": {
                "Lat": 25.670,
                "Lon": -100.338,
                "Height": 0.560},
            "noreste": {
                "Lat": 25.750,
                "Lon": -100.255,
                "Height": 0.476},
            "noroeste": {
                "Lat": 25.757,
                "Lon": -100.366,
                "Height": 0.571},
            "sureste2": {
                "Lat": 25.646,
                "Lon": -100.096,
                "Height": 0.387},
            "suroeste": {
                "Lat": 25.676,
                "Lon": -100.464,
                "Height": 0.694}
        }
        self.lat = stations[station]["Lat"]
        self.lon = stations[station]["Lon"]
        self.height = stations[station]["Height"]

    def atmosphere_state(self):
        pass

    def run(self, day=1, month=1, year=2000, o3=250.51, aod=0.2, name="", path=""):
        """
        Función que ejecuta el modelo SMARTS
        ### inputs:
        + day   ----> Dia del año
        + month ----> Mes del año númerico
        + year  ----> Año del dia por analizar
        + o3    ----> ozono del dia
        + aod   ----> AOD del dia
        + name  ----> nombre del archivo de resultados
        + path  ----> direccion para guardar los archivos
        """
        file_date = open("{}/{}.txt".format(path,
                                            name),
                         "w")
        for minute in range(self.total_minute):
            # Hora y minutos a hora con decimal
            minutes = self.hour_and_minute_to_hours(minute)
            # Escribir el archivo de input para el modelo SMARTS
            self.write_data_input(day,
                                  month,
                                  year,
                                  minutes,
                                  o3,
                                  aod)
            os.system("./smarts.out")
            # Resultado de la in7tegral a partir de los resultaos del modelo SMARTS
            integral = self.read_results()
            # Escritura de los resultados
            file_date.write("{} {}\n".format(minutes,
                                             integral))
        file_date.close()

    def hour_and_minute_to_hours(self, minute=5):
        return round(self.parameters["hour initial"]+minute/60, 4)

    def read_results(self, name_result="data.ext.txt"):
        """
        Funcion que realiza la lectura de los resultados del SMARTS
        y realiza la integral del especto a cada minuto
        Describción de variables
        + wavelength ----> longitudes de onda de los resultados del modelo SMARTS
        + irra       ----> Valor del especto de los resultados del modelo SMARTS
        + integral   ----> Valor que irradiancia solar
        """
        # Lectura de los resultados del modelo SMARTS
        wavelength, irradiance = np.loadtxt(
            name_result, skiprows=self.delta_lon, unpack=True)
        integral = irradiance[0]
        # Calculo de la irradiancia solar a partir de los resultados del modelo SMARTS
        size = np.size(irradiance)
        for i in range(1, size):
            integral += irradiance[i]*(wavelength[i]-wavelength[i-1])
        # Eliminación de los archivos
        os.system("rm data*")
        # Formato de la integral
        integral = str(round(integral))
        return integral

    def write_data_input(self, day=1, month=1, year=2000, hour=8, ozono=250.51, aod=0.5):
        """
        Formato del input del modelo SMARTS
        ### inputs:
        + day   -> Dia del año
        + month -> Mes del año númerico
        + year  -> Año del dia por analizar
        + hour  -> Hora del calculo de la irradiancia
        + ozono -> ozono del dia
        + aod   -> AOD del dia
        + igas  -> Card 6a
        """
        file = open("data.inp.txt", "w")
        file.write(" 'AOD={} '\n".format(aod))
        # Card 2
        file.write(" 2\n")
        # Card 2a
        # lat,altit,height
        file.write(" {:.3f} {} {}\n".format(self.lat,
                                            self.height,
                                            0))
        # Card 3
        # IATMOS
        file.write(" 1\n")
        # Card 3a
        file.write(" 'USSA'\n")
        # Card 4
        # H2O
        file.write(" 1\n")
        # Card 4a
        file.write(" 0\n")
        # Card 5
        # Ozono
        file.write(" {} {:.4f}\n".format(1,
                                         ozono/1000))
        # Card 6
        file.write(" 0\n")
        # Card 6a
        # Pristine ----> 1
        # Moderate ----> 3
        file.write(" {}\n".format(self.parameters["igas"]))
        # Card 7
        # Co2
        file.write(" 390\n")
        # Card 7a
        file.write(" 0\n")
        # Card 8
        file.write(" 'S&F_URBAN'\n")
        # Card 9
        file.write(" 5\n")
        # Card 9a
        file.write(" {} {}\n".format(aod,
                                     2))
        # Card 10
        file.write(" 18\n")
        # Card 10b
        file.write(" 1\n")
        # Card 10d
        # IALBDG, TILT,WAZIM
        file.write(" {} {} {}\n".format(51,
                                        37.,
                                        180.))
        # Card 11---
        # Wave min, Wave max, suncor, solar cons
        file.write(" {} {} {} {}\n".format(self.parameters["wavelength initial"],
                                           self.parameters["wavelength final"],
                                           1,
                                           1366.1))
        # ------Card 12---
        file.write(" 2\n")
        # Card 12a
        # Wave min, Wave max, inter wave
        file.write(" {} {} {}\n".format(self.parameters["wavelength initial"],
                                        self.parameters["wavelength final"],
                                        1))
        # Card 12b
        file.write(" 1\n")
        # Card 12c
        file.write(" 4\n")
        # Card 13
        file.write(" 1\n")
        # Card 13a
        #  slope, apert, limit
        file.write(" 0 2.9 0\n")
        # Card 14
        file.write(" 0\n")
        # Card 15
        file.write(" 0\n")
        # Card 16
        file.write(" 1\n")
        # Card 17
        file.write(" 3\n")
        # Card 17a
        # Year, month, day, hour, latit, longit, zone
        file.write(" {} {} {} {} {} {} {}\n".format(year,
                                                    month,
                                                    day,
                                                    hour,
                                                    self.lat,
                                                    self.lon,
                                                    -6))
        file.close()


class SMARTS_DR(SMARTS):
    """
    Clase heredada de SMARTS, uso especifico para la versión del modelo
    que calcula el AOD a partir de las mediciones y una RD dada
    """

    def __init__(self, parameters={}, station=""):
        """
        Valores con los cuales se inicializa el modelo SMARTS
        ### inputs
        + hour_i       ----> Hora inicial para correr el modelo
        + hour_f       ----> Hora final para correr el modelo
        + lon_ i       ----> Longitud de onda inicial para el modelo
        + lon_ f       ----> Longitud de onda final para el modelo
        + delta_lon    ----> Número de longitudes de onda que se saltara
                           el resultado del modelo
        + total_minute ----> Total minutos que correra el modelo
        + RD_lim       ----> RD al cual se quiere llegar
        + RD_delta     ----> Mas menos del RD
        """
        SMARTS.__init__(self,
                        parameters=parameters,
                        station=station)
        self.parameters = parameters
        self.station = station
        self.delta_hour = int(
            self.parameters["hour final"]-self.parameters["hour initial"])
        self.select_path_name_for_results()

    def select_path_name_for_results(self):
        names = {
            1: "pristine",
            3: "moderate"
        }
        name = names[self.parameters["igas"]]
        self.parameters["path results"] = self.parameters["path results"]+name+"/"
        self.parameters["file results"] = self.parameters["file results"]+name

    def run_search(self):
        # Direccion donde se encuentran los datos de cada estacion
        station_path = "{}{}/".format(self.parameters["path stations"],
                                      self.station)
        path_results = "{}{}".format(station_path,
                                     self.parameters["path results"])
        # Creacion de la carpeta resultados si es que no existe
        mkdir(self.parameters["path results"],
              path=station_path)
        # Archivo de resultados donde se guardara el AOD y la RD de cada dia
        AOD_file = open("{}{}.csv".format(station_path,
                                          self.parameters["file results"]),
                        "w")
        AOD_file.write("Date,year,month,day,ozone,AOD,RD\n")
        # Lectura de los parametros de entrada de cada dia
        data = pd.read_csv("{}{}".format(station_path,
                                         self.parameters["file data"]))
        for index in data.index:
            print("\n\tCalculando el dia {}-{}-{}".format(data["Year"][index],
                                                          str(data["Month"][index]).zfill(
                2),
                str(data["Day"][index]).zfill(2)))
            print("\tAOD_i\tAOD\tAOD_f\tRD")
            self.initialize_aod(self.parameters["AOD inicial"],
                                self.parameters["AOD limite"])
            # Lectura de las mediciones
            hour, measurements = np.loadtxt("{}/Mediciones/{}.txt".format(station_path,
                                                                          data["Date"][index]),
                                            skiprows=self.parameters["hour initial"],
                                            unpack=True)
            # Valor maximo de medicion, esta se usara para el calculo de la RD
            data_max = np.max(measurements[0:self.delta_hour+1])
            var = False
            # Primer valor de AOD, se puede cambiar por cualquier otro siempre y cuando este entre aod_i y aod_lim
            aod = self.obtain_aod(self.aod_i,
                                  self.aod_lim)
            # Control de iteracciones
            iter = 0
            while not(var) and iter < 10:
                # Ejecucion del modelo SMARTS con los parametros de cada dia
                self.run(day=data["Day"][index],
                         month=data["Month"][index],
                         year=data["Year"][index],
                         o3=data["Ozone"][index],
                         aod=aod,
                         name=data["Date"][index],
                         path=path_results)
                # Valor maximo de los resultados del modelo SMARTS
                data_model = self.obtain_maximum_from_results(data["Date"][index],
                                                              path=path_results)
                # Calculo del RD y verificación si se cumple la condicion
                var, RD = self.RD_decision(data_model,
                                           data_max)
                print("\t{}\t{}\t{}\t{}".format(self.aod_i,
                                                aod,
                                                self.aod_lim,
                                                RD,))
                if var:
                    # Si se cumple entonces se escribiran los parametros, el AOD y la RD en el archivo de resultados
                    self.write_results(AOD_file,
                                       data["Date"][index],
                                       data["Year"][index],
                                       data["Month"][index],
                                       data["Day"][index],
                                       data["Ozone"][index],
                                       aod,
                                       RD)
                else:
                    # Se calculara un nuevo AOD siguiendo el algoritmo de busqueda binaria
                    aod = self.aod_binary_search(aod, RD)
                    # Si se queda en un intervalo muy pequeño se verificara que cumpla la condicion si lo hace entonces escribira en el archivo el resultado, esto llega a pasar  si se pone un delta_RD menor a 1
                    if self.aod_lim == aod and abs(RD-self.RD_lim) < 2:
                        self.write_results(AOD_file,
                                           data["Date"][index],
                                           data["Year"][index],
                                           data["Month"][index],
                                           data["Day"][index],
                                           data["Ozone"][index],
                                           aod,
                                           RD)
                        var = True
                    iter += 1
        AOD_file.close()

    def initialize_aod(self, aod_i, aod_lim):
        """
        Funcion que inicializa el limite inferior y superior del AOD
        """
        self.aod_i = aod_i
        self.aod_lim = aod_lim

    def obtain_aod(self, aod_i, aod_f):
        return round((aod_i+aod_f)/2, 3)

    def obtain_maximum_from_results(self, name, path=""):
        data_model = np.loadtxt("{}{}.txt".format(path,
                                                  name),
                                usecols=1)
        pos = (np.where(np.max(data_model) == data_model)[0])[0]
        data_model = np.mean(data_model[pos-30:pos+31])
        return data_model

    def RD_decision(self, model, measurement):
        """
        Funcion que calcula la RD entre el modelo y la medicion
        """
        var = False
        RD = round(100*(model-measurement)/measurement, 3)
        if self.RD_search(RD):
            var = True
        return var, RD

    def aod_binary_search(self, aod, RD):
        """
        Función que calcula el AOD que se introducira en el modelo SMARTS
        este emplea una busqueda binaria para que sea más eficiente
        """
        if self.RD_search(RD):
            self.aod_i = aod
        elif RD > self.parameters["RD limite"]+self.parameters["RD delta"]:
            self.aod_i = aod
        else:
            self.aod_lim = aod
        aod = self.obtain_aod(self.aod_lim,
                              self.aod_i)
        return aod

    def RD_search(self, RD):
        lim_i = self.parameters["RD limite"]-self.parameters["RD delta"]
        lim_f = self.parameters["RD limite"]+self.parameters["RD delta"]
        return lim_i < RD < lim_f

    def write_results(self, file, date, year, month, day, o3, aod, RD):
        file.write("{},{},{},{},{},{:.3f},{:.2f}\n".format(date,
                                                           year,
                                                           month,
                                                           day,
                                                           o3,
                                                           aod,
                                                           RD))


class SMARTS_DR_SSAAER_CUSTOM(SMARTS_DR):
    def __init__(self, parameters={}, station=""):
        SMARTS_DR.__init__(self,
                           parameters=parameters,
                           station=station)
        self.parameters = parameters

    def write_data_input(self, day=1, month=1, year=2000, hour=8, ozono=250.51, aod=0.5):
        """
        Formato del input del modelo SMARTS
        day   ----> Dia del año
        month ----> Mes del año númerico
        year  ----> Año del dia por analizar
        hour  ----> Hora del calculo de la irradiancia
        ozono ----> ozono del dia
        aod   ----> AOD del dia
        igas  ----> Card 6a
        """
        file = open("data.inp.txt", "w")
        file.write(" 'AOD={} '\n".format(aod))
        # Card 2
        file.write(" 2\n")
        # Card 2a
        # lat,altit,height
        file.write(" {:.3f} {} {}\n".format(self.lat,
                                            self.height,
                                            0))
        # Card 3
        # IATMOS
        file.write(" 1\n")
        # Card 3a
        file.write(" 'USSA'\n")
        # Card 4
        # H2O
        file.write(" 1\n")
        # Card 4a
        file.write(" 0\n")
        # Card 5
        # Ozono
        file.write(" {} {:.4f}\n".format(1,
                                         ozono/1000))
        # Card 6
        file.write(" 0\n")
        # Card 6a
        # Pristine ----> 1
        # Moderate ----> 3
        file.write(" {}\n".format(self.parameters["igas"]))
        # Card 7
        # Co2
        file.write(" 390\n")
        # Card 7a
        file.write(" 0\n")
        # Card 8
        file.write(" 'USER'\n")
        # Card 8a
        # SSAAER Palancar
        # Asymmetry Promedio de 550 nm y humedad ente 50-70%
        file.write(" {} {} {} {}\n".format(1, 1, 0.8, 0.68))
        # Card 9
        file.write(" 5\n")
        # Card 9a
        file.write(" {} {}\n".format(aod,
                                     2))
        # Card 10
        file.write(" 18\n")
        # Card 10b
        file.write(" 1\n")
        # Card 10d
        # IALBDG, TILT,WAZIM
        file.write(" {} {} {}\n".format(51,
                                        37.,
                                        180.))
        # Card 11---
        # Wave min, Wave max, suncor, solar cons
        file.write(" {} {} {} {}\n".format(self.parameters["wavelength initial"],
                                           self.parameters["wavelength final"],
                                           1,
                                           1366.1))
        # ------Card 12---
        file.write(" 2\n")
        # Card 12a
        # Wave min, Wave max, inter wave
        file.write(" {} {} {}\n".format(self.parameters["wavelength initial"],
                                        self.parameters["wavelength final"],
                                        1))
        # Card 12b
        file.write(" 1\n")
        # Card 12c
        file.write(" 4\n")
        # Card 13
        file.write(" 1\n")
        # Card 13a
        #  slope, apert, limit
        file.write(" 0 2.9 0\n")
        # Card 14
        file.write(" 0\n")
        # Card 15
        file.write(" 0\n")
        # Card 16
        file.write(" 1\n")
        # Card 17
        file.write(" 3\n")
        # Card 17a
        # Year, month, day, hour, latit, longit, zone
        file.write(" {} {} {} {} {} {} {}\n".format(year,
                                                    month,
                                                    day,
                                                    hour,
                                                    self.lat,
                                                    self.lon,
                                                    -6))
        file.close()
