import matplotlib.pyplot as plt
import numpy as np
import os
dir_stations = "../Stations/"
stations = sorted(os.listdir(dir_stations))
dates = np.loadtxt(dir_stations+"noreste/days.txt", dtype=str, skiprows=400)
for date in dates:
    plt.title(date)
    for station in stations:
        try:
            hour, data = np.loadtxt(dir_stations+station +
                                    "/Mediciones/"+date+".txt", unpack=True)
            plt.plot(hour, data, label=station)
        except:
            pass
    plt.ylim(0, 1200)
    plt.xlim(5, 20)
    plt.legend(frameon=False)
    plt.show()
