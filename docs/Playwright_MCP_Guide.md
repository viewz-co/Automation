# Playwright MCP Server Integration Guide

## Overview

The Playwright MCP (Model Context Protocol) server provides browser automation capabilities for AI agents. This integration allows AI assistants to interact with web pages through structured accessibility snapshots, enabling powerful automation workflows.

## Installation

The Playwright MCP server has been installed globally on your system:

```bash
npm install -g @playwright/mcp@latest
```

**Version installed:** 0.0.29

## Configuration

### Server Configuration

The MCP server is configured via `configs/playwright_mcp_config.json`:

```json
{
  "browser": {
    "browserName": "chromium",
    "isolated": false,
    "userDataDir": "./mcp-browser-profile",
    "launchOptions": {
      "channel": "chrome",
      "headless": false,
      "args": ["--start-maximized"]
    },
    "contextOptions": {
      "viewport": null
    }
  },
  "server": {
    "port": 8931,
    "host": "localhost"
  },
  "capabilities": [
    "core", "tabs", "pdf", "history", "wait", "files", "install", "testing"
  ],
  "vision": false,
  "outputDir": "./mcp-output",
  "network": {
    "allowedOrigins": ["https://viewz.co", "https://*.viewz.co"],
    "blockedOrigins": []
  }
}
```

### Key Features

- **Browser**: Chrome with maximized window
- **Profile**: Persistent browser profile for login sessions
- **Port**: Server runs on localhost:8931
- **Output**: Traces and files saved to `./mcp-output/`
- **Network**: Allowed origins configured for Viewz domains

## Starting the Server

### Option 1: Using the Startup Script

```bash
./scripts/start_mcp_server.sh
```

### Option 2: Manual Command

```bash
npx @playwright/mcp@latest \
  --config configs/playwright_mcp_config.json \
  --port 8931 \
  --browser chrome \
  --output-dir ./mcp-output \
  --save-trace
```

### Option 3: Background Server

```bash
npx @playwright/mcp@latest --port 8931 --headless &
```

## MCP Client Configuration

### For Cursor IDE

Add to `~/.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "playwright": {
      "url": "http://localhost:8931/sse"
    }
  }
}
```

### For Claude Desktop

Add to `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "playwright": {
      "command": "npx",
      "args": ["@playwright/mcp@latest"]
    }
  }
}
```

### For Claude Code CLI

```bash
claude mcp add playwright npx @playwright/mcp@latest
```

## Available Tools

### Core Interactions
- **browser_snapshot**: Capture accessibility snapshot of current page
- **browser_click**: Click on web elements
- **browser_type**: Type text into input fields
- **browser_hover**: Hover over elements
- **browser_drag**: Drag and drop operations
- **browser_select_option**: Select dropdown options
- **browser_press_key**: Press keyboard keys
- **browser_wait_for**: Wait for conditions

### Navigation
- **browser_navigate**: Navigate to URLs
- **browser_navigate_back**: Go back in history
- **browser_navigate_forward**: Go forward in history

### Resources
- **browser_take_screenshot**: Capture page screenshots
- **browser_pdf_save**: Save page as PDF
- **browser_network_requests**: Monitor network activity
- **browser_console_messages**: Get console logs

### Tab Management
- **browser_tab_list**: List open tabs
- **browser_tab_new**: Open new tabs
- **browser_tab_select**: Switch between tabs
- **browser_tab_close**: Close tabs

### File Operations
- **browser_file_upload**: Upload files
- **browser_handle_dialog**: Handle browser dialogs

### Testing
- **browser_generate_playwright_test**: Generate test code
- **browser_install**: Install browser binaries
- **browser_close**: Close browser
- **browser_resize**: Resize browser window

## Usage Examples

### Basic Web Automation

```javascript
// AI can use these tools through MCP:
// 1. Navigate to a website
browser_navigate("https://viewz.co")

// 2. Take a snapshot to understand the page
browser_snapshot()

// 3. Click on elements
browser_click("Login button", "button[data-testid='login']")

// 4. Fill forms
browser_type("Email field", "input[type='email']", "user@example.com")

// 5. Take screenshots for documentation
browser_take_screenshot("login_page.png")
```

### Integration with Your Test Framework

The MCP server can complement your existing Playwright Python tests:

1. **Test Generation**: Use `browser_generate_playwright_test` to create new tests
2. **Debugging**: Use `browser_snapshot` and `browser_take_screenshot` for investigation
3. **Data Extraction**: Use `browser_network_requests` to monitor API calls
4. **Cross-browser Testing**: Switch between Chrome, Firefox, and Safari

### AI-Driven Testing Workflows

```python
# Your existing Python tests can be enhanced with AI assistance:
# 1. AI analyzes page structure via MCP
# 2. AI generates new test scenarios
# 3. AI helps debug failing tests
# 4. AI creates documentation from test runs
```

## Advanced Configuration

### Vision Mode

Enable screenshot-based interactions:

```bash
npx @playwright/mcp@latest --vision
```

### Isolated Sessions

Run in isolated mode (no persistent profile):

```bash
npx @playwright/mcp@latest --isolated
```

### Custom Device Emulation

```bash
npx @playwright/mcp@latest --device "iPhone 15"
```

### Proxy Configuration

```bash
npx @playwright/mcp@latest --proxy-server "http://proxy:3128"
```

## Integration with TestRail

The MCP server can enhance your TestRail integration:

1. **Automated Test Creation**: AI generates tests from TestRail requirements
2. **Enhanced Reporting**: Screenshots and traces automatically attached
3. **Intelligent Debugging**: AI analyzes failures and suggests fixes
4. **Cross-platform Testing**: Test scenarios across different browsers

## Troubleshooting

### Common Issues

1. **Port Already in Use**
   ```bash
   lsof -ti:8931 | xargs kill -9
   ```

2. **Browser Not Found**
   ```bash
   npx @playwright/mcp@latest --browser-install
   ```

3. **Permission Errors**
   ```bash
   chmod +x scripts/start_mcp_server.sh
   ```

### Logs and Debugging

- Server logs: Check terminal output
- Browser traces: Saved to `./mcp-output/`
- Network logs: Use `browser_network_requests` tool

## Security Considerations

1. **Network Access**: Limited to allowed origins (Viewz domains)
2. **File Access**: Restricted to output directory
3. **Profile Data**: Stored locally in `./mcp-browser-profile/`
4. **Traces**: May contain sensitive data - review before sharing

## Best Practices

1. **Profile Management**: Use isolated mode for testing, persistent for development
2. **Resource Cleanup**: Always close tabs and browsers when done
3. **Error Handling**: Use wait conditions and timeouts
4. **Performance**: Use headless mode for CI/CD pipelines
5. **Security**: Regularly clear browser profiles and traces

## Next Steps

1. **Start the MCP server**: `./scripts/start_mcp_server.sh`
2. **Configure your AI client** (Cursor, Claude, etc.)
3. **Test basic functionality** with simple navigation commands
4. **Integrate with existing test workflows**
5. **Explore advanced automation scenarios**

## Support and Resources

- **Playwright MCP Documentation**: https://github.com/microsoft/playwright-mcp
- **MCP Protocol Specification**: https://modelcontextprotocol.io/
- **Your Test Framework**: Located in `tests/` directory
- **Configuration Files**: Located in `configs/` directory 