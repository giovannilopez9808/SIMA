import pandas as pd
data=pd.read_csv("../Archivos/2019.csv",low_memory=False)
for i in range(365):
    print(i)
    for j in range(24):
        print(data["Date"][i*24+j+2])