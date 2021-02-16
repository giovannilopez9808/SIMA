import pandas as pd
import numpy as np


class AOD_list:
    def __init__(self, path, station, year_i, year_f):
        self.names_files()
        self.path = path+station.lower()+"/"
        self.station = station
        self.year_i = year_i
        self.year_f = year_f
        self.initialize_AOD_files()
        self.read_AOD_files()

    def names_files(self):
        names = ["pristine", "moderate", "SSAAER_pristine", "SSAAER_moderate"]
        self.types = ["Data_found_"]*4
        for name, i in zip(names, range(4)):
            self.types[i] += name

    def initialize_AOD_files(self):
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
        self.pristine.read_data()
        self.moderate.read_data()
        self.SSAAER_pristine.read_data()
        self.SSAAER_moderate.read_data()

    def calc_month_mean_AOD_list(self):
        self.pristine.calc_month_mean()
        self.moderate.calc_month_mean()
        self.SSAAER_pristine.calc_month_mean()
        self.SSAAER_moderate.calc_month_mean()


class AOD:
    def __init__(self, path, file, year_i, year_f):
        self.years = [year for year in range(year_i, year_f+1)]
        self.path = path
        self.year_i = year_i
        self.year_f = year_f
        self.file = file

    def read_data(self):
        self.data = pd.read_csv(self.path+self.file+".csv")
        self.len_data = len(self.data["Date"])

    def calc_month_mean(self):
        month_sum = pd.DataFrame(
            columns=self.years, index=np.arange(1, 13))
        month_count = pd.DataFrame(
            columns=self.years, index=np.arange(1, 13))
        month_sum = month_sum.fillna(0.0)
        month_count = month_count.fillna(0.0)
        self.month_mean = self.month_mean = pd.DataFrame(columns=self.years,
                                                         index=[i for i in range(1, 13)])
        for i in range(self.len_data):
            month = self.data["month"][i]
            year = self.data["year"][i]
            AOD_value = self.data["AOD"][i]
            month_sum[year][month] += AOD_value
            month_count[year][month] += 1
        for year in self.years:
            for month in range(1, 13):
                if month_count[year][month] != 0:
                    self.month_mean[year][month] = month_sum[year][month] / \
                        month_count[year][month]
                else:
                    self.month_mean[year][month] = 0
