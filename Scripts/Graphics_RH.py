import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


def autolabel(rects):
    for rect in rects:
        height = round(rect.get_height(), 2)
        plt.annotate('{:.1f}'.format(height),
                     xy=(rect.get_x() + rect.get_width() / 2, height),
                     xytext=(0, 3),  # 3 points vertical offset
                     textcoords="offset points",
                     ha='center', va='bottom',)


year_i = 2015
dir_data = "../Archivos/"
data = pd.read_csv(dir_data+"RH_SIMA.csv")
data.index = pd.to_datetime(data["Dates"])
data = data.drop("Dates", 1)
mean_year = data.resample("YS").mean()
mean_year = mean_year.mean(axis=1)
print(mean_year.mean())
num = np.array([i for i in range(len(mean_year))])
years = num+year_i
plt.ylim(50, 70)
plt.xlabel("Years")
plt.ylabel("Relative Humidity (%)")
rect = plt.bar([i for i in range(len(mean_year))], mean_year)
plt.xticks(num, years)
autolabel(rect)
plt.show()
