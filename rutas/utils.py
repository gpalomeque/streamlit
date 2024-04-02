import geopandas as gpd
import pandas as pd

class Rutas:
    def __init__(self, path_rutas, path_rutas_paradas):
        #self.df_rutas = gpd.read_file(path_rutas)
        #self.df_rutas_paradas = gpd.read_file(path_rutas_paradas)
        #self.df_base = pd.read_csv("data/ubicaciones_base.csv")
        self.df_rutas = gpd.read_file('/vsicurl/https://github.com/gpalomeque/streamlit/blob/main/rutas/data/rtp_shp.zip')
        self.df_rutas_paradas = gpd.read_file('/vsicurl/https://github.com/gpalomeque/streamlit/blob/main/rutas/data/CConcesionado_Paradas.shp')
        self.df_base = pd.read_csv('/vsicurl/https://github.com/gpalomeque/streamlit/blob/main/rutas/data/ubicaciones_base.csv')

    
    def get_rutas(self, claves):
        new_claves = [item for item in claves if item is not None]
        print(new_claves)
        df_filtrado = self.df_rutas[self.df_rutas.NOMENCL.isin(new_claves)]

        return df_filtrado
    
    #def get_nomenclatura(self,ruta):

    
    def get_paradas_ruta(self,clave):
        df_filtrado = self.df_rutas_paradas[self.df_rutas_paradas["NOMENCL"]==clave]
        return df_filtrado
