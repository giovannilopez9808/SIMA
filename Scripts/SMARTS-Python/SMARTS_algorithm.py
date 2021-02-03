from math import ceil
import numpy as np
import os


class SMARTS:

    def __init__(self, hour_i, hour_f, lon_i, lon_f):
        self.hour_i = hour_i
        self.hour_f = hour_f
        self.lon_i = lon_i
        self.lon_f = lon_f
        self.delta_lon = lon_i-280+1
        self.delta_hour = int(hour_f-hour_i)
        self.total_minute = int((hour_f-hour_i)*60)

    def run_SMARTS(self, day, month, year, o3, aod, name, path=""):
        file_date = open(path+name+".txt", "w")
        for min in range(self.total_minute):
            minutes = str(round(self.hour_i+min/60, 4))
            self.write_data_input_SMARTS(day, month, year,
                                         minutes, o3, aod)
            os.system("./smarts.out")
            integral = self.read_results_SMARTS()
            file_date.write(minutes+" "+integral+"\n")
        file_date.close()

    def read_results_SMARTS(self, name_result="data.ext.txt"):
        wavelength, irra = np.loadtxt(
            name_result, skiprows=self.delta_lon, unpack=True)
        integral = irra[0]
        size = np.size(irra)
        for i in range(1, size):
            integral += irra[i]*(wavelength[i]-wavelength[i-1])
        os.system("rm data*")
        integral = str(round(integral))
        return integral

    def write_data_input_SMARTS(self, day, month, year, hour, ozono, aod):
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

    def __init__(self, hour_i, hour_f, lon_i, lon_f, aod_ini, aod_delta, aod_lim, RD_lim):
        SMARTS.__init__(self, hour_i, hour_f, lon_i, lon_f)
        self.aod_i = aod_ini
        self.delta_aod = aod_delta
        self.aod_lim = aod_lim
        self.max_aod = ceil(aod_lim/aod_ini)
        self.RD_lim = RD_lim

    def RD_decision(self, model, measurement):
        var = False
        DR = 100*(model-measurement)/measurement
        if abs(DR) < self.RD_lim or DR < 0:
            var = True
        return var, DR
