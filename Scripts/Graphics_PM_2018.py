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
plt.figure(figsize=(18, 8))
for station, title, color in zip(stations, stations_titles, colors):
    PM_data = SIMA_data(
        inputs["year initial"],
        inputs["year final"],
        station,
        inputs["particle type"],
    )
    PM_data.read_data(inputs["path data"])
    PM_data.cut_data_year("2018-07-01", "2018-08-01")
    PM_2018 = PM_data.section
    plt.plot(np.arange(len(PM_2018)), PM_2018,
             label=title, color=color)
ticks = np.linspace(0, 31, 5, dtype=int)
dates_ticks = []
for day in ticks:
    dates_ticks.append(str(consecutiveday2date(int(day)+181, 2018)))
plt.grid(ls="--", color="#000", alpha=0.5, lw=2)
plt.xlim(0, 744)
plt.ylim(0, 350)
plt.legend(frameon=False, ncol=2, mode="expand", fontsize=16)
plt.subplots_adjust(left=0.07, bottom=0.193, right=0.95, top=0.912)
plt.xticks(ticks*24, dates_ticks, rotation=30, fontsize=16)
plt.xlabel("Dates", fontsize=16)
plt.ylabel("PM$_{10}$ $(\mu g/m^3)$", fontsize=16)
plt.savefig(inputs["path graphics"]+"PM10_July_2018.png", dpi=400)
