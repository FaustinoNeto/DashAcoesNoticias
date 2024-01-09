from chave import chave_api
import requests
import pandas as pd

# Symbol => PETR4.SA, CEAB3.SA, WEGE3.SA

# apikey below with your own key from https://www.alphavantage.co/support/#api-key
url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=PETR4.SA&apikey={chave_api}'
r = requests.get(url)
data = r.json()

# Extrair apenas as informações relevantes do JSON (por exemplo, os valores de fechamento)
time_series = data.get('Time Series (Daily)', {})

# Criar um DataFrame do pandas com os dados
df = pd.DataFrame(time_series).T  # Transpor para que as datas se tornem índices
df['4. close'] = df['4. close'].astype(float)  # Converter o valor de fechamento para float

# Configurar temporariamente o número máximo de linhas a serem exibidas
pd.set_option('display.max_rows', 10)  # Defina o número desejado de linhas

# Exibir apenas a coluna '4. close' (fechamento)
print(df['4. close'])

# Restaurar as configurações padrão
pd.reset_option('display.max_rows')

import plotly.graph_objects as go

# Criar um gráfico de candlestick
fig = go.Figure(data=[go.Candlestick(x=df.index,
                open=df['1. open'],
                high=df['2. high'],
                low=df['3. low'],
                close=df['4. close'])])

# Adicionar rótulos e título
fig.update_layout(title='Candlestick Chart - PETR4.SA',
                  xaxis_title='Data',
                  yaxis_title='Preço em BRL')

# Exibir o gráfico
fig.show()
