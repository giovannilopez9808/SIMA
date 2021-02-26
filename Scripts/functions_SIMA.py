import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import datetime


class SIMA_data:
    """
    Clase que guarda toda la logica para analizar los datos del SIMA
    Describcion de variables
    year_i      ----> Año inicial del que se tiene datos
    day_i       ----> Dia inicial del años
    year_f      ----> Año final del que se tienen datos
    years       ----> Años en que analizaran 
    stations    ----> Estaciones que se analizaran
    hour        ----> Hora que se analizara
    """

    def __init__(self, year_i, year_f, station, file):
        self.year_i = year_i
        self.day_i = [year_i, 1, 1]
        self.year_f = year_f
        self.years = [year for year in range(year_i, year_f+1)]
        self.station = station
        self.file = file

    def read_data(self, path):
        """
        Lectura y limpieza de datos que no se usaran para el analisis
        """
        self.data = pd.read_csv(path+self.file+"_SIMA.csv")
        self.data_hour = pd.read_csv(path+self.file+"_hour_SIMA.csv")
        self.clean_data()
        self.index_to_datetime()

    def clean_data(self):
        """
        Funcion que limpia la base de datos de informacion que no sera usada
        """
        # Limpieza de columnas que no seran usadas
        for key in self.data.keys():
            if not key in ["Dates", "Hours", self.station]:
                self.data = self.data.drop(key, 1)
        for key in self.data_hour.keys():
            if not key in ["Dates", "Hours", self.station]:
                self.data_hour = self.data_hour.drop(key, 1)

    def index_to_datetime(self):
        """
        Funcion que realiza el formato a Datetime el index de cada Dataframe
        """
        # Formatea la hora a dos digitos
        self.data['Hours'] = self.data['Hours'].astype(str).str.zfill(2)
        # Une fecha con horas
        self.data['Datetime'] = self.data["Dates"] + ' ' + self.data['Hours']
        # Formato datetime
        self.data['Datetime'] = pd.to_datetime(self.data['Datetime'])
        self.data.index = self.data['Datetime']
        self.data = self.data.drop(['Dates', 'Hours', 'Datetime'], axis=1)
        self.data_hour["Dates"] = pd.to_datetime(self.data_hour["Dates"])
        self.data_hour.index = self.data_hour["Dates"]
        self.data_hour = self.data_hour.drop("Dates", axis=1)

    def calc_month_hour_mean(self):
        """
        Funcion que calcula el promedio mensual por cada año basado
        en las mediciones a una hora
        """
        self.month_hour_mean = pd.DataFrame(columns=self.years,
                                            index=[i for i in range(1, 13)])
        data_mean = self.data_hour.resample("MS").mean()
        month_consecutive = 0
        for year in self.years:
            for month in range(1, 13):
                self.month_hour_mean[year][month] = round(
                    data_mean[self.station][month_consecutive], 1)
                month_consecutive += 1

    def calc_month_mean(self):
        """
        Funcion que calcula el promedio mensual por cada año para todas las horas
        """
        self.month_mean = pd.DataFrame(columns=self.years,
                                       index=[i for i in range(1, 13)])
        data_mean = self.data.resample("MS").mean()
        month_consecutive = 0
        for year in self.years:
            for month in range(1, 13):
                self.month_mean[year][month] = round(
                    data_mean[self.station][month_consecutive], 1)
                month_consecutive += 1

    def calc_month_sum(self):
        """
        Funcion que calcula la suma mensual por cada año para todas las horas
        """
        self.month_mean = pd.DataFrame(columns=self.years,
                                       index=[i for i in range(1, 13)])
        data_mean = self.data.resample("MS").sum()
        month_consecutive = 0
        for year in self.years:
            for month in range(1, 13):
                self.month_mean[year][month] = round(
                    data_mean[self.station][month_consecutive], 1)
                month_consecutive += 1

    def plot_month_means_AOD(self, AOD_list, MODIS_list):
        """
        Funcion que grafica en diferentes subplots el promedio mensual en
        cada año junto con los datos de AOD promedio mensual
        """
        # Calculo de los nombres de los meses a imprimir
        choose_months = np.arange(1, 11, 3)
        choose_months = np.append(choose_months, 12)
        month_names = obtain_month_names(choose_months)
        # Divisón de las graficas
        fig, axs = plt.subplots(2, 3,
                                sharex=True,
                                sharey=True,
                                figsize=(10, 12))
        plt.subplots_adjust(left=0.083, right=0.9, top=0.9)
        axs = np.reshape(axs, 6)
        for year, ax in zip(self.years, axs):
            ax2 = ax.twinx()
            ax.set_xticks(choose_months)
            ax.set_xticklabels(month_names, rotation=45, fontsize=12)
            ax.set_xlim(1, 12)
            ax.set_ylim(30, 110)
            ax.set_yticks(np.linspace(30, 110, 5))
            ax.set_title("Year: {}".format(year))
            ax.grid(ls="--", color="grey", alpha=0.5, lw=2)
            # Ploteo del valor de PM10
            ax.plot(np.arange(1, 13), list(self.month_hour_mean[year]),
                    ls="--", color="purple",
                    marker="o", label="PM$_{10}$", alpha=0.75)
            ax2.set_ylim(0, 1.2)
            ax2.set_yticks(np.linspace(0, 1.2, 5))
            if not ax in [axs[2], axs[5]]:
                ax2.set_yticks(([]))
            # Ploteo de la lista de AOD de los data found
            self.plot_month_another_stuff(ax2, AOD_list, year)
            # Ploteo de la lista de AOD de MODIS y de OMI
            self.plot_month_another_stuff(ax2, MODIS_list, year)
        fig.text(0.02, 0.5, "PM$_{10}$", rotation=90, fontsize=14)
        fig.text(0.95, 0.5, "AOD$_{550nm}$", rotation=-90, fontsize=14)
        lines, labels = fig.axes[-1].get_legend_handles_labels()
        lines.append(fig.axes[0].get_legend_handles_labels()[0][0])
        labels.append(fig.axes[0].get_legend_handles_labels()[1][0])
        fig.legend(lines, labels, loc="upper center",
                   ncol=7, frameon=False, fontsize=11)
        plt.show()

    def plot_month_another_stuff(self, ax, data_list, year):
        """
        funcion que grafica los promedios mensuales de diferentes datos datos por una lista
        que cotiene los datos, el titulo y color a plotear respectivamente
        """
        for data_title in data_list:
            data, title, color = data_title
            data_to_plot = []
            months = []
            for month in range(1, 13):
                if data[year][month] != 0:
                    data_to_plot.append(data[year][month])
                    months.append(month)
            ax.plot(months, data_to_plot,
                    label=title, ls="--", marker="o",
                    color=color, alpha=0.75)

    def plot_month_means_Rain(self, Rain_data_title):
        """
        Funcion que grafica en diferentes subplots el promedio mensual en
        cada año junto con los datos de lluvia
        """
        choose_months = np.arange(1, 11, 3)
        choose_months = np.append(choose_months, 12)
        month_names = obtain_month_names(choose_months)
        fig, axs = plt.subplots(
            2, 3, sharex=True, sharey=True, figsize=(10, 12))
        plt.subplots_adjust(left=0.083, right=0.9, top=0.9)
        axs = np.reshape(axs, 6)
        for year, ax in zip(self.years, axs):
            ax2 = ax.twinx()
            ax.set_xticks(choose_months)
            ax.set_xticklabels(month_names, rotation=45, fontsize=12)
            ax.set_xlim(1, 12)
            ax.set_ylim(50, 110)
            ax.set_title("Year: {}".format(year))
            ax.grid(ls="--", color="grey", alpha=0.5, lw=2)
            # Ploteo del valor de PM10
            ax.plot(np.arange(1, 13),
                    self.month_mean[year], ls="--", color="purple", marker="o", label="PM$_{10}$")
            Rain_data, title = Rain_data_title
            ax2.set_ylim(0, 0.5)
            if not ax in [axs[2], axs[5]]:
                ax2.set_yticks(([]))
            # Ploteo del valor de lluvias
            ax2.bar(np.arange(
                1, 13), Rain_data[year], 0.5, label=title)
        fig.text(0.02, 0.5, "PM$_{10}$ $(\mu g/m^3)$",
                 rotation=90, fontsize=14)
        fig.text(0.95, 0.3, "Accumulated Rainfall (mm/hr)",
                 rotation=-90, fontsize=14)
        lines, labels = fig.axes[-1].get_legend_handles_labels()
        lines.append(fig.axes[0].get_legend_handles_labels()[0][0])
        labels.append(fig.axes[0].get_legend_handles_labels()[1][0])
        fig.legend(lines, labels, loc="upper center",
                   ncol=5, frameon=False, fontsize=12)
        plt.show()

    def cut_year(self, date_i, date_f):
        """
        funcion que realiza el corte de los datos a partir de unas fechas dadas
        """
        self.section = self.data.loc[(self.data.index >= date_i) &
                                     (self.data.index <= date_f)]

    def calc_season_hour_mean(self, station):
        """
        Función que separa los dias en estaciones y calcula el promedio horario
        """
        season_names = ["Spring Sum", "Summer Sum", "Autumn Sum", "Winter Sum",
                        "Spring Count", "Summer Count", "Autumn Count", "Winter Count"]
        seasons = ["Spring", "Summer", "Autumn", "Winter"]
        seasons_dates = {'Summer': (datetime.date(2020, 6, 21), datetime.date(2020, 9, 22)),
                         'Autumn': (datetime.date(2020, 9, 23), datetime.date(2020, 12, 20)),
                         'Spring': (datetime.date(2020, 3, 21), datetime.date(2020, 6, 20))}
        season_count = pd.DataFrame(columns=season_names,
                                    index=np.arange(24))
        season_count = season_count.fillna(0)
        total_days = count_days(date_i=self.day_i,
                                date_f=[self.year_f, 12, 31])
        for hour in range(24):
            for year in range(self.year_f-self.year_i+1):
                for day in range(365):
                    date = consecutiveday2date(day, 2020)
                    season_name = get_season(date, seasons_dates)
                    hour_value = (year*365+day)*24+hour
                    value = self.data[station][hour_value]
                    if str(value) != "nan":
                        season_count[season_name+" Sum"][hour] += value
                        season_count[season_name+" Count"][hour] += 1
        self.season_hourly_mean = pd.DataFrame(columns=seasons,
                                               index=np.arange(24))
        for season in seasons:
            for hour in range(24):
                self.season_hourly_mean[season][hour] = round(
                    season_count[season+" Sum"][hour]/season_count[season+" Count"][hour], 1)

    def plot_season_means(self):
        seasons = ["Spring", "Summer", "Autumn", "Winter"]
        xticks = np.arange(0, 22, 2)
        xticks = np.append(xticks, 23)
        plt.xlim(0, 23)
        plt.xticks(xticks)
        plt.ylim(30, 100)
        plt.xlabel("Local Time (h)")
        plt.ylabel("PM$_{10}$", fontsize=12)
        for season in seasons:
            plt.plot(self.season_hourly_mean[season], label=season)
        plt.legend(frameon=False, ncol=4, mode="expand",
                   bbox_to_anchor=(0, 1.07, 1, 0.02))
        plt.grid(ls="--", color="grey", alpha=0.5, lw=2)
        plt.show()


