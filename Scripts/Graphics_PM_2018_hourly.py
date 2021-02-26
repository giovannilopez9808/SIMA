import matplotlib.pyplot as plt
from functions_SIMA import *
from functions import *
inputs = {
    "year initial": 2015,
    "year final": 2020,
    "path data": "../Archivos/",
    "path graphics": "../Graphics/",
    "path stations": "../Stations/",
    "particle type": "PM10",
}
stations = ["NOROESTE", "NORESTE"]
stations_titles = ["Northwest", "Northeast"]
colors = ["r", "b"]
plt.figure(figsize=(8, 6))
for station, title, color in zip(stations, stations_titles, colors):
    PM_data = SIMA_data(
        inputs["year initial"],
        inputs["year final"],
        station,
        inputs["particle type"],
    )
    PM_data.read_data(inputs["path data"])
    PM_data.cut_year("2018-07-01", "2018-08-01")
    PM_2018 = PM_data.section.groupby(PM_data.section.index.hour).mean()
    plt.plot(np.arange(len(PM_2018)), PM_2018,
             label=title, color=color, lw=2.5, marker="o", ls="--")
plt.grid(ls="--", color="#000", alpha=0.5, lw=2)
plt.xlim(0, 24)
plt.ylim(0, 200)
plt.xticks(np.linspace(0, 24, 7))
plt.legend(frameon=False, ncol=2, mode="expand", fontsize=16)
plt.subplots_adjust(left=0.12, bottom=0.11, right=0.94, top=0.912)
plt.xlabel("Dates", fontsize=16)
plt.ylabel("PM$_{10}$ $(\mu g/m^3)$", fontsize=16)
plt.savefig(inputs["path graphics"]+"PM10_July_2018_hour.png", dpi=400)
