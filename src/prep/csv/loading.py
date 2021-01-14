import pandas as pd
import streamlit as st


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
