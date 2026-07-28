# Generate without prompts

Use default answers when a non-interactive run is more important than
customization:

```console
uvx python-project-foundry /path/to/new/project --defaults
```

Combine the command with `--pretend` to preview Copier's work without writing
files:

```console
uvx python-project-foundry /path/to/new/project --defaults --pretend
```

Other useful controls are:

| Option | Effect |
| --- | --- |
| `--overwrite` | Replace files that already exist in the destination. |
| `--skip-tasks` | Render files without running template setup tasks. |
| `--pretend` | Preview changes without writing them. |

Run the command's detailed help when scripting a generation:

```console
uvx python-project-foundry template --help
```
