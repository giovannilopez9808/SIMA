import matplotlib.pyplot as plt
from functions_SIMA import *
import pandas as pd

inputs = {
    "year initial": 2015,
    "year final": 2019,
    "path data": "../Archivos/",
    "stations": ["NOROESTE", "NORESTE"],
}

estacion="NORESTE"

PM10 = SIMA( inputs["year initial"], inputs["year final"], inputs["stations"] )
PM25 = SIMA( inputs["year initial"], inputs["year final"], inputs["stations"] )

PM10.read_data("PM10_SIMA.csv",inputs["path data"])
PM25.read_data("PM2.5_SIMA.csv",inputs["path data"])

PM10.cut_year('2020-01-01','2020-12-31')
PM1020=PM10.section
PM10.cut_year('2015-01-01','2019-12-31')
PM10.data=PM10.section

PM10_month_mean = PM10.data.groupby(PM10.data.index.month).mean()
PM1020_month_mean = PM1020.groupby(PM1020.index.month).mean()

choose_months = np.arange(1, 12, 1)
choose_months = np.append(choose_months, 12)
month_names = obtain_month_names(choose_months)
fig,ax=plt.subplots(figsize=(10, 6))
ax.set_ylabel("PM$_{10}$", fontsize=12)
ax.set_xticks(choose_months)
ax.set_xticklabels(month_names, rotation=45, fontsize=14)
ax.set_xlim(1, 12)
ax.set_ylim(0, 120)
ax.set_title("PM$_{10}$ monthly mean",fontsize=18)
ax.grid(ls="--", color="grey", alpha=0.2, lw=1.6)
ax.plot(np.arange(1, 13), PM10_month_mean[estacion], ls="--", color="blue", lw=2.5, marker="o", label="2015-2019")
ax.plot(np.arange(1, 13), PM1020_month_mean[estacion], ls="--", color="orangered", lw=2.5, marker="o",label="2020")
ax.legend(loc=(0.7,0.8),fontsize=14)

plt.show()