import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import requests
import pandas as pd
import plotly.graph_objects as go
from chave import chave_api

from noticia import get_stock_news


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Estilo geral para a página
page_style = {
    'backgroundColor': '#000000',
    'color': '#10cf3d',
}
# Estilo para as colunas
column_style = {
    'margin-left': '2px',
    
}

# Layout 
app.layout = dbc.Container(style=page_style, className='my-container', children=[
    html.H1(children='VAROS', className='my-heading'),
    html.Div(children='''
        Tomando conta do seu dinheiro e fazendo ele crescer.
    ''', style={'color': '#10cf3d', 'margin-bottom': '20px'}),

    dcc.Dropdown(
        id='acao-dropdown',
        options=[
            {'label': 'CEAB3', 'value': 'CEAB3.SA'},
            {'label': 'WEGE3', 'value': 'WEGE3.SA'},
            {'label': 'PETR4', 'value': 'PETR4.SA'},
        ],
        value='CEAB3.SA',
        style={'color': '#10cf3d', 'margin-bottom': '20px'}
    ),

    dbc.Row([
        dbc.Col([
            html.H2(children='Cotação', className='my-subheading'),
            dcc.Graph(id='candlestick-grafico'),
        ], width=8, style=column_style, className='my-graph-col'),

        dbc.Col([
            html.H2(children='Notícias', className='my-subheading'),
            html.Div(id='noticias-div', style={'color': '#10cf3d'}),
        ], width=3, style=column_style, className='my-news-col')
    ])
])

# Callback para atualizar o gráfico de candlestick e as notícias com base na ação selecionada
@app.callback(
    [Output('candlestick-grafico', 'figure'),
     Output('noticias-div', 'children')],
    [Input('acao-dropdown', 'value')]
)
def update_content(selected_acao):
    # Usei a biblioteca requests para obter dados de cotação em tempo real da Alpha Vantage
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={selected_acao}&apikey={chave_api}'
    r = requests.get(url)
    data = r.json()

    # Extrai apenas as informações relevantes do JSON (por exemplo, os valores de fechamento)
    time_series = data.get('Time Series (Daily)', {})

    # Criação de um DataFrame do pandas com os dados
    df = pd.DataFrame(time_series).T  # Transpor para que as datas se tornem índices
    df['4. close'] = df['4. close'].astype(float)  # Converter o valor de fechamento para float

    # Criação de um gráfico de candlestick
    candlestick_fig = go.Figure(data=[go.Candlestick(x=df.index,
                                     open=df['1. open'],
                                     high=df['2. high'],
                                     low=df['3. low'],
                                     close=df['4. close'])])

    # Adiciona rótulos e título
    candlestick_fig.update_layout(title=f'{selected_acao}',
                                  xaxis_title='Data',
                                  yaxis_title='Preço em BRL',
                                  plot_bgcolor='#000000',   
                                  paper_bgcolor='#000000' ,                                  
                                  xaxis=dict(showgrid=True, gridcolor='#000000'),
                                  yaxis=dict(showgrid=True, gridcolor='#000000'),
                                  )

    # Lógica para obter notícias
    noticias = get_stock_news(selected_acao)
    noticias_links = [f"- [{noticia['title']}]({noticia['link']})" for noticia in noticias]
    noticias_markdown = dcc.Markdown('\n'.join(noticias_links))

    return candlestick_fig, noticias_markdown

if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=False)
