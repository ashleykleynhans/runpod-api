# Changelog

## [0.1.0] - 2026-07-28

- Renamed `runpod` module to `rpapi` package to avoid conflicts with the official Runpod Python module
- Converted from flat script with symlinks to a proper installable Python package (`rpapi/__init__.py`)
- Added `pyproject.toml` with `pip install -e .` support
- Removed all `runpod.py` symlinks from subdirectories
- Added `sys.path` fixup to subdirectory scripts for development use without installation
