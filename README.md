![clinical-calc-mcp project banner](https://raw.githubusercontent.com/Umarjaum/clinical-calc-mcp/main/assets/clinical-calc-banner.png)

# clinical-calc-mcp

[![clinical-calc-mcp logo](https://raw.githubusercontent.com/Umarjaum/clinical-calc-mcp/main/assets/clinical-calc-mark.png)](https://github.com/Umarjaum/clinical-calc-mcp/blob/main/assets/clinical-calc-mark.png)

[![Tests](https://github.com/Umarjaum/clinical-calc-mcp/actions/workflows/test.yml/badge.svg)](https://github.com/Umarjaum/clinical-calc-mcp/actions/workflows/test.yml)
[![PyPI version](https://img.shields.io/pypi/v/clinical-calc-mcp)](https://pypi.org/project/clinical-calc-mcp/)
[![Python versions](https://img.shields.io/pypi/pyversions/clinical-calc-mcp)](https://pypi.org/project/clinical-calc-mcp/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

A local-only [FastMCP](https://gofastmcp.com/) server providing validated, deterministic clinical calculation tools for nursing and emergency-care education and authorized clinical software workflows.

> **Clinical safety:** This project is a calculation utility, not a diagnostic or treatment-decision system. It does not determine what is appropriate for any particular patient. Clinical decisions must follow current institutional protocols, clinician judgment, and applicable guidance. Verify every input, unit, and result independently.

## Features

- Three focused MCP tools with typed inputs, explicit units, validation, and structured results.
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
| `drip_rate_calculator` | `volume_ml`, `time_hours`, optional `drop_factor` (default `15 gtt/mL`) | `mL/hr`, exact `gtt/min` to 2 decimals, whole-drop `gtt/min` | `mL/hr = volume / time`; `gtt/min = (volume × drop factor) / (hours × 60)`. Whole drops use nearest integer, ties rounded up. A rounded rate is not necessarily clinically appropriate. |

Inputs must be finite numbers greater than zero. TBSA must be at most 100%. Drop factor must be a positive whole number. Invalid inputs produce understandable tool errors; no calculation tool silently substitutes a value.

Results are rounded to two decimal places where applicable. Calculated values outside finite floating-point range fail with a clear error. This package does not add arbitrary demographic or body-size limits.

## Installation

### Install from PyPI

After the first GitHub Trusted Publishing workflow completes successfully, install the latest published release with:

```bash
python -m pip install clinical-calc-mcp
clinical-calc-mcp
```

The package is currently prepared for its first PyPI upload. Until that workflow succeeds, use the GitHub installation below.

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

Add the following server entry to Claude Desktop's MCP configuration file. The command name works when the package is installed in an environment visible to Claude Desktop:

```json
{
  "mcpServers": {
    "clinical-calc-mcp": {
      "command": "clinical-calc-mcp"
    }
  }
}
```

If Claude Desktop cannot find the command, use the full path to the executable inside the environment where you installed the package. To find it, run `which clinical-calc-mcp` on macOS/Linux or `where clinical-calc-mcp` on Windows. Alternatively, configure the environment's Python executable with arguments `-m clinical_calc_mcp` and set the corresponding working directory if your client supports it.

Configuration-file locations can vary by OS and app version. Use the current MCP / developer settings in Claude Desktop to locate or edit its configuration rather than relying on a hard-coded path. Restart or reload the client after changing configuration, then confirm the three tool names appear.

## MCP client configuration

The same stdio command pattern applies to other MCP clients. Example configuration shape:

```json
{
  "mcpServers": {
    "clinical-calc-mcp": {
      "command": "clinical-calc-mcp",
      "args": []
    }
  }
}
```

If installed only inside an isolated virtual environment, point `command` at that environment's `clinical-calc-mcp` executable. The server is local and does not require credentials or a remote endpoint.

## Development

Requirements: Python 3.11 or newer and Git. Clone the repository, then install its development dependencies:

```bash
git clone https://github.com/Umarjaum/clinical-calc-mcp.git
cd clinical-calc-mcp
uv sync --extra dev
```

The runtime is deliberately small: FastMCP and Pydantic. Tests use pytest; Ruff supplies optional lint checks. No external service credentials are needed.

## Release and PyPI publishing

Releases are built and validated in GitHub Actions, then published to PyPI with short-lived OpenID Connect credentials using PyPI Trusted Publishing; no PyPI token is stored in GitHub. Before the first upload, configure the PyPI publisher and the GitHub `pypi` environment using the exact values in [docs/releasing.md](docs/releasing.md). To upload version `0.1.0`, manually run the **publish** workflow from `main`. Future version tags (`v0.1.1`, for example) trigger the same release process after the version and changelog are updated. PyPI versions cannot be overwritten.

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

Tests cover known calculation examples, validation boundaries, NaN/infinity, invalid drop factors, half-up drop rounding, numeric overflow behavior, and exposure of all three MCP tools.

## Project structure

```text
clinical-calc-mcp/
├── .gitignore
├── .python-version
├── assets/
│   ├── clinical-calc-banner.png
│   └── clinical-calc-mark.png
├── .github/dependabot.yml
├── .github/workflows/publish.yml
├── .github/workflows/test.yml
├── docs/
│   ├── clinical-safety.md
│   └── releasing.md
├── src/clinical_calc_mcp/
│   ├── __init__.py
│   ├── __main__.py
│   ├── py.typed
│   └── server.py
├── tests/test_server.py
├── CHANGELOG.md
├── CONTRIBUTING.md
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
