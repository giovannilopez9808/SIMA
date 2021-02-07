import numpy as np
import os


def mkdir(name, path=""):
    try:
        os.mkdir(path+name)
    except FileExistsError:
        pass


def int_dates(year, month, day):
    year = int(year)
    month = int(month)
    day = int(day)
    return year, month, day


def writeAOD(file, date, year, month, day, o3, aod, DR):
    file.write(str(int(date))+","+str(year)+","+str(month)+","+str(day)+","+str(o3)+","
               + str(round(aod, 3))+","+str(round(DR, 2))+"\n")


def find_max(name, path=""):
    data_model = np.loadtxt(path+name+".txt", usecols=1)
    pos = (np.where(np.max(data_model) == data_model)[0])[0]
    data_model = np.mean(data_model[pos-30:pos+31])
    return data_model
