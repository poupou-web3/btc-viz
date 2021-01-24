import datetime

import pandas as pd
import requests
import streamlit as st

COINDESK_HISTORICAL_URL = 'https://api.coindesk.com/v1/bpi/historical/open.json'
COINDESK_CURRENT_URL = 'https://api.coindesk.com/v1/bpi/currentprice.json'


@st.cache()
def load_historical_data():
    df_btc_daily = pd.read_csv('Data/BTC_USD_2010-07-18_Investing.csv')
    df_btc_daily.set_axis(['Date', 'Price', 'Open', 'High', 'Low', 'Volume', 'Change'], axis=1, inplace=True)

    df_btc_daily['Date'] = pd.to_datetime(df_btc_daily['Date'])
    df_btc_daily['Price'] = df_btc_daily['Price'].str.replace(',', '').astype(float)
    df_btc_daily['Open'] = df_btc_daily['Open'].str.replace(',', '').astype(float)
    df_btc_daily['High'] = df_btc_daily['High'].str.replace(',', '').astype(float)
    df_btc_daily['Low'] = df_btc_daily['Low'].str.replace(',', '').astype(float)

    df_btc_daily = df_btc_daily.iloc[::-1]

    return df_btc_daily


def load_coindesk_data():
    today = datetime.date.today()

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
    df_btc_daily['Date'] = pd.to_datetime(df_btc_daily['Date'])

    return df_btc_daily


def get_btc_daily():
    # load historical data not available on Coindesk
    df_btc_history = load_historical_data()
    df_btc_history = df_btc_history[['Date', 'Open']]

    df_btc_daily = load_coindesk_data()

    df_missing_history = df_btc_history.loc[df_btc_history['Date'] < df_btc_daily.loc[0, 'Date']]
    df_btc_daily = df_missing_history.append(df_btc_daily)

    # remove values before January 2012
    df_btc_daily = df_btc_daily.loc[df_btc_daily['Date'] >= datetime.datetime.strptime('2012/01/01', "%Y/%m/%d")]

    df_btc_daily['200MaOpen'] = df_btc_daily['Open'].rolling(window=200).mean()
    df_btc_daily['Mayer'] = df_btc_daily['Open'] / df_btc_daily['200MaOpen']
    df_btc_daily.dropna(inplace=True)
    df_btc_daily.reset_index(drop=True, inplace=True)

    return df_btc_daily
