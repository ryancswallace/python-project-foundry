<!-- markdownlint-disable MD041 -->
[![Copier](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/copier-org/copier/master/img/badge/badge-grayscale-inverted-border-orange.json)](https://github.com/copier-org/copier)

# Python Project Foundry

## Command-line usage

## Installing

On macOS or Linux, scaffold with one command even if `uv` is not installed:

```console
curl -LsSf https://raw.githubusercontent.com/ryancswallace/python-project-foundry/main/ppf | sh -s -- /path/to/new/project
```

This downloads the repository's small launcher before executing it. The
launcher installs a compatible `uv` version, then runs Python Project Foundry
from GitHub in an isolated environment.

If `uv` is already installed, use `uvx` directly:

```console
uvx --from git+https://github.com/ryancswallace/python-project-foundry ppf /path/to/new/project
```

Without `uv`, clone the repository and use its self-bootstrapping launcher:

```console
git clone https://github.com/ryancswallace/python-project-foundry
cd python-project-foundry
./ppf /path/to/new/project
```

The launcher installs a compatible `uv` version when necessary. `uv` then
installs Python, Copier, and the other runtime dependencies when they are
missing.

The equivalent Make command is:

```console
make template DEST=/path/to/new/project
```

It also installs `uv` when necessary and does not require a separate
`make setup`.

### Persistent installation

Install the command from GitHub if it will be used regularly:

```console
uv tool install git+https://github.com/ryancswallace/python-project-foundry
```

Then scaffold a project:

```console
ppf /path/to/new/project
```

The command prompts for the template's answers and runs its trusted setup tasks.
`ppf template /path/to/new/project` remains available as the explicit form.
Use `ppf template --help` to see options for unattended generation,
overwriting files, previewing changes, and skipping setup tasks.

After the package is published to PyPI, the no-clone command becomes:

```console
uvx python-project-foundry /path/to/new/project
```

### Contributor setup

For work on Python Project Foundry itself, `make setup` installs `uv` when
needed and syncs the complete development environment:

```console
make setup
make check
```
