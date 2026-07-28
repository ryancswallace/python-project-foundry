# Development container

This directory defines the reproducible VS Code development environment for
Python Project Foundry.

It provides:

- Python 3.14 on Debian Bookworm.
- `uv` 0.11.23, within the version range required by `pyproject.toml`.
- The complete Python development dependency group installed by `make setup`.
- Node.js 24 for working on the JavaScript-based tooling in generated projects.
- GitHub CLI and Docker-outside-of-Docker for repository and container workflows.
- Common command-line tools including Git, Make, ripgrep, jq, and ShellCheck.
- VS Code support for Ruff, basedpyright, pytest, Markdown, YAML, TOML, CSpell,
  GitHub Actions, containers, and Makefiles.

VS Code runs the following command when it creates the container:

```console
make setup
```

The virtual environment lives under `/home/vscode/.venvs`, keeping its Linux
artifacts separate from any `.venv` created in the host checkout.

After creation, verify the development environment with:

```console
make check
```

Docker-outside-of-Docker exposes the host Docker daemon inside the development
container. Only open trusted projects in this environment.
