import numpy as np
import pandas as pd

from tyche.backtest.engine import backtest_engine
from tyche.backtest.reporting import PlotConfig, plot_equity, plot_weights


def _make_synthetic_prices(
    dates: pd.DatetimeIndex,
    assets: list[str],
    *,
    seed: int = 7,
    vol_daily: float = 0.03,
) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    n, m = len(dates), len(assets)

    rets = rng.normal(loc=0.0, scale=vol_daily, size=(n, m))
    prices = 100.0 * np.exp(np.cumsum(rets, axis=0))

    return pd.DataFrame(prices, index=dates, columns=assets)


def _make_synthetic_weights(
    dates: pd.DatetimeIndex,
    assets: list[str],
    *,
    seed: int = 11,
    gross_target: float = 1.0,
    rebalance_every_days: int = 7,
) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    n, m = len(dates), len(assets)

    w = np.zeros((n, m), dtype=float)

    for t in range(0, n, rebalance_every_days):
        raw = rng.normal(size=m)
        raw = raw - raw.mean()
        if np.allclose(raw, 0.0):
            raw[0] = 1.0

        scaled = raw / np.sum(np.abs(raw)) * gross_target
        w[t, :] = scaled

    w = pd.DataFrame(w, index=dates, columns=assets)
    w = w.ffill()

    return w


def main() -> None:
    dates = pd.date_range("2022-01-01", periods=180, freq="D")
    assets = ["BTC", "ETH", "SOL", "BNB", "XRP", "ADA", "DOGE", "AVAX"]

    prices = _make_synthetic_prices(dates, assets, seed=7, vol_daily=0.03)
    weights = _make_synthetic_weights(dates, assets, seed=11, gross_target=1.5, rebalance_every_days=7)

    res = backtest_engine(prices, weights, nan_policy="fill", weight_lag=1, initial_equity=100.0)

    plot_equity(res)
    plot_weights(res, kind="heatmap")
    plot_weights(res, kind="area", config=PlotConfig(max_assets=6))


if __name__ == "__main__":
    main()
