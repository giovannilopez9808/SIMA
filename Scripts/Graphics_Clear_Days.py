import matplotlib.pyplot as plt
from functions import *
import numpy as np
dir_stations = "../Stations/"
stations = ["noreste", "noroeste"]
titles = ["Northeast", "Northwest"]
dates_list = [["190813", "180827"], ["160212", "170915"]]
fig, axs_list = plt.subplots(2, 2, sharex=True, sharey=True, figsize=(8, 8))
plt.subplots_adjust(left=0.133,
                    bottom=0.11,
                    right=0.96,
                    top=0.88,
                    wspace=0.148)
axs_list = np.transpose(axs_list)
for station, title, axs, dates_select in zip(stations, titles, axs_list, dates_list):
    dir_station = dir_stations+station+"/"
    dates = np.loadtxt(dir_station+"days.txt", dtype=str)
    n_dates = len(dates)
    for i, ax, date in zip(range(2), axs, dates_select):
        date_title = yymmdd2yyyy_mm_dd(date)
        ax.set_xlim(8, 20)
        ax.set_ylim(0, 1000)
        ax.set_xticks(np.arange(8,21))
        ax.set_title("Date {}".format(date_title))
        hour, data = np.loadtxt(dir_station+"Mediciones/" +
                                date+".txt", unpack=True)
        ax.plot(hour, data, color="#852A20",lw=3,marker="o")
fig.text(0.26, 0.93, "Northeast", fontsize=13)
fig.text(0.71, 0.93, "Northwest", fontsize=13)
fig.text(0.04, 0.35, "Irradiance solar (W/m$^2$)", rotation=90, fontsize=13)
fig.text(0.47, 0.04, "Local Time (h)", fontsize=13)
plt.savefig("../Graphics/Clear_days.png",dpi=400)
