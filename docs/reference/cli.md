# Command-line reference

Both executable names invoke the same CLI:

```console
uvx python-project-foundry --help
ppf --help
ppf --version
```

`ppf` is available when the package is installed as a persistent tool or run
from a source checkout.

The top-level `--version` option prints the installed
`python-project-foundry` package version and exits.

## `template`

Create a generated project:

```console
uvx python-project-foundry template DESTINATION [OPTIONS]
```

The subcommand can be omitted:

```console
uvx python-project-foundry DESTINATION [OPTIONS]
```

### Arguments and options

| Name | Required | Description |
| --- | --- | --- |
| `DESTINATION` | Yes | Directory in which to render the project |
| `--defaults` | No | Accept all questionnaire defaults without prompting |
| `--overwrite` | No | Allow replacement of existing destination files |
| `--pretend` | No | Show Copier operations without writing files |
| `--skip-tasks` | No | Render without post-copy setup tasks |
| `-h`, `--help` | No | Display command help |

### Side effects

Without `--pretend`, the command writes generated files. Unless tasks are
skipped, trusted bundled Copier tasks may also:

- initialize a Git repository on `main`;
- create the initial commit;
- install locked Python and Node dependencies;
- install pre-commit and pre-push hooks.

Task selection also depends on the questionnaire answers and operating system.

## `update`

Update a generated repository to the template tag matching the installed
Foundry package:

```console
uvx python-project-foundry update [PROJECT] [OPTIONS]
```

`PROJECT` defaults to the current directory.

### Arguments and options

| Name | Required | Default | Description |
| --- | --- | --- | --- |
| `PROJECT` | No | `.` | Generated repository root |
| `--defaults` | No | Off | Accept defaults for newly introduced questions |
| `--pretend` | No | Off | Preview the update without writing changes |
| `--skip-tasks` | No | Off | Skip regular tasks; required migrations still run |
| `--conflict MODE` | No | `inline` | Write conflicts `inline` or to `.rej` files |
| `-h`, `--help` | No | — | Display command help |

### Update behavior

The command:

1. reads `.python-project-foundry.answers.yaml`;
2. fetches the recorded old template tag and the target tag from GitHub;
3. retains recorded questionnaire answers;
4. applies Copier's three-way update and migrations;
5. leaves the resulting diff for review and validation.

The destination must be a clean Git repository. Local validation and Copier
update failures return exit status `2` with an `error:` message.

## `publish`

Create and push a configured GitHub repository:

```console
uvx python-project-foundry publish [PROJECT] \
  --visibility {private,public,internal} [OPTIONS]
```

`PROJECT` defaults to the current directory.

### Arguments and options

| Name | Required | Default | Description |
| --- | --- | --- | --- |
| `PROJECT` | No | `.` | Generated project root |
| `--visibility` | Yes | — | GitHub repository visibility |
| `--remote NAME` | No | `origin` | Git remote to create |
| `--skip-pages` | No | Off | Do not configure GitHub Pages |
| `--dry-run` | No | Off | Check local state and print commands without GitHub writes |
| `-h`, `--help` | No | — | Display command help |

### Repository discovery

The command reads:

| `pyproject.toml` field | Purpose |
| --- | --- |
| `project.description` | GitHub repository description |
| `project.urls.Source` | GitHub `OWNER/REPOSITORY` and repository URL |
| `project.urls.Documentation` | Repository homepage and Pages destination |

The source URL must have this form:

```text
https://github.com/OWNER/REPOSITORY
```

### Preflight checks

`publish` requires:

- Git;
- GitHub CLI for a real publish;
- the exact Git repository root;
- a clean working tree;
- the `main` branch;
- no existing selected remote;
- active GitHub CLI authentication.

Local validation failures return exit status `2` with an `error:` message.
