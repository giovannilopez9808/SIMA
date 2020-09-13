import numpy as np 
import matplotlib.pyplot as plt
def plot(range,hist):
    fig,ax=plt.subplots(figsize=(9,7))
    x = np.arange(np.size(hist))  # the label locations
    width =0.75  # the width of the bars
    rects1=plt.bar(x,hist,width,label='MODIS',facecolor="purple")
    plt.xticks(np.arange(5),range)
    plt.ylim(0,100)
    plt.xlim(-0.5,4.5)
    plt.ylabel("Percentage (%)")
    plt.xlabel("AOD$_{550nm}$")
    plt.legend(fontsize=15,frameon=False)
    autolabel(rects1)
    plt.show()
def autolabel(rects):
    for rect in rects:
        height =round(rect.get_height(),2)
        plt.annotate('{}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0,3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom',)
dir="../Archivos/"
data_MODIS=np.loadtxt(dir+"MODIS-AOD.csv",delimiter=",",skiprows=1,usecols=2)
zeros_i=np.size(data_MODIS[data_MODIS<0]);zeros=zeros_i
range=np.round(np.arange(0.2,1.2,0.2),2)
hist=[]
for value in range:
    n=np.size(data_MODIS[data_MODIS<=value])-zeros
    hist=np.append(hist,n)
    zeros+=n
zeros+=-zeros_i
hist=(hist/zeros)*100
plot(range,hist)