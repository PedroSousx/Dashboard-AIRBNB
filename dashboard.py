#!/usr/bin/env python
# coding: utf-8

# #DASHBOARD 1º BIMESTRE

# In[ ]:


#Importação das variáveis

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import dash
from dash import Dash, dcc, html, Input, Output
from scipy.stats import skew, kurtosis

import os
print("Diretório atual:", os.getcwd())

from pathlib import Path

# # pega a pasta onde o dashboard.py está
# base_path = Path(__file__).parent
# caminhoArquivo = base_path / "AB_NYC_2019.csv"

# df = pd.read_csv(caminhoArquivo)

df = pd.read_csv('AB_NYC_2019.csv')

#Carregar arquivos
# caminhoArquivo = r'c:\\Fatec\\Estatística - Python\\DASHBOARD_1BI\\AB_NYC_2019.csv'
# df = pd.read_csv("AB_NYC_2019.csv")
df = df.fillna({'reviews_per_month': 0, 'number_of_reviews': 0})

print(f"Número total de linhas no DataFrame original: {len(df)}")

df['last_review'] = pd.to_datetime(df['last_review'], errors='coerce')
ultima_data_valida = df['last_review'].max()
data_padrao = ultima_data_valida  
df['last_review'] = df['last_review'].fillna(data_padrao)
df['listings_count'] = df.groupby('neighbourhood_group')['id'].transform('count')
df['availability_365'] = df['availability_365'].clip(lower=0, upper=365)
df['occupied_days'] = (365 - df['availability_365']).clip(lower=0, upper=365)


df['last_review_year'] = df['last_review'].dt.year
anos_com_reviews = sorted([int(year) for year in df['last_review_year'].unique()])

quantitative_columns = [
    'price', 'minimum_nights', 'number_of_reviews', 'reviews_per_month',
    'calculated_host_listings_count', 'availability_365', 'occupied_days'
]

app = Dash(__name__, suppress_callback_exceptions=True)

server = app.server


region_options = [{'label': reg, 'value': reg} for reg in df['neighbourhood_group'].unique()]
room_options = [{'label': room, 'value': room} for room in df['room_type'].unique()]

# Valores iniciais dos filtros
initial_region_value = [reg['value'] for reg in region_options]
initial_room_value = [room['value'] for room in room_options]
initial_price_value = [int(df['price'].min()), int(df['price'].max())]
initial_reviews_value = [int(df['number_of_reviews'].min()), int(df['number_of_reviews'].max())]
initial_listings_value = [int(df['listings_count'].min()), int(df['listings_count'].max())]
initial_year_value = [min(anos_com_reviews), max(anos_com_reviews)]

