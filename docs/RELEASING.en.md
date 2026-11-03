# Release cycle and maintenance

[Português](RELEASING.md) | **English**

This document describes how to release new versions of **Sonda-Huawei** and synchronize its distribution channels (**FreeBSD Ports** and **Homebrew Tap**).

## Versioning

The project follows [Semantic Versioning](https://semver.org/) (`vMAJOR.MINOR.PATCH`).

- **MAJOR**: incompatible changes to the CLI or internal API.
- **MINOR**: new features (for example, new VRP commands or support for other router models).
- **PATCH**: bug fixes, ping regular-expression updates, dependency adjustments, and documentation.

## Steps for a new release

### 1. Update the package version

Set the version to `X.Y.Z` in:

1. [`pyproject.toml`](../pyproject.toml):
   ```toml
   version = "X.Y.Z"
   ```
2. [`sonda_huawei/__init__.py`](../sonda_huawei/__init__.py):
   ```python
   __version__ = "X.Y.Z"
   ```
3. Record the changes in [`CHANGELOG.md`](../CHANGELOG.md).

### 2. Run the tests locally

```sh
python3 -m unittest discover -s tests -v
```

### 3. Create the release commit and tag

```sh
git add pyproject.toml sonda_huawei/__init__.py CHANGELOG.md
git commit -m "chore(release): bump version to vX.Y.Z"
git tag -a vX.Y.Z -m "Release vX.Y.Z"

git push origin main
git push origin vX.Y.Z
```

The [`.github/workflows/release.yml`](../.github/workflows/release.yml) CI/CD workflow runs automatically:

- Cross-checks the tag against `pyproject.toml`.
- Builds source (`.tar.gz`) and wheel (`.whl`) packages.
- Generates `SHA256SUMS` checksums.
- Publishes the official GitHub release with the artifacts attached.

## Updating distribution channels

After publishing the GitHub tag, use the helper script to retrieve the exact hashes:

```sh
./ci/update-release-hashes.sh X.Y.Z
```

### FreeBSD port (`freebsd/`)

1. Update the version in [`freebsd/Makefile`](../freebsd/Makefile):
   ```makefile
   DISTVERSION=    X.Y.Z
   ```
2. Replace the entries in [`freebsd/distinfo`](../freebsd/distinfo) with the script output.
3. Commit and push the changes:
   ```sh
   git add freebsd/Makefile freebsd/distinfo
   git commit -m "feat(freebsd): update port to vX.Y.Z"
   git push origin main
   ```

### Homebrew Tap (`Formula/sonda-huawei.rb`)

In the [tap repository](https://github.com/cleberalves40/homebrew-tap):

1. Update the URL and `sha256` in `Formula/sonda-huawei.rb`:
   ```ruby
   url "https://github.com/cleberalves40/Sonda-Huawei/archive/refs/tags/vX.Y.Z.tar.gz"
   sha256 "<new-sha256>"
   ```
2. Commit and push to the `main` branch:
   ```sh
   git commit -am "sonda-huawei X.Y.Z"
   git push origin main
   ```

The tap workflow tests and audits installation of the new version.
