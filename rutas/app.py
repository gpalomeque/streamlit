import streamlit as st
from streamlit_folium import st_folium
import folium
import geopy.distance
from shapely.geometry import Point
import random
from utils import Rutas

ruta_concesionado = "data/CConcesionado_Rutas.shp"
ruta_paradas = "data/CConcesionado_Paradas.shp"

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
    #return df

def my_color():
    return ["#" + "".join([random.choice("0123456789ABCDEF") for j in range(6)])]


def agregar_ruta(mapa,df):
#     print(df.describe())
#     tooltip = folium.GeoJsonTooltip(
#     fields=["RUTA", "NOMENCL"],
#     aliases=["RUTA:", "NOMENCL	:"],
#     localize=True,
#     sticky=False,
#     labels=True,
#     style="""
#         background-color: #F0EFEF;
#         border: 2px solid black;
#         border-radius: 3px;
#         box-shadow: 3px;
#     """,
#     max_width=800,
# )

    lines = folium.GeoJson(df,
                    #tooltip=tooltip,
                    style_function=lambda NOMEN_COR: {         
            "color": my_color(),
            "weight": 2,
            "dashArray": "5, 5",
        },)
    mapa.add_child(lines)
    # folium.Choropleth(
    #     geo_data=df['geometry'],
    #     columns=['RUTA', 'UBICACION'],
    #     fill_opacity=0.3,
    #     line_weight=2,
    # ).add_to(mapa)
    return mapa

def agregar_paradas(df,latitud,longitud):
    # OpenStreetMap de la CDMX 19.42847, -99.12766
    mapa = folium.Map(location=[latitud, longitud], tiles="OpenStreetMap", zoom_start=15)
   
    # Create a geometry list from the GeoDataFrame
    geo_df_list = [[point.xy[1][0], point.xy[0][0]] for point in df.geometry]
    i = 0
    for coordinates in geo_df_list:
        type_color = "purple"

        # Place the markers with the popup labels and data
        mapa.add_child(
            folium.Marker(
                location=coordinates,
                popup="Nomenclatura: "
                + str(df.NOMENCL[i])
                + "<br>"
                + "Ubicación: "
                + str(df.UBICACION[i])
                + "<br>"
                + "Ruta: "
                + str(df.RUTA[i])          
                + "<br>"
                + "Coordenadas: "
                + str(geo_df_list[i]),
                #icon=folium.Icon(color="%s" % type_color),
                #icon=folium.Icon(icon_color=my_color())
            )
        )
        i = i + 1
    return mapa

def agregar_mapa(df_rutas,df_paradas,latitud,longitud):
    # OpenStreetMap de la CDMX 19.42847, -99.12766
    mapa = folium.Map(location=[latitud, longitud], tiles="OpenStreetMap", zoom_start=15)
    
    #agrega rutas
    lines = folium.GeoJson(df_rutas,
                    #tooltip=tooltip,
                    style_function=lambda NOMEN_COR: {         
            "color": my_color(),
            "weight": 2,
            "dashArray": "5, 5",
        },)
    mapa.add_child(lines)


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


    return mapa


def buscar(latitud,longitud,distancia):
    if latitud and longitud:
        with st.spinner('Procesando...'):  
            ## ejecutar la búsqueda
            point_of_interest = (latitud, longitud)
            #st.sidebar.write(latitud + "  ,  " + longitud)
            df_paradas = filter_points(st.session_state.datos_rutas.df_rutas_paradas,point_of_interest,distancia)
            st.dataframe(df_paradas[["ORIG_DEST","RUTA","UBICACION","NOMENCL","CORREDOR"]])

            mapa = folium.Map(location=[latitud, longitud], tiles="OpenStreetMap", zoom_start=15)
    

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

            st_data = st_folium(mapa) 


###### pagina

if "datos_rutas" not in st.session_state:
  st.session_state.datos_rutas = Rutas(ruta_concesionado, ruta_paradas)



st.set_page_config(
  page_title="Rutas-CDMX",
  page_icon="✂️",
  layout="wide",
  initial_sidebar_state="expanded",
)
st.title("Rutas-CDMX")
st.markdown("""Muestra las rutas y paradas cercanas a la ubicación proporcionada.""")
st.dataframe(st.session_state.datos_rutas.df_base)
st.divider()

### mostrar si se desea seleccionar una ruta
# option = st.selectbox(
#     'Selecciona la ruta a mostrar',
#     st.session_state.datos_rutas.df_rutas["RUTA"] + "|" + st.session_state.datos_rutas.df_rutas["NOMENCL"],
#     )

# st.write('Ruta seleccionada:', option)

# st.write(st.session_state.datos_rutas.get_rutas(option))


latitud = st.sidebar.text_input('Latitud')
longitud = st.sidebar.text_input('Longitud')
distancia = st.sidebar.number_input('Distancia',300)
#distancia = st.sidebar.text_input('Distancia Máx.',300)
#19.5782602 , -99.2554378 centro
#19.4560541702827,-99.17585293990068
btn_buscar = st.sidebar.button('Buscar',on_click=buscar(latitud,longitud,distancia))
