# Tyche

Tyche is a crypto trading research and simulation project structured to separate:
- Alpha research (exploration and experiments)
- Data ingestion and normalization
- Feature / factor pipelines
- Strategy implementations (plug-in)
- Backtesting (strategy-agnostic engine)
- Execution (simulation now, live adapters later)

## Repository structure (high-level)
- `src/tyche/`: production-quality code (stable, testable)
- `research/`: notebooks/experiments/reports (exploration; non-prod)
- `configs/`: versioned configurations for reproducible runs
- `scripts/`: simple entrypoints to run pipelines and backtests
- `docs/`: architecture notes and decisions (ADRs)
- `tests/`: unit/integration tests

## Getting started
1. Create and activate a virtual environment.
2. Install dependencies:
   ```bash
   pip install -e ".[dev]"
   ```
3. Run a minimal check:
   ```bash
   python -c "import tyche; print('tyche ok')"
   ```

## Notes
This repository is intended to evolve toward spot + perps support with controlled leverage and
scheduled rebalancing (weekly by default), while remaining modular and reproducible.
