# -*- coding: utf-8 -*-
"""
@author: btc-viz
"""

# %% import packages
import streamlit as st

from src.pages.mayer.historical import page_mayer_historical
from src.pages.mayer.multiple import page_mayer_multiple
from src.pages.mayer.simulation import page_simulation

PAGES = ['Mayer Multiple', 'Simulation', 'Historical comparison']


def main():
    # %% the GUI
    st.title('Bitcoin visualization')

    page = st.sidebar.selectbox(label="Page",
                                options=PAGES)

    if page == 'Mayer Multiple':
        page_mayer_multiple()
    elif page == 'Simulation':
        page_simulation()
    else:
        page_mayer_historical()
    st.info(
        """ By: [Poupou](https://github.com/poupou-web3) | 
        Code Source: [GitHub](https://github.com/poupou-web3/btc-viz) |
        Data Powered by [CoinDesk](https://www.coindesk.com/price/bitcoin)"""
    )


if __name__ == "__main__":
    main()
