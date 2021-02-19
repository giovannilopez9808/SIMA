import matplotlib.pyplot as plt
import numpy as np
import datetime


def obtain_month_names(months):
    names = []
    for month in months:
        date = datetime.date(2020, month, 1)
        names.append(date.strftime("%b"))
    return names


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
o3 = np.transpose(np.loadtxt("../Archivos/Ozono_OMI.csv",
                             skiprows=1, usecols=np.arange(1, 17), delimiter=","))
# <-------------Datos para las graficas y calculos--------------->
Meses = obtain_month_names(np.arange(1, 13))
# <------Informacion para las graficas------------->
year_i = 2005
year_f = 2020
delta = 3
levels = np.arange(230, 290+10, 10)
nums, years = define_yticks(year_i, year_f, delta)
daysnum = np.arange(0, 365, 30.5)
# <-------Mapa de colores---------->
mapcolor = "viridis"
plt.subplots_adjust(left=0.11, right=0.97, bottom=0.133, top=0.94)
title = "Period "+str(year_i)+"-"+str(year_f)
#plt.title(title, fontsize="large")
plt.xticks(daysnum, Meses, rotation=60, fontsize="large")
plt.yticks(nums, years, fontsize="large")
plot_grids(daysnum, year_i, year_f)
plt.contourf(o3, cmap=mapcolor, levels=levels)
cbar = plt.colorbar()
cbar.ax.set_ylabel("Total Ozone Column (DU)", rotation=-
                   90, va="bottom", fontsize="large")
# <---------Guardado de la grafica---------->
plt.savefig("../Graphics/Ozono_Daily.png", dpi=400)
