# BO Snapshot Testing Guide

Comprehensive guide for BO (Back Office) environment snapshot testing including visual, DOM, workflow, and component snapshots.

## 🎯 **Overview**

BO Snapshot testing extends the framework's snapshot capabilities to cover the BO environment at `https://bo.viewz.co`. This includes specialized testing for:

1. **📸 BO Visual Snapshots** - Complete page screenshots for UI regression detection
2. **🔍 BO DOM Snapshots** - HTML structure comparison for BO-specific elements
3. **🔄 BO Workflow Snapshots** - Step-by-step visual documentation of BO processes
4. **🧩 BO Component Snapshots** - Individual BO UI component testing

## 📁 **Directory Structure**

```
tests/
├── e2e/bo/
│   ├── test_bo_complete_flow.py       # Main BO workflow tests
│   └── test_bo_snapshots.py           # BO snapshot test suite
configs/
├── bo_env_config.json                # BO environment configuration
snapshots/
├── visual/                           # BO visual snapshots
│   ├── bo_bo_login_snapshot.png
│   ├── bo_bo_accounts_snapshot.png
│   ├── bo_workflow_01_login.png
│   └── bo_workflow_02_accounts.png
├── dom/                              # BO DOM snapshots
│   └── bo_dom_snapshot_*.html
└── api/                              # BO API snapshots (if needed)
pages/
├── bo_login_page.py                  # BO login page object
└── bo_accounts_page.py               # BO accounts page object
```

## 🚀 **Quick Start**

### Run All BO Snapshot Tests
```bash
# Set TestRail environment
export TESTRAIL_ENABLED=true
export TESTRAIL_URL=https://viewz.testrail.io
export TESTRAIL_USERNAME=automation@viewz.co
export TESTRAIL_PASSWORD='your_password'

# Run complete BO snapshot suite
source venv/bin/activate
python3 run_bo_tests.py snapshots
```

### Run Specific BO Snapshot Types
```bash
# Visual snapshots only
python3 run_bo_tests.py visual

# Workflow snapshots only
python3 run_bo_tests.py workflow

# Component snapshots only
python3 run_bo_tests.py components

# DOM snapshots only
python3 run_bo_tests.py dom
```

## 📸 **BO Visual Snapshot Testing**

### How It Works
Captures full page screenshots of key BO pages:

- **BO Login Page** - Initial authentication interface
- **BO Accounts Page** - Account management dashboard after login
- **BO Account Detail** - Individual account views (if accessible)

### Test Coverage
```python
@testrail_case(27985)  # BO Visual Snapshots
async def test_bo_visual_snapshots(self, page: Page):
    """Test visual snapshots of key BO pages"""
```

### What's Captured
- Login page state before authentication
- Accounts management page after successful login
- Full page screenshots with proper wait times
- Screenshot files stored in `snapshots/visual/`

### Use Cases
- Detect BO UI regressions
- Monitor BO layout changes
- Validate BO visual consistency
- Document BO interface evolution

## 🔍 **BO DOM Snapshot Testing**

### Critical BO Elements
Captures HTML structure of BO-specific elements:

- **BO Header/Navigation** - Main BO navigation structure
- **BO Accounts Table** - Account data table HTML
- **BO Main Content** - Primary content areas
- **BO Sidebar** - Navigation sidebar elements
- **BO Action Buttons** - Relogin and management buttons

### Test Coverage
```python
@testrail_case(27986)  # BO DOM Snapshots  
async def test_bo_dom_snapshots(self, page: Page):
    """Test DOM snapshots of critical BO elements"""
```

### Normalization
BO DOM content is normalized to remove:
- Session IDs and JWT tokens
- Dynamic timestamps
- User-specific data attributes
- Temporary style attributes

### Benefits
- Detect BO structural changes
- Monitor BO element consistency
- Validate BO HTML integrity
- Track BO markup evolution

## 🔄 **BO Workflow Snapshot Testing**

### Workflow Steps Captured
Documents the complete BO process:

1. **Step 1: Login Page** - `bo_workflow_01_login.png`
2. **Step 2: Accounts Page** - `bo_workflow_02_accounts.png`
3. **Step 3: Account Selection** - `bo_workflow_03_account_selection.png`
4. **Step 4: Relogin Process** - `bo_workflow_04_relogin_success.png`

### Test Coverage
```python
@testrail_case(27987)  # BO Workflow Snapshots
async def test_bo_workflow_snapshots(self, page: Page):
    """Test snapshots throughout the BO workflow process"""
```

### Process Documentation
- Visual documentation of each workflow step
- Evidence of successful BO process completion
- Step-by-step regression detection
- Process consistency validation

### Use Cases
- Document BO workflow for training
- Detect process flow changes
- Validate workflow consistency
- Provide visual evidence for testing

## 🧩 **BO Component Snapshot Testing**

### BO Components Tested
Individual BO UI elements:

