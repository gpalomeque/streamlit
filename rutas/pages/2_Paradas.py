import streamlit as st
from streamlit_folium import st_folium
import folium
import geopy.distance
from shapely.geometry import Point
import random
from utils import Rutas


###### funciones


def filter_points(df, point_of_interest, distance_limit):
    df['geometry2'] = df['geometry'].apply(lambda pointz: Point(pointz.x, pointz.y))
    
    # Crear un objeto Point para el punto de interés
    poi = Point(point_of_interest[::-1])  # Invertir para (longitud, latitud)
    # Calcular la distancia desde cada punto en el DataFrame al punto de interés
    df['distance'] = df['geometry2'].apply(lambda x: geopy.distance.geodesic(x.coords[0][::-1], poi.coords[0][::-1]).meters)
    # Filtrar los puntos que están a más de la distancia límite
    df_filtered = df[df['distance'] <= distance_limit]
    df_filtered.reset_index(drop=True, inplace=True)
    return df_filtered


def buscar(latitud,longitud,distancia):
    df_paradas=None
    if latitud and longitud:
        with st.spinner('Procesando...'):  
            ## ejecutar la búsqueda
            point_of_interest = (latitud, longitud)
            #st.sidebar.write(latitud + "  ,  " + longitud)
            df_paradas = filter_points(st.session_state.datos_rutas.df_rutas_paradas,point_of_interest,distancia)
            
            st.dataframe(df_paradas[["ORIG_DEST","RUTA","UBICACION","NOMENCL","CORREDOR"]])    
            mapa = folium.Map(location=[latitud, longitud], tiles="OpenStreetMap", zoom_start=15)
            type_color = "blue"
            mapa.add_child(
                    folium.Marker(
                        location=point_of_interest,
                        icon=folium.Icon(color="%s" % type_color),
                    )
                )
            # Create a geometry list from the GeoDataFrame
            geo_df_list = [[point.xy[1][0], point.xy[0][0]] for point in df_paradas.geometry]
            i = 0
            for coordinates in geo_df_list:
                type_color = "purple"
                # Place the markers with the popup labels and data
                mapa.add_child(
                    folium.Marker(
                        location=coordinates,
                        popup="Nomenclatura: "
                        + str(df_paradas.NOMENCL[i])
                        + "<br>"
                        + "Ubicación: "
                        + str(df_paradas.UBICACION[i])
                        + "<br>"
                        + "Ruta: "
                        + str(df_paradas.RUTA[i])          
                        + "<br>"
                        + "Coordenadas: "
                        + str(geo_df_list[i]),
                        icon=folium.Icon(color="%s" % type_color),
                    )
                )
                i = i + 1
            #, width =500, height = 600, control_scale =True
            st_data = st_folium(mapa, width = 500) 

###### para el st.dataframe de ubicaciones pre-cargadas

def dataframe_with_selections(df):
    df_with_selections = df.copy()
    df_with_selections.insert(0, "Select", False)

    # Get dataframe row-selections from user with st.data_editor
    edited_df = st.data_editor(
        df_with_selections,
        hide_index=True,
        column_config={"Select": st.column_config.CheckboxColumn(required=True)},
        disabled=df.columns,
    )

    # Filter the dataframe using the temporary column, then drop the column
    selected_rows = edited_df[edited_df.Select]

    if len(selected_rows.index) > 0:
        return (selected_rows.iloc[0]['latitud'],selected_rows.iloc[0]['longitud'])
    else:
        return 1

###### pagina

if "datos_rutas" not in st.session_state:
  st.session_state.datos_rutas = Rutas()



st.set_page_config(
  page_title="Rutas-CDMX",
  page_icon="✂️",
  layout="wide",
  initial_sidebar_state="expanded",
)
st.title("Rutas-CDMX")
st.subheader("""Muestra las rutas y paradas cercanas a la ubicación proporcionada.""")
st.divider()
st.markdown("Proporciona la siguiente información:")


latitud = st.text_input('Latitud', key="latitud")
longitud = st.text_input('Longitud',key="longitud")
distancia = st.number_input('Distancia',300)

btn_buscar = st.button('Buscar',on_click=buscar(latitud,longitud,distancia))


