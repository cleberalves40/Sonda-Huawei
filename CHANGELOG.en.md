# Changelog

[Português](CHANGELOG.md) | **English**

All notable changes to this project are documented here. This changelog follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and the project follows [Semantic Versioning](https://semver.org/).

---

## [0.1.1] - 2026-10-31

### Added
- `-P` alias for selecting the SSH TCP port (`--port` / `-P`).
- Complete CLI parameter reference and alternate management port tips in `README.md`.
- Unit tests for validating the SSH port `-P` parameter.
- Automated GitHub release CI/CD workflow (`release.yml`) for building and publishing releases.
- Release checksum helper script (`ci/update-release-hashes.sh`).
- Official release guide in `docs/RELEASING.md`.

## [0.1.0] - 2026-10-31

### Added
- Official Python package structure (PEP 621) using `pyproject.toml`.
- Executable CLI entry point: `sonda-huawei`.
- `sonda_huawei` module containing `HuaweiProbe` and ICMP parsing routines for VRPv5/VRPv8.
- `--version` / `-V` option to show the current version.
- `--json` option for exporting results to automation and dashboards.
- Formatting fallback when `tabulate` is not installed.
- Unit test suite in `tests/test_probe.py` covering parsing and CLI arguments.
- Continuous integration (CI) in `.github/workflows/test.yml` for Python 3.8 through 3.12.
- Official **FreeBSD port** structure in `freebsd/` (`Makefile`, `distinfo`, `pkg-descr`).
- **Homebrew Tap** formula in `Formula/sonda-huawei.rb` in the `cleberalves40/homebrew-tap` repository.
- Installation documentation for Homebrew, FreeBSD Ports, and Python virtual environments in the README.