app.layout = html.Div([
    # Título
    html.Div([
        html.H1("Dashboard Airbnb NYC", id='titulo', style={
            'color': '#fff',
            'font-family': "'Roboto', sans-serif",
            'font-size': '36px',
            'margin': '0'
        }),
    ], style={
        'align-items': 'center',
        'margin-bottom': '20px'
    }),
    html.P("Use os filtros abaixo pra explorar os dados do Airbnb em Nova York", style={
        'color': '#fff',
        'text-align': 'center',
        'margin-bottom': '20px',
        'font-family': "'Roboto', sans-serif"
    }),
    # Total de acomodações 
    html.Div(id='total-accommodations', style={
        'color': '#fff',
        'text-align': 'center',
        'margin-bottom': '20px',
        'font-family': "'Roboto', sans-serif",
        'font-size': '20px'
    }),
    html.Div([
        html.Div([
            html.Label(
                ["Selecione a região:", 
                 html.Span(" ℹ️", title="Escolha uma ou mais regiões (ex.: Manhattan, Brooklyn).")],
                style={'color': '#fff', 'font-family': "'Roboto', sans-serif"}
            ),
            dcc.Dropdown(
                id='region-filter',
                options=region_options,
                value=initial_region_value,  
                multi=True,
                style={'background-color': '#555', 'color': '#000'}
            ),
        ], style={'width': '48%', 'display': 'inline-block', 'margin-right': '4%'}),
        html.Div([
            html.Label(
                ["Selecione o tipo de acomodação:", 
                 html.Span(" ℹ️", title="Escolha um ou mais tipos de acomodação (ex.: Entire home/apt, Private room).")],
                style={'color': '#fff', 'font-family': "'Roboto', sans-serif"}
            ),
            dcc.Dropdown(
                id='room-filter',
                options=room_options,
                value=initial_room_value,  
                multi=True,
                style={'background-color': '#555', 'color': '#000'}
            ),
        ], style={'width': '48%', 'display': 'inline-block'}),
    ], style={
        'display': 'flex',
        'justify-content': 'space-between',
        'background-color': '#444',
        'padding': '20px',
        'border-radius': '10px',
        'box-shadow': '0 4px 8px rgba(0, 0, 0, 0.2)',
        'margin-bottom': '20px'
    }),
    html.Div([
        html.Div([
            html.Label(
                ["Faixa de preço:", 
                 html.Span(" ℹ️", title="Selecione uma faixa de preço (em USD) pra filtrar os anúncios.")],
                style={'color': '#fff', 'font-family': "'Roboto', sans-serif"}
            ),
            dcc.RangeSlider(
                id='price-slider',
                min=df['price'].min(),
                max=df['price'].max(),
                step=50,
                marks={i: str(i) for i in range(0, int(df['price'].max()) + 1, 500)},
                value=initial_price_value
            ),
        ], style={'width': '48%', 'display': 'inline-block', 'margin-right': '4%'}),
        html.Div([
            html.Label(
                ["Faixa de reviews:", 
                 html.Span(" ℹ️", title="Selecione uma faixa de número de avaliações pra filtrar os anúncios.")],
                style={'color': '#fff', 'font-family': "'Roboto', sans-serif"}
            ),
            dcc.RangeSlider(
                id='reviews-slider',
                min=df['number_of_reviews'].min(),
                max=df['number_of_reviews'].max(),
                step=25,
                marks={i: str(i) for i in range(0, int(df['number_of_reviews'].max()) + 1, 50)},
                value=initial_reviews_value
            ),
        ], style={'width': '48%', 'display': 'inline-block'}),
    ], style={
        'display': 'flex',
        'justify-content': 'space-between',
        'background-color': '#444',
        'padding': '20px',
        'border-radius': '10px',
        'box-shadow': '0 4px 8px rgba(0, 0, 0, 0.2)',
        'margin-bottom': '20px'
    }),
    html.Div([
        html.Label(
            ["Faixa de quantidade de anúncios por região:", 
             html.Span(" ℹ️", title="Selecione uma faixa de quantidade de anúncios por região pra filtrar os dados (ex.: regiões com 5.000 a 10.000 anúncios).")],
            style={'color': '#fff', 'font-family': "'Roboto', sans-serif"}
        ),
        dcc.RangeSlider(
            id='listings-slider',
            min=df['listings_count'].min(),
            max=df['listings_count'].max(),
            step=100,
            marks={i: str(i) for i in range(int(df['listings_count'].min()), int(df['listings_count'].max()) + 1, 2500)},
            value=initial_listings_value
        ),
    ], style={
        'background-color': '#444',
        'padding': '20px',
        'border-radius': '10px',
        'box-shadow': '0 4px 8px rgba(0, 0, 0, 0.2)',
        'margin-bottom': '20px'
    }),
    #Botões de estatísticas e área de texto
    html.Div([
        html.H2("Estatísticas das Colunas Quantitativas", style={
            'color': '#fff',
            'font-family': "'Roboto', sans-serif",
            'margin-bottom': '10px'
        }),
        html.Div([
            html.Button("Média", id='mean-button', n_clicks=0, style={
                'margin-right': '10px',
                'background-color': '#FF4B4B',
                'color': '#fff',
                'border': 'none',
                'padding': '10px 20px',
                'border-radius': '5px',
                'cursor': 'pointer'
            }),
            html.Button("Moda", id='mode-button', n_clicks=0, style={
                'margin-right': '10px',
                'background-color': '#FF4B4B',
                'color': '#fff',
                'border': 'none',
                'padding': '10px 20px',
                'border-radius': '5px',
                'cursor': 'pointer'
            }),
            html.Button("Mediana", id='median-button', n_clicks=0, style={
                'margin-right': '10px',
                'background-color': '#FF4B4B',
                'color': '#fff',
                'border': 'none',
                'padding': '10px 20px',
                'border-radius': '5px',
                'cursor': 'pointer'
            }),
            html.Button("Assimetria", id='skew-button', n_clicks=0, style={
                'margin-right': '10px',
                'background-color': '#FF4B4B',
                'color': '#fff',
                'border': 'none',
                'padding': '10px 20px',
                'border-radius': '5px',
                'cursor': 'pointer'
            }),
            html.Button("Curtose", id='kurtosis-button', n_clicks=0, style={
                'margin-right': '10px',
                'background-color': '#FF4B4B',
                'color': '#fff',
                'border': 'none',
                'padding': '10px 20px',
                'border-radius': '5px',
                'cursor': 'pointer'
            }),
            html.Button("Quartis", id='quartiles-button', n_clicks=0, style={
                'margin-right': '10px',
                'background-color': '#FF4B4B',
                'color': '#fff',
                'border': 'none',
                'padding': '10px 20px',
                'border-radius': '5px',
                'cursor': 'pointer'
            }),
            html.Button("Percentis", id='percentiles-button', n_clicks=0, style={
                'margin-right': '10px',
                'background-color': '#FF4B4B',
                'color': '#fff',
                'border': 'none',
                'padding': '10px 20px',
                'border-radius': '5px',
                'cursor': 'pointer'
            }),
            html.Button("Desvio Padrão", id='std-button', n_clicks=0, style={
                'margin-right': '10px',
                'background-color': '#FF4B4B',
                'color': '#fff',
                'border': 'none',
                'padding': '10px 20px',
                'border-radius': '5px',
                'cursor': 'pointer'
            }),
            html.Button("Coeficiente", id='coefficient-button', n_clicks=0, style={
                'margin-right': '10px',
                'background-color': '#FF4B4B',
                'color': '#fff',
                'border': 'none',
                'padding': '10px 20px',
                'border-radius': '5px',
                'cursor': 'pointer'
            }),
            html.Button("Soma Total", id='sum-button', n_clicks=0, style={
                'margin-right': '10px',
                'background-color': '#FF4B4B',
                'color': '#fff',
                'border': 'none',
                'padding': '10px 20px',
                'border-radius': '5px',
                'cursor': 'pointer'
            }),
        ], style={'margin-bottom': '20px'}),
        html.Div(id='stats-output', style={
            'background-color': '#555',
            'padding': '20px',
            'border-radius': '10px',
            'color': '#fff',
            'font-family': "'Roboto', sans-serif",
            'white-space': 'pre-wrap'
        })
    ], style={
        'background-color': '#444',
        'padding': '20px',
        'border-radius': '10px',
        'box-shadow': '0 4px 8px rgba(0, 0, 0, 0.2)',
        'margin-bottom': '20px'
    }),
    html.Div(style={'height': '40px'}),
    # Linha 1: Gráfico 1 (Acomodações por Região) e Gráfico 2 (Quantidade de Anúncios por Tipo de Acomodação)
    html.Div([
        html.Div([
            html.H2('Acomodações por Região', id='subtitulo-grafico1', style={'color': '#fff', 'font-family': "'Roboto', sans-serif"}),
            dcc.Graph(id='anuncios-bar-graph', style={'height': '400px', 'width': '100%'}),
        ], style={
            'width': '48%',
            'display': 'inline-block',
            'margin-right': '4%',
            'background-color': '#444',
            'padding': '10px',
            'border-radius': '10px',
            'box-shadow': '0 4px 8px rgba(0, 0, 0, 0.2)'
        }),
        html.Div([
            html.H2('Quantidade de Anúncios por Tipo de Acomodação', id='subtitulo-grafico2', style={'color': '#fff', 'font-family': "'Roboto', sans-serif"}),
            dcc.Graph(id='anuncio-acomodacao-bar-graph', style={'height': '400px', 'width': '100%'}),
        ], style={
            'width': '48%',
            'display': 'inline-block',
            'background-color': '#444',
            'padding': '10px',
            'border-radius': '10px',
            'box-shadow': '0 4px 8px rgba(0, 0, 0, 0.2)'
        }),
    ], style={'display': 'flex', 'justify-content': 'space-between'}),
    html.Div(style={'height': '40px'}),
    # Linha 2: Gráfico 3 (Localização - Mapa 1, agrupado por região)
    html.Div([
        html.H2('Localização (Mapa 1 - Agrupado por Região)', id='subtitulo-grafico3', style={'color': '#fff', 'font-family': "'Roboto', sans-serif"}),
        dcc.Graph(id='map-graph', style={'height': '700px', 'width': '100%'}),
    ], style={
        'background-color': '#444',
        'padding': '10px',
        'border-radius': '10px',
        'box-shadow': '0 4px 8px rgba(0, 0, 0, 0.2)'
    }),
    html.Div(style={'height': '40px'}),
    # Linha 3: Gráfico 11 (Localização - Mapa 2, cada anúncio individual)
    html.Div([
        html.H2('Localização (Mapa 2 - Cada Anúncio)', id='subtitulo-grafico11', style={'color': '#fff', 'font-family': "'Roboto', sans-serif"}),
        dcc.Graph(id='map-graph-2', style={'height': '700px', 'width': '100%'}),
    ], style={
        'background-color': '#444',
        'padding': '10px',
        'border-radius': '10px',
        'box-shadow': '0 4px 8px rgba(0, 0, 0, 0.2)'
    }),
    html.Div(style={'height': '40px'}),
    # Linha 4: Gráfico 4 (Preço Médio por Região), Gráfico 5 (Preços por Acomodação), Gráfico 6 (Quantidade Mínima por Noites)
    html.Div([
        html.Div([
            html.H2('Preço Médio por Região', id='subtitulo-grafico4', style={'color': '#fff', 'font-family': "'Roboto', sans-serif"}),
            dcc.Graph(id='avg-price-bar-graph', style={'height': '400px', 'width': '100%'}),
        ], style={
            'width': '31%',
            'display': 'inline-block',
            'margin-right': '1%',
            'background-color': '#444',
            'padding': '10px',
            'border-radius': '10px',
            'box-shadow': '0 4px 8px rgba(0, 0, 0, 0.2)'
        }),
        html.Div([
            html.H2('Preços por Acomodação', id='subtitulo-grafico5', style={'color': '#fff', 'font-family': "'Roboto', sans-serif"}),
            dcc.Graph(id='price-histogram', style={'height': '400px', 'width': '100%'}),
        ], style={
            'width': '31%',
            'display': 'inline-block',
            'margin-right': '1%',
            'background-color': '#444',
            'padding': '10px',
            'border-radius': '10px',
            'box-shadow': '0 4px 8px rgba(0, 0, 0, 0.2)'
        }),
        html.Div([
            html.H2('Quantidade Mínima por Noites', id='subtitulo-grafico6', style={'color': '#fff', 'font-family': "'Roboto', sans-serif"}),
            dcc.Graph(id='minimum-nights-histogram', style={'height': '400px', 'width': '100%'}),
        ], style={
            'width': '31%',
            'display': 'inline-block',
            'background-color': '#444',
            'padding': '10px',
            'border-radius': '10px',
            'box-shadow': '0 4px 8px rgba(0, 0, 0, 0.2)'
        }),
    ], style={'display': 'flex', 'justify-content': 'space-between'}),
    html.Div(style={'height': '40px'}),
    # Linha 5: Gráfico 7 (Ocupação ao Longo do Ano), Gráfico 8 (Total de Avaliações por Região), Gráfico 9 (Total de Avaliações por Tipo de Acomodação)
    html.Div([
        html.Div([
            html.H2('Ocupação ao Longo do Ano', id='subtitulo-grafico7', style={'color': '#fff', 'font-family': "'Roboto', sans-serif"}),
            dcc.Graph(id='occupancy-histogram', style={'height': '400px', 'width': '100%'}),
        ], style={
            'width': '31%',
            'display': 'inline-block',
            'margin-right': '1%',
            'background-color': '#444',
            'padding': '10px',
            'border-radius': '10px',
            'box-shadow': '0 4px 8px rgba(0, 0, 0, 0.2)'
        }),
        html.Div([
            html.H2('Total de Avaliações por Região', id='subtitulo-grafico8', style={'color': '#fff', 'font-family': "'Roboto', sans-serif"}),
            dcc.Graph(id='avaliacao-bar-graph', style={'height': '400px', 'width': '100%'}),
        ], style={
            'width': '31%',
            'display': 'inline-block',
            'margin-right': '1%',
            'background-color': '#444',
            'padding': '10px',
            'border-radius': '10px',
            'box-shadow': '0 4px 8px rgba(0, 0, 0, 0.2)'
        }),
        html.Div([
            html.H2('Total de Avaliações por Tipo de Acomodação', id='subtitulo-grafico9', style={'color': '#fff', 'font-family': "'Roboto', sans-serif"}),
            dcc.Graph(id='reviews-room-type-bar-graph', style={'height': '400px', 'width': '100%'}),
        ], style={
            'width': '31%',
            'display': 'inline-block',
            'background-color': '#444',
            'padding': '10px',
            'border-radius': '10px',
            'box-shadow': '0 4px 8px rgba(0, 0, 0, 0.2)'
        }),
    ], style={'display': 'flex', 'justify-content': 'space-between'}),
    html.Div(style={'height': '40px'}),
    # Linha 6: Gráfico 10 (Número de Reviews por Data da Última Review)
    html.Div([
        html.Label(
            ["Selecione o intervalo de anos:", 
             html.Span(" ℹ️", title="Escolha o intervalo de anos pra visualizar as reviews.")],
            style={'color': '#fff', 'font-family': "'Roboto', sans-serif", 'margin-bottom': '10px'}
        ),
        dcc.RangeSlider(
            id='year-slider',
            min=min(anos_com_reviews),
            max=max(anos_com_reviews),
            step=1,
            marks={int(year): str(year) for year in anos_com_reviews},
            value=initial_year_value
        ),
        html.H2('Número de Reviews', id='subtitulo-grafico10', style={'color': '#fff', 'font-family': "'Roboto', sans-serif", 'margin-top': '20px'}),
        dcc.Graph(id='reviews-line-graph', style={'height': '400px', 'width': '100%'}),
    ], style={
        'background-color': '#444',
        'padding': '20px',
        'border-radius': '10px',
        'box-shadow': '0 4px 8px rgba(0, 0, 0, 0.2)'
    }),
    html.Div(style={'height': '40px'}),
    # Integrantes do grupo
    html.Div([
        html.H2("Integrantes do Grupo", style={
            'color': '#fff',
            'font-family': "'Roboto', sans-serif",
            'text-align': 'center',
            'margin-bottom': '10px'
        }),
        html.H3("Pedro Henrique Sousa Cintra", style={
            'color': '#fff',
            'font-family': "'Roboto', sans-serif",
            'text-align': 'center',
            'margin': '5px 0'
        }),
        html.H3("Bruno Serapião Ribeiro", style={
            'color': '#fff',
            'font-family': "'Roboto', sans-serif",
            'text-align': 'center',
            'margin': '5px 0'
        }),
        html.H3("Maysa de Jesus Bernardes", style={
            'color': '#fff',
            'font-family': "'Roboto', sans-serif",
            'text-align': 'center',
            'margin': '5px 0'
        }),
    ], style={
        'background-color': '#444',
        'padding': '20px',
        'border-radius': '10px',
        'box-shadow': '0 4px 8px rgba(0, 0, 0, 0.2)',
        'margin-bottom': '20px'
    }),
], style={
    'background-color': '#333',
    'padding': '20px',
    'min-height': '100vh',
    'font-family': "'Roboto', sans-serif"
})

