# Develop a generated project

Run these commands from the generated repository root.

## Prepare the environment

```console
make ready
```

`make ready` installs the locked development environment and runs the standard
validation suite. To install dependencies and Git hooks without the full
check:

```console
make hooks-install
```

## Daily commands

| Command | Purpose |
| --- | --- |
| `make format` | Apply Ruff fixes and formatting |
| `make lint` | Check Python lint and formatting |
| `make typecheck` | Run BasedPyright |
| `make test` | Run Pytest with the configured coverage gate |
| `make docs` | Build the MkDocs site in strict mode |
| `make serve-docs` | Preview documentation with live reload |
| `make check` | Run the standard local quality, security, docs, and build suite |
| `make precommit` | Run pre-commit-stage hooks against all files |
| `make check-all` | Add hooks, the Nox matrix, and Docker validation |

Run `make help` for the complete target list.

## Repository layout

| Path | Responsibility |
| --- | --- |
| `src/<package>/` | Importable package and typed public API |
| `tests/` | Unit and public API tests |
| `docs/` | MkDocs source |
| `examples/` | Runnable usage examples |
| `.github/workflows/` | CI, security, docs, container, and release automation |
| `pyproject.toml` | Package metadata and Python tool configuration |
| `uv.lock` | Cross-platform locked Python dependencies |
| `package.json` / `package-lock.json` | Prose and Dockerfile tooling |
| `Makefile` | Stable local command interface |

## Change dependencies

```console
uv add PACKAGE
uv add --group test PACKAGE
uv remove PACKAGE
```

Commit both `pyproject.toml` and `uv.lock`.

For Node-based development tools:

```console
npm install --save-dev PACKAGE
```

Commit both `package.json` and `package-lock.json`.

## Containers

| Command | Result |
| --- | --- |
| `make docker-build` | Build the minimal runtime image |
| `make docker-test` | Build and run the pytest image |
| `make docker-scan` | Scan runtime and test images for fixed critical vulnerabilities |
| `make docker-check` | Lint, build, test, smoke-test, and scan both images |

Docker commands require a reachable Docker daemon. The included dev container
forwards the host Docker socket.
