#!/bin/bash

echo "🧪 Testing Playwright MCP Server Installation"
echo "=============================================="
echo ""

# Test 1: Check if npx is available
echo "1️⃣  Checking Node.js and npx..."
if command -v npx &> /dev/null; then
    echo "✅ npx is available"
    node --version
    npm --version
else
    echo "❌ npx not found"
    exit 1
fi
echo ""

# Test 2: Check if Playwright MCP is installed
echo "2️⃣  Checking Playwright MCP installation..."
if npx @playwright/mcp@latest --version &> /dev/null; then
    echo "✅ Playwright MCP is installed"
    npx @playwright/mcp@latest --version
else
    echo "❌ Playwright MCP not found"
    exit 1
fi
echo ""

# Test 3: Check configuration file
echo "3️⃣  Checking configuration file..."
if [ -f "configs/playwright_mcp_config.json" ]; then
    echo "✅ Configuration file exists"
    echo "📁 Location: configs/playwright_mcp_config.json"
else
    echo "❌ Configuration file not found"
    exit 1
fi
echo ""

# Test 4: Validate JSON configuration
echo "4️⃣  Validating JSON configuration..."
if python3 -m json.tool configs/playwright_mcp_config.json > /dev/null 2>&1; then
    echo "✅ Configuration JSON is valid"
else
    echo "❌ Configuration JSON is invalid"
    exit 1
fi
echo ""

# Test 5: Check directories
echo "5️⃣  Checking required directories..."
mkdir -p mcp-output mcp-browser-profile
echo "✅ Created output directories"
echo "📁 mcp-output/ - for traces and files"
echo "📁 mcp-browser-profile/ - for browser profile"
echo ""

# Test 6: Test help command with config
echo "6️⃣  Testing configuration loading..."
if npx @playwright/mcp@latest --config configs/playwright_mcp_config.json --help > /dev/null 2>&1; then
    echo "✅ Configuration loads successfully"
else
    echo "❌ Configuration loading failed"
    exit 1
fi
echo ""

echo "🎉 All tests passed! Playwright MCP Server is ready to use."
echo ""
echo "📚 Next steps:"
echo "   1. Start the server: ./scripts/start_mcp_server.sh"
echo "   2. Configure your AI client (Cursor, Claude, etc.)"
echo "   3. Read the guide: docs/Playwright_MCP_Guide.md"
echo "" 