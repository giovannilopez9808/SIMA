import matplotlib.pyplot as plt
from functions_AOD_OMI import *
from functions_SIMA import *
inputs = {"year initial": 2015,
          "year final": 2020,
          # Dates cut
          "day initial": "2018-07-01",
          "day final": "2018-08-01",
          "path data": "../Archivos/",
          "station": "NOROESTE",
          "stations": ["NOROESTE", "NORESTE"],
          # AOD specification
          "wavelength": "500",
          "resolution": "1", }
AOD = AOD_OMI_data(inputs["year initial"],
                   inputs["year final"],
                   inputs["wavelength"],
                   inputs["resolution"])
AOD.read_data(inputs["path data"])
AOD.cut_data_year(inputs["day initial"],
                  inputs["day final"])
PM10_noroeste = SIMA_data(inputs["year initial"],
                          inputs["year final"],
                          inputs["stations"][0],
                          "PM10",)
PM10_noroeste.read_data(inputs["path data"])
PM10_noroeste.cut_data_hour_year(inputs["day initial"],
                                 inputs["day final"])
PM10_noreste = SIMA_data(inputs["year initial"],
                         inputs["year final"],
                         inputs["stations"][1],
                         "PM10",)
PM10_noreste.read_data(inputs["path data"])
PM10_noreste.cut_data_hour_year(inputs["day initial"],
                                inputs["day final"])
PM10_july_2018_noroeste = PM10_noroeste.section.groupby(
    PM10_noroeste.section.index.day).mean()
PM10_july_2018_noreste = PM10_noreste.section.groupby(
    PM10_noreste.section.index.day).mean()
AOD_dates = [i for i in range(len(AOD.section.index))]
fig, ax = plt.subplots()
ax2 = ax.twinx()
ax.set_ylim(0, 200)
ax2.set_ylim(0, 1)
ax.plot(PM10_july_2018_noreste.index,
        PM10_july_2018_noreste, label="Northeast", ls="--", marker="o")
ax.plot(PM10_july_2018_noroeste.index,
        PM10_july_2018_noroeste, label="Northwest", ls="--", marker="o")
ax2.plot(AOD_dates, AOD.section, label="OMI",
         color="green", ls="--", marker="o")
lines, labels = fig.axes[0].get_legend_handles_labels()
lines.append(fig.axes[1].get_legend_handles_labels()[0][0])
labels.append(fig.axes[1].get_legend_handles_labels()[1][0])
fig.legend(lines, labels, loc="upper center",
           ncol=5, frameon=False, fontsize=12)
plt.show()
