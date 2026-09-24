# Connect `clinical-calc-mcp` to an AI client

`clinical-calc-mcp` is a local **stdio MCP server**. It can run in an AI application that supports starting local MCP commands using standard input and output [1]. MCP standardizes the connection, but each AI app chooses which MCP transports it supports. A website or hosted AI that accepts only remote HTTP servers cannot launch a process on your computer; this package does not provide an internet-facing endpoint.

## One-time setup

Install [uv](https://docs.astral.sh/uv/), which provides the `uvx` command for running a Python tool [4]. Until version `0.2.0` is published to PyPI, use the GitHub source command below to get the current six-tool version. After `0.2.0` is released, you can replace the GitHub URL in each `--from` argument with `clinical-calc-mcp` to install from PyPI. Alternatively, install a release using pip and set `command` to the full path of the installed `clinical-calc-mcp` executable.

Quick local check:

```bash
uvx --from git+https://github.com/Umarjaum/clinical-calc-mcp.git clinical-calc-mcp
```

The command starts an MCP stdio process rather than an interactive terminal application. Stop it with Ctrl-C when testing manually. It needs internet access when `uvx` first downloads the source from GitHub and dependencies from PyPI. Once the dependencies are cached, it runs locally; calculation inputs are not sent to this project or another service.

## Docker (optional)

If Docker is installed, build a non-root local image:

```bash
docker build -t clinical-calc-mcp:local .
```

Use it as a local stdio server in an MCP client that supports command-based container launch:

```json
{
  "mcpServers": {
    "clinical-calc-mcp": {
      "command": "docker",
      "args": ["run", "--rm", "-i", "clinical-calc-mcp:local"]
    }
  }
}
```

The image runs the same local calculation server. Review the Dockerfile and rebuild the image when updating the package. This container is not a remotely hosted MCP endpoint.

## Claude Desktop

Open **Settings → Developer → Edit Config** in Claude Desktop. Add this entry inside the existing `mcpServers` object, save the JSON file, and restart or reload the application [1]:

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

Use Claude Desktop's **Developer** settings to locate its active configuration file; paths vary by operating system. The executable must be available to the application. If it cannot find `uvx`, replace `"uvx"` with the full path returned by `which uvx` on macOS/Linux or `where.exe uvx` on Windows.

## Cursor

Create or edit `.cursor/mcp.json` in a project, or use `~/.cursor/mcp.json` for a global server. Cursor documents both standard-input servers and their configuration fields [2]. Add:

```json
{
  "mcpServers": {
    "clinical-calc-mcp": {
      "type": "stdio",
      "command": "uvx",
      "args": ["--from", "git+https://github.com/Umarjaum/clinical-calc-mcp.git", "clinical-calc-mcp"]
    }
  }
}
```

Reload or restart the MCP client, then check that the server is enabled and its tools are listed in Cursor's MCP controls.

## Visual Studio Code

For a workspace configuration, create `.vscode/mcp.json` with the VS Code `servers` format documented by Visual Studio Code [3]:

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

Open the file and use VS Code's MCP controls or the Command Palette to start and inspect the server. VS Code also supports user-profile configuration. See the current VS Code MCP documentation for its profile and workspace options.

## Other compatible clients

For a client whose schema uses an `mcpServers` map, the generic entry is:

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

Follow the client’s own instructions for configuration location, whether a `type` field is required, and how to enable or reload tools. Do not copy a configuration intended for a different application without checking its schema.

## Confirm and troubleshoot

After startup, confirm that the client lists these six tools: `parkland_formula`, `bsa_mosteller`, `vital_signs_summary`, `drip_rate_calculator`, `temperature_converter`, and `weight_converter`. If the tools do not appear, check that uv is installed, `uvx` is on the client’s process path, and the client can reach GitHub and PyPI for the initial install. Look at the client’s MCP/server logs for startup or JSON configuration errors. A missing tool in one client does not imply that a remote AI provider supports local MCP.

For an isolated calculation test, ask the client to convert `37 C` to Fahrenheit or calculate the mathematical summary for a blood pressure of `120/80 mmHg` and a heart rate of `80 bpm`. Check the tool’s units and safety notice. Do not provide protected health information unless your organization authorizes that use of the AI client.

## Sources

[1]: https://modelcontextprotocol.io/docs/2026-07-28/develop/connect-local-servers "Connect to local MCP servers — Model Context Protocol"
[2]: https://cursor.com/docs/mcp "MCP — Cursor Documentation"
[3]: https://code.visualstudio.com/docs/agent-customization/mcp-servers "Add and manage MCP servers — Visual Studio Code"
[4]: https://docs.astral.sh/uv/guides/tools/ "Installing tools — uv Documentation"
