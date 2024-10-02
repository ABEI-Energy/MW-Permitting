import datetime as dt
import locale as lc
import pandas as pd
import streamlit as st
from functions import *
import time
from streamlit_folium import st_folium
import folium


global countries

countries = ['ITALY','SPAIN','FRANCE','UK','POLAND','USA']
# countries = ['SPAIN','FRANCE','USA','ITALY','UK','POLAND']

CENTER_START = [0, 0]
ZOOM_START = 2

if 'disable_opt' not in st.session_state:
    st.session_state.disable_opt = False

#Set the language for datetime
lc.setlocale(lc.LC_ALL,'es_ES.UTF-8')
month = dt.datetime.now().strftime("%B %Y")
time_doc = dt.datetime.now().strftime("%y%m")

class pict:
    def __init__(self, name, file):
        self.name = name
        self.file = file

def normalize(string):
    return str(round(float(string.replace(",", ".")),2))

def normalize2(string):
    return str(string.replace(",", "."))

st.set_page_config(layout="wide")

if 'finalCheck' not in st.session_state:
    st.session_state['dropped_file'] = False
    st.session_state['dataframe'] = False
    st.session_state["center"] = [0,0]
    st.session_state["zoom"] = 2
    df_origen = pd.read_excel('Resources/Permitting_origen.xlsx')
    df_origen.index = df_origen.COUNTRY
    df_origen.drop(columns = 'COUNTRY', inplace = True)
    df_origen['TOTAL'] = df_origen.sum(axis = 1)

if 'timer' not in st.session_state:
    st.session_state["country"] = countries[0]
    st.session_state["i"] = 0
    st.session_state['timer'] = True

"""
# O&M MW Permitting
"""
st.divider()

# Drag the xlsx file

colx, coly = st.columns(2)

if st.session_state.timer: #Si se ha analizado ya el archivo tirado y el timer vuelve a estar en true

    centroids = [[42.0719,12.7674],[40.4637,-1.7492],[46.8276,1.7137],[55.3781,0.4360],[51.9194,19.1451],[37.7946,-94.5348]]
    # countries = ['ITALY','SPAIN','FRANCE','UK','POLAND','USA'] orden dentro del programa para que el mapa fluya rápido
    # countries = ['SPAIN','FRANCE','USA','ITALY','UK','POLAND'] orden dentro del excel
    zooms = [5,5,4,5,5,5] # Este orden es el que tiene esta gente en el excel 
    #Esto queda guapo pero va a saltos...
    bbox_limits = [[[35.817813,-9.338379],[43.802819,4.372559]],[[42.228517,-5.097656],[51.206883,8.525391]],[[24.607069,-125.244141],[49.037868,-64.072266]],[[36.244273,6.08642],[47.294134,19.423828]],[[49.296472,-12.612305],[59.467408,3.120117]],[[48.487486,13.205566],[55.329144,25.114746]]]


    df = pd.read_excel('Permitting_origen.xlsx')
    df_aux = df.reset_index()
    df_aux['zoom'] = pd.DataFrame(data = zooms)
    df_aux['bbox'] = pd.DataFrame({'Coordinates': bbox_limits})
    df_coord = pd.DataFrame(centroids, columns = ['Latitude','Longitude'])
    df_coord['COUNTRY'] = pd.DataFrame(countries)
    df_coord = df_coord.merge(df_aux, on = 'COUNTRY')
    # df_aux[['Latitude','Longitude']] = pd.DataFrame(centroids, columns = ['Latitude','Longitude'])
    df_coord.index = df_coord['COUNTRY']
    df_coord = df_coord.drop(columns = ['index'])

    placeholder = st.empty()

    @st.fragment(run_every=dt.timedelta(seconds = 5))
    def mapping():

        with placeholder.container():
        
            colz, cola = st.columns(2)

            with cola:

                # Gráfica

                fig = grapher(df_coord.loc[df_coord.COUNTRY== st.session_state["country"], 'COUNTRY'][0],df_coord)
                st.pyplot(fig)

            with colz:

                m = folium.Map(location= CENTER_START, zoom_start=ZOOM_START, tiles = 'Cartodb Positron')
                # m.fit_bounds(df_coord.loc[df_coord.COUNTRY== st.session_state["country"], 'bbox'][0])

                st_folium(m,center=[df_coord.loc[df_coord.COUNTRY== st.session_state["country"], 'Latitude'][0] , df_coord.loc[df_coord.COUNTRY== st.session_state["country"], 'Longitude'][0]],zoom=int(df_coord.loc[df_coord.COUNTRY== st.session_state["country"], 'zoom'][0]),height=400,width=700)

                time.sleep(5)
                st.session_state.i += 1
                if st.session_state.i == 6:
                    st.session_state.i = 0
                    st.session_state.country = countries[0]
                st.session_state.country = countries[st.session_state.i]
        
        placeholder.empty()

    mapping()

st.divider()
