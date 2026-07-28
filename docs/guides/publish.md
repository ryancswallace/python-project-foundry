# Publish to GitHub

Scaffolding creates a local repository. Publishing is a separate, explicit
operation.

## Prerequisites

- Run from the generated repository root, or pass its path.
- Install [GitHub CLI](https://cli.github.com/).
- Authenticate with `gh auth login`.
- Confirm the questionnaire's repository URL in `pyproject.toml`.

## Preview

From the generated repository:

```console
uvx python-project-foundry publish --visibility public --dry-run
```

From another directory:

```console
uvx python-project-foundry publish /path/to/project \
  --visibility public \
  --dry-run
```

## Publish

```console
uvx python-project-foundry publish --visibility public
```

Choose one visibility explicitly:

| Value | GitHub repository |
| --- | --- |
| `public` | Visible to everyone |
| `private` | Visible to granted users |
| `internal` | Visible to members of a supporting GitHub Enterprise account |

## What the command does

1. Reads `project.description`, `project.urls.Source`, and
   `project.urls.Documentation` from `pyproject.toml`.
2. Converts the source URL into `OWNER/REPOSITORY`.
3. Creates the GitHub repository with `gh repo create`.
4. Adds the selected remote, normally `origin`.
5. Pushes the generated `main` branch.
6. Enables GitHub Pages with GitHub Actions as its build source.

The generated Documentation workflow builds and deploys the site after pushes
to `main`.

## Safety checks

Publishing stops unless all checks pass:

| Check | Required state |
| --- | --- |
| Project metadata | `pyproject.toml` contains a GitHub HTTPS source URL |
| Repository root | Selected project path equals `git rev-parse --show-toplevel` |
| Working tree | No uncommitted changes |
| Branch | `main` |
| Remote | Selected remote name does not exist |
| Authentication | Active `gh` login for `github.com` |

## Options

| Option | Use it to |
| --- | --- |
| `--remote upstream` | Create a remote with a name other than `origin` |
| `--skip-pages` | Create and push the repository without enabling Pages |
| `--dry-run` | Run local checks and print external commands only |

## What it does not publish

`ppf publish` does not publish:

- a package to PyPI;
- a container image to GitHub Container Registry;
- a GitHub Release.

Those operations belong to the generated release and Docker workflows.
