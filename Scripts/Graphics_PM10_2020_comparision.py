import matplotlib.pyplot as plt
from functions_SIMA import *
import pandas as pd
import os

inputs = {
    "year initial": 2015,
    "year final": 2019,
    "path data": "../Archivos/",
    "path graphics": "../Graphics/PM10/",
    "stations names file": "Stations_name",
    "particle type": "PM10",
}
stations = pd.read_csv(
    inputs["path data"]+inputs["stations names file"]+".csv")
stations_len = stations["Nombre"].count()
choose_months = np.arange(1, 13, 1)
month_names = obtain_month_names(choose_months)
for station in range(stations_len):
    print("Analizando estation {}".format(
        stations["Nombre"][station].capitalize()))
    PM_10 = SIMA_data(inputs["year initial"],
                      inputs["year final"],
                      stations["Nombre"][station],
                      inputs["particle type"])
    PM_10.read_data(inputs["path data"])
    PM_10.cut_data_year('2020-01-01', '2020-12-31')
    PM_10_2020 = PM_10.section
    PM_10.cut_data_year('2015-01-01', '2019-12-31')
    PM_10_2019 = PM_10.section
    PM_10_2019_month_mean = PM_10_2019.groupby(PM_10_2019.index.month).mean()
    PM_10_2020_month_mean = PM_10_2020.groupby(PM_10_2020.index.month).mean()
    plt.xticks(choose_months, month_names, rotation=45, fontsize=14)
    plt.yticks(fontsize=14)
    plt.xlim(1, 12)
    plt.ylim(0, 120)
    plt.title(stations["Name"][station].capitalize(), fontsize=14)
    plt.grid(ls="--", color="grey", alpha=0.5, lw=2)
    plt.plot(np.arange(1, 13), list(PM_10_2019_month_mean[stations["Nombre"][station]]),
             ls="--", color="blue", lw=4, marker="o", label="2015-2019")
    plt.plot(np.arange(1, 13), list(PM_10_2020_month_mean[stations["Nombre"][station]]),
             ls="--", color="orangered", lw=4, marker="o", label="2020")
    plt.legend(ncol=2, frameon=False, fontsize=12,
               mode="expand", bbox_to_anchor=(0, 1.07, 1, 0.02))
    plt.savefig(inputs["path graphics"]+"2020_comp_" +
                stations["Nombre"][station].capitalize()+".png", dpi=400)
    plt.clf()
