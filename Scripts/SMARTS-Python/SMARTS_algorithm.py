from math import ceil
import numpy as np
import os


class SMARTS:
    """
    Clase que contiene las funciones que interactuaran con el modelo SMARTS
    """

    def __init__(self, hour_i, hour_f, lon_i, lon_f):
        """
        Valores con los cuales se inicializa el modelo SMARTS
        Descripción de las variables
        hour_i       ----> Hora inicial para correr el modelo
        hour_f       ----> Hora final para correr el modelo
        lon_ i       ----> Longitud de onda inicial para el modelo
        lon_ f       ----> Longitud de onda final para el modelo
        delta_lon    ----> Número de longitudes de onda que se saltara
                           el resultado del modelo
        total_minute ----> Total minutos que correra el modelo
        """
        self.hour_i = hour_i
        self.hour_f = hour_f
        self.lon_i = lon_i
        self.lon_f = lon_f
        self.delta_lon = lon_i-280+1
        self.delta_hour = int(hour_f-hour_i)
        self.total_minute = int((hour_f-hour_i)*60)

    def run_SMARTS(self, day, month, year, o3, aod, name, path=""):
        """
        Función que ejecuta el modelo SMARTS
        Describción de las variables
        day   ----> Dia del año
        month ----> Mes del año númerico
        year  ----> Año del dia por analizar
        o3    ----> ozono del dia
        aod   ----> AOD del dia
        name  ----> nombre del archivo resultante
        path  ----> direccion para guardar los archivos
        """
        file_date = open(path+name+".txt", "w")
        for min in range(self.total_minute):
            # Hora y minutos a hora con decimal
            minutes = str(round(self.hour_i+min/60, 4))
            # Escribir el archivo de input para el modelo SMARTS
            self.write_data_input_SMARTS(day, month, year,
                                         minutes, o3, aod)
            os.system("./smarts.out")
            # Resultado de la integral a partir de los resultaos del modelo SMARTS
            integral = self.read_results_SMARTS()
            # Escritura de los resultados
            file_date.write(minutes+" "+integral+"\n")
        file_date.close()

    def read_results_SMARTS(self, name_result="data.ext.txt"):
        """
        Funcion que realiza la lectura de los resultados del SMARTS
        y realiza la integral del especto a cada minuto
        Describción de variables
        wavelength ----> longitudes de onda de los resultados del modelo SMARTS
        irra       ----> Valor del especto de los resultados del modelo SMARTS
        integral   ----> Valor que irradiancia solar
        """
        # Lectura de los resultados del modelo SMARTS
        wavelength, irra = np.loadtxt(
            name_result, skiprows=self.delta_lon, unpack=True)
        integral = irra[0]
        # Calculo de la irradiancia solar a partir de los resultados del modelo SMARTS
        size = np.size(irra)
        for i in range(1, size):
            integral += irra[i]*(wavelength[i]-wavelength[i-1])
        # Eliminación de los archivos
        os.system("rm data*")
        # Formato de la integral
        integral = str(round(integral))
        return integral

    def write_data_input_SMARTS(self, day, month, year, hour, ozono, aod):
        """
        Formato del input del modelo SMARTS
        day   ----> Dia del año
        month ----> Mes del año númerico
        year  ----> Año del dia por analizar
        hour  ----> Hora del calculo de la irradiancia
        ozono ----> ozono del dia
        aod   ----> AOD del dia
        """
        file = open("data.inp.txt", "w")
        file.write(" 'AOD="+str(aod)+"'\n")
        # Card 2
        file.write(" 2\n")
        # Card 2a
        # lat,altit,height
        file.write(" 25.750 0.512 0\n")
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
        file.write(" 1 "+str(round(ozono/1000, 4))+"\n")
        # Card 6
        file.write(" 0\n")
        # Card 6a
        file.write(" 3\n")
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
        file.write(" "+str(aod)+" 2\n")
        # Card 10
        file.write(" 18\n")
        # Card 10b
        file.write(" 1\n")
        # Card 10d
        # IALBDG, TILT,WAZIM
        file.write(" 51 37. 180.\n")
        # Card 11---
        # Wave min, Wave max, suncor, solar cons
        file.write(" "+str(self.lon_i)+" "+str(self.lon_f)+" 1 1366.1\n")
        # ------Card 12---
        file.write(" 2\n")
        # Card 12a
        # Wave min, Wave max, inter wave
        file.write(" "+str(self.lon_i)+" "+str(self.lon_f)+" 1\n")
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
        file.write(" "+str(year)+" "+str(month)+" "+str(day) +
                   " "+hour+" 25.75 -100.25 -6\n")
        file.close()


class SMARTS_DR(SMARTS):
    """
    Clase heredada de SMARTS, uso especifico para la versión del modelo
    que calcula el AOD a partir de las mediciones y una RD dada
    """

    def __init__(self, hour_i, hour_f, lon_i, lon_f, RD_lim, RD_delta):
        """
        Valores con los cuales se inicializa el modelo SMARTS
        Descripción de las variables
        hour_i       ----> Hora inicial para correr el modelo
        hour_f       ----> Hora final para correr el modelo
        lon_ i       ----> Longitud de onda inicial para el modelo
        lon_ f       ----> Longitud de onda final para el modelo
        delta_lon    ----> Número de longitudes de onda que se saltara
                           el resultado del modelo
        total_minute ----> Total minutos que correra el modelo
        RD_lim       ----> RD al cual se quiere llegar
        RD_delta     ----> Mas menos del RD
        """
        SMARTS.__init__(self, hour_i, hour_f, lon_i, lon_f)
        self.RD_lim = RD_lim
        self.RD_delta = RD_delta

    def initialize_aod(self, aod_i, aod_lim):
        """
        Funcion que inicializa el limite inferior y superior del AOD
        """
        self.aod_i = aod_i
        self.aod_lim = aod_lim

    def RD_decision(self, model, measurement):
        """
        Funcion que calcula la RD entre el modelo y la medicion
        """
        var = False
        RD = round(100*(model-measurement)/measurement,3)
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
            aod = round((aod+self.aod_lim)/2, 3)
        elif RD > self.RD_lim+self.RD_delta:
            self.aod_i = aod
            aod = round((aod+self.aod_lim)/2, 3)
        else:
            self.aod_lim = aod
            aod = round((aod+self.aod_i)/2, 3)
        return aod

    def RD_search(self, RD):
        return self.RD_lim-self.RD_delta < RD < self.RD_lim+self.RD_delta
