import pandas as pd
import numpy as np


class AOD_list:
    """
    Clase que contiene los metodos para los diferentes AOD's calculados por
    el modelo SMARTS y contenidos en los archivos Data_found
    """
    def __init__(self, path, station, year_i, year_f):
        """
        Describcion de variables:
        path    ---> direccion donde se encuentran los diferentes archivos de Data_found
        station ---> estacion por analizar
        year_i  ---> año en el que inicia el analisis
        year_f  ---> año en el que finaliza el analisis
        """
        self.names_files()
        self.path = path+station.lower()+"/"
        self.station = station
        self.year_i = year_i
        self.year_f = year_f
        self.initialize_AOD_files()
        self.read_AOD_files()

    def names_files(self):
        """
        funcion la cual genera los diferentes nombres para las variantes del AOD found
        """
        names = ["pristine", "moderate", "SSAAER_pristine", "SSAAER_moderate"]
        self.types = ["Data_found_"]*4
        for name, i in zip(names, range(4)):
            self.types[i] += name

    def initialize_AOD_files(self):
        """
        funcion que activa la clase AOD para los diferentes tipos de AOD
        """
        self.pristine = AOD(
            self.path,
            self.types[0],
            self.year_i,
            self.year_f)
        self.moderate = AOD(
            self.path,
            self.types[1],
            self.year_i,
            self.year_f)
        self.SSAAER_pristine = AOD(
            self.path,
            self.types[2],
            self.year_i,
            self.year_f)
        self.SSAAER_moderate = AOD(
            self.path,
            self.types[3],
            self.year_i,
            self.year_f)

    def read_AOD_files(self):
        """
        funcion que realiza la lectura de datos de los AOD found
        """
        self.pristine.read_data()
        self.moderate.read_data()
        self.SSAAER_pristine.read_data()
        self.SSAAER_moderate.read_data()

    def calc_month_mean_AOD_list(self):
        """
        funcion que ejecuta el calculo del promedio mensual por año en cada 
        tipo del AOD
        """
        self.pristine.calc_month_mean()
        self.moderate.calc_month_mean()
        self.SSAAER_pristine.calc_month_mean()
        self.SSAAER_moderate.calc_month_mean()


class AOD:
    """
    Clase AOD que contiene los metodos para leer cada tipo de AOD found
    """
    def __init__(self, path, file, year_i, year_f):
        """
        Describcion de variables:
        path    ---> direccion donde se encuentran los diferentes archivos de Data_found
        file    ---> archivo el cual leera y analizara
        year_i  ---> año en el que inicia el analisis
        year_f  ---> año en el que finaliza el analisis
        """
        self.years = [year for year in range(year_i, year_f+1)]
        self.path = path
        self.year_i = year_i
        self.year_f = year_f
        self.file = file

    def read_data(self):
        """
        funcion que realiza la lectura de datos y guarda cuantos datos hay en total
        """
        self.data = pd.read_csv(self.path+self.file+".csv")
        self.len_data = len(self.data["Date"])

    def calc_month_mean(self):
        """
        funcion que calcula el promedio mensual anual del AOD dado en la variable file
        """
        month_sum = pd.DataFrame(columns=self.years,
                                 index=np.arange(1, 13))
        month_count = pd.DataFrame(columns=self.years,
                                   index=np.arange(1, 13))
        month_sum = month_sum.fillna(0.0)
        month_count = month_count.fillna(0.0)
        # objeto que contendra la información del promedio mensual anual
        self.month_mean = self.month_mean = pd.DataFrame(columns=self.years,
                                                         index=[i for i in range(1, 13)])
        # calculo del los valores y dias por calcular
        for i in range(self.len_data):
            month = self.data["month"][i]
            year = self.data["year"][i]
            AOD_value = self.data["AOD"][i]
            month_sum[year][month] += AOD_value
            month_count[year][month] += 1
        # calculo del promedio mensual
        for year in self.years:
            for month in range(1, 13):
                if month_count[year][month] != 0:
                    self.month_mean[year][month] = month_sum[year][month] / \
                        month_count[year][month]
                else:
                    self.month_mean[year][month] = 0
