# <----------------Programa que grafica el archivos OzonoMTY.txt en una grafica------------->
import numpy as np
import matplotlib.pyplot as plt
import datetime
print("Leyendo datos de Ozono")
# <----------------Lectura de los archivos------------------>
o3 = np.transpose(np.loadtxt("../Archivos/OzonoMTY.txt"))
# <-------------Datos para las graficas y calculos--------------->
Meses = ["January", "February", "March", "April", "May", "June",
         "July", "August", "September", "October", "November", "December"]
numyear = np.arange(2005, 2020, 2)
# <------Informacion para las graficas------------->
daysnum, year = np.arange(0, 365, 30.5), np.arange(0, 15, 2)
maxi = o3.max()
mini = o3.min()
# <-------Mapa de colores---------->
mapcolor = "viridis"
plt.subplots_adjust(left=0.11, right=0.97, bottom=0.20, top=0.94)
plt.title("Period 2005-2019", fontsize="large")
plt.yticks(year, numyear, fontsize="large")
# plt.grid(linewidth=1,color="black",linestyle="--")
plt.xticks(daysnum, Meses, rotation=60, fontsize="large")
levels = np.arange(mini, maxi+10, 10)
plt.contourf(o3, cmap=mapcolor, levels=levels)
cbar = plt.colorbar()
cbar.ax.set_ylabel("Total Ozone Column (DU)", rotation=-
                   90, va="bottom", fontsize="large")
# <---------Guardado de la grafica---------->
plt.savefig("../Graphics/OzonoDaily.png", dpi=200)
