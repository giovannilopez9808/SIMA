from SMARTS_algorithm import *
from numpy import loadtxt
from functions import *

input_parameters = {
    "path stations": "../../Stations/",
    "stations": ["noroeste"],
    "hour initial": 9,
    "hour final": 16,
    "lon initial": 285,
    "lon final": 2800,
    "AOD inicial": 0.01,
    "AOD delta": 0.025,
    "RD limite": 10,
    "AOD limite": 1,
}

input = SMARTS_DR(input_parameters["hour initial"],
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
    dates, o3_list, years, months, days = loadtxt(
        dir_station+"/datos.txt", unpack=True)
    for date, o3, year, month, day in zip(dates, o3_list, years, months, days):
        date = str(int(date))
        year, month, day = int_dates(year, month, day)
        hour, data = np.loadtxt(dir_station+"/Mediciones/" +
                                date+".txt", skiprows=input.hour_i, unpack=True)
        data_max = np.max(data[0:input.hour_i])
        print("           Calculando el dia ", year, month, day, data_max)
        var = False
        aod = input.aod_i
        while not(var):
            if aod < input.aod_lim:
                input.run_SMARTS(day, month, year, o3, aod,
                                 date, path=dir_results)
                data_model = find_max(date, path=dir_results)
                print(data_model)
                var, RD = RD_decision(data_model, data_max, input.RD_lim)
                print(RD, aod)
                if var:
                    writeAOD(AOD_file, date, year, month, day, o3, aod, RD)
                else:
                    aod += input.aod_i
            else:
                var = False
    AOD_file.close()
