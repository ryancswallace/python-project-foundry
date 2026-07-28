# Release Python Project Foundry

Releases are published automatically to PyPI when a version tag is pushed to
GitHub. Authentication uses PyPI Trusted Publishing; no PyPI API token or
GitHub repository secret is required.

## One-time GitHub setup

The repository and `publish.yml` workflow must exist on GitHub before PyPI can
validate the pending publisher.

1. Create `ryancswallace/python-project-foundry` on GitHub if it does not
   already exist.
2. Configure and push this checkout if it does not yet have an `origin` remote:

   ```console
   git remote add origin git@github.com:ryancswallace/python-project-foundry.git
   git push -u origin main
   ```

3. Open the repository's **Settings → Environments** page.
4. Create an environment named exactly `pypi`.
5. If another trusted maintainer is available, add that maintainer as a required
   reviewer for deployments. A solo maintainer should not enable a rule that
   prevents self-review.
6. Restrict deployment branches and tags to protected tags matching `v*`, if
   that option is available for the repository.
7. Add a repository ruleset that prevents unauthorized creation, update, or
   deletion of tags matching `v*`.

## One-time PyPI setup

The `python-project-foundry` project does not need to exist on PyPI before its
first release. Add a pending publisher while signed in to the PyPI account that
should own the project:

1. Open <https://pypi.org/manage/account/publishing/>.
2. Find **Add a new pending publisher** and select **GitHub**.
3. Enter these exact values:

   | Field | Value |
   | --- | --- |
   | PyPI project name | `python-project-foundry` |
   | GitHub owner | `ryancswallace` |
   | GitHub repository name | `python-project-foundry` |
   | Workflow filename | `publish.yml` |
   | Environment name | `pypi` |

4. Add the pending publisher.

The pending publisher does not reserve the project name. It becomes a normal
trusted publisher when the first release succeeds.

If the project already exists by the time publishing is configured, open the
project's **Manage → Publishing** page and add the same GitHub publisher there
instead.

Do not add a `PYPI_TOKEN` secret. The publishing job receives only
`id-token: write`, which PyPI exchanges for a short-lived publishing token.

## Publish a release

1. Update the version in `pyproject.toml`.
2. Update `CHANGELOG.md`.
3. Refresh and verify the lock file:

   ```console
   uv lock
   make check
   make build
   uv run twine check --strict dist/*
   ```

4. Commit and push the release changes to `main`.
5. Create and push a matching annotated tag:

   ```console
   git tag -a v0.1.0 -m "Release v0.1.0"
   git push origin v0.1.0
   ```

The tag must be `v` followed by the exact package version. For example,
`pyproject.toml` version `0.1.0` requires tag `v0.1.0`. A mismatch fails before
the publishing job receives PyPI credentials.

The workflow:

1. installs dependencies from the locked environment;
2. runs linting, type checks, and tests;
3. builds the wheel and source distribution once;
4. validates both distributions with Twine;
5. transfers those exact artifacts to an environment-protected job;
6. publishes them through PyPI Trusted Publishing with digital attestations.

PyPI versions are immutable. To correct a release, increment the version and
publish a new tag; do not reuse or move an existing release tag.
