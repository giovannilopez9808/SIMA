import pandas as pd
dir_data="../Archivos/"
particle_type="PM10"
hour_select=13
data=pd.read_csv(dir_data+particle_type+"_SIMA.csv")
n = data["Dates"].count()
# Limpieza de horas que no seran usadas
for i in range(n):
    if data["Hours"][i] != hour_select:
        data = data.drop(i)
data.to_csv(dir_data+particle_type+"_hour_SIMA.csv",index=False)