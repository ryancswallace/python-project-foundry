# Documentation

Documentation source is Markdown under `docs/`. Site configuration and
navigation live in `mkdocs.yml`.

## Write and preview

Start the development server:

```console
make serve-docs
```

MkDocs prints the local preview URL and rebuilds changed pages automatically.

Add new pages to the `nav` section of `mkdocs.yml`. A strict build reports
pages omitted from navigation, broken internal references, and invalid
configuration.

## Test

Build exactly as continuous integration does:

```console
make docs
```

Also crawl links in the generated site:

```console
make docs-linkcheck
```

## API reference

`docs/_scripts/gen_api_reference.py` discovers public modules under
`src/python_project_foundry/`. It creates virtual Markdown pages containing
mkdocstrings directives during each build. Do not edit generated pages under
`reference/api/`; edit source docstrings or the generation script instead.

## Publish

The Documentation workflow builds pull requests without deploying them. A
successful documentation build on `main` uploads the static site and deploys it
to the `github-pages` environment.

Before the first deployment, select **GitHub Actions** as the Pages source under
the repository's **Settings → Pages** page. No deployment branch or GitHub
secret is required.
