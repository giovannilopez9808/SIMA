import matplotlib.pyplot as plt
from functions_AOD_OMI import *
from functions_SIMA import *
inputs = {"year initial": 2015,
          "year final": 2020,
          # Dates cut
          "day initial": "2018-07-01",
          "day final": "2018-08-01",
          "path data": "../Archivos/",
          "path graphics": "../Graphics/PM10/",
          "path stations": "../Stations/",
          "stations names file": "Stations_name",
          # AOD specification
          "wavelength": "500",
          "resolution": "1", }
stations = pd.read_csv(
    inputs["path data"]+inputs["stations names file"]+".csv")
stations_len = stations["Nombre"].count()
colors = ['lightcoral',
          'coral',
          'chocolate',
          'orange',
          'lightgreen',
          'springgreen',
          'paleturquoise',
          'lightskyblue',
          'lightsteelblue',
          'mediumpurple',
          'violet',
          'orchid',
          'palevioletred']
fig, ax = plt.subplots(figsize=(10, 8))
ax2 = ax.twinx()
for station_i, color in zip(range(stations_len), colors):
    station = stations["Nombre"][station_i]
    title = stations["Name"][station_i].capitalize()
    PM10 = SIMA_data(inputs["year initial"],
                     inputs["year final"],
                     station,
                     "PM10",)
    PM10.read_data(inputs["path data"])
    PM10.cut_data_hour_year(inputs["day initial"],
                            inputs["day final"])
    PM10_july_2018 = PM10.section.groupby(
        PM10.section.index.day).mean()
    x = np.array(PM10_july_2018.index)-1
    ax.plot(x, list(PM10_july_2018[station]),
            label=title,
            ls="--",
            marker="o",
            color=color
            )
AOD = AOD_OMI_data(inputs["year initial"],
                   inputs["year final"],
                   inputs["wavelength"],
                   inputs["resolution"])
AOD.read_data(inputs["path data"])
AOD.cut_data_year(inputs["day initial"],
                  inputs["day final"])
AOD_dates = [i for i in range(len(AOD.section.index))]
ax.set_xlim(0, 30)
ax.set_ylim(0, 200)
ax2.set_ylim(0, 1)
ticks = np.linspace(0, 30, 5, dtype=int)
dates_ticks = []
for day in ticks:
    dates_ticks.append(str(consecutiveday2date(int(day)+181, 2018)))
ax.set_xticks(ticks)
ax.set_xticklabels(dates_ticks, rotation=30)
ax2.plot(AOD_dates, AOD.section, label="OMI",
         color="green", ls="--", marker="o")
ax.grid(ls="--", alpha=0.5, color="#000000")
lines, labels = fig.axes[0].get_legend_handles_labels()
lines.append(fig.axes[1].get_legend_handles_labels()[0][0])
labels.append(fig.axes[1].get_legend_handles_labels()[1][0])
fig.legend(lines, labels, loc="upper center",
           ncol=7, frameon=False, fontsize=9)
plt.savefig(inputs["path graphics"]+'July_2018.png')
