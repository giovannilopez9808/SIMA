import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import datetime


def obtain_month_names(months):
    names = []
    for month in months:
        date = datetime.date(2020, month, 1)
        names.append(date.strftime("%b"))
    return names


def define_yticks(year_i, year_f, delta):
    years = np.arange(year_i, year_f, delta)
    if not(year_f in years):
        years = np.append(years, year_f)
    nums = years-year_i
    return nums, years


dir = "../Archivos/"
year_i = 2015
year_f = 2020
delta = 1
levels = np.arange(230, 290+10, 10)
nums, years = define_yticks(year_i, year_f, delta)
daysnum = np.arange(0, 365, 30.5)
Meses = obtain_month_names(np.arange(1, 13))
data_MODIS = pd.read_csv(dir+"MODIS_AOD.csv", usecols=[1, 2])
data_MODIS = data_MODIS.fillna(0)
fig, axs = plt.subplots(1, 2, sharey=True, figsize=(12, 5))
for ax, key in zip(axs, data_MODIS):
    ax.set_xticks(daysnum)
    ax.set_xticklabels(Meses, rotation=60, fontsize="large")
    ax.set_yticks(nums)
    ax.set_yticklabels(years, fontsize="large")
    ax.set_title(key)
    data = np.array(data_MODIS[key][0:365*6])
    data = np.reshape(data, (6, 365))
    img = ax.contourf(data, cmap="cool")
    ax.grid(ls="--", color="#000", lw=2, alpha=0.5)
cbar = fig.colorbar(img, fraction=.1, ax=axs,)
cbar.ax.set_ylabel("Aerosol Optical Depth at 550 nm from MODIS", rotation=-
                   90, va="bottom", fontsize="large")
plt.savefig("../Graphics/AOD_Daily_MODIS.png", dpi=400)
