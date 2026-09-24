# Contributing

Contributions that improve correctness, clarity, accessibility, maintainability, or test coverage are welcome. Keep this project narrowly scoped: new calculators should be proposed and reviewed separately, and must not introduce unsupported clinical guidance.

## Development setup

Use Python 3.11 or newer:

```bash
git clone https://github.com/Umarjaum/clinical-calc-mcp.git
cd clinical-calc-mcp
uv sync --extra dev
```

## Before submitting

Run the test suite and lint checks:

```bash
uv run pytest
uv run ruff check .
uv run python -m build
```

Add regression tests for any formula or validation change. Tests should cover representative values, boundary conditions, invalid and non-finite inputs, and expected units. Changes to clinical formulas should cite authoritative sources in the pull request and document assumptions; do not add interpretation or treatment recommendations without an explicit, reviewed scope change.

## Engineering expectations

Maintain Python 3.11 compatibility, type hints, deterministic calculations, finite-number validation, explicit units, and understandable errors. Do not add network access, telemetry, persistence, patient-data logging, dynamic execution, or new runtime dependencies without a clear need and security review. Keep MCP tool names stable; discuss breaking changes before implementing them.

Never include patient-identifying or confidential information in source code, test fixtures, issues, or pull requests. This repository is not a channel for patient-specific clinical advice.

## Pull requests

Describe the change and its rationale, list tests run, explain any user-visible behavior change, and note any added dependency or security consideration. All contributions are subject to review; submitting a pull request does not imply clinical endorsement.
