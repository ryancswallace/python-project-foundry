# Python Project Foundry

Python Project Foundry scaffolds maintainable Python projects with a single
command. It packages a [Copier](https://copier.readthedocs.io/) template behind
a focused command-line interface so that users do not need to clone the
template repository or learn Copier's invocation details.

## Create a project

With [`uv`](https://docs.astral.sh/uv/getting-started/installation/) installed:

```console
uvx python-project-foundry /path/to/new/project
```

Python Project Foundry asks how the project should be shaped, renders the
matching files, and optionally runs the generated project's setup tasks.

[Get started](quickstart.md){ .md-button .md-button--primary }
[Browse the guides](guides/index.md){ .md-button }

## Documentation map

| Section | Purpose |
| --- | --- |
| [Quickstart](quickstart.md) | Generate a first project. |
| [Guides](guides/index.md) | Complete specific scaffolding tasks. |
| [Reference](reference/index.md) | Look up commands, options, and Python APIs. |
| [How it works](explanation/how-it-works.md) | Understand the CLI, template, and Copier relationship. |
| [Development](contributing/development.md) | Work on Python Project Foundry itself. |
