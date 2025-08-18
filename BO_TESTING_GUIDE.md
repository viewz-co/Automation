# 🎯 BO Environment Testing Guide

## 📋 Overview

This guide covers the BO (Back Office) environment testing framework that provides:

1. **BO Login with OTP** - Admin authentication to BO environment
2. **Accounts Navigation** - Access to accounts management page
3. **Account Relogin** - Relogin functionality with OTP for specific accounts
4. **Sanity Testing** - Automated regression tests after relogin
5. **Complete Workflow** - End-to-end BO testing automation

---

## 🔧 Configuration

### BO Environment Configuration
**File**: `configs/bo_env_config.json`

```json
{
  "base_url": "https://bo.viewz.co",
  "username": "sharonadmin",
  "password": "V1ewz345%$#",
  "otp_secret": "ME2DIJTWJNSGEOJSKJDUI6LSNY3SC2C3",
  "environment_name": "BO"
}
```

### Security Note
The BO configuration contains sensitive credentials. In production:
- Use environment variables instead of hardcoded values
- Store OTP secrets securely
- Implement proper access controls

---

## 🚀 Quick Start

### 1. Run Complete BO Workflow
```bash
python run_bo_tests.py complete
```

### 2. Test BO Login Only
```bash
python run_bo_tests.py login
```

### 3. Test Accounts Navigation Only
```bash
python run_bo_tests.py accounts
```

### 4. Run All BO Tests
```bash
python run_bo_tests.py quick
```

---

## 🧪 Test Structure

### Main Test File
**Location**: `tests/e2e/bo/test_bo_complete_flow.py`

### Test Methods

| Test Method | Description | Duration |
|-------------|-------------|----------|
| `test_bo_complete_workflow` | Complete BO flow with all steps | ~5-10 minutes |
| `test_bo_login_only` | BO login verification only | ~1-2 minutes |
| `test_bo_accounts_navigation_only` | Accounts navigation after login | ~2-3 minutes |

### Page Objects

| Page Object | File | Purpose |
|-------------|------|---------|
| `BOLoginPage` | `pages/bo_login_page.py` | BO login and OTP handling |
| `BOAccountsPage` | `pages/bo_accounts_page.py` | Accounts management and relogin |

---

## 🔄 Complete Workflow Steps

The complete BO workflow performs these steps:

### Step 1: BO Login with OTP
- Navigate to https://bo.viewz.co/login
- Enter username: `sharonadmin`
- Enter password: `V1ewz345%$#`
- Generate and enter OTP using secret: `ME2DIJTWJNSGEOJSKJDUI6LSNY3SC2C3`
- Verify successful login

### Step 2: Navigate to Accounts
- Find and click on "Accounts" navigation
- Verify accounts page loads
- Retrieve list of available accounts

### Step 3: Account Relogin
- Select first available account (or specified index)
- Click "Relogin" button for selected account
- Generate and enter OTP for relogin process
- Verify relogin success

### Step 4: Sanity Testing
- **Home Page Verification**: Check if home page loads correctly
- **Navigation Test**: Verify navigation elements are present
- **Responsiveness Test**: Measure page load performance
- **Form Interactions**: Test basic form elements
- **Error Handling**: Verify proper error responses

---

## 🎛️ Advanced Usage

### Manual Test Execution with pytest

```bash
# Run complete workflow
pytest tests/e2e/bo/test_bo_complete_flow.py::TestBOCompleteFlow::test_bo_complete_workflow -v -s

# Run with headless mode
pytest tests/e2e/bo/test_bo_complete_flow.py -v --headless

# Run specific test with detailed output
pytest tests/e2e/bo/test_bo_complete_flow.py::TestBOCompleteFlow::test_bo_login_only -v -s --tb=long
```

### Standalone Execution

```python
# Run from Python script
from tests.e2e.bo.test_bo_complete_flow import run_bo_complete_flow
import asyncio

asyncio.run(run_bo_complete_flow())
```

---

## 📸 Screenshots & Debugging

### Screenshot Naming Convention
All screenshots are automatically captured during test execution:

- `bo_01_initial_login_page.png` - Initial BO login page
- `bo_02_login_success.png` - After successful login
- `bo_03_accounts_page.png` - Accounts page view
- `bo_04_relogin_success.png` - After account relogin
- `bo_05_sanity_tests_complete.png` - Final test completion
- `bo_ERROR_*.png` - Error screenshots for debugging

### Screenshot Locations
- Screenshots saved to: `login_test_screenshots/` or `screenshots/`
- Error screenshots have descriptive names for easy debugging

