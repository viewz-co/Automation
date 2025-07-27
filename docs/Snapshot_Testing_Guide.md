# Snapshot Testing Guide

Comprehensive guide for visual, DOM, and API snapshot testing in the Playwright Python framework.

## 🎯 **Overview**

Snapshot testing captures the current state of your application (visually, structurally, or data-wise) and compares it against future runs to detect regressions. This framework implements three types of snapshot testing:

1. **📸 Visual Snapshots** - Screenshot comparison for UI regression detection
2. **🔍 DOM Snapshots** - HTML structure comparison for markup changes
3. **🌐 API Response Snapshots** - API response pattern comparison

## 📁 **Directory Structure**

```
tests/
├── e2e/snapshot/
│   └── test_snapshot_regression.py    # Main snapshot test suite
├── conftest.py                        # TestRail mappings for snapshot tests
snapshots/
├── dom/                              # DOM snapshots storage
├── api/                              # API response snapshots
└── visual/                           # Visual snapshots (auto-generated)
screenshots/                          # Component screenshots
pytest.ini                           # Pytest configuration
playwright.config.js                 # Playwright snapshot settings
```

## 🚀 **Quick Start**

### Run All Snapshot Tests
```bash
# Run complete snapshot test suite
TESTRAIL_ENABLED=true python -m pytest tests/e2e/snapshot/ -v --headless

# Run specific snapshot test type
python -m pytest tests/e2e/snapshot/test_snapshot_regression.py::TestSnapshotRegression::test_visual_snapshots_key_pages -v
```

### Update Snapshots
```bash
# Update all visual snapshots (when UI changes are expected)
python -m pytest tests/e2e/snapshot/ --update-snapshots

# Update specific snapshot
python -m pytest tests/e2e/snapshot/test_snapshot_regression.py::TestSnapshotRegression::test_visual_snapshots_key_pages --update-snapshots
```

## 📸 **Visual Snapshot Testing**

### How It Works
- Captures full page screenshots using Playwright's `to_have_screenshot()`
- Compares pixel-by-pixel with baseline images
- Threshold: 0.1 (10% difference tolerance)
- Automatically handles animations and dynamic content

### Key Features
```python
# Example from test_visual_snapshots_key_pages
await expect(page).to_have_screenshot("home_page_snapshot.png", threshold=0.1)
```

### Pages Covered
- ✅ Home page
- ✅ Reconciliation page
- ✅ Ledger (Financial Dashboard) page

### Best Practices
1. **Consistent Environment**: Always run in same browser/viewport
2. **Disable Animations**: Use `reducedMotion: 'reduce'` in config
3. **Stable Data**: Use test data that doesn't change frequently
4. **Exclude Dynamic Areas**: Clip timestamps, counters, etc.

## 🔍 **DOM Snapshot Testing**

### How It Works
- Captures HTML structure of critical page elements
- Normalizes content (removes dynamic attributes, IDs, styles)
- Stores as `.html` files for comparison
- Detects structural changes in markup

### Critical Elements Monitored
```python
critical_elements = [
    {"page": "Home", "selector": "main", "name": "main_content"},
    {"page": "Home", "selector": "nav, header", "name": "navigation_header"},
    {"page": "Reconciliation", "selector": ".data-container, table", "name": "data_tables"},
    {"page": "Ledger", "selector": ".dashboard, .kpi", "name": "dashboard_kpis"}
]
```

### Normalization Process
- Removes `data-*` attributes
- Strips dynamic `style` attributes
- Removes timestamp-based IDs
- Normalizes whitespace

### Use Cases
- Detect unintentional markup changes
- Monitor critical component structure
- Validate accessibility attributes remain consistent

## 🌐 **API Response Snapshot Testing**

### How It Works
- Intercepts network requests during test execution
- Captures response metadata (status, headers, patterns)
- Groups by endpoint patterns
- Stores normalized response data as JSON

### What's Captured
```python
normalized_resp = {
    'status': resp['status'],
    'headers_count': len(resp['headers']),
    'has_auth_header': 'authorization' in headers,
    'content_type': resp['headers'].get('content-type', 'unknown')
}
```

### Endpoints Monitored
- `/api/*` - Main API endpoints
- `/auth/*` - Authentication endpoints
- `/data/*` - Data retrieval endpoints

### Use Cases
- Detect API contract changes
- Monitor authentication flow changes
- Validate response structure consistency

## 🧩 **Component Snapshot Testing**

### Individual Component Screenshots
Captures isolated screenshots of specific UI components:

- **Login Form** - Authentication UI
- **Navigation Menu** - Main navigation structure
- **Data Tables** - Reconciliation data displays
- **Dashboard KPIs** - Financial metrics widgets

### Benefits
- Granular change detection
- Component-level regression testing
- Design system consistency validation

## 🔄 **Snapshot Comparison Workflow**

### Workflow Test
The `test_snapshot_comparison_workflow` demonstrates:
1. **Baseline Capture** - Initial page state
2. **Change Simulation** - Scroll/interaction
3. **Difference Detection** - Expected changes caught
4. **State Reset** - Return to baseline
5. **Consistency Verification** - Matches original

## ⚙️ **Configuration**

