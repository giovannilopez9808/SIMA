from functions_CONS import *
from cycler import cycler

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

plt.rc('axes', prop_cycle=(cycler('color', ['firebrick', 'deeppink', 'darkorange', 'gold','limegreen','darkgreen',
              'darkslategrey','darkturquoise','dodgerblue','saddlebrown','indigo','blueviolet','lightsalmon'])))
fig= plt.figure(figsize=(6,6))
plt.grid(ls="--", color="grey", alpha=0.5, lw=2)
for station in PM10_hour.data.columns:
    df = {'PM10':PM10_hour.data[station],'AOD':AOD.data[inputs['wavelen']]}
    AOD_PM10 = pd.DataFrame(df).resample("D").mean().dropna().sort_values("PM10")
    plt.plot(AOD_PM10["PM10"],AOD_PM10["AOD"],".",markersize=6,alpha=0.8,label=station)
plt.title('AOD vs. PM10 2015-2020 ')
plt.ylabel('AOD (500 nm)')
plt.xlabel('PM10')
lines, labels = fig.axes[-1].get_legend_handles_labels()
fig.legend(lines, labels, loc=7,bbox_to_anchor=(0.85, 0.7),
        ncol=2, frameon=True, fontsize=10)
plt.savefig('../Graphics/PM10-AOD/0ALL.png')