from functions_season import *
from functions_SIMA import *
import plotly.express as px
import pandas as pandas
from functions import *
import numpy as np
import os


def obtain_direction_and_speed(data):
    bins_dir = [0.,  11.25, 33.75,  56.25,  78.75, 101.25, 123.75, 146.25, 168.75,
                191.25, 213.75, 236.25, 258.75, 281.25, 303.75, 326.25, 348.75, 360]
    cardinals = ['N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE',
                 'S', 'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW', 'temp']
    bins_speed = [0,  0.3,  1.6,  5.5, 10.8,  17.2,  24.5, np.inf]
    data['direction'] = pd.cut(data['WDR'],
                               bins_dir,
                               labels=cardinals)
    data['direction'] = data['direction'].replace('temp', 'N')
    data['speed'] = pd.cut(data['WSR'], bins_speed)


def obtain_rose_data(data):
    rose_data = data.groupby(['direction', 'speed'], as_index=False).count()
    rose_data['WSR'] = rose_data['WSR']/(360*24)
    return rose_data


def plot_wind_rose(data, title, path, name):
    fig = px.bar_polar(data,
                       r="WSR",
                       theta="direction",
                       color="speed",
                       template="plotly",
                       color_discrete_sequence=px.colors.sequential.Plasma_r,
                       title=title)
    fig.write_image(path+name+".png")
    fig.write_html(path+name+".html")


inputs = {"year i": 2015,
          "year f": 2020,
          "dir stations": "../Stations/",
          "path data": "../Archivos/",
          "dir graphics": "../Graphics/"}

stations = [station.capitalize()
            for station in sorted(os.listdir(inputs["dir stations"]))]
for station in stations:
    print("Analizando la estacion {}".format(station))
    mkdir(station, path=inputs["dir graphics"]+"Wind_rose/")
    WSR = SIMA_data(inputs["year i"],
                    inputs["year f"],
                    station.upper(),
                    'WSR')
    WDR = SIMA_data(inputs["year i"],
                    inputs["year f"],
                    station.upper(),
                    'WDR')
    WDR.read_data(inputs['path data'])
    WSR.read_data(inputs['path data'])
    years = WDR.years
    data = {'WSR': WSR.data[station.upper()],
            'WDR': WDR.data[station.upper()]}
    wind_data = pd.concat(data, axis=1)
    obtain_direction_and_speed(wind_data)
    rose_data = obtain_rose_data(wind_data)
    plot_wind_rose(rose_data,
                   station.capitalize(),
                   inputs["dir graphics"]+"Wind_rose/General/",
                   station.capitalize())
    for year in years:
        rose_data = wind_data.loc[(wind_data.index >= str(year)+'-01-01')
                                  & (wind_data.index < str(year+1)+'-01-01')]
        rose_data = obtain_rose_data(rose_data)
        plot_wind_rose(rose_data,
                       station.capitalize()+" "+str(year),
                       inputs["dir graphics"]+"Wind_rose/"+station+"/",
                       str(year))
    data_season = season_data(wind_data)
    data_season.calc_season_data()
    for season in data_season.seasons:
        data = data_season.obtain_season_data(season)
        rose_data = obtain_rose_data(data)
        plot_wind_rose(rose_data,
                       station.capitalize()+" "+season,
                       inputs["dir graphics"]+"Wind_rose/"+station+"/",
                       season)
