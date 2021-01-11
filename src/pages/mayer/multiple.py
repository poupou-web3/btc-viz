import streamlit as st
import pandas as pd
from datetime import date
import requests

from src.plot.plotly import plot_current_multiple

COINDESK_HISTORICAL_URL = 'https://api.coindesk.com/v1/bpi/historical/open.json'
COINDESK_CURRENT_URL = 'https://api.coindesk.com/v1/bpi/currentprice.json'


def page_mayer_multiple():
    st.header('Mayer multiple')

    st.write('The mayer multiple has been first used by Trace Mayer, it is the multiple between the 200 days moving '
             'average of bitcoin price and the current price. Trace Mayer evaluated that the best returns was '
             'obtained by accumulating bitcoins when the multiple is below 2.4. However, that simulation depends on '
             'the data used. Here we present the mayer multiple calculated with data starting on the 2013-10-01. ')

    today = date.today()

    url = (COINDESK_HISTORICAL_URL + '?start=2013-10-01&end={}').format(
        today.isoformat()[:10],
        today.isoformat())

    json = requests.get(url).json()
    dict_bpi = json.get('bpi')

    # update with current bpi
    json_current = requests.get(COINDESK_CURRENT_URL).json()
    current_price = json_current.get('bpi').get('USD').get('rate_float')
    current_date = json_current.get('time').get('updatedISO')[:10]
    dict_bpi[current_date] = current_price

    series_daily = pd.Series(dict_bpi)
    df_btc_daily = series_daily.reset_index()
    df_btc_daily.set_axis(['Date', 'Open'], axis=1, inplace=True)

    df_btc_daily['200MaOpen'] = df_btc_daily['Open'].rolling(window=200).mean()
    df_btc_daily['Mayer'] = df_btc_daily['Open'] / df_btc_daily['200MaOpen']

    mayer_mean = df_btc_daily['Mayer'].mean()
    mayer_today = df_btc_daily.dropna().loc[len(df_btc_daily) - 1, 'Mayer']
    mayer_percent = (df_btc_daily.loc[:, 'Mayer'].dropna() > mayer_today).sum() / len(
        df_btc_daily.loc[:, 'Mayer'].dropna()) * 100

    st.write(plot_current_multiple(df_btc_daily))

    st.write('Today, the 200 days moving average is **${}** and the btc price is **${}**'
             .format(round(df_btc_daily.dropna().loc[len(df_btc_daily) - 1, '200MaOpen'], 1),
                     round(df_btc_daily.dropna().loc[len(df_btc_daily) - 1, 'Open']), 1))

    st.write('Today, the mayer multiple is **{}**, the average multiple is _{}_, the multiple has been '
             'higher **{}**% of the time'.format(mayer_today.round(2), mayer_mean.round(2), mayer_percent.round(2)))
