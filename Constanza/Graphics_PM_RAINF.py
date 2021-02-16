import matplotlib.pyplot as plt
from functions_SIMA import *
import pandas as pd


inputs = {
    "year initial": 2015,
    "year final": 2020,
    "path data": "../Archivos/",
    "stations": ["NOROESTE", "NORESTE"],
}

estacion="NORESTE"
rainfmax=0.15
rainfstep=0.05

PM10 = SIMA( inputs["year initial"], inputs["year final"], inputs["stations"] )
PM25 = SIMA( inputs["year initial"], inputs["year final"], inputs["stations"] )
RAINF = SIMA( inputs["year initial"], inputs["year final"], inputs["stations"] )

PM10.read_data("PM10_SIMA.csv",inputs["path data"])
PM25.read_data("PM2.5_SIMA.csv",inputs["path data"])
RAINF.read_data("RAINF_SIMA.csv",inputs["path data"])

PM10.calc_month_mean(estacion)
PM25.calc_month_mean(estacion)
RAINF.calc_month_mean(estacion)

choose_months = np.arange(1, 11, 3)
choose_months = np.append(choose_months, 12)
month_names = obtain_month_names(choose_months)
fig, axs = plt.subplots(2, 3, sharex=True, sharey=True, figsize=(14, 7))
plt.subplots_adjust(left=0.083, right=0.95, top=0.926)
axs = np.reshape(axs, 6)
for year, ax in zip(PM10.years, axs):
    ax.set_xticks(choose_months)
    ax.set_xticklabels(month_names, rotation=45, fontsize=10)
    ax.set_xlim(1, 12)
    ax.set_ylim(0, 110)
    ax.set_title("Year: {}".format(year))
    ax.grid(ls="--", color="grey", alpha=0.5, lw=2)
    ax.plot( np.arange(1, 13), PM10.month_mean[year], ls="--", 
            color="green", lw=3, marker="o",label="PM$_{10}$")
    ax.plot(np.arange(1, 13), PM25.month_mean[year], ls="--", 
            color="purple", lw=3, marker="o",label="PM$_{2.5}$")
    ax0=ax.twinx()
    ax0.bar(np.arange(1, 13),RAINF.month_mean[year],0.5,label="Rainfall",color="gray",alpha=0.6)
    #ax0.set_ylim(0, rainfmax)
    ax0.set_yticks(np.arange(0, rainfmax, step=rainfstep))
    if year == 2015 or year == 2018: ax.set_ylabel("PM (ug/m3)", fontsize=12)
    if year == 2017 or year == 2020: 
        ax0.set_ylabel("Rainfall (mm/hr)", fontsize=12)
#ax.legend(loc=(0.3,0.65),prop={'size': 8})
#ax0.legend(loc=(0.3,0.55),prop={'size': 8})

plt.show()