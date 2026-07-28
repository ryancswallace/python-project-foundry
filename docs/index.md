# Python Project Foundry

Create an opinionated, production-ready Python package repository from one
interactive command.

```console
uvx python-project-foundry ./my-project
```

[Create your first project](quickstart.md){ .md-button .md-button--primary }
[See what gets generated](reference/generated-project.md){ .md-button }

## What you get

| Area | Included |
| --- | --- |
| Package | `src/` layout, typed public API, tests, examples, and package metadata |
| Quality | Ruff, BasedPyright, Pytest, Hypothesis, coverage, and pre-commit hooks |
| Security | Bandit, pip-audit, detect-secrets, CodeQL, dependency review, and Scorecard |
| Documentation | MkDocs Material, generated API reference, and GitHub Pages workflow |
| Delivery | Wheel and source builds, SBOM, artifact attestations, PyPI trusted publishing |
| Development | uv lockfile, Make targets, dev container, Docker images, and Nox matrix |

## Typical workflow

1. **Scaffold** — answer the project questionnaire.
2. **Review** — inspect the generated files and run `make check`.
3. **Publish** — explicitly create and push the GitHub repository.
4. **Develop** — use the generated Make targets and automation.

Scaffolding is local by default. GitHub resources are created only when you run
the [`publish` command](guides/publish.md).

## Find what you need

| Goal | Start here |
| --- | --- |
| Generate a project interactively | [Quickstart](quickstart.md) |
| Understand or choose questionnaire answers | [Configure a project](guides/configure.md) |
| Work in the generated repository | [Develop a generated project](guides/development.md) |
| Create the GitHub repository and Pages site | [Publish to GitHub](guides/publish.md) |
| Run without prompts | [Automate generation](guides/unattended.md) |
| Resolve a failure | [Troubleshooting](guides/troubleshooting.md) |
| Look up every CLI option | [Command-line reference](reference/cli.md) |
