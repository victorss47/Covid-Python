import pandas as pd
import numpy as np
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go
import re
import json
import folium
import pycep_correios

Dados = pd.read_csv('./caso.csv', parse_dates=['date'])
Dados2= pd.read_csv('./covid_19.csv', parse_dates=['ObservationDate'])

#padronizando as colunas
def corrige_colunas(col_name):
    return re.sub(r"[/| ]", "", col_name).lower()
Dados.columns = [corrige_colunas(col) for col in Dados.columns]
Dados2.columns = [corrige_colunas(col) for col in Dados2.columns]
#Filtro de dados
#Base de dados1
br = Dados.loc[Dados.place_type == 'state', ['state', 'confirmed', 'deaths', 'is_last', 'date']]
br.loc[br.deaths.isnull(), 'deaths']=0

#Base de dados 2
br2 = Dados2.loc[(Dados2.countryregion == 'Brazil') & (Dados2.confirmed >0)]

#Local da busca
Origem = input("Digite um Cep para pesquisa..:")
LocalOrigem =pycep_correios.get_address_from_cep(Origem)
print("Cep de Origem.:",LocalOrigem['uf'])

#Mapa
mapa = folium.Map(width=800, height= 600, location=[-15.77972, -47.92972], zoom_start=4)
#Mapa estilo
Atua = br.loc[br.is_last == True, ['state', 'confirmed', 'deaths', 'date']]
estados = "states.json"
geojs=json.load(open(estados))

#mapa de casos no brasil - recomendando usar o colab
"""mapa.choropleth(coods,
                name="Casos",
                data= Atua,
                columns =['state', 'confirmed'],
                key_on = 'feature.id',
                fill_color = 'Reds',
                fill_opacity = 0.8,
                line_color ='blue',
                line_opacity = 0.8,
                show = True,
                legend_name= "Casos de Covid no Brasil"
)"""
#Grafico de casos confirmados
#Gra = px.line(br2, 'observationdate', 'confirmed', title='casos confirmados no brasil')
#Gra.show()

UF = br.loc[br.state == LocalOrigem['uf'], ['state', 'confirmed', 'deaths', 'date']]
Gra = px.line(UF, 'date', 'confirmed', title='casos confirmados')
Gra.show()

#Gra = px.line(UF, 'date', 'deaths', title='Mortes no estado')
#Gra.show()

