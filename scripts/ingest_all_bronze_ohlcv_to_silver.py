from __future__ import annotations

import re
from pathlib import Path

from tyche.data.ingest.ingest_spot_csv import ingest_spot_csv_to_parquet, IngestSpec

BRONZE_DIR = Path("data/bronze")
SILVER_ROOT = Path("data/silver/bars")

# Matches:
#   spot_ohlcv_1d__cryptoquant_agg__BTCUSD.csv
#   perp_ohlcv_1d__cryptoquant_agg__BTCUSD.csv
PATTERN = re.compile(
    r"^(?P<market_type>spot|perp)_ohlcv_1d__cryptoquant_agg__(?P<symbol>.+)\.csv$"
)


def main() -> None:
    csv_files = sorted([p for p in BRONZE_DIR.glob("*.csv") if PATTERN.match(p.name)])
    if not csv_files:
        raise SystemExit(
            f"No matching CSV files found in {BRONZE_DIR}. "
            f"Expected names like spot_ohlcv_1d__cryptoquant_agg__BTCUSD.csv or perp_ohlcv_1d__cryptoquant_agg__BTCUSD.csv"
        )

    ok, failed = 0, 0

    for csv_path in csv_files:
        m = PATTERN.match(csv_path.name)
        assert m is not None

        market_type = m.group("market_type")  # "spot" or "perp"
        symbol = m.group("symbol")

        spec = IngestSpec(
            exchange="cryptoquant_agg",
            market_type=market_type,
            timeframe="1d",
            quote_ccy="USD",  # adjust to USDT if needed
        )

        out_path = (
            SILVER_ROOT
            / f"exchange={spec.exchange}"
            / f"market_type={spec.market_type}"
            / f"timeframe={spec.timeframe}"
            / f"symbol={symbol}"
            / "part-000.parquet"
        )

        try:
            ingest_spot_csv_to_parquet(
                csv_path=csv_path,
                out_parquet_path=out_path,
                symbol=symbol,
                spec=spec,
                strict_continuity=False,
                strict_ohlc=False,  # your VWAP-like OHLC can violate containment
            )
            ok += 1
            print(f"[OK] {csv_path.name} -> {out_path.as_posix()}")
        except Exception as e:
            failed += 1
            print(f"[FAIL] {csv_path.name}: {e}")

    print(f"\nDone. OK={ok}, FAIL={failed}, total={ok+failed}")


if __name__ == "__main__":
    main()
