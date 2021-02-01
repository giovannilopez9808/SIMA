import datetime
import math
import os


def mkdir(name, path=""):
    try:
        os.mkdir(path+name)
    except FileExistsError:
        print()


def format_date(date):
    date = str(date)
    date = "0"*(2-len(date))+date
    return date


def xlsxdate2date(xldate):
    date = datetime.datetime(1899, 12, 30) + datetime.timedelta(days=xldate)
    day = format_date(date.day)
    month = format_date(date.month)
    year = str(date.year)[2:4]
    date = year+month+day
    return date


def save_measurement(data):
    if data == "":
        data = 0
    if math.isnan(data) == True:
        data = 0
    else:
        data = float(data)
    # Si la medicion es menor a 0, dar el valor de 0
    if data < 0:
        data = 0
    # Cambios de medicion a W/m^2
    data = data*1000
    return str(data)
