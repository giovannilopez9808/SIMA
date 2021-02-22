import pandas as pd
import numpy as np


class MODIS_data:
    def __init__(self, file, year_i, year_f, type_AOD):
        self.years = [year for year in range(year_i, year_f+1)]
        self.type_AOD = type_AOD
        self.year_i = year_i
        self.year_f = year_f
        self.file=file

    def read_data(self, path):
        self.data = pd.read_csv(path+self.file+".csv")
        self.clean_data()
        self.data = self.data.fillna(-1)
        self.len_data=len(self.data[self.type_AOD])

    def clean_data(self):
        for key in self.data.keys():
            if not key in ["Dates", self.type_AOD]:
                self.data = self.data.drop(key, 1)

    def calc_month_mean(self):
        month_sum = pd.DataFrame(columns=self.years,
                                 index=np.arange(1, 13))
        month_count = pd.DataFrame(columns=self.years,
                                   index=np.arange(1, 13))
        month_sum = month_sum.fillna(0.0)
        month_count = month_count.fillna(0.0)
        self.month_mean = self.month_mean = pd.DataFrame(columns=self.years,
                                                         index=[i for i in range(1, 13)])
        for i in range(self.len_data):
            year, month = self.obtain_date_from_file(i)
            AOD_value = self.data[self.type_AOD][i]
            if AOD_value >= 0:
                month_sum[year][month] += AOD_value
                month_count[year][month] += 1
        for year in self.years:
            for month in range(1, 13):
                if month_count[year][month] != 0:
                    self.month_mean[year][month] = month_sum[year][month] / \
                        month_count[year][month]
                else:
                    self.month_mean[year][month] = 0

    def obtain_date_from_file(self, i):
        year = int(self.data["Dates"][i][0:4])
        month = int(self.data["Dates"][i][5:7])
        return year, month
