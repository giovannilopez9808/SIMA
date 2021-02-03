from SMARTS_algorithm import *
from numpy import loadtxt
from functions import *

input_parameters = {
    "path stations": "../../Stations/",
    "stations": ["noroeste", "noreste"],
    "hour initial": 9,
    "hour final": 16,
    "lon initial": 285,
    "lon final": 2800,
    "AOD inicial": 0.01,
    "AOD delta": 0.025,
    "RD limite": 10,
    "AOD limite": 1,
}

SMARTS_Model = SMARTS_DR(input_parameters["hour initial"],
                         input_parameters["hour final"],
                         input_parameters["lon initial"],
                         input_parameters["lon final"],
                         input_parameters["AOD inicial"],
                         input_parameters["AOD delta"],
                         input_parameters["AOD limite"],
                         input_parameters["RD limite"])

for station in input_parameters["stations"]:
    print("Calculando estacion "+station)
    dir_station = input_parameters["path stations"]+station+"/"
    mkdir("Results_SMARTS_DR", path=dir_station)
    dir_results = dir_station+"Results_SMARTS_DR/"
    AOD_file = open(dir_station+"/DataAOD_found.txt", "w")
    AOD_file.write("Date,year,month,day,ozone,AOD,RD\n")
    dates, o3_list, years, months, days = loadtxt(
        dir_station+"/datos.txt", unpack=True)
    for date, o3, year, month, day in zip(dates, o3_list, years, months, days):
        date = str(int(date))
        year, month, day = int_dates(year, month, day)
        hour, data = np.loadtxt(dir_station+"/Mediciones/" +
                                date+".txt", skiprows=SMARTS_Model.hour_i, unpack=True)
        data_max = np.max(data[0:SMARTS_Model.hour_i])
        print("\tCalculando el dia ", year, month, day)
        var = False
        aod = SMARTS_Model.aod_i
        while not(var):
            if aod < SMARTS_Model.aod_lim:
                SMARTS_Model.run_SMARTS(day, month, year, o3, aod,
                                        date, path=dir_results)
                data_model = find_max(date, path=dir_results)
                var, RD = SMARTS_Model.RD_decision(data_model, data_max)
                if var:
                    writeAOD(AOD_file, date, year, month, day, o3, aod, RD)
                else:
                    aod += SMARTS_Model.delta_aod
            else:
                var = False
    AOD_file.close()
