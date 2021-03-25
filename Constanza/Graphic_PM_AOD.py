from functions_CONS import *
from cycler import cycler

inputs = {"year i": 2015,
          "year f": 2020,
          "path data": "../Archivos/",
          #AOD specification
          "wavelen": "500nm", 
          "resolution": "1"}
    
PM10_hour=SIMA_data('PM10_hour')
PM10_hour.read_data_SIMA(inputs['path data'])

AOD=AOD_OMI_data(inputs['wavelen'],inputs['resolution'])
AOD.read_data(inputs['path data'])
AOD.calc_month_mean(inputs['year i'],inputs['year f'])

choose_months = np.arange(1, 11, 3)
choose_months = np.append(choose_months, 12)
month_names = obtain_month_names(choose_months)
fig, axs = plt.subplots(2, 3, sharex=True, sharey=True, figsize=(18, 8))
plt.subplots_adjust(left=0.083, right=0.9, top=0.9)
axs = np.reshape(axs, 6)
for year, ax in zip(AOD.years, axs):
    ax2 = ax.twinx()
    ax.set_xticks(choose_months)
    ax.set_xticklabels(month_names, rotation=45, fontsize=12)
    ax.set_xlim(1, 12)
    ax.set_ylim(0, 140)
    ax.set_title("Year: {}".format(year))
    ax.grid(ls="--", color="grey", alpha=0.5, lw=2)
    # Ploteo del valor de PM10 para cada estacion en distinto color
    ax.set_prop_cycle(cycler('color', ['firebrick', 'deeppink', 'darkorange', 'gold','limegreen','darkgreen',
              'darkslategrey','darkturquoise','dodgerblue','saddlebrown','indigo','blueviolet','lightsalmon']))
    for station in PM10_hour.data.columns:
        PM10_hour.calc_month_mean(station,inputs['year i'],inputs['year f'])
        ax.plot(np.arange(1, 13), PM10_hour.month_mean[year], ls="--", marker="o", label=station)
    ax2.set_ylim(0, 1)
    if not ax in [axs[2], axs[5]]:
        ax2.set_yticks(([]))
    # Ploteo del valor de A0D
    ax2.bar(np.arange(1, 13), AOD.month_mean[year], 0.5, label="OMI AOD",alpha=0.6)
fig.text(0.02, 0.5, "PM$_{10}  (\mu g/m^3)$", rotation=90, fontsize=14)
fig.text(0.95, 0.5, "AOD (500nm)", rotation=-90, fontsize=14)
lines, labels = fig.axes[-1].get_legend_handles_labels()
for st in range(len(PM10_hour.data.columns)):
    lines.append(fig.axes[0].get_legend_handles_labels()[0][st])
    labels.append(fig.axes[0].get_legend_handles_labels()[1][st])
fig.legend(lines, labels, loc="upper center",
        ncol=7, frameon=False, fontsize=10)
plt.savefig('../Graphics/PM10_AOD_OMI.png')
plt.show()