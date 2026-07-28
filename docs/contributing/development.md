# Development

## Set up

Clone the repository, then install the complete development environment:

```console
make setup
```

## Validate

Run the full suite before submitting changes:

```console
make check
```

Useful focused commands include:

| Command | Purpose |
| --- | --- |
| `make format` | Apply Ruff fixes and formatting. |
| `make lint` | Check Ruff lint and formatting rules. |
| `make typecheck` | Run Basedpyright. |
| `make test` | Run Pytest. |
| `make docs` | Build documentation strictly. |
| `make docs-linkcheck` | Build documentation and crawl its links. |
| `make serve-docs` | Preview documentation with live reload. |

## Project layout

| Path | Responsibility |
| --- | --- |
| `src/python_project_foundry/` | Published CLI and GitHub publishing code |
| `copier.yaml` and `copier/` | Questionnaire and Copier lifecycle configuration |
| `template/` | Generated repository content |
| `tests/` | CLI, publishing, and rendered-template tests |
| `docs/` | This documentation site |

For questionnaire or generated-file changes, follow
[Template development](template.md).

See the repository's
[contribution guide](https://github.com/ryancswallace/python-project-foundry/blob/main/CONTRIBUTING.md)
for contribution expectations.
