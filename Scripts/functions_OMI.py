from math import ceil
import numpy as np
import datetime
import h5py


class OMI_data:
    def __init__(self, year_i, year_f, lon, lat):
        self.div = 0.25
        self.lon_i = 90
        self.lat_i = -180
        self.year_i = year_i
        self.year_f = year_f
        self.lon = lon
        self.lat = lat
        self.pos_lon = self.loc(self.lon_i, self.lon)
        self.pos_lat = self.loc(self.lat_i, self.lat)
        self.delta_year = year_f-year_i+1
        self.data = np.zeros([365, self.delta_year])
        self.month_mean = np.zeros([12, 2])

    def loc(self, pos_i, pos_loc):
        pos = ceil((pos_i-pos_loc)/self.div)
        return pos

    def obtain_data_from_he5(self, o3_values, year, month, day):
        data, n = 0, 0
        # Calculo de los promedios con los vecinos
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                o3 = o3_values[self.pos_lat+i][self.pos_lon+j]
                # Si existe el valor, contabilizarlo
                if o3 > 0:
                    data += o3
                    n += 1
        # Asignacion del valor si es que se realizaron mediciones
        if n != 0:
            o3 = round(data/n,3)
            date = date2consecutiveday(year, month, day)
            if date > 364:
                date = 364
            self.data[date, year-self.year_i] = o3

    def calculate_mensual_mean(self):
        # Calculo del promedio mensual en el periodo
        for year in range(self.delta_year):
            for day in range(365):
                o3 = self.data[day, year]
                # Si hubo mediciones, se contabiliza
                if o3 > 0:
                    month = obtain_month(year, self.year_i, day)
                    # Registro de los dato
                    self.month_mean[month, 0] += o3
                    self.month_mean[month, 1] += 1
        print("Calculando promedios")
        for month in range(12):
            if self.month_mean[month, 1] != 0:
                self.month_mean[month, 0] = round(
                    self.month_mean[month, 0]/self.month_mean[month, 1],3)

    def fill_empty_data(self):
        # Asignacion a los dias en que no hubo medicion
        for year in range(self.delta_year):
            for day in range(365):
                if self.data[day, year] == 0:
                    month = obtain_month(year, self.year_i, day)
                    self.data[day, year] = self.month_mean[month, 0]

    def write_data(self, name, path=""):
        print("Escribiendo archivo final")
        file = open(path+name+".csv", "w")
        file.write(",")
        years = np.array(np.arange(self.year_i, self.year_f+1), dtype=str)
        for year in years:
            file.write(year+",")
        file.write("\n")
        for day in range(365):
            date = consecutiveday2mmdd(day)
            file.write(date+",")
            for year in range(self.delta_year):
                file.write(str(self.data[day, year])+",")
            file.write("\n")
        file.close()


class OMI_data_ozone(OMI_data):
    def __init__(self, year_i, year_f, lon, lat):
        super().__init__(year_i, year_f, lon, lat)

    def read_files_he5(self, files, path):
        name_year = 0
        # Archivo resultante
        for file in files:
            dir_file = path+file
            year, month, day = self.obtain_date_from_name(file)
            if year != name_year:
                print("Analizando año "+str(year))
            data_HD5 = h5py.File(dir_file, "r")
            o3_values = list(
                data_HD5["/HDFEOS/GRIDS/OMI Column Amount O3/Data Fields/ColumnAmountO3"])
            self.obtain_data_from_he5(o3_values, year, month, day)
            data_HD5.close()

    def obtain_date_from_name(self, name):
        year = int(name[19:23])
        month = int(name[24:26])
        day = int(name[26:28])
        return year, month, day


class OMI_data_AOD(OMI_data):
    def __init__(self, year_i, year_f, lon, lat, wave):
        super().__init__(year_i, year_f, lon, lat)
        self.wave = wave

    def read_files_he5(self, files, path):
        name_year = 0
        # Archivo resultante
        for file in files:
            dir_file = path+file
            year, month, day = self.obtain_date_from_name(file)
            if year != name_year:
                print("Analizando año "+str(year))
                name_year = year
            data_HD5 = h5py.File(dir_file, "r")
            o3_values = list(
                data_HD5["/HDFEOS/GRIDS/ColumnAmountAerosol/Data Fields/AerosolOpticalThicknessMW"][self.wave]/1000)
            self.obtain_data_from_he5(o3_values, year, month, day)
            data_HD5.close()

    def obtain_date_from_name(self, name):
        year = int(name[20:24])
        month = int(name[25:27])
        day = int(name[27:29])
        return year, month, day


def obtain_month(year, year_i, day):
    month = (datetime.date(year+year_i, 1, 1) +
             datetime.timedelta(days=day)).month-1
    return month


def date2consecutiveday(year, month, day):
    return (datetime.date(year, month, day)-datetime.date(year, 1, 1)).days


def consecutiveday2mmdd(day):
    date = datetime.date(2019, 1, 1)+datetime.timedelta(days=day)
    month = format_date(date.month)
    day = format_date(date.day)
    date = month+"/"+day
    return date


def format_date(date):
    date = str(date)
    date = "0"*(2-len(date))+date
    return date
