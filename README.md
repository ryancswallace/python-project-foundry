<!-- markdownlint-disable MD041 -->
[![Copier](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/copier-org/copier/master/img/badge/badge-grayscale-inverted-border-orange.json)](https://github.com/copier-org/copier)
[![CI](https://github.com/ryancswallace/python-project-foundry/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/ryancswallace/python-project-foundry/actions/workflows/ci.yml)
[![Documentation](https://github.com/ryancswallace/python-project-foundry/actions/workflows/docs.yml/badge.svg?branch=main)](https://github.com/ryancswallace/python-project-foundry/actions/workflows/docs.yml)
[![Python 3.11-3.14](https://img.shields.io/badge/python-3.11%20%7C%203.12%20%7C%203.13%20%7C%203.14-3776AB?logo=python&logoColor=white)](https://github.com/ryancswallace/python-project-foundry/blob/main/pyproject.toml)
[![Typed with basedpyright](https://img.shields.io/badge/types-basedpyright-2f6fdd)](https://github.com/DetachHead/basedpyright)
[![Linted with Ruff](https://img.shields.io/badge/lint-Ruff-46a2f1)](https://docs.astral.sh/ruff/)

# Python Project Foundry

## Create a project

With [`uv`](https://docs.astral.sh/uv/getting-started/installation/) installed,
scaffold a project directly from the published package:

```console
uvx python-project-foundry /path/to/new/project
```

If `uv` is not installed, macOS and Linux users can bootstrap it and scaffold
the project with one command:

```console
curl -LsSf https://raw.githubusercontent.com/ryancswallace/python-project-foundry/main/ppf | sh -s -- /path/to/new/project
```

The launcher installs a compatible `uv` version when necessary, then runs
Python Project Foundry in an isolated environment. No repository clone or
separate setup command is required.

Both commands prompt for the template's answers and execute the generated
project's setup tasks. Run
`uvx python-project-foundry template --help` to see options for unattended
generation, overwriting files, previewing changes, and skipping setup tasks.

## Contributor setup

For work on Python Project Foundry itself, `make setup` installs `uv` when
needed and syncs the complete development environment:

```console
make setup
make check
```
