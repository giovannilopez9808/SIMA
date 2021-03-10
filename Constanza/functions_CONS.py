import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import datetime

def obtain_month_names(months):
    names = []
    for month in months:
        date = datetime.date(2020, month, 1)
        names.append(date.strftime("%b"))
    return names

class SIMA_data:
    def __init__(self, file):
        self.file = file

    def read_data_SIMA(self,path_data):
        self.data=pd.read_csv(path_data + self.file + '_SIMA.csv')
        self.data['Hours'] = self.data['Hours'].astype(str).str.zfill(2)
        self.data['Datetime'] = self.data["Dates"] + ' ' + self.data['Hours']
        self.data['Datetime']=pd.to_datetime(self.data['Datetime'])
        self.data.index=self.data['Datetime']
        self.data=self.data.drop(['Dates','Hours','Datetime'], axis=1)

    def calc_month_mean(self,station,year_i,year_f):
        self.years = [year for year in range(year_i, year_f+1)]
        self.month_mean = pd.DataFrame(columns=self.years,index=[i for i in range(12)])
        i=0
        for year in self.years:
            for month in range(1, 13):
                self.month_mean[year][month - 1] = self.data.resample("MS").mean()[station][i]
                i=i+1

    def calc_month_sum(self,station,year_i,year_f):
        self.years = [year for year in range(year_i, year_f+1)]
        self.month_sum = pd.DataFrame(columns=self.years,index=[i for i in range(12)])
        i=0
        for year in self.years:
            for month in range(1, 13):
                self.month_sum[year][month - 1] = self.data.resample("MS").sum()[station][i]
                i=i+1

    def cut_year(self, date_i, date_f):
        self.section = self.data.loc[(self.data.index >= date_i) &
                                          (self.data.index < date_f)] 

class AOD_OMI_data:
    def __init__(self, wavelen, res):
        self.wavelen = wavelen
        self.res = res

    def read_data(self,path_data):
        self.data=pd.read_csv(path_data + 'AOD_OMI_' + self.res + '_clean.csv',index_col=0)
        self.data.index=pd.to_datetime(self.data.index,format='%Y-%m-%d')#'%y%m%d')
        for key in self.data.keys():
            if not key in self.wavelen and not key in ["Dates"]:
                self.data = self.data.drop(key, 1)
       
    def calc_month_mean(self,year_i,year_f):
        self.years = [year for year in range(year_i, year_f+1)]
        self.month_mean = pd.DataFrame(columns=self.years,index=[i for i in range(12)])
        i=0
        for year in self.years:
            for month in range(1, 13):
                self.month_mean[year][month - 1] = self.data.resample("MS").mean()[self.wavelen][i]
                i=i+1
                
    def cut_year(self, date_i, date_f):
        self.section = self.data.loc[(self.data.index >= date_i) &
                                          (self.data.index < date_f)] 
                            
class grouping:

    def __init__(self,df):
        self.df=df        

    def hourly_mean_weekdays(self):
        self.mon=self.df.loc[self.df.index.weekday == 0]
        self.tue=self.df.loc[self.df.index.weekday == 1]
        self.wed=self.df.loc[self.df.index.weekday == 2]
        self.thu=self.df.loc[self.df.index.weekday == 3]
        self.fri=self.df.loc[self.df.index.weekday == 4]
        self.sat=self.df.loc[self.df.index.weekday == 5]
        self.sun=self.df.loc[self.df.index.weekday == 6]
        self.mon=self.mon.groupby(self.mon.index.hour).mean()
        self.tue=self.tue.groupby(self.tue.index.hour).mean()
        self.wed=self.wed.groupby(self.wed.index.hour).mean()
        self.thu=self.thu.groupby(self.thu.index.hour).mean()
        self.fri=self.fri.groupby(self.fri.index.hour).mean()
        self.sat=self.sat.groupby(self.sat.index.hour).mean()
        self.sun=self.sun.groupby(self.sun.index.hour).mean()

    def seasons(self):
        spri =(self.df.index >= '2015-03-20') & (self.df.index < '2015-06-21') | (self.df.index >= '2016-03-19') & (self.df.index < '2016-06-20')|(self.df.index >= '2017-03-20') & (self.df.index < '2017-06-20')|(self.df.index >= '2018-03-20') & (self.df.index < '2018-06-21')|(self.df.index >= '2019-03-20') & (self.df.index < '2019-06-21')|(self.df.index >= '2020-03-19') & (self.df.index < '2020-06-20')
        summ = (self.df.index >= '2015-06-21') & (self.df.index < '2015-09-23') |(self.df.index >= '2016-06-20') & (self.df.index < '2016-09-22')|(self.df.index >= '2017-06-20') & (self.df.index < '2017-09-22')|(self.df.index >= '2018-06-21') & (self.df.index < '2018-09-22')|(self.df.index >= '2019-06-21') & (self.df.index < '2019-09-23')|(self.df.index >= '2020-06-20') & (self.df.index < '2020-09-22')
        autu = (self.df.index >= '2015-09-23') & (self.df.index < '2015-12-21')|(self.df.index >= '2016-09-22') & (self.df.index < '2016-12-21')|(self.df.index >= '2017-09-22') & (self.df.index < '2017-12-21')|(self.df.index >= '2018-09-22') & (self.df.index < '2018-12-21')|(self.df.index >= '2019-09-23') & (self.df.index < '2019-12-21')|(self.df.index >= '2020-09-22') & (self.df.index < '2020-12-21')
        wint = (self.df.index >= '2014-12-21') & (self.df.index < '2015-03-20')|(self.df.index >= '2015-12-21') & (self.df.index < '2016-03-19')|(self.df.index >= '2016-12-21') & (self.df.index < '2017-03-20')|(self.df.index >= '2017-12-21') & (self.df.index < '2018-03-20')|(self.df.index >= '2018-12-21') & (self.df.index < '2019-03-20')|(self.df.index >= '2019-12-21') & (self.df.index < '2020-03-19')|(self.df.index >= '2020-12-21') & (self.df.index < '2021-03-20')
        self.summer=self.df.loc[summ]
        self.autumn=self.df.loc[autu]
        self.winter=self.df.loc[wint]
        self.spring=self.df.loc[spri]

    def hourly_season_mean(self):
        self.spring=self.spring.groupby(self.spring.index.hour).mean()
        self.summer=self.summer.groupby(self.summer.index.hour).mean()
        self.autumn=self.autumn.groupby(self.autumn.index.hour).mean()
        self.winter=self.winter.groupby(self.winter.index.hour).mean()