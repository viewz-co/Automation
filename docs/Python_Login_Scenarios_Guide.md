# Python Login Scenarios Guide

## Overview

This guide covers **three different Python approaches** to execute the Viewz login scenarios:

1. **Direct Playwright Python** - Standalone script using Playwright Python API
2. **Python MCP Client** - Python script that communicates with MCP server
3. **Traditional Pytest Tests** - Integrated with your existing test framework

## 🐍 **Option 1: Direct Playwright Python (Recommended)**

### Script: `scripts/run_login_scenarios.py`

This is a **standalone Python script** that executes the login scenarios directly using Playwright Python. It doesn't require the MCP server and can run independently.

#### Features:
- ✅ **Complete automation** of login scenarios
- 🔍 **Intelligent page analysis** to find form elements
- 🔑 **Credential discovery** from page content
- 📸 **Automatic screenshots** at each step
- 📊 **Comprehensive reporting** with JSON output
- 🎯 **Assertion generation** for test validation

#### Usage:

```bash
# Run directly
python scripts/run_login_scenarios.py

# Or with pytest
pytest scripts/run_login_scenarios.py -v -s
```

#### What it does:

1. **Navigate** to https://new.viewz.co/login
2. **Analyze** page structure to find email, password, and login button
3. **Scan** for demo credentials on the page
4. **Execute** valid login scenario with discovered/default credentials
5. **Verify** login success by checking URL and page elements
6. **Execute** logout scenario
7. **Verify** logout success
8. **Generate** comprehensive report and assertions

#### Output Files:
- `screenshots/login_page_initial_*.png` - Initial page screenshot
- `screenshots/login_attempt_result_*.png` - After login attempt
- `screenshots/before_logout_*.png` - Before logout
- `screenshots/after_logout_*.png` - After logout
- `screenshots/test_complete_*.png` - Final state
- `fixtures/discovered_selectors.json` - Found form selectors
- `fixtures/discovered_credentials.json` - Found demo credentials
- `fixtures/test_report.json` - Complete test report
- `fixtures/generated_assertions.txt` - Generated test assertions

## 🌐 **Option 2: Python MCP Client**

### Script: `scripts/mcp_python_client.py`

This script **communicates with the running MCP server** via HTTP requests to execute browser automation commands.

#### Prerequisites:
- MCP server must be running: `./scripts/start_mcp_server.sh`
- httpx package: `pip install httpx` (already installed)

#### Usage:

```bash
# Ensure MCP server is running first
./scripts/start_mcp_server.sh

# In another terminal, run the Python client
python scripts/mcp_python_client.py
```

#### Features:
- 🌐 **HTTP communication** with MCP server
- 🔄 **Server health checking** before execution
- 📡 **Command-response pattern** for browser automation
- 📊 **Same comprehensive reporting** as direct approach
- 🛡️ **Error handling** for server communication issues

#### How it works:

```python
# Example MCP commands sent via HTTP:
await client.browser_navigate("https://new.viewz.co/login")
await client.browser_snapshot()  # Get page structure
await client.browser_type("Email field", "input[type='email']", "demo@viewz.co")
await client.browser_click("Login button", "button[type='submit']")
await client.browser_take_screenshot("result.png")
```

## 🧪 **Option 3: Traditional Pytest Tests**

### Script: `tests/e2e/test_login_scenarios.py`

This integrates with your **existing Playwright Python test framework** and includes TestRail integration.

#### Usage:

```bash
# Run with pytest
pytest tests/e2e/test_login_scenarios.py -v

# Run with TestRail integration
export TESTRAIL_ENABLED=true
pytest tests/e2e/test_login_scenarios.py -v
```

#### Features:
- 🧪 **Pytest integration** with fixtures and markers
- 📊 **TestRail reporting** with screenshots
- 🏗️ **Page Object Model** integration
- 🔄 **Reusable test components**
- 📸 **Failure screenshots** automatically captured

## 📋 **Comparison Table**

| Feature | Direct Python | MCP Client | Pytest Tests |
|---------|---------------|------------|--------------|
| **Standalone** | ✅ Yes | ❌ Needs MCP server | ❌ Needs framework |
| **Speed** | 🟢 Fast | 🟡 Medium | 🟢 Fast |
| **Setup** | 🟢 Simple | 🟡 MCP server required | 🟡 Framework setup |
| **AI Integration** | ❌ No | ✅ Yes | ❌ No |
| **TestRail** | ❌ No | ❌ No | ✅ Yes |
| **Screenshots** | ✅ Yes | ✅ Yes | ✅ Yes |
| **Reporting** | ✅ JSON | ✅ JSON | ✅ HTML + TestRail |
| **Page Analysis** | ✅ Comprehensive | 🟡 Basic | ✅ Comprehensive |
| **Credential Discovery** | ✅ Yes | ❌ No | ✅ Yes |

