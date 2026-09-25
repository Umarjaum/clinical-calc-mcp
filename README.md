![clinical-calc-mcp project banner](https://raw.githubusercontent.com/Umarjaum/clinical-calc-mcp/main/assets/clinical-calc-banner.png)

# clinical-calc-mcp

[![clinical-calc-mcp logo](https://raw.githubusercontent.com/Umarjaum/clinical-calc-mcp/main/assets/clinical-calc-mark.png)](https://github.com/Umarjaum/clinical-calc-mcp/blob/main/assets/clinical-calc-mark.png)

[![Tests](https://github.com/Umarjaum/clinical-calc-mcp/actions/workflows/test.yml/badge.svg)](https://github.com/Umarjaum/clinical-calc-mcp/actions/workflows/test.yml)
[![PyPI version](https://img.shields.io/pypi/v/clinical-calc-mcp)](https://pypi.org/project/clinical-calc-mcp/)
[![Python versions](https://img.shields.io/pypi/pyversions/clinical-calc-mcp)](https://pypi.org/project/clinical-calc-mcp/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

A local-only [FastMCP](https://gofastmcp.com/) server providing validated, deterministic clinical calculation tools for nursing and emergency-care education and authorized clinical software workflows. Visit the [project website](https://clinical-calc-mcp.pages.dev/) for quick start instructions, AI client setup, project resources, and contribution information.

> **Clinical safety:** This project is a calculation utility, not a diagnostic or treatment-decision system. It does not determine what is appropriate for any particular patient. Clinical decisions must follow current institutional protocols, clinician judgment, and applicable guidance. Verify every input, unit, and result independently.

## Features

- Six focused MCP tools for common clinical calculations and unit conversions, with typed inputs, explicit units, validation, and structured results.
- Deterministic arithmetic; no external API, database, patient file access, or network access is needed to calculate.
- Clear input errors for non-finite, zero, negative, out-of-range, and inappropriate drop-factor values.
- FastMCP-generated tool schemas; usable with MCP-compatible clients.
- Python 3.11+ package, installable with `pip` or `uv`, with a `clinical-calc-mcp` command.
- No patient data is retained or logged by this application.

## Available tools

| Tool | Inputs | Outputs | Formula and limitations |
| --- | --- | --- | --- |
| `parkland_formula` | `weight_kg`, `tbsa_percentage` | Estimated 24-hour volume, first 8-hour and remaining 16-hour volumes and average rates | Classic formula: `4 mL × kg × %TBSA`. The first 8 hours are conventionally measured from burn time, not arrival. Account for fluid already administered. Protocols may differ; this is not an actual fluid-requirement determination. |
| `bsa_mosteller` | `weight_kg`, `height_cm` | `height_m`, BSA in `m²`, BMI in `kg/m²` | Mosteller: `sqrt((height_cm × weight_kg) / 3600)`. BMI: `weight_kg / height_m²`. No BMI category or diagnosis is given. |
| `vital_signs_summary` | `heart_rate_bpm`, `systolic_bp_mmhg`, `diastolic_bp_mmhg` | Pulse pressure, estimated MAP, shock index | Returns calculations only. It provides no thresholds, risk category, diagnosis, triage, or treatment recommendation. |
| `drip_rate_calculator` | `volume_ml`, `time_hours`, optional `drop_factor` (default `15 gtt/mL`) | `mL/hr`, exact `gtt/min` to 2 decimals, whole-drop `gtt/min` | `mL/hr = volume / time`; `gtt/min = (volume × drop factor) / (hours × 60)`. Whole drops use nearest integer, ties rounded up. A rounded rate is not necessarily clinically appropriate. |
| `temperature_converter` | `temperature`, `from_unit` (`C` or `F`) | Converted temperature | Celsius/Fahrenheit conversion only; temperatures below absolute zero are rejected. No interpretation is provided. |
| `weight_converter` | `weight`, `from_unit` (`kg` or `lb`) | Converted weight | Kilogram/pound conversion only; non-positive weights are rejected. No dosing or interpretation is provided. |

Inputs must be finite, with tool-specific positive-value, unit, and range checks. TBSA cannot exceed 100%; systolic pressure must exceed diastolic pressure; drop factor must be a positive whole number; temperature must be at or above absolute zero. Invalid inputs produce understandable tool errors; no tool silently substitutes a value.

Results are rounded to two decimal places where applicable. Calculated values outside finite floating-point range fail with a clear error. This package does not add arbitrary demographic or body-size limits.

## Installation

### Install from PyPI

Install the latest published release from PyPI with:

```bash
python -m pip install clinical-calc-mcp
clinical-calc-mcp
```

PyPI currently serves version `0.1.0`, which includes the original three tools. The six-tool `0.2.0` source is published on GitHub `main` but is not yet on PyPI. Trusted Publishing setup is documented for the next PyPI release.

To let an MCP client launch the current six-tool GitHub version directly without a separate global install, a client with `uvx` support can run this command (requires [uv](https://docs.astral.sh/uv/)):

```bash
uvx --from git+https://github.com/Umarjaum/clinical-calc-mcp.git clinical-calc-mcp
```

### Install directly from GitHub with pip

```bash
python -m pip install "git+https://github.com/Umarjaum/clinical-calc-mcp.git"
clinical-calc-mcp
```

To install a specific release tag, replace `main` with a tag, for example:

```bash
python -m pip install "clinical-calc-mcp @ git+https://github.com/Umarjaum/clinical-calc-mcp.git@v0.1.0"
```

### Install from a local checkout with pip

```bash
git clone https://github.com/Umarjaum/clinical-calc-mcp.git
cd clinical-calc-mcp
python -m venv .venv
```

Activate the environment:

```bash
# macOS / Linux
source .venv/bin/activate

# Windows PowerShell
.venv\Scripts\Activate.ps1

# Windows Command Prompt
.venv\Scripts\activate.bat
```

Then install and launch:

```bash
python -m pip install .
clinical-calc-mcp
```

For local development, install test and lint tools too:

```bash
python -m pip install -e '.[dev]'
```

### Install with uv

```bash
git clone https://github.com/Umarjaum/clinical-calc-mcp.git
cd clinical-calc-mcp
uv sync
uv run clinical-calc-mcp
```

`uv sync` installs the locked project dependencies from `uv.lock`. For development extras, use `uv sync --extra dev`.

## Running the server

The installed command starts FastMCP using its default **stdio** transport:

```bash
clinical-calc-mcp
```

You can also run it as a Python module:

```bash
python -m clinical_calc_mcp
```

For development from the checkout:

```bash
uv run clinical-calc-mcp
# or, after activating the venv and installing editable:
python -m clinical_calc_mcp
```

Keep the process attached to the MCP client; stdio is a protocol transport, not an interactive terminal interface. Do not add arbitrary shell commands or network-exposed transports to a clinical deployment without a separate security review.

## Claude Desktop integration

To run the current six-tool GitHub version using Claude Desktop, add this server entry to its MCP configuration file:

```json
{
  "mcpServers": {
    "clinical-calc-mcp": {
      "command": "uvx",
      "args": ["--from", "git+https://github.com/Umarjaum/clinical-calc-mcp.git", "clinical-calc-mcp"]
    }
  }
}
```

This configuration requires [uv](https://docs.astral.sh/uv/) and internet access to fetch the source and dependencies. If you have installed the package in a virtual environment instead, replace the command with the full executable path; find it with `which clinical-calc-mcp` on macOS/Linux or `where.exe clinical-calc-mcp` on Windows.

Configuration-file locations can vary by OS and app version. Use the current MCP / developer settings in Claude Desktop to locate or edit the configuration file rather than relying on a hard-coded path. Restart or reload the client after changing configuration, then confirm the six tool names appear.

## Configure other MCP clients

Any AI client that supports launching local MCP servers over stdio can use this package. For Claude Desktop and Cursor, use the following configuration shape:

```json
{
  "mcpServers": {
    "clinical-calc-mcp": {
      "command": "uvx",
      "args": ["--from", "git+https://github.com/Umarjaum/clinical-calc-mcp.git", "clinical-calc-mcp"]
    }
  }
}
```

For VS Code, the workspace `.vscode/mcp.json` format uses a top-level `servers` key and an explicit `stdio` type:

```json
{
  "servers": {
    "clinical-calc-mcp": {
      "type": "stdio",
      "command": "uvx",
      "args": ["--from", "git+https://github.com/Umarjaum/clinical-calc-mcp.git", "clinical-calc-mcp"]
    }
  }
}
```

For tested steps and troubleshooting, see [docs/client-setup.md](docs/client-setup.md). These instructions cover clients that can run local stdio servers. A hosted or browser-only AI that accepts only remote HTTP MCP servers cannot connect to this local package without a separately hosted, secured service; this project does not expose patient calculations over the internet. Do not assume every AI platform supports MCP or local servers.

## Community and project discovery

Read the current [MCP client and catalog compatibility notes](docs/discovery.md). Bug reports and narrow, sourced calculation suggestions are welcome through [GitHub Issues](https://github.com/Umarjaum/clinical-calc-mcp/issues); broader discussion is available in [GitHub Discussions](https://github.com/Umarjaum/clinical-calc-mcp/discussions). Use synthetic examples only—never post patient data, confidential information, or secrets.

## Development

Requirements: Python 3.11 or newer and Git. Clone the repository, then install its development dependencies:

```bash
git clone https://github.com/Umarjaum/clinical-calc-mcp.git
cd clinical-calc-mcp
uv sync --extra dev
```

The runtime is deliberately small: FastMCP and Pydantic. Tests use pytest; Ruff supplies optional lint checks. No external service credentials are needed.

## Release and PyPI publishing

Releases are built and validated in GitHub Actions, then published to PyPI with short-lived OpenID Connect credentials using PyPI Trusted Publishing. The public `0.1.0` release was uploaded directly; configure the publisher and GitHub `pypi` environment in [docs/releasing.md](docs/releasing.md) before using the automated path for a later version. PyPI versions cannot be overwritten.

## Testing

Run the full suite (including an in-memory MCP client handshake/tool call):

```bash
uv run pytest
```

Or use pip in an activated virtual environment:

```bash
python -m pip install -e '.[dev]'
python -m pytest
ruff check .
```

Tests cover known calculation examples, validation boundaries, NaN/infinity, absolute-zero limits, invalid drop factors, half-up drip rounding, numeric overflow behavior, and protocol exposure of all six MCP tools.

## Project structure

```text
clinical-calc-mcp/
├── .dockerignore
├── .gitignore
├── .python-version
├── assets/
│   ├── clinical-calc-banner.png
│   └── clinical-calc-mark.png
├── .github/dependabot.yml
├── .github/ISSUE_TEMPLATE/bug_report.yml
├── .github/ISSUE_TEMPLATE/feature_request.yml
├── .github/workflows/publish.yml
├── .github/workflows/test.yml
├── docs/
│   ├── client-setup.md
│   ├── clinical-safety.md
│   ├── discovery.md
│   └── releasing.md
├── src/clinical_calc_mcp/
│   ├── __init__.py
│   ├── __main__.py
│   ├── py.typed
│   └── server.py
├── tests/test_server.py
├── CHANGELOG.md
├── CITATION.cff
├── CONTRIBUTING.md
├── Dockerfile
├── LICENSE
├── pyproject.toml
├── SECURITY.md
├── uv.lock
└── README.md
```

## Security and privacy model

The calculator functions are deterministic local arithmetic. This application makes no outbound HTTP requests, has no API keys, database, telemetry, or patient-file access, and does not persist or log tool inputs. It does not evaluate user-provided code, execute shell commands, dynamically import modules based on user input, or make external decisions. MCP clients may maintain their own logs or conversation history; review the privacy and retention behavior of the client and deployment environment separately. Do not send identifiable patient data to an AI client unless permitted by your organization's policies.

## Clinical safety notice

This software is provided for calculation support and educational or authorized software workflows only. It is not medical advice, does not diagnose, prescribe, or recommend treatment, and has not been validated for a specific clinical workflow. Mathematical correctness does not establish clinical suitability. Confirm inputs, units, rounding, equipment, current guidance, and institutional protocols with a qualified clinician. The developers and contributors do not assume responsibility for clinical decisions made using this software. See [docs/clinical-safety.md](docs/clinical-safety.md).

## License

Released under the [MIT License](LICENSE). See [CONTRIBUTING.md](CONTRIBUTING.md) for contribution expectations and [CHANGELOG.md](CHANGELOG.md) for release notes.
