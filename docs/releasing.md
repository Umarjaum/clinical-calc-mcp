# Releasing and publishing to PyPI

Version `0.1.0` is currently published on [PyPI](https://pypi.org/project/clinical-calc-mcp/). It includes the original three calculator tools. Version `0.2.0` adds three further tools, expanded safety and client documentation, and a Docker build; it is not published yet. PyPI releases are immutable, so a version number must never be reused.

The repository contains a GitHub Actions workflow for **PyPI Trusted Publishing**. Before using it, the PyPI account owner must register the GitHub publisher once and create the matching GitHub environment. No API token is needed in GitHub.

## One-time Trusted Publisher setup

Sign in to the PyPI account that owns `clinical-calc-mcp` and open [Manage account → Publishing](https://pypi.org/manage/account/publishing/). Add a publisher with these exact values:

| PyPI field | Value |
| --- | --- |
| PyPI Project Name | `clinical-calc-mcp` |
| Owner | `Umarjaum` |
| Repository name | `clinical-calc-mcp` |
| Workflow name | `publish.yml` |
| Environment name | `pypi` |

Then open the repository's **Settings → Environments** on GitHub and create the environment `pypi`. Required reviewers may be added if the owner wants a manual approval gate before each release. Ensure the publisher environment name and workflow name match exactly. In the workflow, only the publish job receives `id-token: write`; the build/test job does not have publishing permissions.

## Release 0.2.0

After the `0.2.0` source is merged to `main`, the maintainer should run the release checks below, confirm the PyPI Trusted Publisher and `pypi` environment are configured, and then create and push tag `v0.2.0`. The tag starts the GitHub Actions build, tests, metadata validation, and publish jobs. The published package can then be installed using:

```bash
python -m pip install --upgrade clinical-calc-mcp
```

or launched directly by a local MCP client with uv:

```bash
uvx --from clinical-calc-mcp clinical-calc-mcp
```

Do not push the tag until the matching publisher has been added to the PyPI account; without it, the OIDC publish job will fail. If a version has already been uploaded, increment the package version before attempting any later release. Do not manually rerun an upload for an already-published version.

## Local release checks

From a clean checkout with development dependencies installed:

```bash
uv sync --extra dev
uv run pytest
uv run ruff check .
uv run python -m build
uv run twine check dist/*
```

The GitHub workflow does not publish to TestPyPI or create a GitHub Release automatically. A maintainer can create a GitHub release separately after verifying the PyPI publication.

## PyPI project

The live package page and download statistics are available at [pypi.org/project/clinical-calc-mcp](https://pypi.org/project/clinical-calc-mcp/).
