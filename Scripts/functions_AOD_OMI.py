import pandas as pd


class AOD_OMI_data:
    def __init__(self, year_i, year_f, wavelength, scale):
        self.years = [year for year in range(year_i, year_f+1)]
        self.wavelength = wavelength
        self.scale = scale

    def read_data(self, path_data):
        self.data = pd.read_csv(
            path_data + "AOD_OMI_" + self.scale + "_clean.csv", index_col=0)
        self.data.index = pd.to_datetime(self.data.index)
        self.clean_data()

    def clean_data(self):
        for key in self.data.keys():
            if not key in [self.wavelength]:
                self.data = self.data.drop(key, 1)

    def calc_month_mean(self):
        self.month_mean = pd.DataFrame(
            columns=self.years, index=[i for i in range(1, 13)])
        data_mean = self.data.resample("MS").mean()
        month_consecutive = 0
        for year in self.years:
            for month in range(1, 13):
                self.month_mean[year][month] = data_mean[self.wavelength +
                                                         "nm"][month_consecutive]
                month_consecutive += 1

    def cut_data_year(self, date_i, date_f):
        self.section = self.data.loc[(self.data.index >= date_i) &
                                     (self.data.index < date_f)]
