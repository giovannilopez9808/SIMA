from SMARTS_algorithm import *
from functions import *
import numpy as np

input_parameters = {
    "path stations": "../../Stations/",
    "path results": "Results_SMARTS_DR/",
    "file results": "Data_found_2015.csv",
    "file data": "datos.txt",
    "stations": ["noroeste"],
    "hour initial": 9,
    "hour final": 16,
    "lon initial": 285,
    "lon final": 2800,
    "AOD inicial": 0.01,
    "AOD limite": 1,
    "RD limite": 10,
    "RD delta": 0.5,
}

SMARTS_Model = SMARTS_DR(input_parameters["hour initial"],
                         input_parameters["hour final"],
                         input_parameters["lon initial"],
                         input_parameters["lon final"],
                         input_parameters["RD limite"],
                         input_parameters["RD delta"])

for station in input_parameters["stations"]:
    print("Calculando estacion "+station)
    dir_station = input_parameters["path stations"]+station+"/"

    mkdir(input_parameters["path results"], path=dir_station)
    dir_results = dir_station+input_parameters["path results"]
    AOD_file = open(dir_station+input_parameters["file results"], "w")
    AOD_file.write("Date,year,month,day,ozone,AOD,RD\n")
    dates, o3_list, years, months, days = np.loadtxt(
        dir_station+input_parameters["file data"], unpack=True)
    for date, o3, year, month, day in zip(dates, o3_list, years, months, days):
        date = str(int(date))
        SMARTS_Model.initialize_aod(input_parameters["AOD inicial"],
                                    input_parameters["AOD limite"])
        year, month, day = int_dates(year, month, day)
        hour, data = np.loadtxt(dir_station+"/Mediciones/" +
                                date+".txt", skiprows=SMARTS_Model.hour_i, unpack=True)
        data_max = np.max(data[0:SMARTS_Model.hour_i])
        print("\tCalculando el dia ", year, month, day)
        var = False
        aod = (SMARTS_Model.aod_i+SMARTS_Model.aod_lim)/2
        iter = 0
        while not(var):
            if iter < 40:
                SMARTS_Model.run_SMARTS(day, month, year, o3, aod,
                                        date, path=dir_results)
                data_model = find_max(date, path=dir_results)
                var, RD = SMARTS_Model.RD_decision(data_model, data_max)
                if var:
                    print(SMARTS_Model.aod_i, "\t",
                          aod, "\t", SMARTS_Model.aod_lim, "\t", RD)
                    writeAOD(AOD_file, date, year, month, day, o3, aod, RD)
                else:
                    print(SMARTS_Model.aod_i, "\t", aod,
                          "\t", SMARTS_Model.aod_lim, "\t", RD)
                    aod = SMARTS_Model.aod_binary_search(aod, RD)
                    if (SMARTS_Model.aod_i == aod or SMARTS_Model.aod_lim == aod) and abs(RD-SMARTS_Model.RD_lim) < 2:
                        writeAOD(AOD_file, date, year, month, day, o3, aod, RD)
                        var = True
                    iter += 1
            else:
                var = False
    AOD_file.close()
