import pandas as pd
dir_data = "../Archivos/"
particle_type = "WSR"
hour_select = 13
data = pd.read_csv(dir_data+particle_type+"_SIMA.csv")
data["Dates"] = pd.to_datetime(data["Dates"])
n = data["Dates"].count()
# Limpieza de horas que no seran usadas
for i in range(n):
    if data["Dates"][i].hour != hour_select:
        data = data.drop(i)
data.to_csv(dir_data+particle_type+"_hour_SIMA.csv", index=False)
