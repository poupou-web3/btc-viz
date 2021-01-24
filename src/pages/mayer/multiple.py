import streamlit as st

from src.plot.plotly import plot_current_multiple
from src.prep.csv.loading import get_btc_daily


def page_mayer_multiple():
    st.header('Mayer multiple')

    st.write('The mayer multiple has been first used by Trace Mayer, it is the multiple between the 200 days moving '
             'average of bitcoin price and the current price. Trace Mayer evaluated that the best returns was '
             'obtained by accumulating bitcoins when the multiple is below 2.4. However, that simulation depends on '
             'the data used. Here we present the mayer multiple calculated with data starting on the 2013-10-01. ')

    df_btc_daily = get_btc_daily()

    mayer_mean = df_btc_daily['Mayer'].mean()
    mayer_today = df_btc_daily.loc[len(df_btc_daily) - 1, 'Mayer']
    mayer_percent = (df_btc_daily.loc[:, 'Mayer'] > mayer_today).sum() / len(
        df_btc_daily.loc[:, 'Mayer']) * 100

    st.write(plot_current_multiple(df_btc_daily))

    st.write('Today, the 200 days moving average is **${}** and the btc price is **${}**'
             .format(round(df_btc_daily.dropna().loc[len(df_btc_daily) - 1, '200MaOpen'], 1),
                     round(df_btc_daily.dropna().loc[len(df_btc_daily) - 1, 'Open']), 1))

    st.write('Today, the mayer multiple is **{}**, the average multiple is _{}_, the multiple has been '
             'higher **{}**% of the time'.format(mayer_today.round(2), mayer_mean.round(2), mayer_percent.round(2)))
