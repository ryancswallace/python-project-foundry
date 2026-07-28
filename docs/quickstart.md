# Quickstart

## Prerequisite

Install [`uv`](https://docs.astral.sh/uv/getting-started/installation/) if it is
not already available.

On macOS and Linux, the project also provides a one-command bootstrap path:

```console
curl -LsSf https://raw.githubusercontent.com/ryancswallace/python-project-foundry/main/ppf | sh -s -- /path/to/new/project
```

## Generate a project

Run the published command with the destination directory:

```console
uvx python-project-foundry /path/to/new/project
```

Answer the prompts. Python Project Foundry renders the selected project
structure and runs the template's trusted setup tasks.

!!! warning

    Review generated files and tasks before using the tool with a template
    revision you do not trust.

## Explore the result

Move into the generated project and inspect its own README:

```console
cd /path/to/new/project
make help
make check
```

The generated repository documents its enabled features and developer commands.
