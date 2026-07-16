---
name: mcp-server-builder
description: Scaffold a slim, lightweight custom MCP (Model Context Protocol) server from a plain-language description of what it should do. Use this whenever the user wants to build, create, or wrap something as an MCP server — e.g. "make an MCP server for my ticketing API", "expose these DB queries as MCP tools", "wrap this internal API so Claude can call it", or any request to turn an API/script/data source into MCP tools. Favors the minimal official SDK pattern (Python or TypeScript) over heavyweight frameworks — no unnecessary abstraction layers, no unused transport options, no boilerplate the user didn't ask for.
---
# MCP Server Builder

Build smallest correct MCP server. Every unnecessary dependency, tool, or abstraction is maintenance cost user now owns — default to minimal.

## Workflow

1. **Pin down server shape before writing code.** Ask (batched into one round):
   - What does it wrap? (HTTP API, database, local files, script/CLI)
   - What operations need tool exposure? Get concrete list — don't invent extra tools "for completeness."
   - Read-only or write/mutate? (changes validation and confirmation logic needed)
   - Auth: API key/token needed? Where should it live (env var — never hardcoded)?
   - Language: Python or TypeScript. No preference — pick from surrounding project (`package.json` vs `pyproject.toml`/`requirements.txt`) or default to Python (`mcp` SDK) for lower ceremony.

2. **Scaffold using minimal SDK pattern**, not framework. Read `references/python-minimal.md` or `references/typescript-minimal.md` — each shows smallest correct server (stdio transport, decorator-based tool registration, no unused capabilities).

3. **One tool per real operation, named after what it does, not how implemented.** `get_ticket(ticket_id)` not `query_api(endpoint, params)`. Thin pass-through tools that proxy raw request params push interpretation work back onto the calling model. Design tool signatures around the task, validate inputs at tool boundary, let the underlying client handle actual API/DB call.

4. **Dependencies: only load-bearing.** Official MCP SDK + whatever client the wrapped system needs (`requests`/`httpx` for HTTP, `psycopg2`/`sqlite3` for DB). No web framework, ORM, or config-management library unless description specifically requires it.

5. **Write server, `README.md` with run instructions, and (if secrets involved) `.env.example`** — never real `.env` with live credentials. Tell user where to put actual key.

6. **Verify it starts.** Run server entrypoint, confirm tools register without errors. If live credentials needed, tell user exactly what to set and how to test.

## What "lightweight" means here (and what it doesn't)

Lightweight: minimal dependencies, no unused MCP capabilities, no speculative tools, no premature config abstraction.

Not lightweight: skipping input validation, skipping error handling at tool boundary, hardcoded auth tokens. Tool that crashes on malformed argument or silently swallows upstream API error is broken, not lightweight. Validate at boundary; surface real errors as clear MCP tool errors, not stack traces.

## Reference files

- `references/python-minimal.md` — minimal Python MCP server pattern (stdio transport, `@server.tool()` style)
- `references/typescript-minimal.md` — minimal TypeScript MCP server pattern (`McpServer` + `StdioServerTransport`)

Read only the one matching chosen language — don't load both.