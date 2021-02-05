import numpy as np
import os
names = np.loadtxt("files.txt", usecols=1, dtype=str,delimiter="\t")
files=names[np.arange(0,np.size(names),2)]
url="https://acdisc.gsfc.nasa.gov/data/Aura_OMI_Level3/OMTO3e.003/"
for file in files:
    year=file[19:23]
    url_download=url+year+"/"+file
    os.system("wget "+url_download)
