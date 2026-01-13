from __future__ import annotations

from dataclasses import dataclass
from typing import Dict

import pandas as pd


@dataclass(frozen=True)
class BacktestResult:
    equity: pd.Series
    returns: pd.Series
    weights_used: pd.DataFrame
    asset_returns: pd.DataFrame
    gross_exposure: pd.Series
    net_exposure: pd.Series
    turnover: pd.Series
    metadata: Dict[str, object]

    def to_frame(self) -> pd.DataFrame:
        return pd.DataFrame(
            {
                "equity": self.equity,
                "returns": self.returns,
                "gross_exposure": self.gross_exposure,
                "net_exposure": self.net_exposure,
                "turnover": self.turnover,
            }
        )
