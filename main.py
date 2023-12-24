
from dash import Dash, html, dcc, dash_table, callback, Output, Input
import pandas as pd
import datetime
import numpy as np
import plotly.express as px
import plotly.graph_objs as go
from collections import deque
from scrapingMoviesAnalises import movies_analises

# Chamada do aquivo do scraping
aurelio = movies_analises()

# Dataframe das Avaliações
movie_analyses = aurelio['movie_analyses']

# Dataframe dos Detalhes do Filme
movie_detail = aurelio['movie_detail']

# Dataframe do Elenco do filme
movie_cast = aurelio['movie_cast']


app = Dash(__name__)

app.layout = html.Div(
    children=[
        html.Div(children=[
            html.H3(children='Tabela Review dos Filmes'),
            dash_table.DataTable(data=movie_analyses.to_dict("records"), page_size=10),
        ]),

        html.Div(children=[
            html.H3(children='Tabela de Detalhes dos Filmes'),
            dash_table.DataTable(data=movie_detail.to_dict("records"), page_size=10),
        ]),

        html.Div(children=[
            html.H3(children='Tabela de Elenco dos filmes'),
            dash_table.DataTable(data=movie_cast.to_dict("records"), page_size=10),
        ]),
    ]
)

if __name__ == '__main__':
    app.run(debug=True)