# Função para criar um gráfico vazio com mensagem
def create_empty_graph(message="Nenhum dado disponível com os filtros selecionados"):
    fig = go.Figure()
    fig.add_annotation(
        text=message,
        xref="paper",
        yref="paper",
        showarrow=False,
        font=dict(size=20, color="#fff"),
        x=0.5,
        y=0.5
    )
    fig.update_layout(
        plot_bgcolor='#444',
        paper_bgcolor='#444',
        font_color='#e0e0e0',
        margin=dict(l=40, r=40, t=40, b=40),
        xaxis=dict(showgrid=False, zeroline=False),
        yaxis=dict(showgrid=False, zeroline=False)
    )
    return fig

# Função de filtro
def filter_dataframe(selected_regions, selected_rooms, price_range, reviews_range, listings_range):
    if not selected_regions:
        selected_regions = df['neighbourhood_group'].unique().tolist()
    if not selected_rooms:
        selected_rooms = df['room_type'].unique().tolist()

    # filtro por região e tipo de acomodação
    filtered_df = df[
        (df['neighbourhood_group'].isin(selected_regions)) &
        (df['room_type'].isin(selected_rooms))
    ]

    # Filtro por faixa de preço e reviews
    filtered_df = filtered_df[
        (filtered_df['price'].between(price_range[0], price_range[1])) &
        (filtered_df['number_of_reviews'].between(reviews_range[0], reviews_range[1]))
    ]

    # Filtro por listings_count
    if filtered_df.empty:
        print("DataFrame vazio após filtros de região, tipo de acomodação, preço e reviews.")
        return filtered_df

    # Agrupar por neighbourhood_group para verificar quais regiões atendem ao filtro de listings_count
    listings_by_region = filtered_df.groupby('neighbourhood_group')['listings_count'].first().reset_index()
    valid_regions = listings_by_region[
        listings_by_region['listings_count'].between(listings_range[0], listings_range[1])
    ]['neighbourhood_group'].tolist()

    if not valid_regions:
        print("Nenhuma região atende ao filtro de listings_count. Retornando DataFrame vazio.")
        return pd.DataFrame(columns=filtered_df.columns)

    # Filtrar o DataFrame para incluir apenas as regiões válidas
    filtered_df = filtered_df[filtered_df['neighbourhood_group'].isin(valid_regions)]

    print(f"Filtrando dados:")
    print(f"Regiões selecionadas: {selected_regions}")
    print(f"Tipos de acomodação: {selected_rooms}")
    print(f"Faixa de preço: {price_range}")
    print(f"Faixa de reviews: {reviews_range}")
    print(f"Faixa de listings: {listings_range}")
    print(f"Regiões válidas após filtro de listings_count: {valid_regions}")
    print(f"Tamanho do DataFrame filtrado: {len(filtered_df)}")

    return filtered_df