### Playwright Settings (`playwright.config.js`)
```javascript
expect: {
  toHaveScreenshot: {
    threshold: 0.1,              // 10% difference tolerance
    animations: 'disabled',      // Disable animations for consistency
  }
}
```

### Pytest Settings (`pytest.ini`)
```ini
markers =
    snapshot: marks tests as snapshot tests for visual regression

# Snapshot testing settings
snapshot_update = false
snapshot_threshold = 0.1
```

### TestRail Integration
```python
# conftest.py mappings
'test_visual_snapshots_key_pages': 8066,
'test_dom_snapshots_critical_elements': 8067,
'test_api_response_snapshots': 8068,
'test_component_snapshots': 8069,
'test_snapshot_comparison_workflow': 8070,
```

## 📊 **TestRail Integration**

### Test Case Mapping
| Test Method | TestRail ID | Description |
|-------------|-------------|-------------|
| `test_visual_snapshots_key_pages` | C8066 | Visual regression testing for key application pages |
| `test_dom_snapshots_critical_elements` | C8067 | DOM structure monitoring for critical elements |
| `test_api_response_snapshots` | C8068 | API response pattern validation |
| `test_component_snapshots` | C8069 | Individual component visual testing |
| `test_snapshot_comparison_workflow` | C8070 | Snapshot testing workflow validation |

### Execution Reporting
- ✅ **Pass**: Snapshots match within threshold
- ❌ **Fail**: Differences detected beyond threshold
- 📸 **Screenshots**: Failure screenshots auto-captured
- 📊 **TestRail**: Results automatically updated

## 🛠️ **Troubleshooting**

### Common Issues

#### 1. **Snapshot Mismatches**
```bash
# Update snapshots if changes are expected
python -m pytest --update-snapshots

# Increase threshold for minor differences
await expect(page).to_have_screenshot("test.png", threshold=0.2)
```

#### 2. **Dynamic Content Issues**
```python
# Wait for content to stabilize
await asyncio.sleep(2)

# Hide dynamic elements
await page.add_style_tag(content=".timestamp { display: none !important; }")
```

#### 3. **Cross-Platform Differences**
- Use consistent OS/browser for CI/CD
- Consider separate snapshot sets per platform
- Increase threshold for minor rendering differences

#### 4. **Animation Interference**
```javascript
// In playwright.config.js
use: {
  reducedMotion: 'reduce',
  animations: 'disabled'
}
```

### Debugging Tips

1. **View Diff Images**: Check `test-results/` for visual diffs
2. **Manual Inspection**: Compare snapshots manually in file system
3. **Gradual Updates**: Update one snapshot at a time
4. **Environment Consistency**: Ensure same browser/OS/viewport

## 📈 **CI/CD Integration**

### Pipeline Configuration
```yaml
# Example GitHub Actions
- name: Run Snapshot Tests
  run: |
    python -m pytest tests/e2e/snapshot/ --headless
    
- name: Upload Diff Images
  if: failure()
  uses: actions/upload-artifact@v3
  with:
    name: snapshot-diffs
    path: test-results/
```

### Best Practices for CI
1. **Consistent Environment**: Use same browser versions
2. **Baseline Management**: Store approved snapshots in version control
3. **Review Process**: Require manual review for snapshot updates
4. **Parallel Execution**: Run snapshot tests in isolated workers

## 🎯 **Success Metrics**

### Coverage Goals
- ✅ **Visual**: 3+ key pages covered
- ✅ **DOM**: 4+ critical elements monitored  
- ✅ **API**: All major endpoints tracked
- ✅ **Components**: Core UI components tested

### Quality Metrics
- **Regression Detection**: Catch 95%+ of visual regressions
- **False Positives**: < 5% failure rate from environmental differences
- **Coverage**: 100% of critical user paths include snapshot validation
- **Maintenance**: Snapshot updates required < 10% of deployments

## 🚀 **Advanced Usage**

### Custom Snapshot Helpers
```python
# Custom snapshot with exclusions
async def take_stable_snapshot(page, name, exclude_selectors=[]):
    for selector in exclude_selectors:
        await page.add_style_tag(content=f"{selector} {{ visibility: hidden !important; }}")
    
    await expect(page).to_have_screenshot(f"{name}.png", threshold=0.1)
```

### Conditional Snapshots
```python
# Only snapshot in stable environments
if os.getenv('SNAPSHOT_MODE') == 'update':
    await expect(page).to_have_screenshot("test.png")
else:
    # Just validate without snapshot comparison
    assert await page.locator("main").is_visible()
```

### Cross-Browser Snapshots
```python
# Compare across different browsers
@pytest.mark.parametrize("browser", ["chromium", "firefox", "webkit"])
async def test_cross_browser_snapshot(browser, page):
    await expect(page).to_have_screenshot(f"page_{browser}.png")
```

## 📚 **Related Documentation**

- [Playwright Visual Testing Guide](https://playwright.dev/docs/test-screenshots)
- [TestRail Integration Documentation](./TestRail_Complete_Integration.md)
- [Performance Testing Guide](./Performance_Testing_Guide.md)
- [Browser Compatibility Testing](./Browser_Compatibility_Guide.md)

---

**📧 Support**: For questions about snapshot testing, check the troubleshooting section above or review the test implementation in `tests/e2e/snapshot/test_snapshot_regression.py`. 