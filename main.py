import datetime as dt
import io
import locale as lc
import pandas as pd
import streamlit as st
from functions import *
import streamlit_toggle as tog
from docx.shared import Cm
from zipfile import ZipFile
import matplotlib.pyplot as plt
import plotly.express as px
import time
from streamlit_folium import st_folium
import folium
import random


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
    df_origen = pd.read_excel('Resources\Permitting_origen.xlsx')
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

'''
with colx:

    uploadedFile = st.file_uploader("Drag here the .xlsx file with the Permitting data).", accept_multiple_files = False,type = 'xlsx' ,key = 'ss_file')

    if (uploadedFile) and (uploadedFile.name.endswith('xlsx')) and (st.session_state.dataframe == False): # sólo entra una vez si se ha tirado un archivo, si es de tipo xlsx y si el session_state no ha pasado por el bucle

        with coly:

            st.session_state.dropped_file = True

            if st.session_state.dropped_file:
            
                # Mapa y gráficas
                df = pd.read_excel(uploadedFile)
                df.index = df.COUNTRY
                df.drop(columns = 'COUNTRY', inplace = True)
                df['TOTAL'] = df.sum(axis = 1)

                st.dataframe(df)

                st.session_state.dataframe = True
'''
st.divider()


# if st.session_state.dataframe and st.session_state.timer: #Si se ha analizado ya el archivo tirado y el timer vuelve a estar en true
if st.session_state.timer: #Si se ha analizado ya el archivo tirado y el timer vuelve a estar en true

    cole, colr, colt = st.columns(3)
    colz, cola = st.columns(2)

# countries = ['ITALY','SPAIN','FRANCE','UK','POLAND','USA']
    centroids = [[41.8719,12.5674],[40.4637,3.7492],[46.2276,2.2137],[55.3781,3.4360],[51.9194,19.1451],[-38.7946,106.5348]]

    # centroids = [[40.4637,3.7492],[46.2276,2.2137],[-38.7946,106.5348],[41.8719,12.5674],[55.3781,3.4360],[51.9194,19.1451]]
# countries = ['SPAIN','FRANCE','USA','ITALY','UK','POLAND']

    df = pd.read_excel('Resources\Permitting_origen.xlsx')
    df_aux = df.reset_index()
    df_aux[['Latitude','Longitude']] = pd.DataFrame(centroids, columns = ['Latitude','Longitude'])
    df_aux.index = df_aux['COUNTRY'].drop(columns = 'COUNTRY')

    @st.fragment(run_every=dt.timedelta(seconds = 5))
    def mapping():

        m = folium.Map(location= CENTER_START, zoom_start=ZOOM_START)

        st_folium(m,center=[df_aux.loc[df_aux.COUNTRY== st.session_state["country"], 'Latitude'][0] , df_aux.loc[df_aux.COUNTRY== st.session_state["country"], 'Longitude'][0]],zoom=5,height=400,width=400)
        
        time.sleep(5)
        st.session_state.i += 1
        if st.session_state.i == 6:
            st.session_state.i = 0
            st.session_state.country = countries[0]
        st.session_state.country = countries[st.session_state.i]
        pass
    
    mapping()
'''
    placeholder = st.empty()
    with placeholder.container():
        m = folium.Map(location= CENTER_START, zoom_start=ZOOM_START)

        st_folium(m,center=[df_aux.loc[df_aux.COUNTRY== st.session_state["country"], 'Latitude'][0] , df_aux.loc[df_aux.COUNTRY== st.session_state["country"], 'Longitude'][0]],zoom=6,height=400,width=700)
        
        time.sleep(5)
        st.session_state += 1
'''
'''
    for country in df.index:

        key_str = random.random()

        st.session_state["center"] = [df_aux.loc[df_aux.COUNTRY== country, 'Latitude'][0] , df_aux.loc[df_aux.COUNTRY== country, 'Longitude'][0]]
           
        st.session_state["zoom"] = 4

        m = folium.Map(location= CENTER_START, zoom_start=ZOOM_START)

        placeholder = st.empty()
        with placeholder.container():
            st_folium(m,center=[df_aux.loc[df_aux.COUNTRY== country, 'Latitude'][0] , df_aux.loc[df_aux.COUNTRY== country, 'Longitude'][0]],zoom=4,key=key_str,height=400,width=700)

            time.sleep(5)
        placeholder.empty()
    del st.session_state.timer
'''






'''
    for country in df.index:
        # html_show = px.scatter_mapbox(df_aux, lat='Latitude', lon='Longitude', mapbox_style="open-street-map", center = dict(lat = df_aux.loc[df_aux.COUNTRY== country, 'Latitude'][0], lon = df_aux.loc[df_aux.COUNTRY== country, 'Longitude'][0] ), zoom = 6, height = 800, width = 1800)
    
    # with cole:
    #     pass
    # with colr:
    #     st.title(f"{country}")
    # with colt:
    #     pass

        with colz:
            # Mapa
            # st.write(html_show)
            # st.map(latitude=df_aux.loc[df_aux.COUNTRY== country, 'Latitude'][0], longitude=df_aux.loc[df_aux.COUNTRY== country, 'Longitude'][0], zoom = 20)
            pass

        with cola:
            # Gráfica

            fig = grapher(country,df)
            st.pyplot(fig)


        time.sleep(2)
    '''