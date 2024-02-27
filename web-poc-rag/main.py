import streamlit as st
import json
import requests

URL = st.secrets["API_URL"]

def search(query,c_name):    
    DATA = {
            "query": query,
            "index_name": c_name
        }
    response = requests.post(URL, json=DATA)
    
    return  response


def go_search(query,c_name):
    if query and c_name:
        with st.spinner('Procesando...'):
            response = search(query,c_name)
        results =  response.json()     
        #st.json(results)
        st.write (" :question: " + query)

        if response.status_code == 200:
            st.write("Tiempo de respuesta: " + str(results["time"]) + " :sunglasses:")
            st.text_area("Respuesta", results["response"]) 
            if results["source"]!=None:                           
                st.markdown("""Contexto obtenido:""")
                for item in results["source"]:
                    with st.container():
                        st.write (" :id: " + item["doc"] + " - Página: " + str(item["page"]))
                        st.text_area("Texto:",item["context"])                              
                #st.dataframe(results["source"])             
        else:
            st.error(results["detail"])
    else:
         st.sidebar.info("Debe proporcionar la pregunta y el nombre de la colección")
        

def main():
    st.set_page_config(
        page_title="POC de Busqueda",
        page_icon=":search:",
        layout="wide",
        initial_sidebar_state="expanded",
        )
    st.title("POC de Busqueda")
    st.markdown("""Intentare responder la pregunta utilizando un modelo de lenguaje y la información que has almacenado en la base de conocimientos configurada.""")

    st.divider()
    
    query = st.sidebar.text_input("Escribe tu pregunta")
    c_name = st.sidebar.text_input("Escribe el nombre de la colección")
    boton = st.sidebar.button('Buscar',on_click=go_search(query,c_name))
                        

if __name__ == '__main__':
	main()
