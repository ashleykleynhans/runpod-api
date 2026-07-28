# Changelog

## [0.1.0] - 2026-07-28

- Renamed `runpod` module to `rpapi` package to avoid conflicts with the official Runpod Python module
- Converted from flat script with symlinks to a proper installable Python package (`rpapi/__init__.py`)
- Added `pyproject.toml` with `pip install -e .` support
- Removed all `runpod.py` symlinks from subdirectories
- Added `sys.path` fixup to subdirectory scripts for development use without installation
- Improved `get_referral_earned.py` with Rich formatting: panels, tables, and referral stats
- Fixed `get_referral_earned.py` to handle partial GraphQL errors gracefully
- Switched core API from GraphQL to REST v2 (`https://api.runpod.io/v2`) with Bearer token auth
- Rewrote `rpapi/__init__.py`: `Client` base class, `API` (pods/templates/catalog/volumes), `Serverless` (endpoints), `Endpoints` (dreambooth)
- Kept `get_myself()` as GraphQL fallback (no REST v2 equivalent for account/referral data)
- Updated all scripts for new response format (flat JSON instead of GraphQL `data.*` nesting)
- Converted pod create/start/stop/terminate from GraphQL mutations to REST v2 endpoints
- Converted serverless endpoint management from GraphQL mutations to REST v2 PATCH endpoints
- Template creation scripts now use structured REST v2 JSON bodies instead of GraphQL string interpolation
- Added test suite with 131 tests covering all classes (Client, API, Serverless)
- Configured `pytest-cov` with `--cov-fail-under=100` for 100% coverage enforcement
- Added `test_imports.py` verifying all project scripts parse successfully
- Added GitHub Actions CI workflow (`tests.yml`) running on Python 3.10-3.14
- Removed `Endpoints` class and dreambooth scripts (API deprecated by Runpod)
