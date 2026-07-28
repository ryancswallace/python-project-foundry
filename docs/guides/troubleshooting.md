# Troubleshooting

## Generation and setup

| Symptom | Cause | Fix |
| --- | --- | --- |
| Only one or a few prompts appear | An older package or incomplete template configuration is running | Run `uvx --refresh python-project-foundry ...` and confirm the command's version/source |
| A post-copy task fails | Git, Make, uv, Node.js, or npm is unavailable | Install the missing tool, or regenerate with `--skip-tasks` |
| Destination files conflict | The directory already contains files Copier manages | Preview with `--pretend`; use `--overwrite` only after reviewing |
| Hooks are missing | Git initialization or setup tasks were disabled | Initialize Git if needed, then run `make hooks-install` |

## uv cannot write its tool directory

Example:

```text
failed to create directory ~/.local/share/uv/tools: Permission denied
```

Check ownership:

```console
ls -ld "$HOME/.local" "$HOME/.local/share"
```

Repair incorrect ownership, or point uv at a writable location:

```console
mkdir -p "$HOME/.uv/tools"
UV_TOOL_DIR="$HOME/.uv/tools" uvx python-project-foundry --help
```

Set `UV_TOOL_DIR` in the shell or container environment to make the override
persistent.

## Generated project checks

| Symptom | Fix |
| --- | --- |
| `.venv` is missing or stale | Run `make install` |
| BasedPyright reports a virtual-environment path error | Run type checks through `make typecheck`; the Makefile pins `UV_PROJECT_ENVIRONMENT=.venv` |
| npm reports a lock mismatch | Run `npm install`, review both package files, then commit them |
| Docker daemon is not reachable | Start Docker and verify `docker info`; check socket forwarding in a dev container |
| Trivy reports a fixed critical vulnerability | Update the owning locked dependency or base image; do not add an ignore unless the finding is proven inapplicable |

## Publish failures

| Error | Fix |
| --- | --- |
| Working tree has changes | Commit or discard them |
| Current branch is not `main` | Switch to the generated `main` branch |
| Remote already exists | The repository may already be published; inspect `git remote -v` instead of replacing it |
| GitHub CLI is missing | Install `gh` |
| Authentication fails | Run `gh auth login`, then `gh auth status` |
| Source URL is rejected | Set `project.urls.Source` to `https://github.com/OWNER/REPOSITORY` |

Use `--dry-run` before retrying a publish operation that has not created a
remote repository.

## Pages does not deploy

Check, in order:

1. **Actions** — the generated Documentation workflow completed successfully.
2. **Settings → Pages** — the source is **GitHub Actions**.
3. **Environments** — `github-pages` permits deployments from `main`.
4. **URL** — `project.urls.Documentation` matches the expected Pages URL.

Publishing with `--skip-pages` intentionally leaves Pages unconfigured.
