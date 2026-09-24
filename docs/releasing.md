# Releasing and publishing to PyPI

Version `0.1.0` is published on [PyPI](https://pypi.org/project/clinical-calc-mcp/). It was uploaded as a wheel and source archive and verified with a clean `pip install`. The GitHub workflow is prepared to publish future releases through **PyPI Trusted Publishing** (OpenID Connect), so no long-lived PyPI token needs to be stored in GitHub.

## Optional one-time Trusted Publisher setup

To enable future releases from GitHub Actions, sign in to the PyPI account that owns `clinical-calc-mcp` and open [Manage account → Publishing](https://pypi.org/manage/account/publishing/). Add a publisher with these values:

| PyPI field | Value |
| --- | --- |
| PyPI Project Name | `clinical-calc-mcp` |
| Owner | `Umarjaum` |
| Repository name | `clinical-calc-mcp` |
| Workflow name | `publish.yml` |
| Environment name | `pypi` |

In GitHub, open the repository's **Settings → Environments** and create an environment named `pypi`. Optionally add required reviewers as a manual approval gate before each live publish. The environment must match the PyPI publisher configuration. In the workflow, only the publish job receives `id-token: write`; the build-and-test job has no publishing permission.

## Future releases

Do **not** manually run the workflow against the current `0.1.0` package version: PyPI versions are immutable and that version is already published. For each future release, update `project.version` in `pyproject.toml` and add the changes to `CHANGELOG.md`. Run the full test and release checks, commit the changes, and push a version tag matching the package version (for example, `v0.1.1`). Once the Trusted Publisher above is configured, pushing a `v*` tag triggers a test/build job followed by a separate PyPI publish job. PyPI will reject an already-used version; do not retry a published version.

## Local release checks

From a clean checkout with development dependencies installed:

```bash
uv sync --extra dev
uv run pytest
uv run ruff check .
uv run python -m build
uv run twine check dist/*
```

The workflow does not publish to TestPyPI or create a GitHub release automatically. Create a GitHub release separately when desired.
