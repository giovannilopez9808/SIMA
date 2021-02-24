import requests  # get the requsts library from https://github.com/requests/requests
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import matplotlib.dates as mdates
from sklearn.linear_model import LinearRegression


############################## VARIABLES ##############################
# graf --> los datos de AOD-OMI
# dates --> fechas de AOD-OMI (2015-2018) ***no tiene ciertas fechas
# values --> valores AOD-OMI (2015-2018)
# dosmil15, dosmil16, dosmil17, dosmil18 --> locaciones de values
# ano2015, ano2016, ano2017, ano2018 --> fechas de AOD-OMI
# val2015, val2016, val2017, val2018 --> valores de AOD-OMI
# bb --> tabla del SIMA 2015 cruda
# NO --> Datos Noroeste 2015 PM10 y PM2.5 promedio diario
# NE --> Datos Noreste 2015 PM10 y PM2.5 promedio diario
# SBE --> Datos Noroeste 2016-2019 PM10 y PM2.5 promedio por hora
# SNI --> Datos Noreste 2016-2019 PM10 y PM2.5 promedio por hora
# NOSBE --> Merge datos PM10 y PM2.5 para Noroeste 2015-2019
# NESNI --> Merge datos PM10 y PM2.5 para Noreste 2015-2019
# frames1, frames 2 --> variable que uso temporalmente para merge, mejor no usarla.
# NOresult --> Datos de Noroeste 2015-2018 AOD, PM10 y PM2.5 promedio diario
# NEresult --> Datos de Noreste 2015-2018 AOD, PM10 y PM2.5 promedio diario
# NEr --> Solo AOD y PM10/2.5 (temp)
# X --> valores de PM10 o PM2.5 (temp) 2015-2019
# Y --> valores de AOD 2015-2018
# linear_regressor, Y_pred --> Para regresión linear

# overriding requests.Session.rebuild_auth to mantain headers when redirected

class SessionWithHeaderRedirection(requests.Session):

    AUTH_HOST = 'urs.earthdata.nasa.gov'

    def __init__(self, username, password):

        super().__init__()

        self.auth = (username, password)

   # Overrides from the library to keep headers when redirected to or from

   # the NASA auth host.

    def rebuild_auth(self, prepared_request, response):

        headers = prepared_request.headers

        url = prepared_request.url

        if 'Authorization' in headers:

            original_parsed = requests.utils.urlparse(response.request.url)

            redirect_parsed = requests.utils.urlparse(url)

            if (original_parsed.hostname != redirect_parsed.hostname) and redirect_parsed.hostname != self.AUTH_HOST and original_parsed.hostname != self.AUTH_HOST:

                del headers['Authorization']

        return


# create session with the user credentials that will be used to authenticate access to the data

username = "constanzazu"

password = "T0totlan'"

session = SessionWithHeaderRedirection(username, password)


# All the urls we want to download
# borrar primeros dos links

# Para solo 2015:
#url_list = open("subset_OMAERUVd_V003_20190830_011347.txt").read().splitlines()
# Para 2015-2018
url_list = open("subset_OMAERUVd_V003_20190901_160425.txt").read().splitlines()
len(url_list)


# loop to extract every file and save it in an ultimate file
m = 1
d = 1
a = 2015
f = 28
u = 1

# primera columna de DataFrame de promedios
aod = pd.DataFrame(columns=["date", "(25.5,-100.5)"])

# loop para descargar todos los datos y hacer un Dataframe de promendios
for url in url_list:
    # filename for the url to be used when saving the file
    filename = 'temp.csv'
    # url[url.rfind('/')+1:]

    try:
        # submit the request using the session
        response = session.get(url, stream=True)
        print(response.status_code)
        # raise an exception in case of http errors
        response.raise_for_status()
        # save the file
        with open(filename, 'wb') as fd:
            for chunk in response.iter_content(chunk_size=1024*1024):
                fd.write(chunk)
    except requests.exceptions.HTTPError as e:
        # handle any errors here
        if e != 200:
            print(e, "Problema en {}-{:02d}-{:02d}".format(a, m, d))

    # Leer el archivo y acomodar
    datos = pd.read_csv(filename, engine='python', header=None, skiprows=1,
                        skipfooter=2, names=["meh", "-101.5", "-100.5", "-99.5", "-98.5"])
    datos.insert(1, "lat/lon", [22.5, 23.5, 24.5, 25.5, 26.5, 27.5], True)
    df = datos.drop('meh', axis=1)
    # para guardar cada dia:
    # export_csv=df.to_csv("./AOD/AOD-{}-{:02d}-{:02d}.csv".format(a,m,d),index=False)

    # agregando lineas al DataFrame de promedios
    # df=pd.read_csv("./AOD/AOD-{}-{:02d}-{:02d}.csv".format(a,m,d))
    y = df.at[3, "-100.5"]
    if y < 0:
        sum = 0
        p = 0
        for i in range(2, 5):
            for c in range(1, 4):
                h = df.iat[i, c]
                if h > 0:
                    p = p+1
                    sum = sum+h
        if sum == 0:
            y = "NaN"
        else:
            y = sum/p
    aod.loc[u] = ["{}-{:02d}-{:02d}".format(a, m, d), y]
    u = u+1
    # para ir cambiando fechas
    if m == 4 or m == 6 or m == 9 or m == 11:
        # se toman en cuenta las exepciones de 2016
        if a == 2016 and m == 6 and d == 10:
            d = 14
            # u=u+4
        elif d < 30:
            d = d+1
        else:
            m = m+1
            d = 1
    elif m == 2:
        if d < f:
            d = d+1
        else:
            m = m+1
            d = 1
    else:
        # se toman en cuenta las exepciones de 2016 y 2017
        if a == 2016 and m == 5 and d == 29:
            m = 6
            d = 10
            # u=u+12
        elif a == 2017 and m == 3 and d == 12:
            d = 17
            # u=u+5
        elif d < 31:
            d = d+1
        elif m == 12:
            a = a+1
            m = 1
            d = 1
            # para el año bisiesto:
            if a == 2016 or a == 2020:
                f = 29
            else:
                f = 28
        else:
            m = m+1
            d = 1

# Guardar arshivo de promedios
aod = aod.replace('NaN', '')
export_csv = aod.to_csv("./AOD/Promedios.csv", index=False)