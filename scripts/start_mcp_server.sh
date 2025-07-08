#!/bin/bash

# Playwright MCP Server Startup Script
# This script starts the Playwright MCP server with custom configuration

echo "🚀 Starting Playwright MCP Server..."
echo "📍 Configuration: configs/playwright_mcp_config.json"
echo "🌐 Server will be available at: http://localhost:8931/sse"
echo ""

# Create output directory if it doesn't exist
mkdir -p mcp-output

# Start the MCP server with configuration
npx @playwright/mcp@latest \
  --config configs/playwright_mcp_config.json \
  --port 8931 \
  --browser chrome \
  --output-dir ./mcp-output \
  --save-trace

echo ""
echo "🏁 Playwright MCP Server stopped." 