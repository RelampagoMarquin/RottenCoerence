from dash import Dash, html, dcc, dash_table, Output, Input
import pandas as pd
import plotly.express as px
from scrapingMoviesAnalises import movies_analises


def correct(row):
    if row['Polarity'] == row['Score']:
        return 1
    else:
        return 0


# Chamada do aquivo do scraping
aurelio = movies_analises()

# Dataframe do Elenco do filme
movie_cast = aurelio['movie_cast']
movie_cast.to_csv('dataframes/movie_cast.csv', index=False)
movie_cast = pd.read_csv('dataframes/movie_cast.csv')

# Dataframe das Avaliações
movie_analyses = aurelio['movie_analyses']
movie_analyses.to_csv('dataframes/movie_analyses.csv', index=False)
movie_analyses = pd.read_csv('dataframes/movie_analyses.csv')
# mudando o valor da polarity para 0 e 1
movie_analyses['Polarity'] = movie_analyses['Polarity'].apply(lambda x: 1 if x >= 0 else 0)
movie_analyses['Correct'] = movie_analyses.apply(correct, axis=1)

# Dataframe dos Detalhes do Filme
movie_detail = aurelio['movie_detail']
movie_detail.to_csv('dataframes/movie_detail.csv', index=False)
movie_detail = pd.read_csv('dataframes/movie_detail.csv')

movie_detail["Review_polarity"] = 0
# fazendo a média do valor da polaridade da review de cada filme e adicionando na coluna nova
count = 0
for i in movie_detail["Title"]:
    rows = movie_analyses.loc[movie_analyses['Movie_Name'] == i]
    if rows["Polarity"].count() != 0:
        Review_polarity = (rows["Polarity"].sum() / rows["Polarity"].count())
    else:
        Review_polarity = None
    if Review_polarity:
        movie_detail["Review_polarity"][count] = round(Review_polarity * 100, 2)
    else:
        movie_detail["Review_polarity"][count] = None
    count += 1

movie_detail["Score_comparative"] = 0
# fazendo a média do valor do score da review de cada filme e adicionando na coluna nova
count = 0
for i in movie_detail["Title"]:
    rows = movie_analyses.loc[movie_analyses['Movie_Name'] == i]
    if rows["Score"].count() != 0:
        Review_score = (rows["Score"].sum() / rows["Score"].count())
    else:
        Review_score = None
    if Review_score:
        movie_detail["Score_comparative"][count] = round(Review_score * 100, 2)
    else:
        movie_detail["Score_comparative"][count] = None
    count += 1

# isso corrige a proporção de Consesus_Polarity
movie_detail["Consesus_Polarity"] = movie_detail["Consesus_Polarity"].apply(lambda x: (50 * x) + 50)

# descobrir os acertos das analises
correct_values = movie_analyses['Correct'].value_counts()
fig = px.pie(names=["Correct", "False"], values=correct_values.values, title='Contagem de Valores')

movies_per_page = 10
num_pages = len(movie_detail) // movies_per_page + 1


# Função para gerar o gráfico para uma página específica
def generate_scatter_page(page):
    start_idx = page * movies_per_page
    end_idx = (page + 1) * movies_per_page
    fig2 = px.scatter(movie_detail[start_idx:end_idx], x="Title", y=["Consesus_Polarity", "Tomatometer_Score",
                                                                     "Audience_Score", "Review_polarity",
                                                                     "Score_comparative"], opacity=0.6)
    novo_tamanho = 15
    fig2.update_traces(marker=dict(size=novo_tamanho))
    fig2.update_layout(title_text=f"Page {page + 1}")
    # Configura o eixo y para variar de 0 a 100
    fig2.update_yaxes(range=[0, 110])
    return fig2


app = Dash(__name__)


@app.callback(
    Output('scatter-plot', 'figure'),
    [Input('page-slider', 'value')]
)
def update_scatter_plot(selected_page):
    return generate_scatter_page(selected_page)


