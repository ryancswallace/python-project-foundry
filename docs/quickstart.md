# Quickstart

Python Project Foundry generates Python package/library repositories.

## 1. Check the prerequisites

| Requirement | Needed for |
| --- | --- |
| [uv](https://docs.astral.sh/uv/getting-started/installation/) | Running Python Project Foundry and managing Python dependencies |
| Git | Initializing and publishing the generated repository |
| Make | Generated setup and development commands |
| Node.js and npm | Markdown, spelling, and Dockerfile checks |

The automatic post-copy setup tasks run on Linux and macOS. On another
platform, render with `--skip-tasks` and prepare the project in a POSIX
environment.

## 2. Generate the package/library repository

```console
uvx python-project-foundry /path/to/new/project
```

The shorter invocation above is equivalent to:

```console
uvx python-project-foundry template /path/to/new/project
```

Answer the prompts. Before accepting a derived default, check these values:

- `repository_owner` — defaults to `acme`;
- `repository_name` — becomes the GitHub repository name;
- `author_name` and `author_email` — appear in package and Git metadata;
- supported Python versions;
- whether to initialize Git and install development tools.

See [Configure a project](guides/configure.md) for the complete questionnaire.

## 3. Validate the result

```console
cd /path/to/new/project
make help
make check
```

If setup tasks were skipped:

```console
make hooks-install
make check
```

`make hooks-install` installs the locked Python and Node development
dependencies before installing the Git hooks.

## 4. Publish when ready

Preview the GitHub operations:

```console
uvx python-project-foundry publish --visibility private --dry-run
```

Then publish:

```console
uvx python-project-foundry publish --visibility private
```

Publishing creates the configured GitHub repository, pushes `main`, and enables
the generated GitHub Pages workflow. See [Publish to GitHub](guides/publish.md)
for prerequisites and safety checks.

## Without a preinstalled uv

On macOS or Linux, the repository launcher can install a compatible uv release:

```console
curl -LsSf https://raw.githubusercontent.com/ryancswallace/python-project-foundry/main/ppf |
  sh -s -- /path/to/new/project
```

Review remote scripts before piping them to a shell.
