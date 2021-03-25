from functions_CONS import *
from sklearn.linear_model import LinearRegression

inputs = {"year i": 2015,
          "year f": 2020,
          "path data": "../Archivos/",
          #AOD specification
          "wavelen": "500nm", 
          "resolution": "1"}

AOD=AOD_OMI_data(inputs['wavelen'],inputs['resolution'])
AOD.read_data(inputs['path data'])
 
PM10_hour=SIMA_data('PM10_hour')
PM10_hour.read_data_SIMA(inputs['path data'])

for station in PM10_hour.data.columns:
    df = {'PM10':PM10_hour.data[station],'AOD':AOD.data[inputs['wavelen']]}
    AOD_PM10 = pd.DataFrame(df).resample("D").mean().dropna().sort_values("PM10")

    bins=[n for n in range(0,160+1,20)]

    AOD_PM10_bins=AOD_PM10.groupby(pd.cut(AOD_PM10['PM10'],bins)).mean()
    AOD_PM10_error=AOD_PM10.groupby(pd.cut(AOD_PM10['PM10'],bins)).std()

    X=AOD_PM10_bins["PM10"].values.reshape(-1, 1)
    Y=AOD_PM10_bins["AOD"].values.reshape(-1, 1)
    linear_regressor = LinearRegression()
    linear_regressor.fit(X, Y)
    Y_pred = linear_regressor.predict(X)
    r_sqd=linear_regressor.score(X,Y)

    #PLOT
    fig= plt.figure(figsize=(6,6))
    plt.grid(ls="--", color="grey", alpha=0.5, lw=2)
    plt.plot(AOD_PM10["PM10"],AOD_PM10["AOD"],"g.",markersize=6,alpha=0.8,color="slateblue")
    plt.plot(X, Y_pred, color='maroon')
    plt.plot(X,Y,"r.",markersize=10,color='red')
    plt.errorbar(X,Y,AOD_PM10_error["AOD"],linestyle="None",lw=1.5,color="orange")
    plt.title('AOD vs. PM10 2015-2020 '+ station)
    plt.ylabel('AOD (500 nm)')
    plt.xlabel('PM10')
    plt.text(100,0.85,'R\u00b2='+str(r_sqd))
    plt.savefig('../Graphics/PM10-AOD/'+station+'.png')