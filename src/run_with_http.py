"""
Entry point for running the MCP server with HTTP/SSE transport.
This is specifically designed for cloud deployments (like Zeabur) 
that expect an HTTP server and might set a PORT environment variable.
"""

import os
import sys

# 1. Configure Environment Variables BEFORE importing server
# This ensures that when server module initializes, it picks up these values.

# Force SSE transport for HTTP deployments
os.environ["MCP_TRANSPORT"] = "sse"

# Map PORT (common in PaaS) to MCP_PORT if not already set
if "PORT" in os.environ and "MCP_PORT" not in os.environ:
    os.environ["MCP_PORT"] = os.environ["PORT"]

# Ensure we listen on all interfaces (0.0.0.0) for container access
if "MCP_HOST" not in os.environ:
    os.environ["MCP_HOST"] = "0.0.0.0"

# 2. Import the initialized MCP instance
# Note: server.py will use the env vars set above during import
try:
    from server import mcp
except ImportError:
    # Fallback if running from root directory instead of src
    sys.path.append(os.path.join(os.getcwd(), "src"))
    from server import mcp

if __name__ == "__main__":
    print(f"Starting Taiwan Health MCP (HTTP/SSE Mode)")
    print(f"Host: {os.environ.get('MCP_HOST')}")
    print(f"Port: {os.environ.get('MCP_PORT')}")
    
    # Run the server
    # Transport is already set to 'sse' via env var which server.config picked up, 
    # but we can implement specific run logic here if needed.
    mcp.run(transport="sse")
