import matplotlib.pyplot as plt
from functions import *
import pandas as pd
import numpy as np
import datetime

dir = "../Archivos/"
year_i = 2015
year_f = 2020
delta = 1
days = np.arange(0, 365*7, 365)
years = np.arange(year_i, year_f+2, 1)
data_MODIS = pd.read_csv(dir+"MODIS_AOD.csv", usecols=[1, 2])
data_MODIS = data_MODIS.fillna(0)
plt.xticks(days, years, rotation=60, fontsize="large")
plt.ylabel("AOD$_{550nm}$",fontsize=12)
plt.xlabel("Years",fontsize=12)
plt.grid(ls="--", color="#000", lw=2, alpha=0.5)
plt.ylim(0, 0.8)
plt.xlim(0, 365*6)
plt.subplots_adjust(left=0.11,
                    bottom=0.18,
                    right=0.95,
                    top=0.93)
for key in data_MODIS:
    label=key.replace("AOD ","")
    data = np.array(data_MODIS[key])
    x = np.arange(len(data))
    plt.scatter(x[data != 0], data[data != 0],
                label=label, marker=".", alpha=0.6)
    plt.legend(frameon=False, ncol=2, mode="expand",
               bbox_to_anchor=(0, 1.07, 1, 0.02), markerscale=2)
plt.savefig("../Graphics/AOD_Daily_MODIS.png", dpi=400)
