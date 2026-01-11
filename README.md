# Tyche

Tyche is a crypto trading research project.  
The goal is to build a modular, reproducible platform to research alpha, develop factor models (Barra-like adapted to crypto), and evaluate strategies via a strategy-agnostic backtesting engine.

This repository is intentionally structured to separate:
- **Alpha research** (fast iteration, notebooks, experiments)
- **Data** (ingestion, normalization, storage)
- **Features / factors** (standardized computation pipelines)
- **Strategies** (plug-in implementations consuming features and producing targets)
- **Backtesting** (engine + costs + metrics + reporting)
- **Execution** (simulation now; live adapters later)

## Principles

- **Separation of concerns**: each layer has a single responsibility.
- **Reproducibility**: runs are configuration-driven and versioned.
- **Modularity**: swap data sources, strategies, and cost models without refactoring the whole system.
- **Strategy-agnostic backtesting**: the engine does not embed alpha logic.
- **Extensibility**: a clean path toward live execution (later) without contaminating research/backtest layers.

## Repository layout (high-level)

### Production code (`src/tyche/`)
- `core/`: shared contracts, interfaces, configuration, logging, utilities
- `data/`: ingestion, normalization, storage, dataset builders
- `features/`: transforms, factor library, feature pipelines
- `universe/`: eligibility rules and universe construction
- `strategies/`: plug-in strategy implementations (baseline, factor models, overlays)
- `portfolio/`: portfolio construction and constraints
- `backtest/`: engine, cost models, metrics, reporting
- `execution/`: simulation (now) and live adapters (later)

### Research area (`research/`)
- `notebooks/`: exploratory analysis and prototyping
- `experiments/`: reproducible experiment scripts
- `reports/`: generated outputs (tables, plots, tear sheets)

### Run scaffolding
- `configs/`: versioned configuration files (data/backtest/strategy)
- `scripts/`: simple entrypoints (download data, build features, run backtests)
- `docs/`: architecture and decisions (ADRs)
- `tests/`: unit and integration tests

## Getting started

### Requirements
- Python 3.11+