# Callback para atualizar o número total de acomodações
@app.callback(
    Output('total-accommodations', 'children'),
    [Input('region-filter', 'value'),
     Input('room-filter', 'value'),
     Input('price-slider', 'value'),
     Input('reviews-slider', 'value'),
     Input('listings-slider', 'value')]
)
def update_total_accommodations(selected_regions, selected_rooms, price_range, reviews_range, listings_range):
    filtered_df = filter_dataframe(selected_regions, selected_rooms, price_range, reviews_range, listings_range)
    total_count = len(filtered_df)
    return f"Total: {total_count:,} acomodações"

# Callback para os botões de estatísticas
@app.callback(
    Output('stats-output', 'children'),
    [Input('mean-button', 'n_clicks'),
     Input('mode-button', 'n_clicks'),
     Input('median-button', 'n_clicks'),
     Input('skew-button', 'n_clicks'),
     Input('kurtosis-button', 'n_clicks'),
     Input('sum-button', 'n_clicks'),
     Input('quartiles-button', 'n_clicks'),
     Input('percentiles-button', 'n_clicks'),
     Input('std-button', 'n_clicks'),
     Input('coefficient-button', 'n_clicks'),  
     Input('region-filter', 'value'),
     Input('room-filter', 'value'),
     Input('price-slider', 'value'),
     Input('reviews-slider', 'value'),
     Input('listings-slider', 'value')]
)
def update_stats(mean_clicks, mode_clicks, median_clicks, skew_clicks, kurtosis_clicks, sum_clicks,
                quartiles_clicks, percentiles_clicks, std_clicks, coefficient_clicks,  
                selected_regions, selected_rooms, price_range, reviews_range, listings_range):
    filtered_df = filter_dataframe(selected_regions, selected_rooms, price_range, reviews_range, listings_range)
    
    if filtered_df.empty:
        return "Nenhum dado disponível com os filtros selecionados."

    ctx = dash.callback_context
    if not ctx.triggered:
        return "Clique em um botão para ver as estatísticas."

    button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    result = []

    if button_id == 'mean-button':
        result.append("Média das colunas quantitativas:\n")
        for col in quantitative_columns:
            mean_value = filtered_df[col].mean()
            result.append(f"{col}: {mean_value:.2f}\n")

    elif button_id == 'mode-button':
        result.append("Moda das colunas quantitativas:\n")
        for col in quantitative_columns:
            mode_value = filtered_df[col].mode()[0] if not filtered_df[col].mode().empty else "N/A"
            result.append(f"{col}: {mode_value}\n")

    elif button_id == 'median-button':
        result.append("Mediana das colunas quantitativas:\n")
        for col in quantitative_columns:
            median_value = filtered_df[col].median()
            result.append(f"{col}: {median_value:.2f}\n")

    elif button_id == 'skew-button':
        result.append("Assimetria das colunas quantitativas:\n")
        for col in quantitative_columns:
            skew_value = skew(filtered_df[col].dropna())
            result.append(f"{col}: {skew_value:.2f}\n")

    elif button_id == 'kurtosis-button':
        result.append("Curtose das colunas quantitativas:\n")
        for col in quantitative_columns:
            kurtosis_value = kurtosis(filtered_df[col].dropna())
            result.append(f"{col}: {kurtosis_value:.2f}\n")


    elif button_id == 'quartiles-button':
        result.append("Quartis das colunas quantitativas:\n")
        for col in quantitative_columns:
            q1 = filtered_df[col].quantile(0.25)  
            q2 = filtered_df[col].quantile(0.50)  
            q3 = filtered_df[col].quantile(0.75)  
            result.append(f"{col}:\n  Q1 (25%): {q1:.2f}\n  Q2 (50%): {q2:.2f}\n  Q3 (75%): {q3:.2f}\n")

    elif button_id == 'percentiles-button':
        result.append("Percentis das colunas quantitativas:\n")
        percentiles = [0.10, 0.25, 0.50, 0.75, 0.90]  
        for col in quantitative_columns:
            perc_values = filtered_df[col].quantile(percentiles)
            result.append(f"{col}:\n")
            for p, value in zip(percentiles, perc_values):
                result.append(f"  {int(p*100)}%: {value:.2f}\n")

    elif button_id == 'std-button':
        result.append("Desvio Padrão das colunas quantitativas:\n")
        for col in quantitative_columns:
            std_value = filtered_df[col].std()
            result.append(f"{col}: {std_value:.2f}\n")

    elif button_id == 'coefficient-button':
        result.append("Coeficiente de Variação das colunas quantitativas:\n")
        for col in quantitative_columns:
            mean_value = filtered_df[col].mean()
            std_value = filtered_df[col].std()
            if mean_value != 0:  # Evitar divisão por zero
                cv_value = (std_value / mean_value) * 100  
                result.append(f"{col}: {cv_value:.2f}%\n")
            else:
                result.append(f"{col}: N/A (média é zero)\n")

    elif button_id == 'sum-button':
        result.append("Soma total das colunas quantitativas:\n")
        for col in quantitative_columns:
            sum_value = filtered_df[col].sum()
            result.append(f"{col}: {sum_value:.2f}\n")
    return "".join(result)

