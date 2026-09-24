# Releasing and publishing to PyPI

The package is published to PyPI through GitHub Actions with **Trusted Publishing** (OpenID Connect). The workflow does not store a PyPI API token or other long-lived publishing secret in GitHub. Every release candidate is tested, linted, built, and checked before the separate publishing job receives the short-lived OIDC permission.

## One-time PyPI publisher setup

Sign in to the PyPI account that should own `clinical-calc-mcp`, then open [Manage account → Publishing](https://pypi.org/manage/account/publishing/). Add a pending publisher with the following values. For a new project, PyPI creates the project when the first trusted publishing workflow succeeds.

| PyPI field | Value |
| --- | --- |
| PyPI Project Name | `clinical-calc-mcp` |
| Owner | `Umarjaum` |
| Repository name | `clinical-calc-mcp` |
| Workflow name | `publish.yml` |
| Environment name | `pypi` |

In GitHub, open the repository's **Settings → Environments** and create an environment named `pypi`. Optionally configure required reviewers if you want a manual approval gate before each live publish. The environment name must match the PyPI trusted publisher configuration exactly. The publishing workflow grants `id-token: write` only to the publish job; build and test jobs receive no publishing permission.

## First upload of version 0.1.0

The currently configured project version is `0.1.0`. After adding the PyPI trusted publisher and creating the GitHub `pypi` environment, start the workflow from the `main` branch:

1. Open the repository's **Actions** tab and choose **publish**.
2. Select **Run workflow**, leave the branch set to `main`, and start the run.
3. Wait for both jobs to pass. The build job runs pytest and Ruff, builds a wheel and source archive, and checks the distributions; the publish job submits them using PyPI Trusted Publishing.
4. Verify the project at <https://pypi.org/project/clinical-calc-mcp/> and install it with `python -m pip install clinical-calc-mcp`.

Do not run the initial workflow again after version `0.1.0` is uploaded: PyPI releases are immutable and rejects duplicate versions.

## Future releases

For every subsequent release, update `project.version` in `pyproject.toml` and the changelog, run the full local test/build checks, commit the change, and push a version tag that matches the package version (for example, `v0.1.1`). The tag push triggers this workflow. It will build and publish only after tests and distribution validation succeed. Do not reuse a version that already exists on PyPI. If a release fails because a version was partially or previously uploaded, inspect the PyPI project state before changing the version or retrying.

## Local release checks

From a clean checkout with development dependencies installed:

```bash
uv sync --extra dev
uv run pytest
uv run ruff check .
uv run python -m build
uv run twine check dist/*
```

This workflow intentionally does not publish to TestPyPI or automatically create a GitHub release. PyPI publication is the only publication step; create the GitHub release separately when desired.
