"""
Entry point for running the MCP server with HTTP/streamable-http transport.
Optimized for cloud deployments (Zeabur, Heroku, Railway, etc.)

This script:
1. Sets up environment variables for HTTP mode
2. Properly initializes the MCP server
3. Provides a stable FastAPI/uvicorn HTTP endpoint
"""

import os
import sys
import logging

# Configure logging early
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 1. Configure Environment Variables BEFORE importing server
logger.info("Configuring environment variables...")

# Set transport mode to http (streamable-http)
os.environ["MCP_TRANSPORT"] = "http"

# Map PORT environment variable (common in PaaS platforms)
if "PORT" in os.environ and "MCP_PORT" not in os.environ:
    os.environ["MCP_PORT"] = os.environ["PORT"]
    logger.info(f"Mapped PORT={os.environ['PORT']} to MCP_PORT")

# Default MCP_PORT if not set
if "MCP_PORT" not in os.environ:
    os.environ["MCP_PORT"] = "8000"

# Ensure we listen on all interfaces (0.0.0.0) for container access
if "MCP_HOST" not in os.environ:
    os.environ["MCP_HOST"] = "0.0.0.0"

# Set HTTP path
if "MCP_PATH" not in os.environ:
    os.environ["MCP_PATH"] = "/mcp"

logger.info(f"MCP_HOST: {os.environ['MCP_HOST']}")
logger.info(f"MCP_PORT: {os.environ['MCP_PORT']}")
logger.info(f"MCP_PATH: {os.environ['MCP_PATH']}")

# 2. Import the MCP server instance
# Note: server.py will use the env vars set above during import
try:
    # Ensure src is in path
    src_dir = os.path.dirname(os.path.abspath(__file__))
    if src_dir not in sys.path:
        sys.path.insert(0, src_dir)
    
    from server import mcp
    logger.info("Successfully imported MCP server")
except ImportError as e:
    logger.error(f"Failed to import MCP server: {e}")
    sys.exit(1)

if __name__ == "__main__":
    host = os.environ.get("MCP_HOST", "0.0.0.0")
    port = int(os.environ.get("MCP_PORT", "8000"))
    
    logger.info("=" * 60)
    logger.info("🏥 Taiwan Health MCP Server - HTTP Mode")
    logger.info("=" * 60)
    logger.info(f"Starting server on http://{host}:{port}")
    logger.info(f"MCP endpoint: http://{host}:{port}{os.environ.get('MCP_PATH', '/mcp')}")
    logger.info("=" * 60)
    
    try:
        # Run with streamable-http transport
        mcp.run(transport="streamable-http")
    except Exception as e:
        logger.error(f"Server failed to start: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)