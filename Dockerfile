FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project (data + src)
# Note: Ensure .dockerignore excludes large files if needed
COPY . /app

# Set working directory to src for imports
WORKDIR /app/src

# Environment variables for Streamable HTTP mode
ENV PYTHONUNBUFFERED=1
ENV MCP_TRANSPORT=streamable-http
ENV MCP_HOST=0.0.0.0
ENV MCP_PORT=8000
ENV MCP_PATH=/mcp

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import json, urllib.request; req=urllib.request.Request('http://localhost:8000/mcp', data=json.dumps({'jsonrpc':'2.0','id':1,'method':'initialize','params':{'protocolVersion':'2024-11-05','capabilities':{}}}).encode(), headers={'content-type':'application/json'}); urllib.request.urlopen(req, timeout=5).read()" || exit 1

# Start the MCP server directly (Streamable HTTP)
CMD ["python", "server.py"]
