# TestRail Integration Guide

This guide explains how to integrate your Playwright Python framework with TestRail for automated test reporting.

## 🔧 Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure TestRail Credentials

Create environment variables for TestRail connection:

```bash
# TestRail Configuration
export TESTRAIL_ENABLED=true
export TESTRAIL_URL=https://your-company.testrail.io
export TESTRAIL_USERNAME=your-email@company.com
export TESTRAIL_PASSWORD=your-api-key-here
export TESTRAIL_PROJECT_ID=1
export TESTRAIL_SUITE_ID=1
export TESTRAIL_RUN_NAME="Automated Test Run - Playwright Framework"
export TESTRAIL_RUN_DESCRIPTION="Automated test execution from Playwright Python Framework"
```

### 3. Get TestRail API Key

1. Go to TestRail → User Profile → Settings
2. Click "API Keys" tab
3. Generate a new API key
4. Use this key as `TESTRAIL_PASSWORD`

### 4. Find Project and Suite IDs

1. Go to your TestRail project
2. Look at the URL: `https://your-company.testrail.io/index.php?/projects/overview/1`
3. The number at the end is your Project ID
4. Go to Test Suites → Your Suite → URL will show Suite ID

## 📋 Test Case Mapping

Update the case mapping in `tests/conftest.py`:

```python
case_mapping = {
    'test_login': 1,  # Replace with actual TestRail case IDs
    'test_tab_navigation[text=Home-HomePage]': 2,
    'test_tab_navigation[text=Vizion AI-VizionAIPage]': 3,
    'test_tab_navigation[text=Reconciliation-ReconciliationPage]': 4,
    'test_tab_navigation[text=Ledger-LedgerPage]': 5,
    'test_tab_navigation[text=BI Analysis-BIAnalysisPage]': 6,
    'test_tab_navigation[text=Connections-ConnectionPage]': 7,
    'test_tabs_navigation_single_login': 8,
}
```

## 🚀 Usage

### Run Tests with TestRail Integration

```bash
# Enable TestRail integration
export TESTRAIL_ENABLED=true

# Run all tests
python -m pytest tests/ -v

# Run specific test
python -m pytest tests/e2e/test_login.py -v
```

### Run Tests without TestRail Integration

```bash
# Disable TestRail integration (default)
export TESTRAIL_ENABLED=false

# Or simply don't set the environment variable
python -m pytest tests/ -v
```

## 🔍 Features

### Automatic Test Run Creation
- Creates a new test run in TestRail when tests start
- Includes all mapped test cases

### Real-time Result Updates
- Updates test results in TestRail as tests complete
- Includes pass/fail status, comments, and execution time

### Test Run Closure
- Automatically closes the test run when all tests complete

### Status Mapping
- ✅ **PASSED** (1): Test executed successfully
- ❌ **FAILED** (5): Test failed with error details
- ⏸️ **BLOCKED** (2): Test blocked (not implemented)
- 🔄 **RETEST** (4): Test needs to be retested
- ⚪ **UNTESTED** (3): Test not executed

## 📊 TestRail Dashboard

After running tests, you'll see:

1. **New Test Run** created automatically
2. **Test Results** updated in real-time
3. **Execution Details** including:
   - Pass/Fail status
   - Error messages for failed tests
   - Execution time
   - Comments

## 🛠️ Troubleshooting

### Common Issues

1. **Authentication Error**
   - Verify TestRail URL, username, and API key
   - Check if API access is enabled in TestRail

2. **Project/Suite Not Found**
   - Verify Project ID and Suite ID are correct
   - Check user permissions in TestRail

3. **Test Cases Not Found**
   - Verify case IDs in the mapping are correct
   - Check if test cases exist in the specified suite

### Debug Mode

Enable debug logging:
```bash
export TESTRAIL_DEBUG=true
python -m pytest tests/ -v -s
```

## 🔧 Advanced Configuration

### Custom Test Run Names
```bash
export TESTRAIL_RUN_NAME="Sprint 1 - Smoke Tests"
export TESTRAIL_RUN_DESCRIPTION="Automated smoke tests for Sprint 1 features"
```

### Specific Test Cases Only
Modify `testrail.setup_test_run([case_id1, case_id2])` to run only specific cases.

### Custom Status Updates
Use the TestRail API directly for custom status updates:
```python
from configs.testrail_config import TestRailConfig, TestRailStatus

config = TestRailConfig()
config.update_test_result(run_id, case_id, TestRailStatus.PASSED, "Custom comment")
```

## 📈 Benefits

- **Automated Reporting**: No manual test result entry
- **Real-time Updates**: See results as tests execute
- **Detailed Logs**: Error messages and execution times
- **Centralized Tracking**: All test results in one place
- **Historical Data**: Track test trends over time 