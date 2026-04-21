# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Integration test suite (`tests/test_omlx_integration.py`) covering full add/list/remove cycles
- Unitn- Japanese translation of README (`README.ja.md`)

### Changed
- Forked from [jundot/omlx](https://github.com/jundot/omlx)

## [0.1.0] - 2024-01-01

### Added
- Initial release as fork of jundot/omlx
- `omlx.py` core module with the following functions:
  - `load_config` — loads or creates default configuration file
  - `save_config` — persists configuration to disk
  - `list_apps` — lists all registered applications
  - `add_app` — registers a new application entry
  - `remove_app` — removes an application entry by name
- CLI entry point via `omlx.py`
- MIT License
- `.gitignore` for Python projects
- Bug report and feature request issue templates

[Unreleased]: https://github.com/your-org/omlx/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/your-org/omlx/releases/tag/v0.1.0
