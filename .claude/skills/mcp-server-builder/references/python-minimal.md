# Minimal Python MCP Server

Uses the official `mcp` SDK (`pip install mcp`). Stdio transport — no HTTP server needed for local/Claude Code use.

```python
# server.py
import os
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("my-server-name")

@mcp.tool()
def get_ticket(ticket_id: str) -> dict:
    """Fetch a single ticket by ID from the internal ticketing API."""
    api_key = os.environ["TICKETING_API_KEY"]
    # call the real API here, validate ticket_id, raise a clear error on failure
    ...
    return {"id": ticket_id, "status": "open"}  # shape matches what the caller needs

if __name__ == "__main__":
    mcp.run()
```

`pyproject.toml` (or just `requirements.txt` with `mcp` + whatever client lib is needed):

```toml
[project]
name = "my-server-name"
version = "0.1.0"
dependencies = ["mcp", "httpx"]  # only what's actually used
```

Run locally: `python server.py` (stdio) — register it in the consuming client's MCP config pointing at this entrypoint.

## Rules of thumb

- One `@mcp.tool()` function per operation. Docstring becomes the tool description the model sees — write it for the model, not for a human reading the source.
- Validate arguments inside the tool function; raise `ValueError` (or a clear exception) on bad input rather than letting an upstream client crash with an opaque error.
- Read secrets from `os.environ`, document the required var name in `README.md` / `.env.example`. Never hardcode.
- Don't add `mcp.resource()` or `mcp.prompt()` unless the user's description actually calls for exposing resources or prompt templates — tools alone cover the common "wrap an API" case.
