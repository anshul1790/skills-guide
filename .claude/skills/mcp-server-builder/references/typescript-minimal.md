# Minimal TypeScript MCP Server

Uses `@modelcontextprotocol/sdk`. Stdio transport.

```ts
// server.ts
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";

const server = new McpServer({ name: "my-server-name", version: "0.1.0" });

server.tool(
  "get_ticket",
  "Fetch a single ticket by ID from the internal ticketing API.",
  { ticket_id: z.string() },
  async ({ ticket_id }) => {
    const apiKey = process.env.TICKETING_API_KEY;
    if (!apiKey) throw new Error("TICKETING_API_KEY not set");
    // call the real API here
    return { content: [{ type: "text", text: JSON.stringify({ id: ticket_id, status: "open" }) }] };
  }
);

await server.connect(new StdioServerTransport());
```

`package.json` dependencies — only what's used:

```json
{
  "dependencies": {
    "@modelcontextprotocol/sdk": "^1.0.0",
    "zod": "^3.23.0"
  }
}
```

Run: `node --experimental-strip-types server.ts` (or compile with `tsc` if the project already has a build step — don't add one just for this).

## Rules of thumb

- One `server.tool(...)` call per operation. The description string is what the model sees — write it for the model.
- Validate input with the `zod` schema in the tool definition itself; that's the boundary, not the tool body.
- Read secrets from `process.env`, document required vars in `.env.example`.
- Skip `server.resource()` / `server.prompt()` unless the user's description specifically needs resources or prompt templates.
