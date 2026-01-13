from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Sequence, Tuple

import matplotlib.pyplot as plt
import pandas as pd

from tyche.backtest.engine.types import BacktestResult


@dataclass(frozen=True)
class PlotConfig:
    equity_title: str = "Equity Curve"
    weights_title: str = "Weights (used)"
    figsize_equity: Tuple[float, float] = (10.0, 4.0)
    figsize_weights: Tuple[float, float] = (10.0, 6.0)
    max_assets: int = 25
    top_by: str = "avg_abs_weight"  # or "avg_weight"


def plot_equity(
    result: BacktestResult,
    *,
    ax: Optional[plt.Axes] = None,
    title: Optional[str] = None,
    show: bool = True,
) -> plt.Axes:
    if ax is None:
        _, ax = plt.subplots(figsize=(10, 4))

    series = result.equity.dropna()
    ax.plot(series.index, series.values)
    ax.set_title(title or "Equity Curve")
    ax.set_xlabel("Date")
    ax.set_ylabel("Equity")
    ax.grid(True, linewidth=0.5)

    if show:
        plt.show()

    return ax


def plot_weights(
    result: BacktestResult,
    *,
    ax: Optional[plt.Axes] = None,
    assets: Optional[Sequence[str]] = None,
    config: PlotConfig = PlotConfig(),
    kind: str = "heatmap",  # "heatmap" or "area"
    show: bool = True,
) -> plt.Axes:
    w = result.weights_used.copy()

    if assets is None:
        w = _select_assets(w, max_assets=config.max_assets, top_by=config.top_by)
    else:
        missing = [a for a in assets if a not in w.columns]
        if missing:
            raise ValueError(f"Unknown assets in weights_used: {missing}")
        w = w.loc[:, list(assets)]

    if ax is None:
        _, ax = plt.subplots(figsize=config.figsize_weights)

    if kind == "heatmap":
        _plot_weights_heatmap(w, ax=ax, title=config.weights_title)
    elif kind == "area":
        _plot_weights_area(w, ax=ax, title=config.weights_title)
    else:
        raise ValueError("kind must be one of {'heatmap', 'area'}")

    if show:
        plt.show()

    return ax


def _select_assets(w: pd.DataFrame, *, max_assets: int, top_by: str) -> pd.DataFrame:
    if w.empty:
        return w

    if top_by == "avg_abs_weight":
        score = w.abs().mean(axis=0)
    elif top_by == "avg_weight":
        score = w.mean(axis=0).abs()
    else:
        raise ValueError("top_by must be one of {'avg_abs_weight', 'avg_weight'}")

    cols = score.sort_values(ascending=False).head(int(max_assets)).index
    return w.loc[:, cols]


def _plot_weights_heatmap(w: pd.DataFrame, *, ax: plt.Axes, title: str) -> None:
    data = w.T.values
    im = ax.imshow(data, aspect="auto", interpolation="nearest")

    ax.set_title(title)
    ax.set_xlabel("Time")
    ax.set_ylabel("Asset")

    ax.set_yticks(range(w.shape[1]))
    ax.set_yticklabels(list(w.columns))

    step = max(1, len(w.index) // 8)
    xticks = list(range(0, len(w.index), step))
    ax.set_xticks(xticks)
    ax.set_xticklabels([w.index[i].strftime("%Y-%m-%d") for i in xticks], rotation=30, ha="right")

    plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)


def _plot_weights_area(w: pd.DataFrame, *, ax: plt.Axes, title: str) -> None:
    w.plot.area(ax=ax, stacked=False)
    ax.set_title(title)
    ax.set_xlabel("Date")
    ax.set_ylabel("Weight")
    ax.grid(True, linewidth=0.5)

