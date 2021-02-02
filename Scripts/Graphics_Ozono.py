import matplotlib.pyplot as plt
import numpy as np


def define_yticks(year_i, year_f, delta):
    years = np.arange(year_i, year_f, delta)
    if not(year_f in years):
        years = np.append(years, year_f)
    nums = years-year_i
    return nums, years


def plot_grids(days, year_i, year_f):
    years = np.arange(year_i, year_f+1)-year_i
    for year in years:
        plt.plot([0, 364], [year, year], ls="--", color="#000")
    for day in days:
        plt.plot([day, day], [0, year_f-year_i], ls="--", color="#000")


print("Leyendo datos de Ozono")
# <----------------Lectura de los archivos------------------>
o3 = np.transpose(np.loadtxt("../Archivos/OzonoMty.csv",
                             skiprows=1, usecols=np.arange(1, 17), delimiter=","))
# <-------------Datos para las graficas y calculos--------------->
Meses = ["January", "February", "March", "April", "May", "June",
         "July", "August", "September", "October", "November", "December"]
# <------Informacion para las graficas------------->
year_i = 2005
year_f = 2020
delta = 3
levels = np.arange(210, 300+15, 15)
nums, years = define_yticks(year_i, year_f, delta)
daysnum = np.arange(0, 365, 30.5)
# <-------Mapa de colores---------->
mapcolor = "viridis"
plt.subplots_adjust(left=0.11, right=0.97, bottom=0.20, top=0.94)
title = "Period "+str(year_i)+"-"+str(year_f)
plt.title(title, fontsize="large")
plt.xticks(daysnum, Meses, rotation=60, fontsize="large")
plt.yticks(nums, years, fontsize="large")
plot_grids(daysnum, year_i, year_f)
plt.contourf(o3, cmap=mapcolor, levels=levels)
cbar = plt.colorbar()
cbar.ax.set_ylabel("Total Ozone Column (DU)", rotation=-
                   90, va="bottom", fontsize="large")
# <---------Guardado de la grafica---------->
plt.savefig("../Graphics/OzonoDaily.png", dpi=200)
