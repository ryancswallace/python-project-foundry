# Template development

## Source map

| Path | Edit it to change |
| --- | --- |
| `copier.yaml` | Include order for settings and questions |
| `copier/questions/` | Prompts, defaults, help text, and validation |
| `copier/settings/` | Rendering, tasks, messages, and migrations |
| `copier/shared/` | Reusable question definitions and choices |
| `template/` | Generated repository files |
| `src/python_project_foundry/` | CLI, template updates, and GitHub publishing behavior |
| `tests/test_template.py` | Rendered-project integration coverage |
| `tests/test_generated_project.py` | Generated toolchain end-to-end coverage |

Read [How it works](../explanation/how-it-works.md) for the boundary between
these components.

## Make a template change

1. Add or update the question before using its value in `template/`.
2. Use the `.jinja` suffix only for files that need rendering.
3. Keep derived defaults after the answers they reference in `copier.yaml`.
4. Add the placeholder name to the integration test's expected set.
5. Render with non-default answers.
6. Inspect the generated files and run the tests.

## Render the working tree

The development CLI snapshots uncommitted template files, so a commit is not
required before testing:

```console
make template DEST=/tmp/ppf-example PPF_ARGS="--skip-tasks"
```

For a clean repeat run, choose a new destination. Avoid overwriting a real
project while developing the template.

## Validate

```console
make test
make docs
make check
```

Template integration tests verify:

- custom answers render consistently;
- every known placeholder has a question;
- no placeholder remains in generated files;
- generated Python versions match the selected range;
- important generated configuration remains intact.

CI also creates a repository with default answers, runs its setup tasks,
executes its Python, Node, documentation, security, and build targets, and
checks the resulting wheel, source archive, SBOM, and documentation site.
Run that slower workflow locally with:

```console
PPF_RUN_GENERATED_E2E=1 uv run pytest -q -s tests/test_generated_project.py
```

When changing a generated dependency, update its manifest and lockfile
together and render a fresh project before submitting the change.
