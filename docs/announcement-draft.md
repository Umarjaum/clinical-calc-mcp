# Launch announcement draft — not yet published

**Title**

Meet `clinical-calc-mcp`: six local MCP calculation tools for AI clients

**Post**

`clinical-calc-mcp` is an open-source Python MCP server for clients that can run local stdio tools. It now provides six deterministic calculation and conversion tools: Parkland-formula arithmetic, Mosteller BSA/BMI, pulse pressure and estimated MAP and shock index (without interpretation), infusion-rate arithmetic, Celsius/Fahrenheit conversion, and kilogram/pound conversion.

Install from PyPI with `python -m pip install clinical-calc-mcp`, or use `uvx --from clinical-calc-mcp clinical-calc-mcp` from a compatible client. Setup instructions cover Claude Desktop, Cursor, and VS Code.

The project calculates supplied values; it does not diagnose, recommend treatment or doses, or determine clinical suitability. Inputs are processed locally by the server, which does not make calculation-time network requests. Client-specific privacy and retention still apply.

- PyPI: https://pypi.org/project/clinical-calc-mcp/
- Source, documentation, and issues: https://github.com/Umarjaum/clinical-calc-mcp
- License: MIT

**Platform adaptation note**

This draft is a starting point, not a post already published. Review the destination's rules and character limits. Do not claim universal support: it works with AI clients that support local stdio MCP servers. Do not claim medical approval, clinical validation, treatment guidance, or registry endorsement.
