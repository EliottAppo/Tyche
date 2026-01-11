# Tyche – Global Architecture

This document describes the global architecture of Tyche at a high level.

## Design goals
1. **Separation of concerns**: research, data, features, strategies, and backtesting are distinct layers.
2. **Reproducibility**: each run should be driven by versioned configuration and produce traceable outputs.
3. **Modularity**: swap data sources, storage, factors, strategies, and cost models without refactoring the system.
4. **Strategy-agnostic backtesting**: the engine does not embed alpha logic.
5. **Extensibility**: a path to live execution via adapters, without contaminating research/backtest layers.

## Layered model
- **Research** (`/research`): exploration, notebooks, experiments, reports (non-production).
- **Production platform** (`/src/tyche`):
  - `core`: domain types, contracts, interfaces, config, logging.
  - `data`: ingest + normalize + store + dataset builders.
  - `features`: feature/factor computation and pipelines.
  - `universe`: eligibility rules and universe construction.
  - `strategies`: plug-in strategies (factor models, baselines).
  - `portfolio`: portfolio construction and constraints.
  - `backtest`: strategy-agnostic engine, costs, metrics, reporting.
  - `execution`: simulator now; live adapters later.

## Dependency rules (strict)
- `research/` may import from `src/tyche`, but production code **must not** import from `research/`.
- `strategies/` may depend on `core/`, `features/`, `universe/`, `portfolio/`.
- `backtest/` depends on `core/` and calls strategies via interfaces; it should not depend on strategy internals.
- `data/` produces standardized datasets; it must not contain strategy-specific logic.

## Contracts
- **Data contracts** define canonical schemas for market data (e.g., OHLCV), derivatives data (e.g., funding),
  and metadata (symbols, calendars).
- **Feature contracts** define a standard representation for time-indexed features (date × asset).
- **Strategy contract** defines how a strategy produces targets/orders from data and features.

## Configuration
All runs should be driven by configuration in `/configs`:
- data sources / universe rules
- feature pipeline selection
- strategy selection + parameters
- backtest parameters + cost models
