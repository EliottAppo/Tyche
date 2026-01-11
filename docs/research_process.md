# Research process (high-level)

The intent is to move from exploration to production in controlled steps:

1. Explore ideas in notebooks (`research/notebooks/`) with clear hypotheses.
2. Convert promising ideas into reproducible experiments (`research/experiments/`).
3. Promote stable, reusable components into production:
   - transforms / factors into `src/tyche/features/`
   - strategy logic into `src/tyche/strategies/`
   - evaluation utilities into `src/tyche/backtest/` or `src/tyche/research/` (as appropriate)
4. Enforce interfaces and contracts once promoted.
