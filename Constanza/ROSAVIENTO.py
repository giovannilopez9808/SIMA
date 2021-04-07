from functions_CONS import *
import plotly.express as px

#Datos de entrada
inputs = {"year i": 2015,
          "year f": 2020,
          "path data": "../Archivos/"}

#Lee los archivos correspondientes (speed & direction)
WSR=SIMA_data('WSR')
WSR.read_data_SIMA(inputs['path data'])
WDR=SIMA_data('WDR')
WDR.read_data_SIMA(inputs['path data'])

#Juntar ambos datos en una misma tabla
frames={'WSR':WSR.data,'WDR':WDR.data}
wind_data=pd.concat(frames,axis=1).swaplevel(axis=1)

#Bins para agrupar
bins_dir= [  0. ,  11.25, 33.75,  56.25,  78.75, 101.25, 123.75, 146.25, 168.75,
       191.25, 213.75, 236.25, 258.75, 281.25, 303.75, 326.25, 348.75, 360]
cardinals=['N','NNE','NE','ENE','E','ESE','SE','SSE','S','SSW','SW','WSW','W','WNW','NW','NNW','temp']
bins_speed=[  0,  0.3,  1.6,  5.5, 10.8,  17.2,  24.5, np.inf]

for station in WSR.data.columns:
    wind_data_st=wind_data[station]
    wind_data_st=wind_data[station]
    #Agrupar los datos primero por direccion y luego por velocidad
    wind_data_st['direction'] = pd.cut(wind_data_st['WDR'], bins_dir, labels=cardinals)
    wind_data_st['direction'] = wind_data_st['direction'].replace('temp','N')
    wind_data_st['speed']=pd.cut(wind_data_st['WSR'], bins_speed)
    #Crea un dataframe con los grupos y cuenta la frecuencia de cada uno
    df = wind_data_st.groupby(['direction','speed'],as_index=False).count()
    df['WSR']=df['WSR']/(360*24)
    #Plot
    fig = px.bar_polar(df, r="WSR", theta="direction",
                    color="speed", template="plotly",
                    color_discrete_sequence= px.colors.sequential.Plasma_r,
                    title = station )
    fig.write_image('../Graphics/Wind_rose/gral/'+station+'_gral.png')
    fig.write_html('../Graphics/Wind_rose/gral/'+station+'_gral.html')
    #Graphics separated by year
    years = [year for year in range(wind_data_st.index[0].year, wind_data_st.index[-1].year+1)]
    for year in years:
        df = wind_data_st.loc[(wind_data_st.index >= str(year)+'-01-01') &  (wind_data_st.index < str(year+1)+'-01-01')] 
        df = df.groupby(['direction','speed'],as_index=False).count()
        df['WSR']=df['WSR']/(360*24)
        fig = px.bar_polar(df, r="WSR", theta="direction",
                        color="speed", template="plotly",
                        color_discrete_sequence= px.colors.sequential.Plasma_r,
                        title = station +' '+str(year))
        fig.write_html('../Graphics/Wind_rose/'+station+'/'+str(year)+'.html')
        fig.write_image('../Graphics/Wind_rose/'+station+'/'+str(year)+'.png')
    #Graphics separated by season
    wd_st_seasons = grouping(wind_data_st)
    wd_st_seasons.seasons()
    seasons = ['summer','autumn','winter','spring']
    i=0
    for ssn in [wd_st_seasons.summer, wd_st_seasons.autumn, wd_st_seasons.winter, wd_st_seasons.spring]:
        df = ssn.groupby(['direction','speed'],as_index=False).count()
        df['WSR']=df['WSR']/(360*24)
        fig = px.bar_polar(df, r="WSR", theta="direction",
                    color="speed", template="plotly",
                    color_discrete_sequence= px.colors.sequential.Plasma_r,
                    title = station + ' ' + seasons[i] )
        fig.write_image('../Graphics/Wind_rose/'+station+'/'+seasons[i]+'.png')
        fig.write_html('../Graphics/Wind_rose/'+station+'/'+seasons[i]+'.html')
        i=i+1

