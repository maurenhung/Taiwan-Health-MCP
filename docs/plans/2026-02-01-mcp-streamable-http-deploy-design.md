# MCP Streamable HTTP Deployment Fix

## Context
Claude Desktop cannot complete MCP initialization against the Zeabur deployment. Logs show requests handled by the FastAPI mock server (`http_server.py`), which only returns placeholder responses. The deployment also sets `MCP_TRANSPORT=http`, which is invalid in the current config and falls back to `stdio`, preventing proper HTTP MCP negotiation.

## Decision (Option A)
Run the real MCP server directly using Streamable HTTP and make the transport configuration robust to the `http` alias. This is the smallest change that enables proper MCP initialization from Claude while preserving the existing URL (`/mcp`).

## Planned Changes
- Docker: run `server.py` directly and set `MCP_TRANSPORT=streamable-http`.
- Healthcheck: use a POST `initialize` call to `/mcp` instead of a GET.
- Config: map `MCP_TRANSPORT=http` to `streamable-http` for backward compatibility.
- Zeabur: set `MCP_TRANSPORT=streamable-http`.

## Verification
- POST initialize to `/mcp` should return MCP `serverInfo` and `capabilities`.
- Claude Desktop should complete `initialize` + `tools/list` without `notifications/cancelled`.

## Risks / Follow-ups
- If Zeabur health checks require GET-only, adjust healthcheck type or disable path checking. A TCP/port check would be sufficient.
