# Command-line reference

## Invocation

```console
uvx python-project-foundry DESTINATION [OPTIONS]
```

`DESTINATION` is the directory in which to create the project. The explicit
`template` subcommand is also accepted:

```console
uvx python-project-foundry template DESTINATION [OPTIONS]
```

## Options

| Option | Description |
| --- | --- |
| `--defaults` | Use template defaults instead of prompting. |
| `--overwrite` | Overwrite existing destination files. |
| `--pretend` | Show what Copier would do without writing files. |
| `--skip-tasks` | Render without running template tasks. |
| `-h`, `--help` | Display help. |

The `ppf` executable is an equivalent short entry point when the package is
installed as a persistent tool.
