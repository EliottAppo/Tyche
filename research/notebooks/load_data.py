import pandas as pd
import numpy as np
from support_research import *


def load_data():
    bitcoin_data = pd.read_csv('../../data/bronze/spot_ohlcv_1d__cryptoquant_agg__BTCUSD.csv')[::-1].reset_index(drop=True)
    eth_data = pd.read_csv('../../data/bronze/spot_ohlcv_1d__cryptoquant_agg__ETHUSD.csv')[::-1].reset_index(drop=True)
    xrp_data = pd.read_csv('../../data/bronze/spot_ohlcv_1d__cryptoquant_agg__XRPUSD.csv')[::-1].reset_index(drop=True)
    bitcoin_data['return'] = bitcoin_data['Close'].pct_change()
    eth_data['return'] = eth_data['Close'].pct_change()
    xrp_data['return'] = xrp_data['Close'].pct_change()
    return bitcoin_data, eth_data, xrp_data


def construct_targets(data, horizon=1):
    data['return_horizon_for_target'] = data['Close'].pct_change(horizon)
    data['target'] = data['return_horizon_for_target'].shift(-horizon)
    return data

def construct_signals(data, window=10, horizon=1, k=20, n=10):
    data['signal'] = data['return'].rolling(window=1000).apply(lambda x: applicate_mean(x, window=window, horizon=horizon, k=k, n=n))
    data['signal_std'] = data['return'].rolling(window=1000).apply(lambda x: applicate_std(x, window=window, horizon=horizon, k=k, n=n))
    data['filter'] = np.where(abs(data['signal'] / data['signal_std']) > 0.1, 1, np.nan)
    data['filtered_signal'] = data['signal'] * data['filter']
    return data