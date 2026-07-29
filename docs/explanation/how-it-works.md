# How it works

## Generation pipeline

```text
uvx
  └── published Python package
        └── ppf CLI
              └── bundled Copier template
                    ├── questionnaire
                    ├── rendered files
                    └── trusted setup tasks
```

| Layer | Responsibility |
| --- | --- |
| uvx | Resolve and run Python Project Foundry in an isolated tool environment |
| CLI | Parse the focused `template`, `update`, and `publish` commands |
| Copier | Ask questions, evaluate defaults, render Jinja templates, and run tasks |
| Generated repository | Own its uv/npm locks, Make commands, CI, docs, and release process |

The template is bundled inside the Python wheel. A package release therefore
ships one matched CLI and template version.

Generation uses that bundled snapshot and records the canonical Git template
repository plus the matching release tag in the generated answers file. This
keeps initial generation self-contained while giving later updates the two
tagged revisions required for Copier's three-way merge.

## Copier directory roles

| Path | Contains | Changes when |
| --- | --- | --- |
| `copier/questions/` | User-facing questions, defaults, help, and validators | A new answer or prompt is needed |
| `copier/settings/` | Copier engine behavior, file rules, tasks, migrations, and messages | Rendering or lifecycle behavior changes |
| `copier/shared/` | Reusable questionnaire fragments such as curated choices | Multiple question groups share a definition |
| `template/` | Files copied or rendered into new repositories | Generated project content changes |
| `copier.yaml` | Ordered includes that assemble all sections | A section is added or reordered |

Copier recognizes settings by their leading underscore, such as
`_subdirectory`, `_tasks`, and `_message_after_copy`. Ordinary top-level keys
are questionnaire answers.

## Derived values

Question order matters because later defaults use earlier answers:

```text
destination
  └── project_name
        └── project_slug
              ├── package_name
              ├── repository_name
              └── exception_class_name
```

Repository and documentation URLs then derive from the owner and repository
name.

## Setup tasks

Tasks are enabled because the bundled template is trusted. Depending on the
answers, they may:

1. initialize Git on `main`;
2. create the initial scaffold commit;
3. install locked Python and Node dependencies;
4. install pre-commit and pre-push hooks.

Use `--pretend` to preview file operations or `--skip-tasks` to render without
these commands.

## Publishing boundary

Generation does not contact GitHub. The explicit `publish` command separately
reads the generated `pyproject.toml`, validates local Git state, and invokes
GitHub CLI.

This separation keeps repository visibility and external writes out of the
questionnaire-driven copy step.

## Update boundary

`ppf update` is pinned to the installed Foundry package version rather than an
unbounded latest template. It contacts GitHub only to retrieve the recorded
old tag and that exact target tag. Copier requires a clean generated Git
repository, applies migrations, and leaves all changes uncommitted for review.

## Source checkout behavior

Copier normally renders a committed revision when its source is a Git
repository. During local development, the CLI snapshots `copier.yaml`,
`copier/`, and `template/` without `.git` so uncommitted template edits can be
tested.

## Trust model

- Install the expected `python-project-foundry` package.
- Inspect a new template release before overwriting files.
- Use `--skip-tasks` when only rendered files are desired.
- Never place secrets in questionnaire answers; answers are committed to the
  generated repository.
