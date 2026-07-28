# Automate generation

## Generate with defaults

```console
uvx python-project-foundry /path/to/new/project --defaults
```

Defaults are derived from the destination name where possible:

```text
/tmp/orbit-tools
        ├── project name: Orbit Tools
        ├── distribution: orbit-tools
        └── import package: orbit_tools
```

Review the full [questionnaire reference](../reference/questionnaire.md) before
using defaults in automation. In particular, the GitHub owner defaults to
`acme`.

## Preview without writing

```console
uvx python-project-foundry /path/to/new/project --defaults --pretend
```

## Render without setup tasks

```console
uvx python-project-foundry /path/to/new/project --defaults --skip-tasks
```

This creates files but does not initialize Git, install dependencies, or
install hooks. Run the desired setup later from the generated project:

```console
make hooks-install
```

## Existing destinations

| Option | Behavior |
| --- | --- |
| No option | Copier protects conflicting existing files |
| `--overwrite` | Allow generated files to replace existing files |
| `--pretend` | Show planned file operations only |

!!! warning

    Preview before combining automation with `--overwrite`.

## Custom unattended answers

The focused `ppf` CLI currently supports either interactive answers or all
defaults; it does not accept individual answer flags or a data file. For a
repeatable customized scaffold:

1. generate interactively in a staging directory;
2. record the answers from `.python-project-foundry.answers.yaml`;
3. keep the generated repository as the reproducible artifact.
