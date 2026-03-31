# Development

## Install Dependencies

The repository uses Poetry for local development:

```bash
poetry install --all-extras --all-groups
```

If you are working inside the existing conda environment, make sure the Poetry
environment or local tooling resolves to the same Python version expected by the
project.

## Run Tests

Canonical test command:

```bash
python -m pytest -q
```

Make target:

```bash
make pytest
```

## Run Docs Locally

Start a local docs server:

```bash
make docs-serve
```

Build the static site:

```bash
make docs-build
```

The build output is written to `site/`.

## Deployment

GitHub Pages deployment is handled by GitHub Actions.
The workflow builds the MkDocs site and publishes the generated static files as
the Pages artifact.

Expected repository settings:

- GitHub Pages source should be set to GitHub Actions
- The workflow needs `pages: write` and `id-token: write` permissions

## Project Layout

- `docs/` contains the MkDocs content
- `mkdocs.yml` defines site navigation and theme
- `.github/workflows/docs.yml` builds and deploys the docs site
- `README.md` remains the concise package landing page
