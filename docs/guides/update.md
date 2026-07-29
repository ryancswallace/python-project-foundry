# Update a generated project

`ppf update` applies the template tagged for the installed Python Project
Foundry version. Copier performs a three-way merge so repository changes are
preserved where they do not conflict with template changes.

## Prerequisites

| Requirement | Why |
| --- | --- |
| Clean Git working tree | Makes the generated update diff reviewable and recoverable |
| Committed `.python-project-foundry.answers.yaml` | Identifies the previous template tag and recorded answers |
| Network access to GitHub | Retrieves the old and target tagged templates |
| Target Foundry release | Determines the exact update tag; latest is not selected implicitly |

## Preview and apply

Run from the generated repository root:

```console
uvx --refresh python-project-foundry update --pretend
uvx --refresh python-project-foundry update
```

Or pass the repository explicitly:

```console
uvx --refresh python-project-foundry update /path/to/project
```

Previously answered questions are retained. If a release introduces a new
question, Foundry prompts for it; use `--defaults` to accept its default.

## Review the result

```console
git status
git diff
make check
```

Resolve inline conflict markers before committing. To write unresolved hunks
to separate files instead, use:

```console
uvx python-project-foundry update --conflict rej
```

## Tasks and migrations

| Option | Template files | Migrations | Regular tasks |
| --- | --- | --- | --- |
| Default | Applied | Run | Run |
| `--skip-tasks` | Applied | Run | Skipped |
| `--pretend` | Previewed | Not applied | Not run |

Migrations cannot be skipped because they may be required to make a template
version compatible with the generated repository.