# Gráfico 1: Acomodações por Região
@app.callback(
    Output('anuncios-bar-graph', 'figure'),
    [Input('region-filter', 'value'),
     Input('room-filter', 'value'),
     Input('price-slider', 'value'),
     Input('reviews-slider', 'value'),
     Input('listings-slider', 'value')]
)
def update_accommodations_by_region_chart(selected_regions, selected_rooms, price_range, reviews_range, listings_range):
    filtered_df = filter_dataframe(selected_regions, selected_rooms, price_range, reviews_range, listings_range)
    
    if filtered_df.empty:
        return create_empty_graph()

    accommodation_count_by_region = filtered_df.groupby('neighbourhood_group').size().reset_index(name='count')
    
    fig = px.bar(
        accommodation_count_by_region,
        x='neighbourhood_group',
        y='count',
        labels={'neighbourhood_group': 'Região', 'count': 'Número de Acomodações'},
        color='count',
        color_continuous_scale='Viridis'
    )
    
    fig.update_layout(
        plot_bgcolor='#444',
        paper_bgcolor='#444',
        font_color='#e0e0e0',
        margin=dict(l=40, r=40, t=40, b=40)
    )
    
    fig.update_xaxes(tickangle=45, tickfont=dict(size=12))
    fig.update_yaxes(tickfont=dict(size=12))
    
    return fig

