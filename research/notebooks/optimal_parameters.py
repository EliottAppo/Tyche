import numpy as np
import pandas as pd
from support_research import *
from load_data import construct_targets, construct_signals

param_grid = {
    "window": [6, 8, 10, 12, 15],
    "horizon": [1, 3, 5],
    "k": [10, 15, 20, 30],
    "n": [10, 15, 20, 30],
    "threshold": [0.05, 0.1, 0.15, 0.2]
}



def signal_target_correlation(df):
    df = df[['filtered_signal', 'target']].dropna()
    if len(df) < 30:
        return np.nan
    return np.corrcoef(df['filtered_signal'], df['target'])[0, 1]


def evaluate_params(
    data,
    window,
    horizon,
    k,
    n,
    threshold
):
    df = data.copy()

    df = construct_targets(df, horizon=horizon)

    df['signal'] = df['return'].rolling(window=1000).apply(
        lambda x: applicate_mean(x, window=window, horizon=horizon, k=k, n=n),
        raw=False
    )

    df['signal_std'] = df['return'].rolling(window=1000).apply(
        lambda x: applicate_std(x, window=window, horizon=horizon, k=k, n=n),
        raw=False
    )

    df['filter'] = np.where(
        np.abs(df['signal'] / df['signal_std']) > threshold,
        1,
        np.nan
    )

    df['filtered_signal'] = df['signal'] * df['filter']

    return signal_target_correlation(df)

def evaluate_params_wrapper(bitcoin_data, param_grid=param_grid):
    results = []

    for window in param_grid['window']:
        for horizon in param_grid['horizon']:
            for k in param_grid['k']:
                for n in param_grid['n']:
                    for threshold in param_grid['threshold']:

                        corr = evaluate_params(
                            bitcoin_data,
                            window=window,
                            horizon=horizon,
                            k=k,
                            n=n,
                            threshold=threshold
                        )

                        results.append({
                            "window": window,
                            "horizon": horizon,
                            "k": k,
                            "n": n,
                            "threshold": threshold,
                            "correlation": corr
                        })
    return results

