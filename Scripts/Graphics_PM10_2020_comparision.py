import matplotlib.pyplot as plt
from functions_SIMA import *
import pandas as pd

inputs = {
    "year initial": 2015,
    "year final": 2019,
    "path data": "../Archivos/",
    "stations": ["NOROESTE", "NORESTE"],
    "particle type": "PM10",
}

station = "NORESTE"

PM_10 = SIMA_data(inputs["year initial"],
                  inputs["year final"],
                  inputs["stations"],
                  inputs["particle type"])
PM_10.read_data(inputs["path data"])

PM_10.cut_year('2020-01-01', '2020-12-31')
PM_10_2020 = PM_10.section
PM_10.cut_year('2015-01-01', '2019-12-31')
PM_10_2019 = PM_10.section

PM_10_2019_month_mean = PM_10_2019.groupby(PM_10_2019.index.month).mean()
PM_10_2020_month_mean = PM_10_2020.groupby(PM_10_2020.index.month).mean()

choose_months = np.arange(1, 13, 1)
month_names = obtain_month_names(choose_months)
plt.ylabel("PM$_{10}$ ($\mu g/m^3$)", fontsize=12)
plt.xticks(choose_months, month_names, rotation=45, fontsize=12)
plt.xlim(1, 12)
plt.ylim(0, 120)
plt.grid(ls="--", color="grey", alpha=0.5, lw=2)
plt.plot(np.arange(1, 13), list(PM_10_2019_month_mean[station]),
         ls="--", color="blue", lw=2.5, marker="o", label="2015-2019")
plt.plot(np.arange(1, 13), list(PM_10_2020_month_mean[station]),
         ls="--", color="orangered", lw=2.5, marker="o", label="2020")
plt.legend(frameon=False, mode="expand", fontsize=12, ncol=2)

plt.show()
