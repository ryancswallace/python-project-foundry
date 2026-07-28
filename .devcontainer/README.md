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

## Local Runtime Options

Runtime settings that depend on one developer's machine should stay out of the
shared `devcontainer.json`. This section describes how to configure three common
developer-specific local patches to `devcontainer.json`:

- local secrets;
- host Git configuration;
- a relaxed seccomp profile.

### Preliminary: managing a local patch

If you choose to edit the tracked configuration locally, keep that patch out of
commits. As an optional convenience, tell Git to suppress routine status output:

```bash
git update-index --skip-worktree .devcontainer/devcontainer.json
```

Remember that `skip-worktree` can hide upstream changes. Re-enable normal
tracking before pulling or intentionally editing the shared configuration:

```bash
git update-index --no-skip-worktree .devcontainer/devcontainer.json
```

### Developer-specific settings

Add your machine-specific settings to `.devcontainer/devcontainer.json`. The
following snippet mounts your host `.gitconfig`, mounts in a local environment
variable file, a Codex auth file, and sets `seccomp=unconfined` (e.g., for Codex
sandboxing).

```json
"mounts": [
    "source=${localEnv:HOME}/.gitconfig,target=/home/vscode/.gitconfig,type=bind,consistency=cached",
    "source=${localEnv:HOME}/.local/share/devcontainer-bin,target=/home/vscode/.local/share/host-bin,type=bind,consistency=cached",
    "source=${localEnv:HOME}/.codex-devcontainer,target=/home/vscode/.codex,type=bind,consistency=cached"
],
"runArgs": [
    "--env-file",
    "${localWorkspaceFolder}/.devcontainer/.env.local",
    "--security-opt",
    "seccomp=unconfined"
]
```

If you use the `--env-file` option in `runArgs`, be sure to create
`.devcontainer/.env.local` with your local-only values. For example:

```dotenv
GH_TOKEN=github_pat_example
```

The `.env.local` file is ignored by Git.
