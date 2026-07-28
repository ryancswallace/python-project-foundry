# Questionnaire reference

Answers are prompted in the order shown below. Derived defaults use earlier
answers or the destination directory name.

## Identity and package shape

| Answer | Default | Constraint | Used for |
| --- | --- | --- | --- |
| `project_name` | Destination name in title case | Non-empty; no double quotes | Headings and documentation |
| `project_description` | `A modern Python package scaffold.` | Non-empty; no double quotes | Package and repository metadata |
| `initial_version` | `0.1.0` | Stable `X.Y.Z` form | Initial package and citation version |
| `project_slug` | Slugified project name | Lowercase words separated by single hyphens | Distribution, repository, and image names |
| `package_name` | Slug with hyphens replaced by underscores | Valid Python identifier | Import package under `src/` |
| `exception_class_name` | PascalCase slug plus `Error` | Starts uppercase and ends in `Error` | Public base exception |
| `license` | `MIT` | MIT or BSD 3-Clause | License file, metadata, and classifiers |

## Python and quality

| Answer | Default | Constraint | Used for |
| --- | --- | --- | --- |
| `python_min_version` | `3.11` | Python 3.11–3.14 | Oldest supported Python and minimum-dependency tests |
| `python_default_version` | `3.14` | At least the minimum | Local environment, container, and primary CI version |
| `python_max_version_exclusive` | `3.15` | Immediately after the default | `requires-python` upper bound |
| `coverage_fail_under` | `95` | Integer from 0 through 100 | Pytest coverage gate |

The generated Linux CI matrix includes every minor version from the minimum
through the default. macOS and Windows test the default version.

## Local setup

| Answer | Default | Effect |
| --- | --- | --- |
| `initialize_git_repository` | Yes | Initialize `main` and create an initial scaffold commit |
| `run_setup_tasks` | Yes | Install locked development dependencies and, when Git is initialized, hooks |

Post-copy tasks run only on Linux and macOS.

## Repository and documentation

| Answer | Default | Constraint | Used for |
| --- | --- | --- | --- |
| `repository_owner` | `acme` | Valid GitHub user or organization name | Repository, Pages, image, and policy paths |
| `repository_name` | Project slug | Letters, numbers, `.`, `_`, or `-` | GitHub repository name |
| `repository_url` | `https://github.com/<owner>/<repository>` | Complete HTTPS URL | Package links, badges, image labels, and publishing |
| `documentation_url` | `https://<owner>.github.io/<repository>/` | Complete HTTPS URL | MkDocs site, package metadata, and GitHub homepage |
| `github_environment_reviewer_id` | Empty | Numeric ID or empty | Optional PyPI deployment reviewer in `.github/settings.yml` |

!!! note

    Built-in publishing is stricter than the questionnaire's generic HTTPS URL
    validation: `project.urls.Source` must point to `github.com/OWNER/REPOSITORY`.

The optional reviewer value is a numeric GitHub user or team ID, not a login
name.

## Maintainer metadata

| Answer | Default | Constraint | Used for |
| --- | --- | --- | --- |
| `author_name` | `Acme Maintainers` | Non-empty; no double quotes | Package, citation, license, and initial commit |
| `author_email` | `maintainers@example.com` | Email-shaped value; no double quotes | Package, citation, security policy, and initial commit |
| `copyright_year` | Current year | 1970–9999 | License and site footer |

## Recorded output

All selected values are written to:

```text
.python-project-foundry.answers.yaml
```

Treat the file as repository configuration and commit it. It contains public
project metadata; do not enter secrets in questionnaire fields.