# Gráfico 2: Quantidade de Anúncios por Tipo de Acomodação
@app.callback(
    Output('anuncio-acomodacao-bar-graph', 'figure'),
    [Input('region-filter', 'value'),
     Input('room-filter', 'value'),
     Input('price-slider', 'value'),
     Input('reviews-slider', 'value'),
     Input('listings-slider', 'value')]
)
def update_accommodation_count_by_room_type_chart(selected_regions, selected_rooms, price_range, reviews_range, listings_range):
    filtered_df = filter_dataframe(selected_regions, selected_rooms, price_range, reviews_range, listings_range)
    
    if filtered_df.empty:
        return create_empty_graph()

    accommodation_count_by_room_type = filtered_df.groupby('room_type').size().reset_index(name='count')
    
    fig = px.bar(
        accommodation_count_by_room_type,
        x='room_type',
        y='count',
        labels={'room_type': 'Tipo de Acomodação', 'count': 'Número de Anúncios'},
        color='count',
        color_continuous_scale='Viridis'
    )
    
    fig.update_layout(
        plot_bgcolor='#444',
        paper_bgcolor='#444',
        font_color='#e0e0e0',
        margin=dict(l=40, r=40, t=40, b=40)
    )
    
    fig.update_xaxes(tickangle=45, tickfont=dict(size=12))
    fig.update_yaxes(tickfont=dict(size=12))
    
    return fig

# Gráfico 3: Localização (Mapa 1 - Agrupado por região)
@app.callback(
    Output('map-graph', 'figure'),
    [Input('region-filter', 'value'),
     Input('room-filter', 'value'),
     Input('price-slider', 'value'),
     Input('reviews-slider', 'value'),
     Input('listings-slider', 'value')]
)
def update_map_chart(selected_regions, selected_rooms, price_range, reviews_range, listings_range):
    filtered_df = filter_dataframe(selected_regions, selected_rooms, price_range, reviews_range, listings_range)
    
    if filtered_df.empty:
        return create_empty_graph()

    # Agrupar os dados por neighbourhood_group
    grouped_df = filtered_df.groupby('neighbourhood_group').agg({
        'id': 'count',  
        'price': 'mean',  
        'latitude': 'mean',  
        'longitude': 'mean'  
    }).reset_index()

    # Renomear as colunas para clareza
    grouped_df = grouped_df.rename(columns={
        'id': 'listing_count',
        'price': 'avg_price'
    })

    # Criar o gráfico de mapa com bolas maiores
    fig = px.scatter_mapbox(
        grouped_df,
        lat='latitude',
        lon='longitude',
        size='listing_count',  
        color='avg_price',  
        size_max=50, 
        zoom=10,
        mapbox_style="open-street-map",
        hover_data={
            'neighbourhood_group': True,
            'listing_count': True,
            'avg_price': ':.2f',  
            'latitude': False,  
            'longitude': False 
        },
        color_continuous_scale='Viridis', 
        labels={
            'neighbourhood_group': 'Região',
            'listing_count': 'Número de Anúncios',
            'avg_price': 'Preço Médio (USD)'
        }
    )
    
    fig.update_layout(
        plot_bgcolor='#444',
        paper_bgcolor='#444',
        font_color='#e0e0e0',
        margin=dict(l=40, r=40, t=40, b=40)
    )
    
    return fig

# Gráfico 11: Localização (Mapa 2 - Cada anúncio individual)
@app.callback(
    Output('map-graph-2', 'figure'),
    [Input('region-filter', 'value'),
     Input('room-filter', 'value'),
     Input('price-slider', 'value'),
     Input('reviews-slider', 'value'),
     Input('listings-slider', 'value')]
)
def update_map_chart_2(selected_regions, selected_rooms, price_range, reviews_range, listings_range):
    filtered_df = filter_dataframe(selected_regions, selected_rooms, price_range, reviews_range, listings_range)
    
    if filtered_df.empty:
        return create_empty_graph()

    # Criar o gráfico de mapa com cada anúncio individual
    fig = px.scatter_mapbox(
        filtered_df,
        lat='latitude',
        lon='longitude',
        color='price',  
        size_max=15,  
        zoom=10,
        mapbox_style="open-street-map",
        hover_data={
            'name': True,  
            'neighbourhood_group': True,  
            'room_type': True,  
            'price': ':.2f',  
            'latitude': False,  
            'longitude': False 
        },
        color_continuous_scale='Viridis', 
        labels={
            'name': 'Nome do Anúncio',
            'neighbourhood_group': 'Região',
            'room_type': 'Tipo de Acomodação',
            'price': 'Preço (USD)'
        }
    )
    
    # Ajustar o tamanho dos pontos para serem menores e mais visíveis
    fig.update_traces(marker=dict(size=5, opacity=0.6)) 

    fig.update_layout(
        plot_bgcolor='#444',
        paper_bgcolor='#444',
        font_color='#e0e0e0',
        margin=dict(l=40, r=40, t=40, b=40)
    )
    
    return fig

