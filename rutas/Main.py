import streamlit as st

st.set_page_config(
        page_title="Rutas-CDMX",
          page_icon="✂️",
        layout="wide",
        initial_sidebar_state="expanded",
        )
st.title("Rutas de transporte en la CDMX")
texto="""
La aplicación utiliza la información proporcionada por SEMOVI.


1. Rutas y Paradas del Transporte Concesionado.

***Datos disponibles al 19 de marxo de 2024***.
"""
st.markdown(texto)
st.divider()