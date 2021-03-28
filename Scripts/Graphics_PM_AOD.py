import matplotlib.pyplot as plt
from functions_AOD_OMI import *
from functions_MODIS import *
from functions_SIMA import *
from functions_AOD import *
import pandas as pd


def plot_month_means_AOD(data_list, years):
    """
    Funcion que grafica en diferentes subplots el promedio mensual en
    cada año junto con los datos de AOD promedio mensual
    """
    # Calculo de los nombres de los meses a imprimir
    choose_months = np.arange(1, 11, 3)
    choose_months = np.append(choose_months, 12)
    month_names = obtain_month_names(choose_months)
    # Divisón de las graficas
    fig, axs = plt.subplots(2, 3,
                            sharex=True,
                            sharey=True,
                            figsize=(12, 9))
    plt.subplots_adjust(left=0.083, right=0.9, top=0.9)
    axs = np.reshape(axs, 6)
    for year, ax in zip(years, axs):
        ax2 = ax.twinx()
        ax.set_xticks(choose_months)
        ax.set_xticklabels(month_names, rotation=45, fontsize=12)
        ax.set_xlim(1, 12)
        ax.set_ylim(20, 140)
        ax.set_yticks(np.arange(20, 160, 20))
        ax.set_title("Year: {}".format(year))
        ax.grid(ls="--", color="grey", alpha=0.5, lw=2)
        for data, color, label, ax_data in data_list:
            if ax_data == "AOD":
                ax_plot = ax2
            else:
                ax_plot = ax
            months, data = data_to_plot(data, year)
            ax_plot.plot(months, data,
                         ls="--", color=color,
                         marker="o", label=label, alpha=0.5)
        ax2.set_ylim(0, 1.2)
        if not ax in [axs[2], axs[5]]:
            ax2.set_yticks(([]))
        else:
            ax2.set_yticks(np.linspace(0, 1.2, 5))
    fig.text(0.02, 0.5, "PM$_{10}$", rotation=90, fontsize=14)
    fig.text(0.95, 0.5, "AOD$_{550nm}$", rotation=-90, fontsize=14)
    lines, labels = fig.axes[0].get_legend_handles_labels()
    lines.append(fig.axes[-1].get_legend_handles_labels()[0][0])
    labels.append(fig.axes[-1].get_legend_handles_labels()[1][0])
    fig.legend(lines, labels, loc="upper center",
               ncol=7, frameon=False, fontsize=8)
    plt.show()


def data_to_plot(data, year):
    data_plot = []
    months = []
    for month in range(1, 13):
        if data[year][month] != 0:
            data_plot.append(data[year][month])
            months.append(month)
    return months, data_plot


def read_data(PM, MODIS, OMI, path):
    MODIS.read_data(path)
    OMI.read_data(path)
    PM.read_data(path)


def calc_month_mean_of_data(PM, AOD, MODIS, OMI):
    AOD.calc_month_mean_AOD_list()
    PM.calc_month_hour_mean()
    MODIS.calc_month_mean()
    OMI.calc_month_mean()


inputs = {
    "year initial": 2015,
    "year final": 2020,
    "path data": "../Archivos/",
    "path stations": "../Stations/",
    "path graphics": "../Graphics/PM10/",
    "stations names file": "Stations_name",
    "particle type": "PM10",
    "AOD MODIS file": "MODIS_AOD",
    "AOD MODIS type": "AOD Deep Blue",
    "AOD OMI scale": "1",
    "AOD OMI wavelength": "500nm"
}
stations = pd.read_csv(
    inputs["path data"]+inputs["stations names file"]+".csv")
stations_len = stations["Nombre"].count()
colors = ['firebrick',
          'deeppink',
          'darkorange',
          'gold',
          'limegreen',
          'darkgreen',
          'darkslategrey',
          'darkturquoise',
          'dodgerblue',
          'saddlebrown',
          'indigo',
          'blueviolet',
          'lightsalmon']
data_plot = []
for station, color in zip(range(stations_len), colors):
    PM_data = SIMA_data(
        inputs["year initial"],
        inputs["year final"],
        stations["Nombre"][station],
        inputs["particle type"],
    )
    PM_data.read_data(inputs["path data"])
    PM_data.calc_month_hour_mean()
    data_plot.append([PM_data.month_hour_mean,
                      color,
                      stations["Name"][station].capitalize(),
                      "PM10"])
OMI_data_list = AOD_OMI_data(
    inputs["year initial"],
    inputs["year final"],
    inputs["AOD OMI wavelength"],
    inputs["AOD OMI scale"],
)
OMI_data_list.read_data(inputs["path data"])
OMI_data_list.calc_month_mean()
data_plot.append([OMI_data_list.month_mean, "green", "OMI", "AOD"])
plot_month_means_AOD(data_plot, PM_data.years)
plt.savefig(inputs["path graphics"]+"AOD_OMI.png", dpi=400)
