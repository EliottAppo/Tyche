# ADR 0001 – Repository structure

## Status
Accepted

## Context
Tyche needs a structure that separates alpha research from production code,
while enabling reproducible backtests and future live execution.

## Decision
Use a layered architecture with:
- `research/` for exploratory work (non-prod)
- `src/tyche/` for production code split into core/data/features/strategies/backtest/execution
- `configs/` for versioned run configurations
- `scripts/` for stable entrypoints

## Consequences
- Research iteration stays fast without destabilizing production layers.
- Backtesting remains strategy-agnostic and testable.
- Live execution can be added via adapters.
