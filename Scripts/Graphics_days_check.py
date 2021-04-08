import matplotlib.pyplot as plt
import numpy as np
import os
dir_station = "../Stations/sureste2/"
dates = sorted(os.listdir(dir_station+"Mediciones/"))
for date in dates:
    plt.title(date)
    hour, data = np.loadtxt(dir_station +
                            "Mediciones/"+date, unpack=True)
    plt.plot(hour, data)
    plt.ylim(0, 1200)
    plt.xlim(5, 20)
    plt.savefig(dir_station+"Graphics/"+date.replace(".txt", ".png"))
    plt.clf()