---

## 🔧 Customization

### Modifying Account Selection
To select a different account for relogin:

```python
# In test_bo_complete_flow.py, modify:
relogin_success = await self.bo_accounts_page.perform_complete_relogin_flow(
    otp_secret=self.bo_config["otp_secret"],
    account_index=1  # Change to desired account index (0-based)
)
```

### Adding Custom Sanity Tests
Add new sanity tests in the `_execute_sanity_tests` method:

```python
# === CUSTOM SANITY TEST ===
print("\n🧪 Custom Sanity Test")
sanity_tests_total += 1
try:
    # Your custom test logic here
    custom_test_passed = await self._my_custom_test(page)
    
    if custom_test_passed:
        sanity_tests_passed += 1
        print("✅ Custom test passed")
    else:
        print("⚠️ Custom test failed")
        
except Exception as e:
    print(f"❌ Custom test error: {str(e)}")
```

### Environment Configuration
For different BO environments, create additional config files:

```bash
# Development BO
configs/bo_dev_config.json

# Staging BO  
configs/bo_staging_config.json

# Production BO
configs/bo_prod_config.json
```

---

## 🐛 Troubleshooting

### Common Issues

#### 1. Login Failures
- **Symptom**: BO login fails or OTP not accepted
- **Solutions**:
  - Verify credentials in `bo_env_config.json`
  - Check OTP secret is correct
  - Ensure BO environment is accessible
  - Check for 2FA page detection selectors

#### 2. Accounts Page Navigation
- **Symptom**: Cannot find or navigate to accounts page
- **Solutions**:
  - Check if accounts navigation exists in BO interface
  - Verify accounts page URL pattern
  - Update navigation selectors in `BOAccountsPage`

#### 3. Relogin Button Not Found
- **Symptom**: Cannot find relogin button for accounts
- **Solutions**:
  - Inspect BO interface for correct button selectors
  - Update relogin button selectors in `BOAccountsPage`
  - Verify account row structure

#### 4. OTP Issues
- **Symptom**: OTP generation or input fails
- **Solutions**:
  - Verify OTP secret format (base32 encoded)
  - Check time synchronization for TOTP
  - Update OTP input selectors

### Debug Mode
For detailed debugging, run tests with verbose output:

```bash
python run_bo_tests.py complete 2>&1 | tee bo_debug.log
```

---

## 🔒 Security Considerations

### Credential Management
- Store sensitive data in environment variables
- Use secure credential storage systems
- Rotate OTP secrets regularly
- Implement access logging

### Test Environment Isolation
- Use dedicated test accounts
- Avoid production data in tests
- Implement test data cleanup
- Monitor test execution logs

---

## 📊 Test Reporting

### Success Criteria
- **Login Success**: BO authentication completes successfully
- **Navigation Success**: Accounts page loads properly
- **Relogin Success**: Account relogin process completes
- **Sanity Tests**: At least 50% of sanity tests pass

### Failure Handling
- Screenshots captured on all failures
- Detailed error messages logged
- Test execution continues where possible
- Graceful degradation for optional features

---

## 🎯 Integration with Existing Framework

### TestRail Integration
BO tests can be integrated with existing TestRail framework:

```python
# Add TestRail case IDs to BO tests
@pytest.mark.testrail_case("C1001")  # BO Login Test Case
async def test_bo_login_only(self, page: Page):
    # Test implementation
```

### Regression Testing
BO tests integrate with existing regression framework:

```bash
# Include BO tests in daily regression
TESTRAIL_ENABLED=true python -m pytest tests/e2e/bo/ -v --headless

# Weekly regression with BO
python -m pytest tests/e2e/bo/ tests/e2e/login/ tests/e2e/navigation/ -v
```

---

## ✅ Success Checklist

Before considering BO testing implementation complete:

- [ ] BO login works with provided credentials
- [ ] OTP generation and input functions correctly
- [ ] Accounts page navigation successful
- [ ] Account selection and relogin works
- [ ] Sanity tests execute and provide meaningful results
- [ ] Screenshots capture all important steps
- [ ] Error handling provides useful debugging information
- [ ] Test execution is reliable and repeatable

---

## 📞 Support

For issues with BO testing:

1. Check screenshots in the debug output
2. Review error logs for specific failure points
3. Verify BO environment accessibility
4. Update selectors if BO interface changes
5. Consult existing framework documentation

---

**Your BO testing framework provides comprehensive automation for admin workflows including authentication, account management, and regression testing!** 🚀
