# Tyche

Tyche is a modular quantitative research and simulation codebase.  
The repository is organized to clearly separate exploration work from production-quality components, and to support reproducible runs driven by versioned configuration.

## Repository layout

### 1) Production code (`src/tyche/`)
This is the stable, testable code that can be reused across experiments.

- `core/`  
  Shared foundations: contracts (schemas/conventions), interfaces, configuration helpers, logging, and utilities.

- `data/`  
  Data acquisition/normalization/storage and dataset builders (i.e., producing standardized, ready-to-consume datasets).

- `features/`  
  Feature engineering and factor computation pipelines:
  transforms (primitives), factor library, and orchestration.

- `universe/`  
  Eligibility rules and universe construction (what is included/excluded over time).

- `strategies/`  
  Plug-in implementations that turn inputs (datasets + features) into targets/decisions.
  Includes `baseline/` and more advanced model families.

- `portfolio/`  
  Portfolio construction and constraints (how targets are translated into allocations under rules).

- `backtest/`  
  Strategy-agnostic simulation engine plus costs, metrics, and reporting.

- `execution/`  
  Execution layer:
  simulation components now; adapters for external execution later.

- `reporting/`  
  Shared reporting utilities used across modules.

### 2) Research area (`research/`)
This is the exploration workspace. It can move fast without destabilizing production code.

- `notebooks/` — exploratory analysis and prototyping
- `experiments/` — reproducible experiment scripts
- `reports/` — generated outputs (tables/plots/tear sheets)

**Rule of thumb:** notebooks explore; production code lives in `src/tyche/`.

### 3) Run scaffolding
- `configs/`  
  Versioned configuration files for reproducible runs (data, simulation, strategy parameters).

- `scripts/`  
  Simple entrypoints that orchestrate runs (download/build/run), driven by `configs/`.

- `docs/`  
  Architecture notes and ADRs (Architecture Decision Records) to document key choices.

- `tests/`  
  Unit and integration tests.