- **BO Login Form** - Authentication form component
- **BO Navigation Header** - Main navigation structure
- **BO Accounts Table** - Data table component
- **BO Action Buttons** - Relogin and action buttons
- **BO User Menu** - User management menu

### Test Coverage
```python
@testrail_case(27988)  # BO Component Snapshots
async def test_bo_component_snapshots(self, page: Page):
    """Test snapshots of specific BO UI components"""
```

### Component Isolation
- Individual component screenshots
- Granular change detection
- Component-level regression testing
- Design system consistency

### Benefits
- Detect component-specific changes
- Validate component consistency
- Monitor design system adherence
- Enable component-level testing

## ⚙️ **BO Configuration**

### BO Environment Settings
```json
{
  "base_url": "https://bo.viewz.co",
  "username": "sharonadmin",
  "password": "V1ewz345%$#",
  "otp_secret": "H5YH2NKOIJJSYJTGK5LGQSZGLVFFWSKJ",
  "environment_name": "BO"
}
```

### Playwright BO Settings
- **Viewport**: 1280x720 for consistent snapshots
- **Animations**: Disabled for stable captures
- **Color Scheme**: Light mode for consistency
- **Full Page**: Enabled for workflow snapshots

### TestRail Integration
BO snapshot tests are integrated with TestRail:
- **C27985**: BO Visual Snapshots
- **C27986**: BO DOM Snapshots  
- **C27987**: BO Workflow Snapshots
- **C27988**: BO Component Snapshots

## 🔧 **Available Test Modes**

### BO Test Runner Options
```bash
python3 run_bo_tests.py <mode>
```

**Available Modes:**
- `complete` - Full BO workflow with relogin
- `login` - BO login testing only
- `accounts` - BO accounts navigation only
- `quick` - All BO tests
- `snapshots` - All BO snapshot tests
- `visual` - BO visual snapshots only
- `workflow` - BO workflow snapshots only
- `components` - BO component snapshots only
- `dom` - BO DOM snapshots only

### Test Execution Examples
```bash
# Visual regression testing
python3 run_bo_tests.py visual

# Workflow documentation
python3 run_bo_tests.py workflow

# Component regression testing
python3 run_bo_tests.py components

# Complete BO snapshot suite
python3 run_bo_tests.py snapshots
```

## 📊 **Success Metrics**

### BO Snapshot Coverage Goals
- ✅ **Visual**: 3+ key BO pages covered
- ✅ **DOM**: 5+ critical BO elements monitored
- ✅ **Workflow**: 4-step process documented
- ✅ **Components**: 5+ BO components tested

### Quality Metrics
- **Regression Detection**: Catch 95%+ of BO visual changes
- **Process Documentation**: 100% workflow step coverage
- **Component Coverage**: All critical BO UI elements tested
- **Maintenance**: Snapshot updates required < 10% of deployments

## 🎯 **BO-Specific Features**

### OTP Handling
- TOTP-based OTP generation for authentication
- Multiple time window attempts for reliability
- Secure OTP secret management

### Multi-Window Support
- New window detection for relogin process
- Cross-window session management
- Window-specific snapshot capture

### Account Management
- Account list detection and interaction
- Account selection for relogin testing
- Account-specific workflow documentation

### BO Integration
- BO environment configuration management
- BO-specific page object patterns
- BO workflow automation

## 🚀 **Advanced Usage**

### Custom BO Snapshots
```python
# Custom BO snapshot with specific account
async def capture_bo_account_snapshot(page, account_id):
    await navigate_to_account(account_id)
    await page.screenshot(path=f"snapshots/visual/bo_account_{account_id}.png")
```

### BO Snapshot Comparison
```python
# Compare BO snapshots across environments
def compare_bo_snapshots(prod_snapshot, staging_snapshot):
    # Implement visual comparison logic
    pass
```

### BO Regression Detection
```python
# BO-specific regression detection
async def detect_bo_regressions(baseline_dir, current_dir):
    # Compare BO snapshots for changes
    pass
```

## 📚 **Related Documentation**

- [BO Testing Guide](BO_TESTING_GUIDE.md) - Complete BO testing documentation
- [BO Implementation Summary](BO_IMPLEMENTATION_SUMMARY.md) - Technical implementation details
- [Snapshot Testing Guide](Snapshot_Testing_Guide.md) - General snapshot testing framework
- [Playwright Visual Testing](https://playwright.dev/docs/test-screenshots) - Playwright snapshot capabilities

## 🎉 **Current Status**

**✅ BO Snapshot Testing is fully operational:**

1. **4 Snapshot Test Types** implemented and working
2. **TestRail Integration** ready with case IDs
3. **Multiple Test Modes** available via run script
4. **Visual Evidence** captured and stored properly
5. **Framework Integration** complete with existing patterns

**🎯 BO snapshot testing provides comprehensive visual regression detection and process documentation for the BO environment!**
