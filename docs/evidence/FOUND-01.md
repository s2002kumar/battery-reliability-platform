# FOUND-01 Evidence — Repository Foundation

- **Date:** 2026-10-06
- **Branch:** `chore/FOUND-01-repository-foundation`
- **Result:** Local acceptance checks PASS; both GitHub Actions runs PASS.
- **Architecture/data gate:** ARCH-00 remains BLOCKED. No source parsing, battery schema mapping, SOH, or ML behavior was added.

## Tool versions

| Tool | Version |
|---|---|
| Python | 3.12.13 |
| uv | 0.12.1 |
| Ruff | 0.16.10 |
| Mypy | 1.20.2 |
| pytest | 8.4.2 |
| Docker CLI / Engine | 28.4.0 / 28.4.0 |

The dependency graph is captured in `uv.lock`; Python is pinned in `.python-version`. Ruff, Mypy, pytest, and the Hatchling build backend are constrained in `pyproject.toml`. The Dockerfile pins both the Python and uv image digests.

## Environment and checks

The lockfile check and environment sync succeeded:

```text
uv --cache-dir "$env:TEMP\brip-uv-cache" lock --check
uv --cache-dir "$env:TEMP\brip-uv-cache" sync --locked --all-groups
```

The explicit interpreter install was verified with uv's supported temporary install directory because this managed workstation denies writes to its default uv Python directory:

```text
uv --cache-dir "$env:TEMP\brip-uv-cache" python install --install-dir "$env:TEMP\brip-uv-python"
Installed Python 3.12.13
```

The workstation's existing unmanaged `python3.12.exe` prevented uv from installing its optional executable shim in the user bin directory; the managed interpreter itself installed successfully. The project environment then imported the installed `src/` package and printed version `0.1.0`.

Because the managed host's default uv cache is also access-restricted, the quality commands used an explicit temporary cache path. Results:

| Command | Result |
|---|---|
| `uv --cache-dir "$env:TEMP\brip-uv-cache" run --locked ruff check .` | PASS — all checks passed |
| `uv --cache-dir "$env:TEMP\brip-uv-cache" run --locked ruff format --check .` | PASS — 26 files already formatted |
| `uv --cache-dir "$env:TEMP\brip-uv-cache" run --locked mypy src` | PASS — no issues in 4 source files |
| `uv --offline --cache-dir "$env:TEMP\brip-uv-cache" run --locked pytest` | PASS — 7 tests passed; no network access |
| `uv --cache-dir "$env:TEMP\brip-uv-cache" build --verbose` | PASS — source distribution and wheel built |

No test uses randomness. CI sets `PYTHONHASHSEED=0` for pytest.

## Docker

Build command:

```text
docker --config .tmp/docker-config build --progress plain --tag battery-reliability-platform:found01-final .
```

Result: PASS. The image ID was `sha256:c04f4e9ab72fa9f52a6786ac0a2d58b9629a41a7fefdae4a1cf91f416fe63632`. Running `docker --config .tmp/docker-config run --rm battery-reliability-platform:found01-final` passed all 7 tests under Linux/Python 3.12.13. The Docker config override avoids reading this workstation's protected Docker config directory.

## CI

`.github/workflows/ci.yml` runs on branch pushes and pull requests targeting `main`. It installs pinned uv and Python, syncs with `--locked`, then runs the four quality gates and builds the development/test image. Actions are pinned by immutable commit SHA.

GitHub Actions runs [37511765127](https://github.com/s2002kumar/battery-reliability-platform/actions/runs/37511765127) and [37511771279](https://github.com/s2002kumar/battery-reliability-platform/actions/runs/37511771279) completed successfully on the rebased PR branch. Both passed Python setup, locked environment sync, Ruff lint/format, Mypy, pytest, and Docker image build. FOUND-01 PR [#3](https://github.com/s2002kumar/battery-reliability-platform/pull/3) was squash-merged at `4784bd6fc54b87fff73f825b2ab946e2c7774657`. ARCH-00 documentation PR [#4](https://github.com/s2002kumar/battery-reliability-platform/pull/4) was squash-merged at `60937a8dd9d2b13491a3c2a7826f3c618dab7c42`.

## Files introduced or changed

- Added `.dockerignore`, `.python-version`, `Dockerfile`, `pyproject.toml`, and `uv.lock`.
- Added `.github/workflows/ci.yml`.
- Added `src/battery_reliability/` package modules for settings, JSON logging, and the generic storage URI/filesystem protocol.
- Added `tests/test_foundation.py` (7 tests).
- Added `docs/task-cards/FOUND-01.md` and this evidence file.
- Updated `README.md`, `STATUS.md`, and `WORK_QUEUE.md`.

No secrets, `.env` file, real dataset bytes, or battery-specific code were added. `.env.example` was unnecessary because all settings are optional non-secret defaults.

## Limitations

- ARCH-00 remains BLOCKED. FOUND-01 provides tooling only and does not authorize ingestion or ML implementation.
- The local uv cache/Python install paths required temporary overrides because the default user paths are restricted in this managed environment.
- The generic `FileSystem` is an interface only. There is no local provider implementation, S3 support, or storage behavior.
- ARCH-00 remains BLOCKED, and FOUND-01 does not authorize ingestion or ML implementation.
