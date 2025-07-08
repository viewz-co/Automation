# Playwright Python Framework

A comprehensive end-to-end testing framework built with Playwright and Python, featuring TestRail integration, Page Object Model (POM), and AI-powered automation via MCP server.

## 🚀 Features

### Core Testing Framework
- **Playwright Python**: Modern browser automation
- **Page Object Model (POM)**: Maintainable and scalable test structure
- **TestRail Integration**: Automated test reporting with screenshots
- **Screenshot on Failure**: Automatic capture and reporting
- **Multi-browser Support**: Chrome, Firefox, Safari
- **Async/Await**: High-performance test execution

### AI-Powered Automation
- **Playwright MCP Server**: Browser automation for AI agents
- **AI Test Generation**: Generate tests from requirements
- **Intelligent Debugging**: AI-assisted failure analysis
- **Cross-platform Testing**: Automated testing across browsers

## 📁 Project Structure

```
playwright_python_framework/
├── api/                        # API test utilities
│   ├── __init__.py
│   └── bot_detection_api.py
├── configs/                    # Configuration files
│   ├── env_config.json         # Environment settings
│   ├── playwright.config.py    # Playwright configuration
│   ├── testrail_config.py      # TestRail settings
│   └── playwright_mcp_config.json # MCP server config
├── docs/                       # Documentation
│   ├── TestRail_Integration.md
│   └── Playwright_MCP_Guide.md
├── fixtures/                   # Test data
│   └── test_data.json
├── pages/                      # Page Object Model
│   ├── __init__.py
│   ├── login_page.py
│   ├── home_page.py
│   ├── vizion_AI_page.py
│   ├── reconciliation_page.py
│   ├── ledger_page.py
│   ├── BI_analysis_page.py
│   └── connection_page.py
├── reports/                    # Test reports
│   └── test_report.html
├── screenshots/                # Failure screenshots
├── scripts/                    # Utility scripts
│   ├── start_mcp_server.sh     # Start MCP server
│   └── test_mcp_installation.sh # Test MCP setup
├── tests/                      # Test files
│   ├── conftest.py             # Test configuration
│   ├── api/
│   │   └── test_access_behavior.py
│   └── e2e/
│       ├── test_login.py
│       ├── test_tabs_navigation.py
│       └── test_tabs_navigation_single_login.py
├── utils/                      # Utilities
│   ├── helpers.py
│   ├── testrail_integration.py
│   └── screenshot_helper.py
├── requirements.txt            # Python dependencies
└── README.md
```

## 🛠️ Installation

### Prerequisites
- Python 3.8+
- Node.js 18+ (for MCP server)
- Git

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/viewz-co/Automation.git
   cd playwright_python_framework
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install Playwright browsers**
   ```bash
   playwright install
   ```

5. **Install MCP server** (for AI automation)
   ```bash
   npm install -g @playwright/mcp@latest
   ```

6. **Verify installation**
   ```bash
   ./scripts/test_mcp_installation.sh
   ```

## 🧪 Running Tests

### Basic Test Execution

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/e2e/test_login.py

# Run with HTML report
pytest --html=reports/test_report.html

# Run with TestRail integration
export TESTRAIL_ENABLED=true
pytest tests/e2e/
```

### Test Categories

- **E2E Tests**: End-to-end user workflows
- **API Tests**: Backend API validation
- **Cross-browser**: Multi-browser compatibility

## 🔗 TestRail Integration

### Setup
1. Configure environment variables:
   ```bash
   export TESTRAIL_URL="https://viewz.testrail.io/"
   export TESTRAIL_USERNAME="automation@viewz.co"
   export TESTRAIL_PASSWORD="your_password"
   export TESTRAIL_PROJECT_ID="1"
   export TESTRAIL_SUITE_ID="4"
   export TESTRAIL_ENABLED="true"
   ```

2. Run tests with automatic reporting:
   ```bash
   pytest tests/e2e/
   ```

### Features
- ✅ **Automatic test run creation**
- 📸 **Screenshots on failure**
- ⏱️ **Execution time tracking**
- 📝 **Detailed failure reports**
- 🔄 **Real-time status updates**

## 🤖 AI-Powered Automation (MCP Server)

### Quick Start

1. **Start the MCP server**
   ```bash
   ./scripts/start_mcp_server.sh
   ```

2. **Configure your AI client**
   - **Cursor**: Add to `~/.cursor/mcp.json`
   - **Claude Desktop**: Add to Claude config
   - **Claude Code**: `claude mcp add playwright npx @playwright/mcp@latest`

3. **Use AI commands**
   ```javascript
   // AI can now control your browser:
   browser_navigate("https://viewz.co")
   browser_snapshot()  // Understand page structure
   browser_click("Login button", "button[data-testid='login']")
   browser_type("Email field", "input[type='email']", "user@example.com")
   browser_take_screenshot("result.png")
   ```

### MCP Server Features
- 🖥️ **Browser Control**: Navigate, click, type, screenshot
- 📊 **Page Analysis**: Accessibility snapshots and structure
- 🔄 **Tab Management**: Multi-tab automation
- 📁 **File Operations**: Upload/download handling
- 🧪 **Test Generation**: AI-created test scenarios

## 📖 Documentation

- **[TestRail Integration Guide](docs/TestRail_Integration.md)**: Complete setup and usage
- **[Playwright MCP Guide](docs/Playwright_MCP_Guide.md)**: AI automation setup
- **[Page Object Model](pages/)**: POM implementation examples

## 🔧 Configuration

### Environment Configuration
Edit `configs/env_config.json`:
```json
{
  "dev": {
    "base_url": "https://dev.viewz.co",
    "timeout": 30000
  },
  "prod": {
    "base_url": "https://viewz.co",
    "timeout": 30000
  }
}
```

### TestRail Configuration
Set up in `configs/testrail_config.py` or environment variables.

### MCP Server Configuration
Customize `configs/playwright_mcp_config.json` for AI automation needs.

## 🎯 Test Examples

### Login Test
```python
@pytest.mark.asyncio
async def test_login(perform_login):
    page = perform_login
    login_page = LoginPage(page)
    assert await login_page.is_logged_in()
```

### Tab Navigation Test
```python
@pytest.mark.asyncio
async def test_tab_navigation(perform_login):
    page = perform_login
    await page.click("text=BI Analysis")
    bi_page = BIAnalysisPage(page)
    assert await bi_page.is_loaded()
```

### AI-Generated Test (via MCP)
```javascript
// AI can generate tests like this:
browser_generate_playwright_test(
  "Login Flow Test",
  "Test user login with valid credentials",
  ["Navigate to login", "Enter credentials", "Verify dashboard"]
)
```

## 🛡️ Security

- **Environment Variables**: Sensitive data in env vars
- **Git Secrets**: No credentials in repository
- **TestRail Security**: API key rotation
- **MCP Security**: Network restrictions and sandboxing

## 🚀 CI/CD Integration

```yaml
# GitHub Actions example
- name: Run Playwright Tests
  run: |
    export TESTRAIL_ENABLED=true
    pytest tests/e2e/ --html=reports/test_report.html
    
- name: Upload Test Results
  uses: actions/upload-artifact@v3
  with:
    name: test-results
    path: |
      reports/
      screenshots/
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License.

## 🆘 Support

- **Issues**: [GitHub Issues](https://github.com/viewz-co/Automation/issues)
- **Documentation**: See `docs/` directory
- **TestRail**: Contact automation team
- **MCP Server**: See Playwright MCP documentation

---

**Built with ❤️ by the Viewz Automation Team**
