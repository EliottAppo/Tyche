import pandas as pd

from tyche.backtest.engine import backtest_engine


def test_single_asset_compounds_with_lag_fill():
    idx = pd.to_datetime(["2020-01-01", "2020-01-02", "2020-01-03"])
    prices = pd.DataFrame({"BTC": [100.0, 110.0, 121.0]}, index=idx)
    weights = pd.DataFrame({"BTC": [1.0, 1.0, 1.0]}, index=idx)

    res = backtest_engine(prices, weights, nan_policy="fill", weight_lag=1, initial_equity=100.0)

    assert float(res.equity.iloc[0]) == 100.0
    assert abs(float(res.equity.iloc[-1]) - 121.0) < 1e-12


def test_drop_policy_drops_first_row_due_to_lag():
    idx = pd.to_datetime(["2020-01-01", "2020-01-02", "2020-01-03"])
    prices = pd.DataFrame({"BTC": [100.0, 110.0, 121.0]}, index=idx)
    weights = pd.DataFrame({"BTC": [1.0, 1.0, 1.0]}, index=idx)

    res = backtest_engine(prices, weights, nan_policy="drop", weight_lag=1, initial_equity=100.0)

    assert len(res.equity) == 2
    assert abs(float(res.equity.iloc[-1]) - 121.0) < 1e-12


def test_gross_leverage_limit_raises():
    idx = pd.to_datetime(["2020-01-01", "2020-01-02", "2020-01-03"])
    prices = pd.DataFrame({"A": [100.0, 100.0, 100.0], "B": [100.0, 100.0, 100.0]}, index=idx)
    weights = pd.DataFrame({"A": [2.0, 2.0, 2.0], "B": [1.0, 1.0, 1.0]}, index=idx)

    try:
        backtest_engine(
            prices,
            weights,
            nan_policy="fill",
            weight_lag=1,
            enforce_gross_leverage_max=2.0,
        )
        assert False, "Expected ValueError"
    except ValueError:
        assert True
