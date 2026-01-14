from __future__ import annotations

from dataclasses import dataclass
import pandas as pd


@dataclass(frozen=True)
class ConstantWeightStrategy:
    """
    Constant target weights for a single asset.

    weight:
      +1.0 = +100% notional long
      -2.0 = -200% notional short, etc.
    """
    symbol: str
    weight: float = 1.0

    def generate_weights(self, prices: pd.DataFrame) -> pd.DataFrame:
        """
        prices: wide price matrix (index=timestamps, columns=symbols)
        returns: wide weights matrix aligned to prices
        """
        if self.symbol not in prices.columns:
            raise ValueError(
                f"Symbol '{self.symbol}' not found in prices columns: {list(prices.columns)}"
            )

        w = pd.DataFrame(0.0, index=prices.index, columns=prices.columns, dtype="float64")
        w[self.symbol] = float(self.weight)
        return w
