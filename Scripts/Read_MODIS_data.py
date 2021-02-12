from pyhdf.SD import SD, SDC
import numpy as np
from os import listdir


# LAS COORDENADAS DE LAS ESTACIONES
NElat = 25.75
NElon = -100.366

folder = "MYD04_3K"

# Lee archivo por archivo dentro de la carpeta "MYD04_3K"
files = listdir(folder)

all_data = []
outfile = open("MODIS_AOD.csv", "w")
outfile.write("Date,AOD Land Ocean Mean,AOD Deep Blue\n")
for file in files:
    day = file.split('.')[1][-3:]

    print('\n' + file)
    f = SD("MYD04_3K" + '/' + file, SDC.READ)
    # seleccion de celda según longitud y latitud
    lon = f.select('XDim')[:]
    lat = f.select('YDim')[:]
    AOD = f.select('AOD_550_Dark_Target_Deep_Blue_Combined_Mean')[:]
    AOD_LO = f.select('Aerosol_Optical_Depth_Land_Ocean_Mean')[:]

    idx_lat_sel = np.argmin(abs(lat - NElat))
    idx_lon_sel = np.argmin(abs(lon - NElon))

    AOD_val = float(AOD[idx_lat_sel][idx_lon_sel])
    AOD_LO_val = float(AOD_LO[idx_lat_sel][idx_lon_sel])

    print("Lat={:.3f}, Lon={:.3f}, AOD={:.3f}, AOD_LO={:.3f}".format(
        lat[idx_lat_sel], lon[idx_lon_sel], AOD_val, AOD_LO_val))
    outfile.write("{},{},{}\n".format(day, AOD_LO_val, AOD_val))
outfile.close()
# Name of output file
out_f_name = files[0].split('.')
out_f_name = out_f_name[0] + '.' + out_f_name[1][:-3]
