import matplotlib.pyplot as plt
from functions_SIMA import *
import pandas as pd

inputs = {
    "year initial": 2015,
    "year final": 2019,
    "path data": "../Archivos/",
    "stations": ["NOROESTE", "NORESTE"],
    "stations titles": ["Northwest", "Northeast"],
    "particle type": "PM10",
}
choose_months = np.arange(1, 13, 1)
month_names = obtain_month_names(choose_months)
fig, axs = plt.subplots(1, 2, sharey=True, figsize=(12, 5))
for station, title, ax in zip(inputs["stations"], inputs["stations titles"], axs):
    PM_10 = SIMA_data(inputs["year initial"],
                      inputs["year final"],
                      station,
                      inputs["particle type"])
    PM_10.read_data(inputs["path data"])
    PM_10.cut_year('2020-01-01', '2020-12-31')
    PM_10_2020 = PM_10.section
    PM_10.cut_year('2015-01-01', '2019-12-31')
    PM_10_2019 = PM_10.section
    PM_10_2019_month_mean = PM_10_2019.groupby(PM_10_2019.index.month).mean()
    PM_10_2020_month_mean = PM_10_2020.groupby(PM_10_2020.index.month).mean()
    ax.set_xticks(choose_months)
    ax.set_xticklabels(month_names, rotation=45, fontsize=14)
    ax.set_xlim(1, 12)
    ax.set_ylim(0, 120)
    ax.set_title(title)
    ax.grid(ls="--", color="grey", alpha=0.5, lw=2)
    ax.plot(np.arange(1, 13), list(PM_10_2019_month_mean[station]),
            ls="--", color="blue", lw=4, marker="o", label="2015-2019")
    ax.plot(np.arange(1, 13), list(PM_10_2020_month_mean[station]),
            ls="--", color="orangered", lw=4, marker="o", label="2020")
lines, labels = fig.axes[-1].get_legend_handles_labels()
fig.legend(lines, labels, loc="upper center",
           ncol=5, frameon=False, fontsize=12)
plt.savefig("../Graphics/PM10_2020_comp.png", dpi=400)
