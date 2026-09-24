# Project discovery and directory readiness

`clinical-calc-mcp` is installable from PyPI and can be started as a local stdio MCP process. This fits compatible desktop and developer clients. It does not make the package compatible with every AI product: clients that accept only remote HTTP servers cannot start a process on a user's computer [1]. No one can make all AI clients use a third-party server automatically.

## MCP client reach

The project supplies setup steps for Claude Desktop, Cursor, and VS Code in [client-setup.md](client-setup.md). Other clients may use it if they support local stdio MCP commands and the documented command configuration. A hosted endpoint is not provided and should not be added without a security and privacy design review.

## Public catalogs reviewed

| Catalog | Current fit | Status and next step |
| --- | --- | --- |
| Glama open-source server directory | A local server can be listed from its GitHub source, subject to maintainer ownership verification and successful build, sandbox execution, and tool-schema inspection. | The repository now has a Dockerfile to help produce a reproducible build. A maintainer with GitHub write/admin access would need to sign in and submit the repository. This project has not been listed. [2] |
| Smithery | Local stdio servers are distributed as MCPB bundles. A PyPI package or bare command is not its local upload artifact; its URL path expects hosted Streamable HTTP. | A valid MCPB bundle is not included. Do not deploy an unauthenticated remote endpoint just to obtain a listing. [3] |
| PulseMCP | The directory currently accepts no new submissions and recommends publishing to the Official MCP Registry. | Wait until PulseMCP reopens. The page was updated September 3, 2026. [4] |
| Official MCP Registry | PyPI packages using stdio are supported, but publishing requires a server manifest, a namespace ownership marker, publisher authentication, and a new immutable version. | **Not submitted.** The registry terms prohibit uses where use or failure of the registry could lead to death or personal injury. Because this project documents healthcare workflows, do not submit it there unless the maintainer completes and approves a specific legal and intended-use review. [5] |

A listing is not an endorsement, verification of clinical suitability, or an installation mandate. Directory listings should accurately describe the local-only calculations and their limits.

## Ready-to-use directory description

> `clinical-calc-mcp` is a local Python Model Context Protocol server with six deterministic tools: classic Parkland-formula arithmetic, Mosteller BSA and BMI, pulse pressure and estimated MAP and shock-index calculations (without interpretation), infusion-rate arithmetic, Celsius/Fahrenheit conversion, and kilogram/pound conversion. The server runs locally over stdio, validates units and numeric inputs, and makes no calculation-time network calls. It does not diagnose, recommend treatment, determine an appropriate dose, or assess clinical suitability. Intended for education and independently governed software workflows only.

Before submitting this description anywhere, confirm that the destination permits healthcare-oriented software and check its current terms and submission process.

## References

[1]: https://modelcontextprotocol.io/docs/2026-07-28/develop/connect-local-servers "Connect to local MCP servers — Model Context Protocol"
[2]: https://glama.ai/mcp/methodology "How Glama indexes the MCP ecosystem"
[3]: https://smithery.ai/docs/build/publish "Publish an MCP server — Smithery"
[4]: https://www.pulsemcp.com/submit "Submit a new MCP server or client — PulseMCP"
[5]: https://modelcontextprotocol.io/registry/terms-of-service "Official MCP Registry Terms of Service"
