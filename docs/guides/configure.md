# Configure a project

The questionnaire moves from project identity to repository and maintainer
metadata. Press `Enter` to accept a displayed default.

## Question groups

| Group | Decisions |
| --- | --- |
| Identity | Display name, description, and initial version |
| Package shape | Distribution slug, import package, and base exception |
| License | MIT or BSD 3-Clause |
| Python | Minimum, default, and exclusive maximum versions |
| Tooling | Coverage gate, Git initialization, and post-copy setup |
| GitHub | Owner, repository name and URL, optional environment reviewer |
| Documentation | Published documentation URL |
| Maintainer | Name, public email, and copyright year |

See [Questionnaire reference](../reference/questionnaire.md) for every default
and validation rule.

## Values worth checking

### Names

| Value | Example | Used by |
| --- | --- | --- |
| Project name | `Orbit Tools` | Headings and documentation |
| Project slug | `orbit-tools` | Distribution, repository, and image names |
| Package name | `orbit_tools` | Python imports and `src/` directory |
| Exception class | `OrbitToolsError` | Public package API |

The derived defaults are usually correct. Change them when the PyPI
distribution name, repository name, and import name should differ.

### Python range

The default version controls local development, the dev container, and the
non-Linux CI jobs. The generated Linux test matrix covers every minor version
from the minimum through the default.

```text
minimum 3.11 ─── 3.12 ─── 3.13 ─── default 3.14
                                             └── maximum 3.15 (exclusive)
```

The exclusive maximum must be the minor version immediately after the default.

### GitHub destinations

For built-in publishing, use:

```text
repository URL     https://github.com/OWNER/REPOSITORY
documentation URL  https://OWNER.github.io/REPOSITORY/
```

`ppf publish` reads these values from the generated `pyproject.toml`; it does
not infer the destination from the local directory.

### Setup behavior

| Initialize Git | Run setup | Result on Linux/macOS |
| --- | --- | --- |
| Yes | Yes | Create `main`, make the initial commit, install dependencies and hooks |
| Yes | No | Create `main` and the initial commit only |
| No | Yes | Install Python and Node dependencies; skip hooks |
| No | No | Render files only |

The generated initial commit uses the questionnaire's author name and email
for that commit without changing global Git configuration.

## Recorded answers

The generated `.python-project-foundry.answers.yaml` records the selected
values. Commit it with the repository:

- it documents how names and settings were derived;
- it makes configuration review straightforward;
- it provides input for future template migration tooling.

Python Project Foundry does not currently expose an update command. To compare
a newer template release, generate a fresh project and review the diff.
