# Generated project reference

Python Project Foundry generates Python package/library repositories with an
importable package.

## Top-level layout

| Path | Contents |
| --- | --- |
| `src/<package>/` | Typed package, greeting example, and public exception |
| `tests/` | Unit and public API tests |
| `docs/` | Project, explanation, how-to, runbook, and API reference pages |
| `examples/` | Example placeholder and guidance |
| `scripts/` | Release preparation, pull request, and tag automation |
| `.github/` | Workflows, issue forms, labels, CODEOWNERS, and settings-as-code |
| `.devcontainer/` | Python, Node, GitHub CLI, uv, and Docker tooling |
| `Dockerfile` | Runtime and pytest stages |
| `Makefile` | Development, validation, container, and release interface |
| `pyproject.toml` | Package metadata and Python tool settings |
| `uv.lock` | Locked Python dependency graph |
| `package.json` | Markdown, spelling, workflow, and Dockerfile tools |

## Toolchain

| Concern | Tools |
| --- | --- |
| Dependencies | uv and npm |
| Format and lint | Ruff, markdownlint, CSpell, actionlint, Zizmor |
| Types | BasedPyright and `py.typed` marker |
| Tests | Pytest, pytest-cov, and Hypothesis |
| Docs | MkDocs Material, mkdocstrings, and linkchecker |
| Security | Bandit, pip-audit, detect-secrets, deptry, CodeQL, dependency review |
| Containers | Multi-stage Dockerfile, Buildx, and Trivy |
| Releases | Hatchling, build, Twine, CycloneDX, attestations, and PyPI trusted publishing |

## Make target groups

Run `make help` in a generated repository for the authoritative list.

| Group | Common targets |
| --- | --- |
| Setup | `bootstrap`, `install`, `npm-install`, `hooks-install`, `ready` |
| Python | `format`, `lint`, `typecheck`, `test`, `test-min-deps` |
| Documentation | `docs`, `docs-linkcheck`, `serve-docs` |
| Security | `deps`, `secrets`, `security`, `audit` |
| Containers | `docker-build`, `docker-test`, `docker-scan`, `docker-check` |
| Release | `prepare-release`, `release-pr-ready`, `release-tag`, `build`, `sbom` |
| Suites | `check`, `check-all`, `precommit`, `prepush` |

`make check` does not require Docker. `make check-all` adds the Nox matrix,
hook suite, and full Docker validation.

## GitHub automation

| Workflow | Trigger and purpose |
| --- | --- |
| CI | Quality, cross-platform tests, minimum dependencies, package build, scheduled audit |
| Documentation | Strict build and link check; deploy to Pages from `main` |
| Docker | Build, test, scan, attest, and publish runtime and test images |
| Release verification | Validate candidate release metadata and artifacts |
| Release | Build, attest, upload GitHub assets, publish to PyPI, verify installation |
| CodeQL | Static security analysis |
| Dependency review | Block vulnerable dependency changes in pull requests |
| Scorecard | OpenSSF supply-chain posture |
| Workflow lint | actionlint and Zizmor checks |
| Labeler / draft release | Repository maintenance automation |

## Repository configuration

The generated `.github/settings.yml` is consumed only when the
[GitHub Settings app](https://github.com/apps/settings) is installed. It
describes:

- repository metadata and merge behavior;
- `main` branch protection and required checks;
- `github-pages` and `pypi` deployment environments.

Without the app, configure equivalent settings in GitHub manually.
