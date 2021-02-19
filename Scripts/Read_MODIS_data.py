from pyhdf.SD import SD, SDC
import numpy as np
import datetime
from os import listdir


def format_date(date):
    year = int(date[0:4])
    conse_day = int(date[4:7])-1
    date = str(datetime.date(year, 1, 1)+datetime.timedelta(conse_day))
    return date


def validate_data(data):
    if data < 0:
        data = ""
    data = str(data)
    return data


# LAS COORDENADAS DE LAS ESTACIONES
NElat = 25.75
NElon = -100.366

dir_data = "MODIS/"

# Lee archivo por archivo dentro de la carpeta "MYD04_3K"
files = sorted(listdir(dir_data))

all_data = []
outfile = open("MODIS_AOD.csv", "w")
outfile.write("Date,AOD Land Ocean Mean,AOD Deep Blue\n")
for file in files:
    date = file.split('.')[1][1:]
    date = format_date(date)
    print('\n' + date)
    f = SD(dir_data+file, SDC.READ)
    # seleccion de celda según longitud y latitud
    lon = f.select('XDim')[:]
    lat = f.select('YDim')[:]
    AOD = f.select('AOD_550_Dark_Target_Deep_Blue_Combined_Mean')[:]
    AOD_LO = f.select('Aerosol_Optical_Depth_Land_Ocean_Mean')[:]

    idx_lat_sel = np.argmin(abs(lat - NElat))
    idx_lon_sel = np.argmin(abs(lon - NElon))

    AOD_val = float(AOD[idx_lat_sel][idx_lon_sel])*0.001
    AOD_val = validate_data(AOD_val)
    AOD_LO_val = float(AOD_LO[idx_lat_sel][idx_lon_sel])*0.001
    AOD_LO_val = validate_data(AOD_LO_val)

    print("Lat={:.3f}, Lon={:.3f}, AOD={}, AOD_LO={}".format(
        lat[idx_lat_sel], lon[idx_lon_sel], AOD_val, AOD_LO_val))
    outfile.write("{},{},{}\n".format(date, AOD_LO_val, AOD_val))
outfile.close()
