from pathlib import Path
import pandas as pd

from tyche.data.store.silver import load_silver_bars, bars_to_price_matrix
from tyche.strategies.baseline.constant_weight import ConstantWeightStrategy
from tyche.backtest.run import run_backtest_from_silver
from tyche.backtest.reporting.visualizer import plot_equity, plot_weights


if __name__ == "__main__":
    silver_path = Path(
        "data/silver/bars/"
        "exchange=cryptoquant_agg/market_type=spot/timeframe=1d/symbol=BTCUSD/"
        "part-000.parquet"
    )

    # Load prices to build weights aligned to the exact index/columns
    bars = load_silver_bars(silver_path)
    prices = bars_to_price_matrix(bars, field="close")

    strat = ConstantWeightStrategy(symbol="BTCUSD", weight=1.0)
    weights = strat.generate_weights(prices)

    res = run_backtest_from_silver(
        silver_paths=silver_path,
        weights=weights,
        initial_equity=100.0,
        weight_lag=1,
        nan_policy="drop",
        enforce_gross_leverage_max=2.0,
    )

    exposures = pd.concat([res.gross_exposure, res.net_exposure], axis=1)

    print("\nEquity (tail):")
    print(res.equity.tail())

    print("\nExposure describe:")
    print(exposures.describe())

    print("\nTurnover (tail):")
    print(res.turnover.tail())

    plot_equity(res, title="Equity — Constant 100% Long BTCUSD", show=True)
    plot_weights(res, assets=["BTCUSD"], kind="area", show=True)
