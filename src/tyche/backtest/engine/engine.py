from __future__ import annotations

from dataclasses import asdict
from typing import Dict, Iterable, Literal, Optional, Tuple

import numpy as np
import pandas as pd

from .types import BacktestResult

NanPolicy = Literal["drop", "fill", "raise"]


def backtest_engine(
    prices: pd.DataFrame,
    weights: pd.DataFrame,
    *,
    initial_equity: float = 100.0,
    weight_lag: int = 1,
    nan_policy: NanPolicy = "drop",
    price_fill_method: Literal["ffill", "bfill"] = "ffill",
    enforce_gross_leverage_max: Optional[float] = None,
) -> BacktestResult:
    _validate_inputs(prices=prices, weights=weights, initial_equity=initial_equity, weight_lag=weight_lag)

    px, w = _align(prices, weights)

    if nan_policy == "fill":
        px = _fill_prices(px, method=price_fill_method)
        w = w.fillna(0.0)
    elif nan_policy == "raise":
        _raise_on_nans(px, w)

    asset_ret = px.pct_change()

    w_used = w.shift(weight_lag)

    if nan_policy == "fill":
        w_used = w_used.fillna(0.0)
    elif nan_policy == "raise":
        _raise_on_nans(asset_ret, w_used)

    if enforce_gross_leverage_max is not None:
        _enforce_gross_leverage(w_used, enforce_gross_leverage_max)

    if nan_policy == "drop":
        mask = asset_ret.notna().all(axis=1) & w_used.notna().all(axis=1)
        asset_ret = asset_ret.loc[mask]
        w_used = w_used.loc[mask]

    gross_exposure = w_used.abs().sum(axis=1).rename("gross_exposure")
    net_exposure = w_used.sum(axis=1).rename("net_exposure")

    turnover = (0.5 * (w_used.diff().abs().sum(axis=1))).rename("turnover")
    turnover.iloc[0] = 0.0

    strat_ret = (w_used * asset_ret).sum(axis=1)
    equity = (1.0 + strat_ret).cumprod() * float(initial_equity)

    metadata: Dict[str, object] = {
        "initial_equity": float(initial_equity),
        "weight_lag": int(weight_lag),
        "nan_policy": str(nan_policy),
        "price_fill_method": str(price_fill_method),
        "enforce_gross_leverage_max": enforce_gross_leverage_max,
        "n_assets": int(len(asset_ret.columns)),
        "start": asset_ret.index.min(),
        "end": asset_ret.index.max(),
    }

    return BacktestResult(
        equity=equity.rename("equity"),
        returns=strat_ret.rename("returns"),
        weights_used=w_used,
        asset_returns=asset_ret,
        gross_exposure=gross_exposure,
        net_exposure=net_exposure,
        turnover=turnover,
        metadata=metadata,
    )



def _validate_inputs(*, prices: pd.DataFrame, weights: pd.DataFrame, initial_equity: float, weight_lag: int) -> None:
    if not isinstance(prices, pd.DataFrame) or not isinstance(weights, pd.DataFrame):
        raise TypeError("prices and weights must be pandas DataFrames.")

    if prices.empty or weights.empty:
        raise ValueError("prices and weights must be non-empty.")

    if not prices.index.is_monotonic_increasing:
        prices.sort_index(inplace=True)
    if not weights.index.is_monotonic_increasing:
        weights.sort_index(inplace=True)

    if prices.index.has_duplicates or weights.index.has_duplicates:
        raise ValueError("prices/weights index must not contain duplicates.")

    if initial_equity <= 0:
        raise ValueError("initial_equity must be > 0.")

    if weight_lag < 0:
        raise ValueError("weight_lag must be >= 0.")


def _align(prices: pd.DataFrame, weights: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
    common_cols = prices.columns.intersection(weights.columns)
    if len(common_cols) == 0:
        raise ValueError("prices and weights must share at least one common column (asset).")

    px = prices.loc[:, common_cols].copy()
    w = weights.loc[:, common_cols].copy()

    common_idx = px.index.intersection(w.index)
    if len(common_idx) < 2:
        raise ValueError("Need at least 2 common dates between prices and weights to compute returns.")

    return px.loc[common_idx], w.loc[common_idx]


def _fill_prices(prices: pd.DataFrame, *, method: Literal["ffill", "bfill"]) -> pd.DataFrame:
    if method == "ffill":
        return prices.ffill()
    return prices.bfill()


def _raise_on_nans(a: pd.DataFrame, b: pd.DataFrame) -> None:
    if a.isna().any().any():
        raise ValueError("NaNs detected in prices/returns under nan_policy='raise'.")
    if b.isna().any().any():
        raise ValueError("NaNs detected in weights under nan_policy='raise'.")


def _enforce_gross_leverage(weights_used: pd.DataFrame, gross_max: float) -> None:
    if gross_max <= 0:
        raise ValueError("enforce_gross_leverage_max must be > 0.")

    gross = weights_used.abs().sum(axis=1)
    if (gross > gross_max + 1e-12).any():
        first = gross[gross > gross_max].index[0]
        raise ValueError(f"Gross leverage exceeds limit on {first.date()}: {gross.loc[first]:.6f} > {gross_max:.6f}")
