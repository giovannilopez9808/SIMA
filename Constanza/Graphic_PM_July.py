from functions_CONS import *
from cycler import cycler

inputs = {"year i": 2015,
          "year f": 2020,
          "path data": "../Archivos/",
          #AOD specification
          "wavelen": "500nm", 
          "resolution": "1"}
colorpalette= ['lightcoral', 'coral', 'chocolate', 'orange','lightgreen', 
           'springgreen','paleturquoise','lightskyblue','lightsteelblue',
            'mediumpurple','violet','orchid','palevioletred']

#Read PM10 data
PM10 = SIMA_data('PM10')
PM10.read_data_SIMA(inputs['path data'])
stations = PM10.data.columns

#Graph data of July 2018
PM10.cut_year('2018-07-01', '2018-08-01')
fig = plt.figure(figsize=(18,8))
plt.rc('axes', prop_cycle=(cycler('color', colorpalette)))
for station in stations:
    plt.plot_date(PM10.section.index,PM10.section[station],"-",markersize=10,label=station,alpha=0.8)
plt.grid(ls="--", color="grey", alpha=0.5, lw=2)
plt.gcf().autofmt_xdate()
plt.title('PM$_{10}$ in July 2018')
plt.xlabel('Date')
plt.ylabel('PM$_{10}  (\mu g/m^3)$')
plt.legend(frameon=False, mode="expand", fontsize=12, ncol=4)
# lines, labels = fig.axes[-1].get_legend_handles_labels()
# fig.legend(lines, labels, loc=7,bbox_to_anchor=(0.85, 0.7),
#         ncol=2, frameon=True, fontsize=10)
plt.savefig('../Graphics/PM10/July_2018.png')
plt.close()

#Graph daily means for July 2018
PM10_july_2018_mean = PM10.section.groupby(PM10.section.index.day).mean()
fig = plt.figure(figsize=(16,8))
plt.title('PM$_{10}$ in July 2018 daily mean')
plt.ylabel("PM$_{10}$ ($\mu g/m^3$)", fontsize=12)
plt.xlim(0, 31)
plt.ylim(0, 200)
plt.grid(ls="--", color="grey", alpha=0.5, lw=2)
for station in stations:
    plt.plot(PM10_july_2018_mean.index, list(PM10_july_2018_mean[station]),
            ls="--", lw=2.5, marker="o", label=station)
plt.legend(frameon=False, mode="expand", fontsize=12, ncol=4)
plt.savefig('../Graphics/PM10/July_2018_day.png')
plt.close()

#Graph hourly means for July 2018
PM10_july_2018_hour_mean = PM10.section.groupby(PM10.section.index.hour).mean()
fig = plt.figure(figsize=(16,8))
plt.title('PM$_{10}$ in July 2018 hourly mean')
plt.ylabel("PM$_{10}$ ($\mu g/m^3$)", fontsize=12)
#plt.xlim(0, 31)
plt.ylim(0, 200)
plt.grid(ls="--", color="grey", alpha=0.5, lw=2)
for station in stations:
    plt.plot(PM10_july_2018_hour_mean.index , list(PM10_july_2018_hour_mean[station]),
            ls="--", lw=2.5, marker="o", label=station)
plt.legend(frameon=False, mode="expand", fontsize=12, ncol=3)
plt.savefig('../Graphics/PM10/July_2018_hour.png')
plt.close()

#Comparing it with AOD
AOD=AOD_OMI_data(inputs['wavelen'],inputs['resolution'])
AOD.read_data(inputs['path data'])
AOD.cut_year('2018-07-01', '2018-08-01')
PM10_hour=SIMA_data('PM10_hour')
PM10_hour.read_data_SIMA(inputs['path data'])
PM10_hour.cut_year('2018-07-01', '2018-08-01')
PM10_july_2018_13hour = PM10_hour.section.groupby(PM10_hour.section.index.day).mean()

fig, ax = plt.subplots(figsize=(16,8))
ax.set_ylabel("PM$_{10}$ ($\mu g/m^3$)", fontsize=12)
ax.set_xlim(0, 31)
ax.set_ylim(0, 200)
plt.grid(ls="--", color="grey", alpha=0.5, lw=2)
for station in stations:
    ax.plot(PM10_july_2018_13hour.index, PM10_july_2018_13hour[station],
            ls="--", lw=2.5, marker="o", label=station)
ax0=ax.twinx()
ax0.set_ylim(0,1)
ax0.set_ylabel("AOD (500nm)", fontsize=12)
ax0.bar(PM10_july_2018_13hour.index, list(AOD.section[inputs['wavelen']]),
          color="gray", lw=2.5, alpha=0.6, label="AOD OMI")
lines, labels = fig.axes[-1].get_legend_handles_labels()
for st in range(len(stations)):
    lines.append(fig.axes[0].get_legend_handles_labels()[0][st])
    labels.append(fig.axes[0].get_legend_handles_labels()[1][st])
fig.legend(lines, labels, loc="upper center",
        ncol=5, frameon=True, fontsize=12)
plt.savefig('../Graphics/PM10/July_2018_AOD_day.png')
plt.close()
