import matplotlib.pyplot as plt
from functions import *
import pandas as pd
import numpy as np
import datetime


def get_season(date):
    year = int("20"+date[0:2])
    month = int(date[2:4])
    day = int(date[4:6])
    date = datetime.date(year, month, day)
    seasons = {'Summer': (datetime.date(year, 6, 21), datetime.date(year, 9, 22)),
               'Autumn': (datetime.date(year, 9, 23), datetime.date(year, 12, 20)),
               'Spring': (datetime.date(year, 3, 21), datetime.date(year, 6, 20))}
    for season, (season_start, season_end) in seasons.items():
        if date >= season_start and date <= season_end:
            return season
    else:
        return 'Winter'


def calc_mean_season(data, dir_station):
    seasons = ["Spring", "Autumn", "Summer", "Winter"]
    season_names = ["Spring Sum", "Summer Sum", "Autumn Sum", "Winter Sum",
                    "Spring Count", "Summer Count", "Autumn Count", "Winter Count"]
    season_count = pd.DataFrame(columns=season_names,
                                index=np.arange(24))
    season_count = season_count.fillna(0)
    for date in data:
        measurements = np.loadtxt(dir_station+"Mediciones/" +
                                  date+".txt", unpack=True, usecols=1)
        season = get_season(date)
        for i in range(24):
            if measurements[i] != 0:
                season_count[season+" Sum"][i] += measurements[i]
                season_count[season+" Count"][i] += 1
    season_hourly_mean = pd.DataFrame(columns=seasons,
                                      index=np.arange(24))
    for season in seasons:
        for hour in range(24):
            if season_count[season+" Count"][hour] != 0:
                season_hourly_mean[season][hour] = round(
                    season_count[season+" Sum"][hour]/season_count[season+" Count"][hour], 1)
    return season_hourly_mean


dir_stations = "../Stations/"
season_titles = ["Spring", "Summer", "Autumn", "Winter"]
dates = np.loadtxt(dir_stations+"noreste/days.txt", dtype=str)
season_hourly_mean_noreste = calc_mean_season(dates, dir_stations+"noreste/")
dates = np.loadtxt(dir_stations+"noroeste/days.txt", dtype=str)
season_hourly_mean_noroeste = calc_mean_season(dates, dir_stations+"noroeste/")
hour = np.arange(24)+0.5
fig, axs = plt.subplots(2, 2, sharex=True, sharey=True, figsize=(8, 6))
plt.subplots_adjust(left=0.133,
                    bottom=0.11,
                    right=0.96,
                    top=0.88,
                    wspace=0.148)
axs = np.reshape(axs, 4)
for season_title, ax in zip(season_titles, axs):
    ax.set_xlim(8, 20)
    ax.set_ylim(0, 1000)
    ax.set_xticks(np.arange(8, 21))
    ax.set_title(season_title)
    data = season_hourly_mean_noreste[season_title]
    ax.plot(hour, data, lw=3, marker="o",
            label="Northeast", color="#3e1f47", alpha=0.75)
    data = season_hourly_mean_noroeste[season_title]
    ax.plot(hour, data, lw=3, marker="o",
            label="Northwest", color="#065a60", alpha=0.75)
fig.text(0.04, 0.35, "Solar irradiance (W/m$^2$)", rotation=90, fontsize=13)
fig.text(0.47, 0.04, "Local Time (h)", fontsize=13)
lines, labels = fig.axes[-1].get_legend_handles_labels()
fig.legend(lines, labels, loc="upper center", ncol=2,
           frameon=False, fontsize=12)
plt.savefig("../Graphics/Clear_days.png", dpi=400)
