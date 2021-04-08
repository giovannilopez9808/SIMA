from sklearn.linear_model import LinearRegression
from functions_AOD_OMI import *
from functions_SIMA import *

inputs = {"year i": 2015,
          "year f": 2020,
          "path data": "../Archivos/",
          "path graphics": "../Graphics/PM10/",
          "path stations": "../Stations/",
          "stations names file": "Stations_name",
          # AOD specification
          "wavelen": "500nm",
          "resolution": "1",
          "bins": [n for n in range(0, 160+1, 20)], }
stations = pd.read_csv(
    inputs["path data"]+inputs["stations names file"]+".csv")
stations_len = stations["Nombre"].count()

AOD = AOD_OMI_data(inputs["year i"],
                   inputs["year f"],
                   inputs['wavelen'],
                   inputs['resolution'])
AOD.read_data(inputs['path data'])


for station_i in range(stations_len):
    station = stations["Nombre"][station_i]
    PM10 = SIMA_data(inputs["year i"],
                     inputs["year f"],
                     station,
                     "PM10")
    PM10.read_data(inputs['path data'])
    df = {'PM10': PM10.data_hour[station], 'AOD': AOD.data[inputs['wavelen']]}
    AOD_PM10 = pd.DataFrame(df).resample(
        "D").mean().dropna().sort_values("PM10")

    AOD_PM10_bins = AOD_PM10.groupby(
        pd.cut(AOD_PM10['PM10'],  inputs["bins"])).mean()
    AOD_PM10_error = AOD_PM10.groupby(
        pd.cut(AOD_PM10['PM10'], inputs["bins"])).std()

    X = AOD_PM10_bins["PM10"].values.reshape(-1, 1)
    Y = AOD_PM10_bins["AOD"].values.reshape(-1, 1)
    linear_regressor = LinearRegression()
    linear_regressor.fit(X, Y)
    Y_pred = linear_regressor.predict(X)
    r_sqd = linear_regressor.score(X, Y)

    fig = plt.figure(figsize=(6, 6))
    plt.grid(ls="--",
             color="grey",
             alpha=0.5,
             lw=2)
    plt.scatter(list(AOD_PM10["PM10"]), list(AOD_PM10["AOD"]),
                s=6,
                alpha=0.8,
                color="slateblue")
    plt.plot(X, Y_pred,
             color='maroon')
    plt.scatter(X, Y,
                s=10,
                c='red')
    plt.errorbar(X, Y, AOD_PM10_error["AOD"],
                 linestyle="None",
                 lw=1.5,
                 color="orange")
    plt.title("{} R$^2$={:.2f}".format(
        stations["Name"][station_i].capitalize(), r_sqd))
    plt.ylim(0)
    plt.xlim(0)
    plt.ylabel('AOD$_{500nm}$')
    plt.xlabel('PM$_{10}$')
    plt.savefig(inputs["path graphics"]+"Linear_reg_" +
                station.capitalize()+'.png')