# Gráfico 4: Preço Médio por Região
@app.callback(
    Output('avg-price-bar-graph', 'figure'),
    [Input('region-filter', 'value'),
     Input('room-filter', 'value'),
     Input('price-slider', 'value'),
     Input('reviews-slider', 'value'),
     Input('listings-slider', 'value')]
)
def update_price_average_by_region_chart(selected_regions, selected_rooms, price_range, reviews_range, listings_range):
    filtered_df = filter_dataframe(selected_regions, selected_rooms, price_range, reviews_range, listings_range)
    
    if filtered_df.empty:
        return create_empty_graph()

    average_price_by_region = filtered_df.groupby('neighbourhood_group')['price'].mean().reset_index()
    
    fig = px.bar(
        average_price_by_region,
        x='neighbourhood_group',
        y='price',
        labels={'neighbourhood_group': 'Região', 'price': 'Preço Médio (USD)'},
        color='price',
        color_continuous_scale='Viridis'
    )
    
    fig.update_layout(
        plot_bgcolor='#444',
        paper_bgcolor='#444',
        font_color='#e0e0e0',
        margin=dict(l=40, r=40, t=40, b=40)
    )
    
    fig.update_xaxes(tickangle=45, tickfont=dict(size=12))
    fig.update_yaxes(tickfont=dict(size=12))
    
    return fig

# Gráfico 5: Preços por Acomodação
@app.callback(
    Output('price-histogram', 'figure'),
    [Input('region-filter', 'value'),
     Input('room-filter', 'value'),
     Input('price-slider', 'value'),
     Input('reviews-slider', 'value'),
     Input('listings-slider', 'value')]
)
def update_price_histogram(selected_regions, selected_rooms, price_range, reviews_range, listings_range):
    filtered_df = filter_dataframe(selected_regions, selected_rooms, price_range, reviews_range, listings_range)
    
    if filtered_df.empty:
        return create_empty_graph()

    filtered_df = filtered_df[filtered_df['price'].between(0, 1000)]
    
    fig = px.histogram(
        filtered_df,
        x='price',
        nbins=50,  
        labels={'price': 'Preço (USD)', 'count': 'Quantidade de Anúncios'},
        color_discrete_sequence=['#00CC96']  
    )
    
    fig.update_layout(
        plot_bgcolor='#444',
        paper_bgcolor='#444',
        font_color='#e0e0e0',
        margin=dict(l=40, r=40, t=40, b=40)
    )
    
    fig.update_xaxes(tickfont=dict(size=12))
    fig.update_yaxes(title_text='Quantidade de Anúncios', tickfont=dict(size=12))     
    
    return fig

# Gráfico 6: Quantidade Mínima por Noites
@app.callback(
    Output('minimum-nights-histogram', 'figure'),
    [Input('region-filter', 'value'),
     Input('room-filter', 'value'),
     Input('price-slider', 'value'),
     Input('reviews-slider', 'value'),
     Input('listings-slider', 'value')]
)
def update_minimum_nights_histogram(selected_regions, selected_rooms, price_range, reviews_range, listings_range):
    filtered_df = filter_dataframe(selected_regions, selected_rooms, price_range, reviews_range, listings_range)
    
    if filtered_df.empty:
        return create_empty_graph()

    filtered_df = filtered_df[filtered_df['minimum_nights'].between(0, 30)]
    
    fig = px.histogram(
        filtered_df,
        x='minimum_nights',
        nbins=30,  
        labels={'minimum_nights': 'Quantidade Mínima de Noites', 'count': 'Quantidade de Anúncios'},
        color_discrete_sequence=['#EF553B'] 
    )
    
    fig.update_layout(
        plot_bgcolor='#444',
        paper_bgcolor='#444',
        font_color='#e0e0e0',
        margin=dict(l=40, r=40, t=40, b=40)
    )
    
    fig.update_xaxes(tickfont=dict(size=12))
    fig.update_yaxes(title_text='Quantidade de Anúncios', tickfont=dict(size=12))     
    return fig

# Gráfico 7: Ocupação ao Longo do Ano
@app.callback(
    Output('occupancy-histogram', 'figure'),
    [Input('region-filter', 'value'),
     Input('room-filter', 'value'),
     Input('price-slider', 'value'),
     Input('reviews-slider', 'value'),
     Input('listings-slider', 'value')]
)
def update_occupancy_histogram(selected_regions, selected_rooms, price_range, reviews_range, listings_range):
    filtered_df = filter_dataframe(selected_regions, selected_rooms, price_range, reviews_range, listings_range)
    
    if filtered_df.empty:
        return create_empty_graph()

    filtered_df['occupied_days'] = filtered_df['occupied_days'].clip(lower=0, upper=365)
    
    bin_size = 10
    bins = list(range(0, 366, bin_size))
    
    fig = go.Figure(data=[
        go.Histogram(
            x=filtered_df['occupied_days'],
            xbins=dict(start=0, end=365, size=bin_size),
            marker_color='#636EFA',
            hovertemplate='Dias Ocupados: %{x}<br>Quantidade de Imóveis: %{y}<extra></extra>'
        )
    ])
    
    fig.update_layout(
        plot_bgcolor='#444',
        paper_bgcolor='#444',
        font_color='#e0e0e0',
        margin=dict(l=40, r=40, t=40, b=40),
        xaxis_title="Dias Ocupados por Ano",
        yaxis_title="Quantidade de Imóveis"
    )
    
    fig.update_xaxes(tickfont=dict(size=12), range=[0, 365])
    fig.update_yaxes(tickfont=dict(size=12))

    return fig

