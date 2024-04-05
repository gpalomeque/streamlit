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
st.markdown("Selecciona una ubicación ")


selection = dataframe_with_selections(st.session_state.datos_rutas.df_base)
latitud = st.text_input('Latitud', key="latitud")
longitud = st.text_input('Longitud',key="longitud")
distancia = st.number_input('Distancia',300)

btn_buscar = st.button('Buscar',on_click=buscar(latitud,longitud,distancia))

if selection !=1:
    a,b=selection
    buscar(a,b,distancia)

