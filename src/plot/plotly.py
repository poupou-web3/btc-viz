import plotly.graph_objects as go
from plotly.subplots import make_subplots


def plot_wma_comparison(df_btc_daily):
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Scatter(x=df_btc_daily['Date'], y=df_btc_daily['200MaOpen'],
                             mode='lines',
                             name='200 Open MA'),
                  secondary_y=False)
    fig.add_trace(go.Scatter(x=df_btc_daily['Date'], y=df_btc_daily['200MaHigh'],
                             mode='lines',
                             name='200 High MA'),
                  secondary_y=False)
    fig.add_trace(go.Scatter(x=df_btc_daily['Date'], y=df_btc_daily['200MaLow'],
                             mode='lines',
                             name='200 Low MA'),
                  secondary_y=False)
    fig.add_trace(go.Scatter(x=df_btc_daily['Date'], y=df_btc_daily['Open'],
                             mode='lines',
                             name='BTC Open daily'),
                  secondary_y=False)
    fig.add_trace(go.Scatter(x=df_btc_daily['Date'], y=df_btc_daily['Mayer'],
                             mode='lines',
                             name='Mayer Multiple'),
                  secondary_y=True)
    fig.update_layout(title='Bitcoin price and 200 day moving averages in logarithmic scale and Mayer multiple')
    return fig


def plot_current_multiple(df_btc_daily):
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Scatter(x=df_btc_daily['Date'], y=df_btc_daily['Open'],
                             mode='lines',
                             name='Btc price'),
                  secondary_y=False)
    fig.add_trace(go.Scatter(x=df_btc_daily['Date'], y=df_btc_daily['200MaOpen'],
                             mode='lines',
                             name='200 MA'),
                  secondary_y=False)
    fig.add_trace(go.Scatter(x=df_btc_daily['Date'], y=df_btc_daily['Mayer'],
                             mode='lines',
                             name='Mayer Multiple'),
                  secondary_y=True)
    fig.update_layout(title='Mayer multiple, Bitcoin price in logarithmic scale and 200 days MA')
    return fig