## 🚀 **Quick Start Guide**

### For Immediate Results (Recommended):

```bash
# Option 1: Direct Python execution
python scripts/run_login_scenarios.py
```

### For AI-Powered Automation:

```bash
# Start MCP server
./scripts/start_mcp_server.sh

# In another terminal
python scripts/mcp_python_client.py
```

### For Integration with Existing Tests:

```bash
# Run with your test framework
pytest tests/e2e/test_login_scenarios.py -v -s
```

## 🔧 **Configuration**

### Environment Variables

Set these for custom credentials:

```bash
export VALID_EMAIL="your-test-email@viewz.co"
export VALID_PASSWORD="your-test-password"
```

### Custom Selectors

If the auto-discovery fails, you can modify the selectors in:
- `fixtures/discovered_selectors.json` (after first run)
- Or directly in the script files

### Screenshot Directory

Screenshots are saved to:
- `screenshots/` - For direct Python and pytest
- `mcp-output/` - For MCP server screenshots

## 📊 **Understanding the Output**

### Success Indicators

The scripts check for these login success indicators:
- URL changes from login page
- Presence of "Dashboard", "Welcome", or user menu elements
- Absence of error messages

### Generated Assertions

All scripts generate test assertions you can use:

```javascript
// URL Assertions
expect(page.url).not.toBe('https://new.viewz.co/login');
expect(page.url).toContain('viewz.co');

// Element Assertions
expect(page.locator('input[type="email"]').first).toBeVisible();
expect(page.locator('input[type="password"]').first).toBeVisible();
expect(page.locator('button[type="submit"]').first).toBeVisible();

// Success Assertions
expect(page.locator('text=Dashboard').first).toBeVisible();
expect(page.locator('[data-testid="user-menu"]').first).toBeVisible();
expect(page.locator('text=Logout').first).toBeVisible();
```

## 🛠️ **Troubleshooting**

### Common Issues

1. **"No email field found"**
   - Check if page loaded completely
   - Verify the URL is correct
   - Check network connectivity

2. **"Login failed"**
   - Verify credentials are correct
   - Check for CAPTCHA or additional security
   - Look at error messages in output

3. **"MCP server not running"**
   - Start server: `./scripts/start_mcp_server.sh`
   - Check port 8931 is available
   - Verify Node.js and npm are installed

4. **"Screenshot failed"**
   - Check write permissions in screenshots directory
   - Verify browser is properly launched
   - Check available disk space

### Debug Mode

For more detailed output, modify the scripts:

```python
# In any script, add more verbose logging
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Browser Issues

If browser fails to launch:

```bash
# Install/update browsers
playwright install

# Check browser installation
playwright install --help
```

## 📈 **Advanced Usage**

### Custom Page Analysis

You can extend the page analysis to find specific elements:

```python
# Add to _find_form_elements method
custom_selectors = [
    "[data-testid='custom-login']",
    ".my-custom-class",
    "input[name='custom-field']"
]
```

### Multiple Credential Sets

Test with multiple credential combinations:

```python
credential_sets = [
    ("demo@viewz.co", "demo123"),
    ("test@viewz.co", "test123"),
    ("admin@viewz.co", "admin123")
]

for email, password in credential_sets:
    # Run login scenario
```

### Integration with CI/CD

```yaml
# GitHub Actions example
- name: Run Login Scenarios
  run: |
    python scripts/run_login_scenarios.py
    
- name: Upload Screenshots
  uses: actions/upload-artifact@v3
  with:
    name: login-scenarios-screenshots
    path: screenshots/
```

## 🎯 **Next Steps**

1. **Choose your approach** based on your needs
2. **Run the scenarios** to validate the login flow
3. **Review the generated assertions** for your test suite
4. **Integrate with your CI/CD pipeline**
5. **Extend the scripts** for additional scenarios

## 📚 **Related Documentation**

- [Playwright MCP Guide](Playwright_MCP_Guide.md) - AI automation setup
- [TestRail Integration](TestRail_Integration.md) - Test reporting
- [Main README](../README.md) - Project overview

---

**Happy Testing! 🎉** 