# Gráfico 8: Total de Avaliações por Região
@app.callback(
    Output('avaliacao-bar-graph', 'figure'),
    [Input('region-filter', 'value'),
     Input('room-filter', 'value'),
     Input('price-slider', 'value'),
     Input('reviews-slider', 'value'),
     Input('listings-slider', 'value')]
)
def update_reviews_total_by_neighborhood_chart(selected_regions, selected_rooms, price_range, reviews_range, listings_range):
    filtered_df = filter_dataframe(selected_regions, selected_rooms, price_range, reviews_range, listings_range)
    
    if filtered_df.empty:
        return create_empty_graph()

    reviews_total_by_neighborhood = filtered_df.groupby('neighbourhood_group')['number_of_reviews'].sum().reset_index()
    accommodation_count_by_neighborhood = filtered_df.groupby('neighbourhood_group').size().reset_index(name='accommodation_count')
    combined_data = reviews_total_by_neighborhood.merge(accommodation_count_by_neighborhood, on='neighbourhood_group')
    
    fig = px.bar(
        combined_data,
        x='neighbourhood_group',
        y=['number_of_reviews', 'accommodation_count'],
        labels={'neighbourhood_group': 'Grupo de Bairros', 'value': 'Valores', 'variable': 'Métrica'},
        color_discrete_map={'number_of_reviews': '#636EFA', 'accommodation_count': '#EF553B'},
        barmode='group'
    )
    
    fig.for_each_trace(lambda t: t.update(name='Total de Avaliações' if t.name == 'number_of_reviews' else 'Número de Acomodações'))
    
    fig.update_layout(
        plot_bgcolor='#444',
        paper_bgcolor='#444',
        font_color='#e0e0e0',
        margin=dict(l=40, r=40, t=40, b=40),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    fig.update_xaxes(tickangle=45, tickfont=dict(size=12))
    fig.update_yaxes(tickfont=dict(size=12))
    
    return fig

# Gráfico 9: Total de Avaliações por Tipo de Acomodação
@app.callback(
    Output('reviews-room-type-bar-graph', 'figure'),
    [Input('region-filter', 'value'),
     Input('room-filter', 'value'),
     Input('price-slider', 'value'),
     Input('reviews-slider', 'value'),
     Input('listings-slider', 'value')]
)
def update_reviews_total_by_room_type_chart(selected_regions, selected_rooms, price_range, reviews_range, listings_range):
    filtered_df = filter_dataframe(selected_regions, selected_rooms, price_range, reviews_range, listings_range)
    
    if filtered_df.empty:
        return create_empty_graph()

    reviews_total_by_room_type = filtered_df.groupby('room_type')['number_of_reviews'].sum().reset_index()
    
    fig = px.bar(
        reviews_total_by_room_type,
        x='room_type',
        y='number_of_reviews',
        labels={'room_type': 'Tipo de Acomodação', 'number_of_reviews': 'Total de Avaliações'},
        color='number_of_reviews',
        color_continuous_scale='Viridis'
    )
    
    fig.update_layout(
        plot_bgcolor='#444',
        paper_bgcolor='#444',
        font_color='#e0e0e0',
        margin=dict(l=40, r=40, t=40, b=40)
    )
    
    fig.update_xaxes(tickangle=45, tickfont=dict(size=12))
    fig.update_yaxes(tickfont=dict(size=12))
    
    return fig

# Gráfico 10: Número de Reviews por Data da Última Review
@app.callback(
    Output('reviews-line-graph', 'figure'),
    [Input('region-filter', 'value'),
     Input('room-filter', 'value'),
     Input('price-slider', 'value'),
     Input('reviews-slider', 'value'),
     Input('listings-slider', 'value'),
     Input('year-slider', 'value')]
)
def update_reviews_line_chart(selected_regions, selected_rooms, price_range, reviews_range, listings_range, year_range):
    filtered_df = filter_dataframe(selected_regions, selected_rooms, price_range, reviews_range, listings_range)
    
    if filtered_df.empty:
        return create_empty_graph()


    if year_range is None or len(year_range) != 2:
        year_range = [min(anos_com_reviews), max(anos_com_reviews)]
    else:
        year_range = [int(year) for year in year_range]  
    
    filtered_df = filtered_df[
        (filtered_df['last_review_year'] >= year_range[0]) &
        (filtered_df['last_review_year'] <= year_range[1])
    ]
    
    if filtered_df.empty:
        return create_empty_graph("Nenhum dado disponível para o intervalo de anos selecionado")

    reviews_by_date = filtered_df.groupby(filtered_df['last_review'].dt.date)['number_of_reviews'].sum().reset_index()
    
    if reviews_by_date.empty:
        return create_empty_graph("Nenhum dado disponível após o agrupamento por data")

    x_range = [reviews_by_date['last_review'].min(), reviews_by_date['last_review'].max()]
    y_max = reviews_by_date['number_of_reviews'].max()
    y_range = [0, max(100, y_max * 1.1)]  
    
    fig = px.line(
        reviews_by_date,
        x='last_review',
        y='number_of_reviews',
        labels={'last_review': '', 'number_of_reviews': 'Número de Reviews'},
        line_shape='linear',
        render_mode='svg'
    )
    
    fig.update_traces(
        line_color='#FF4B4B',
        line_width=2,
        hovertemplate='Data: %{x}<br>Número de Reviews: %{y}<extra></extra>'
    )
    
    fig.update_layout(
        plot_bgcolor='#444',
        paper_bgcolor='#444',
        font_color='#e0e0e0',
        margin=dict(l=40, r=40, t=40, b=40),
        xaxis=dict(
            tickformat='%Y-%m-%d',
            tickangle=45,
            tickfont=dict(size=12),
            range=x_range,
            showgrid=True,
            gridcolor='rgba(255, 255, 255, 0.1)'
        ),
        yaxis=dict(
            tickfont=dict(size=12),
            range=y_range,
            showgrid=True,
            gridcolor='rgba(255, 255, 255, 0.1)'
        )
    )
    
    return fig

if __name__ == '__main__':
    app.run(debug=True)
    
print("Acesse o dashboard em: http://127.0.0.1:8050")

