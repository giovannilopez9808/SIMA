import numpy as np
import os
names=np.loadtxt("data.ext.txt",dtype=str)
for name,url in names:
    os.system("ffmpeg -i '"+url+"' -c copy -bsf:a aac_adtstoasc '"+name+".mp4'")