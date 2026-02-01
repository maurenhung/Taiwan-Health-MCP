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

# Environment variables for HTTP mode
ENV PYTHONUNBUFFERED=1
ENV MCP_TRANSPORT=http
ENV MCP_HOST=0.0.0.0
ENV MCP_PORT=8000
ENV MCP_PATH=/mcp

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/mcp').read()" || exit 1

# Start the server using the HTTP runner script
CMD ["python", "run_with_http.py"]