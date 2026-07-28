# Development

Clone the repository, then prepare the complete development environment:

```console
make setup
```

Run the full validation suite before submitting changes:

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

See the repository's
[contribution guide](https://github.com/ryancswallace/python-project-foundry/blob/main/CONTRIBUTING.md)
for contribution expectations.
