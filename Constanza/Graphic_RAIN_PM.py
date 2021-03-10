from functions_CONS import *

inputs = {"year i": 2015,
          "year f": 2020,
          "path data": "../Archivos/"}
    
PM10=SIMA_data('PM10')
PM10.read_data_SIMA(inputs['path data'])

RAINF=SIMA_data('RAINF')
RAINF.read_data_SIMA(inputs['path data'])

for station in PM10.data.columns:
    PM10.calc_month_mean(station,inputs['year i'],inputs['year f'])
    RAINF.calc_month_sum(station,inputs['year i'],inputs['year f'])

    choose_months = np.arange(1, 11, 3)
    choose_months = np.append(choose_months, 12)
    month_names = obtain_month_names(choose_months)
    fig, axs = plt.subplots(2, 3, sharex=True, sharey=True, figsize=(18, 8))
    plt.subplots_adjust(left=0.083, right=0.9, top=0.9)
    axs = np.reshape(axs, 6)
    for year, ax in zip(PM10.years, axs):
        ax2 = ax.twinx()
        ax.set_xticks(choose_months)
        ax.set_xticklabels(month_names, rotation=45, fontsize=12)
        ax.set_xlim(1, 12)
        #ax.set_ylim(0, 120)
        ax.set_title("Year: {}".format(year))
        ax.grid(ls="--", color="grey", alpha=0.5, lw=2)
        # Ploteo del valor de PM10
        ax.plot(np.arange(1, 13), PM10.month_mean[year], ls="--", color="purple", marker="o", label="PM$_{10}  mean$")
        ax2.set_ylim(0, 50)
        if not ax in [axs[2], axs[5]]:
            ax2.set_yticks(([]))
        # Ploteo del valor de lluvias
        ax2.bar(np.arange(1, 13), RAINF.month_sum[year], 0.5, label="Rainfall",alpha=0.6)
    fig.text(0.02, 0.5, "PM$_{10}  (\mu g/m^3)$", rotation=90, fontsize=14)
    fig.text(0.95, 0.5, "Accumulated rainfall (mm/hr)", rotation=-90, fontsize=14)
    lines, labels = fig.axes[-1].get_legend_handles_labels()
    lines.append(fig.axes[0].get_legend_handles_labels()[0][0])
    labels.append(fig.axes[0].get_legend_handles_labels()[1][0])
    fig.legend(lines, labels, loc="upper center",
            ncol=5, frameon=False, fontsize=12)
    plt.savefig('../Graphics/PM10_RAINF_'+station+'.png')
    plt.close()