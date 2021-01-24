import numpy as np
import streamlit as st

from src.plot.plotly import plot_simulation
from src.prep.csv.loading import get_btc_daily


def page_simulation():
    st.header('Mayer multiple Simulation')

    st.write('We run the Mayer simulation, ie. we suppose we buy $1 of bitcoin each day the Mayer multiple is below a '
             'certain threshold and compute the number of accumulated bitcoin. '
             'The standard simulation is using prices between 2012 and today. You can play with these dates. You will '
             'be able to see that 2.4 is a stable value for large periods and smaller values should be selected after '
             'a bull run.')

    df_btc_daily = get_btc_daily()

    df_btc_daily['btc_bought'] = 1/df_btc_daily['Open']

    start_date = st.date_input('Start date', df_btc_daily.loc[0, 'Date'])
    end_date = st.date_input('End date', df_btc_daily.loc[len(df_btc_daily)-1, 'Date'])

    df_btc = df_btc_daily.loc[np.logical_and(np.datetime64(start_date) <= df_btc_daily['Date'],
                                             df_btc_daily['Date'] <= np.datetime64(end_date))]
    
    btc_quantity = []
    mayer_values = np.linspace(0.4, 4, int((4 - 0.4) / 0.1 + 1))
    for multiple_value in mayer_values:
        btc_quantity.append(df_btc.loc[df_btc['Mayer'] < multiple_value, 'btc_bought'].sum())

    fig_simulation = plot_simulation(mayer_values, btc_quantity)
    st.write(fig_simulation)

