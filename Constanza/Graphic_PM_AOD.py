from functions_CONS import *

inputs = {"year i": 2015,
          "year f": 2020,
          "path data": "../Archivos/"}
    
PM10_hour=SIMA_data(PM10_hour')
PM10_hour.read_data_SIMA(inputs['path data'])

for station in PM10.data.columns:
    PM10_hour.calc_month_mean(station,inputs['year i'],inputs['year f'])
    PM10_hour.month_mean_NO=PM10_hour.month_mean