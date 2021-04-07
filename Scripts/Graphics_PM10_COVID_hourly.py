from functions_season import *
from functions_SIMA import *
import os
inputs = {
    "year i": 2015,
    "year f": 2020,
    "station": "NORESTE",
    "path stations": "../Stations/",
    "path data": "../Archivos/",
    "path graphics": "../Graphics/",
}
stations = [station.upper() for station in os.listdir(inputs["path stations"])]
for station in stations:
    PM10_data = SIMA_data(inputs["year i"],
                          inputs["year f"],
                          station,
                          "PM10"
                          )
    PM10_data.read_data(inputs["path data"])
    # Primer caso confirmado de COVID en AMM: '2020-03-11'
    # Empieza cancelación de clases y eventos: '2020-03-11??'
    PM10_data.cut_data_year("2015-01-01", "2020-03-11")
    PM10_PRE_COVID = PM10_data.section
    PM10_data.cut_data_year("2020-03-11", "2021-01-01")
    PM10_COVID = PM10_data.section
    PM10_PRE_COVID = season_data(PM10_PRE_COVID)
    PM10_COVID = season_data(PM10_COVID)
    PM10_PRE_COVID.calc_hourly_day_mean()
    PM10_COVID.calc_hourly_day_mean()
    hours = [i for i in range(0, 23, 3)]
    hours.append(23)
    fig, (ax1, ax2) = plt.subplots(1, 2, sharey=True, figsize=(10, 6))
    for ax in (ax1, ax2):
        ax.set_xlim(0, 23)
        ax.set_ylim(30, 100)
        ax.grid(ls="--", alpha=0.5, color="#000000")
        ax.set_xticks(hours)
    fig.text(0.45, 0.03, "Local Time (h)", fontsize=12)
    ax1.set_ylabel("PM$_{10}$ ($\mu g/m^3$)", fontsize=12)
    ax1.set_title("PRE-COVID", fontsize=14)
    ax2.set_title("COVID", fontsize=14)
    for day in PM10_COVID.days:
        day = PM10_COVID.days[day]
        ax1.plot(list(PM10_PRE_COVID.hourly_day_mean.index), list(PM10_PRE_COVID.hourly_day_mean[day]),
                 label=day, lw=2.5)
        ax2.plot(list(PM10_COVID.hourly_day_mean.index), list(PM10_COVID.hourly_day_mean[day]),
                 label=day, lw=2.5)
    lines, labels = fig.axes[-1].get_legend_handles_labels()
    fig.legend(lines, labels, loc='upper right',
               ncol=7, frameon=False, fontsize=10)
    fig.suptitle(station,fontsize=12, x=0.1)
    plt.savefig(inputs["path graphics"] +
                "/PM10/COVID_compare_"+station+".png",bbox_inches='tight')