app.layout = html.Div(
    className="main_container", children=[
        # html.Div(children=[
        #     html.H3(children='Tabela Review dos Filmes'),
        #     dash_table.DataTable(data=movie_analyses.to_dict("records"), page_size=10),
        # ]),
        #
        # html.Div(children=[
        #     html.H3(children='Tabela de Detalhes dos Filmes'),
        #     dash_table.DataTable(data=movie_detail.to_dict("records"), page_size=10),
        # ]),
        #
        # html.Div(children=[
        #     html.H3(children='Tabela de Elenco dos filmes'),
        #     dash_table.DataTable(data=movie_cast.to_dict("records"), page_size=10),
        # ]),
        html.H1(children="Atividade de análise de dados de filmes do rottentomatoes lançados em 2010",
                className="center"),
        html.H2(children="Objetivo do trabalho", className="center"),
        html.P(className="main_font", children="Neste estudo, propomos a análise dos filmes lançados no ano de 2010, "
                                               "valendo-nos do famoso site de críticas e informações "
                                               "cinematográficas, Rotten Tomatoes. Para efetuarmos as"
                                               "análises pertinentes ao conteúdo do site, empregaremos técnicas de "
                                               "web scraping por meio da biblioteca"
                                               "Beautiful Soup em Python. O intuito é extrair as informações "
                                               "desejadas do Rotten Tomatoes. Posteriormente,"
                                               "utilizaremos a biblioteca TextBlob para identificar a pontuação "
                                               "atribuída aos filmes, explorando a"
                                               "positividade das análises como critério de avaliação."),
        html.P(className="main_font", children="A partir desse ponto, conduziremos análises sobre os valores das "
                                               "avaliações dos filmes, tanto aquelas obtidas pela raspagem de dados "
                                               "quanto as geradas pelo TextBlob. Além"
                                               "disso, examinaremos as discrepâncias entre os dados reais e os "
                                               "analisados pelo TextBlob, com o propósito"
                                               "de avaliar a precisão do TextBlob neste contexto."),
        html.H2(children="Técnicas Utilizadas", className="center"),
        html.P(className="main_font", children="Durante o curso da pesquisa, empregamos técnicas de web scraping ("
                                               "raspagem de dados), utilizando a biblioteca BeautifulSoup, "
                                               "para extrair dados essenciais para a análise."
                                               "Complementarmente, aplicamos a análise de texto proporcionada pelo "
                                               "TextBlob nos dados obtidos. Vale ressaltar"
                                               "que, para apresentar visualmente os resultados dessa análise, optamos "
                                               "por utilizar um dashboard online"
                                               "fornecido pelo Plotly. Além disso, aproveitamos as capacidades "
                                               "gráficas das biblioteca Plotly para exibir"
                                               "gráficos a partir dos resultados obtidos"),
        html.H2(children="Análisando Reviews", className="center"),
        html.P(className="main_font", children="Após realizar a extração de dados de 12 reviews de cada filme ("
                                               "conforme disponível na página inicial do respectivo filme), "
                                               "procedemos à comparação entre a pontuação real do filme e aquela "
                                               "gerada pelo TextBlob ao darmos a review como entrada."),
        html.P(className="main_font", children="Antes de efetuar a comparação, foi necessário converter os dados "
                                               "provenientes do TextBlob, os quais operam em uma escala de 1 a -1, "
                                               "em um formato binário indicando se a avaliação era positiva ou "
                                               "negativa, semelhante à pontuação atribuída na análise. Optamos por "
                                               "considerar valores iguais ou superiores a 0 como positivos e valores "
                                               "inferiores a zero como negativos. Essa abordagem permitiu realizar "
                                               "uma comparação precisa entre os valores reais e as saídas do "
                                               "TextBlob."),
        html.P(className="main_font", children="Os resultados revelaram uma taxa de precisão de apenas 56,1%, "
                                               "um desempenho ligeiramente superior ao lançamento de uma moeda. Essa "
                                               "taxa sugere que os acertos obtidos podem ser mais atribuídos ao acaso "
                                               "do que a uma relação causal significativa entre os dados analisados."),
        html.Div(className="review_movies", children=[
            html.Div(className="review_movies_table", children=[
                html.H3(className="center", children='Tabela Review dos Filmes'),
                dash_table.DataTable(data=movie_analyses.to_dict("records"), columns=[
                    {'name': 'Movie_Name', 'id': 'Movie_Name'},
                    {'name': 'Author_Review', 'id': 'Author_Review'},
                    {'name': 'Polarity', 'id': 'Polarity'},
                    {'name': 'Score', 'id': 'Score'},
                    {'name': 'Correct', 'id': 'Correct'},
                    {'name': 'Text', 'id': 'Text'}
                ], page_size=12, style_cell={'textAlign': 'left'})
            ]),
            html.Div(className="review_movies_graph", children=[
                html.H3(className="center", children='Taxa de acerto do TextBlob'),
                dcc.Graph(id='population-pie-chart', figure=fig)
            ]),
        ]),
        html.Div(className="detail_movies", children=[
            html.H2(children="Análisando resultados referentes aos filmes", className="center"),
            html.P(className="main_font", children="Além da análise individual das avaliações, buscamos realizar uma "
                                                   "análise comparativa entre os filmes que foram objeto das "
                                                   "análises. Nosso objetivo era verificar se, mesmo diante dos "
                                                   "resultados negativos obtidos nas avaliações anteriores, "
                                                   "seria possível identificar alguma correlação entre os valores de "
                                                   "outras variáveis ou descobrir padrões subjacentes."),
            html.Ul(children=[
                html.Li(children=[
                    html.Span(children=[html.Strong(children="Consesus_Polarity: "), "Em todo página inicial do "
                                                                                     "rottentomatoes temos um "
                                                                                     "consenso da critica, "
                                                                                     "que se trata de uma opnião "
                                                                                     "geral da critica sobre o filme "
                                                                                     "em questão, e essa categoria "
                                                                                     "representa no gráfico o "
                                                                                     "resultado da análise do "
                                                                                     "textBlob desse consenso em uma "
                                                                                     "escala de 0 a 100."])
                ]),
                html.Li(children=[
                    html.Span(children=[html.Strong(children="Tomatometer_Score: "), "Representa a porcentagem "
                                                                                     "positiva de criticas feitas "
                                                                                     "pelos criticos especializados."])
                ]),
                html.Li(children=[
                    html.Span(children=[html.Strong(children="Audience_Score: "), "Representa a porcentagem positiva "
                                                                                  "de criticas feitas pelo publico "
                                                                                  "geral do rottentomatoes."])
                ]),
                html.Li(children=[
                    html.Span(children=[html.Strong(children="Review_polarity: "), "Representa a porcentagem positiva "
                                                                                   "das reviews análisadas pelo "
                                                                                   "TextBlob"])
                ]),
                html.Li(children=[
                    html.Span(children=[html.Strong(children="Score_comparative: "), "Representa a porcentagem "
                                                                                     "positiva das reviews reais no "
                                                                                     "qual fizemos a análise de "
                                                                                     "positividade"])
                ]),
            ]),
            dcc.Graph(id='scatter-plot', figure=generate_scatter_page(0)),
            # Controle deslizante para a seleção da página
            dcc.Slider(
                id='page-slider', min=0, max=num_pages - 1, step=1, value=0,
                marks={i: str(i + 1) for i in range(num_pages)},
            ),
            html.P(className="main_font", children="Ao incorporar todos os parâmetros de pontuação disponíveis na "
                                                   "análise do gráfico, podemos concluir que não há uma correlação "
                                                   "significativa entre as avaliações reais e aquelas obtidas pelo "
                                                   "TexBlob. Notamos que, embora haja algumas ocasiões em que os "
                                                   "valores são semelhantes, existem consideráveis discrepâncias em "
                                                   "diversos casos. Além dessa métrica, ao avaliarmos outros "
                                                   "parâmetros, percebemos que as correlações esperadas não se "
                                                   "manifestaram, excluindo a pontuação da crítica e a do público, "
                                                   "que apesar de também ter diferenças, tendem a serem mais próximas "
                                                   "e também a polaridade da frase de consenso e a review do público "
                                                   "geral, uma relação curiosa, mas que não se mostra muito clara, "
                                                   "tendo também as suas variações.")
        ])
    ])

if __name__ == '__main__':
    app.run(debug=True)
