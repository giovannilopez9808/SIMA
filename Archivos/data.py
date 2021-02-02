import matplotlib.pyplot as plt
import numpy as np
years=np.arange(2005,2021,2)
years=np.append(years,2020)
nums=np.arange(0,16,2)
nums=np.append(nums,15)
ozono=np.transpose(np.loadtxt("Ozono3.csv",skiprows=1,usecols=np.arange(1,17),delimiter=","))
plt.ylim(0,15)
plt.yticks(nums,years)
plt.contourf(ozono)
plt.show()