def count_days(date_i, date_f):
    year, month, day = date_f
    year_i, month_i, day_i = date_i
    days = (datetime.date(year, month, day) -
            datetime.date(year_i, month_i, day_i)).days
    return days


def count_days_per_month(date_i, date_f):
    year, month, day = date_f
    day_initial = count_days(date_i, date_f)
    year, month_f = validate_date(date=[year, month])
    day_final = day_initial+count_days(date_i=date_i,
                                       date_f=[year, month_f, day])
    return day_initial, day_final


def count_days_per_year(date_i, date_f):
    year, month, day = date_f
    day_initial = count_days(date_i, date_f)
    day_final = day_initial+count_days(date_i=date_i,
                                       date_f=[year+1, 1, day])
    return day_initial, day_final


def validate_date(date):
    year, month = date
    month += 1
    if month > 12:
        month = 1
        year += 1
    return year, month


def obtain_month(year, day):
    month = (datetime.date(year, 1, 1) +
             datetime.timedelta(days=day)).month
    return month


def obtain_month_names(months):
    names = []
    for month in months:
        date = datetime.date(2020, month, 1)
        names.append(date.strftime("%b"))
    return names


def get_season(date, seasons):
    for season, (season_start, season_end) in seasons.items():
        if date >= season_start and date <= season_end:
            return season
    else:
        return 'Winter'


def consecutiveday2date(conse_day, year):
    date = datetime.date(year, 1, 1)+datetime.timedelta(days=conse_day)
    return date
