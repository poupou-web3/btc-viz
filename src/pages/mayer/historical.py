import pandas as pd
from datetime import date
import streamlit as st

from src.plot.plotly import plot_wma_comparison


def page_mayer_historical():
    st.header('Mayer multiple')
    st.subheader('Open Price vs High price vs Low price')

    st.write('The mayer multiple has been first used by Trace Mayer, it is the multiple between the 200 days moving '
             'average of bitcoin price and the current price.\n'
             'We study the impact of the daily price chosen (high, low, open) on the multiple.')

    df_btc_daily = pd.read_csv('Data/BTC_USD_2013-10-01_2020-11-28-CoinDesk.csv')
    df_btc_daily = df_btc_daily
    df_btc_daily.set_axis(['Currency', 'Date', 'Close', 'Open', 'High', 'Low'], axis=1, inplace=True)
    df_btc_daily['Date'] = pd.to_datetime(df_btc_daily['Date'])

    df_btc_daily['200MaOpen'] = df_btc_daily['Open'].rolling(window=200).mean()
    df_btc_daily['200MaLow'] = df_btc_daily['Low'].rolling(window=200).mean()
    df_btc_daily['200MaHigh'] = df_btc_daily['High'].rolling(window=200).mean()
    df_btc_daily['Mayer'] = df_btc_daily['Open'] / df_btc_daily['200MaOpen']

    fig_wma_comp = plot_wma_comparison(df_btc_daily)
    st.write(fig_wma_comp)

    st.write('The open weighted moving average is almost exactly at equidistant from the 200 High and 200 low WMA.\n'
             'The choice of the day price does not have a significant impact on the 200 days moving average. Though, '
             'in others charts we use the 200 day open price do compute the mayer multiple\n '
             'Note: the historical data will not be updated on a regular basis.')

    return None