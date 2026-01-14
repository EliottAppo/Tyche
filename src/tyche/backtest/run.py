from __future__ import annotations

from pathlib import Path
from typing import Iterable, Optional, Union

import pandas as pd

from tyche.backtest.engine.engine import backtest_engine
from tyche.backtest.engine.types import BacktestResult
from tyche.data.store.silver import load_silver_bars, bars_to_price_matrix

PathLike = Union[str, Path]


def run_backtest_from_silver(
    *,
    silver_paths: PathLike | Iterable[PathLike],
    weights: pd.DataFrame,
    price_field: str = "close",
    initial_equity: float = 100.0,
    weight_lag: int = 1,
    nan_policy: str = "drop",
    price_fill_method: str = "ffill",
    enforce_gross_leverage_max: Optional[float] = None,
) -> BacktestResult:
    """
    Convenience wrapper: load prices from silver parquet and run the pure engine.

    Requirements:
      - silver bars contain [timestamp, symbol, <price_field>]
      - weights is a wide DataFrame with same convention as engine:
            index=timestamp, columns=symbol, values=weights
    """
    bars = load_silver_bars(silver_paths)
    prices = bars_to_price_matrix(bars, field=price_field)

    return backtest_engine(
        prices=prices,
        weights=weights,
        initial_equity=initial_equity,
        weight_lag=weight_lag,
        nan_policy=nan_policy,  # typing: your engine uses NanPolicy Literal; runtime is fine
        price_fill_method=price_fill_method,
        enforce_gross_leverage_max=enforce_gross_leverage_max,
    )
