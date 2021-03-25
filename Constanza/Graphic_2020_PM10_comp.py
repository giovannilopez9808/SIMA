from functions_CONS import *

inputs = {"year i": 2015,
          "year f": 2020,
          "path data": "../Archivos/",
          #AOD specification
          "wavelen": "500nm", 
          "resolution": "1"}

PM10 = SIMA_data('PM10')
PM10.read_data_SIMA(inputs['path data'])
stations = PM10.data.columns

PM10.cut_year('2015-01-01', '2020-01-01')
PM10_2015_2019 = PM10.section
PM10.cut_year('2020-01-01','2021-01-01')
PM10_2020 = PM10.section

PM10_2015_2019_month_mean = PM10_2015_2019.groupby(PM10_2015_2019.index.month).mean()
PM10_2020_month_mean = PM10_2020.groupby(PM10_2020.index.month).mean()

choose_months = np.arange(1, 13, 1)
month_names = obtain_month_names(choose_months)
for station in stations:
    plt.ylabel("PM$_{10}$ ($\mu g/m^3$)", fontsize=12)
    plt.xticks(choose_months, month_names, rotation=45, fontsize=12)
    plt.xlim(1, 12)
    plt.ylim(0, 120)
    plt.title(station)
    plt.grid(ls="--", color="grey", alpha=0.5, lw=2)
    plt.plot(np.arange(1, 13), list(PM10_2015_2019_month_mean[station]),
            ls="--", color="blue", lw=2.5, marker="o", label="2015-2019")
    plt.plot(np.arange(1, 13), list(PM10_2020_month_mean[station]),
            ls="--", color="orangered", lw=2.5, marker="o", label="2020")
    plt.legend(frameon=False, mode="expand", fontsize=12, ncol=2)
    plt.savefig('../Graphics/PM10/2020_comp_'+station+'.png')
    plt.close()