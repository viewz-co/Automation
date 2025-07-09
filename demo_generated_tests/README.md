# CSV-Generated Test Automation Suite

## Overview
This test suite was automatically generated from CSV test cases on 2025-07-09 09:52:33.

## Statistics
- **Total Test Cases**: 19
- **Sections**: 1
- **Generated Files**: 5 (page objects + tests + config files)

## Test Sections
- **WEB-244 - Navigation**: 19 test cases

## File Structure
```
generated_tests/
├── pages/              # Page Object classes
│   ├── __init__.py
│   └── web-244_-_navigation_page.py
├── tests/              # Test files
│   ├── __init__.py
│   ├── conftest.py
│   └── test_web-244_-_navigation.py
├── fixtures/           # Test data and mappings
│   ├── testrail_csv_mapping.json
│   └── testrail_csv_cases.json
└── README.md
```

## Running Tests

### Prerequisites
1. Install dependencies:
```bash
pip install playwright pytest pytest-asyncio
playwright install
```

2. Set up environment configuration:
```bash
export ENV=dev  # or stage, prod
```

3. Configure TestRail (optional):
```bash
export TESTRAIL_ENABLED=true
export TESTRAIL_URL=https://your-instance.testrail.io
export TESTRAIL_USERNAME=your-username
export TESTRAIL_PASSWORD=your-password
export TESTRAIL_PROJECT_ID=1
export TESTRAIL_SUITE_ID=1
```

### Running All Tests
```bash
pytest generated_tests/tests/ -v
```

### Running Specific Section
```bash
pytest generated_tests/tests/test_section_name.py -v
```

### Running with TestRail Integration
```bash
TESTRAIL_ENABLED=true pytest generated_tests/tests/ -v
```

## TestRail Integration
- **Starting Case ID**: C401
- **Case Mapping**: See `fixtures/testrail_csv_mapping.json`
- **Case Definitions**: See `fixtures/testrail_csv_cases.json`

## Customization
1. **Page Objects**: Modify page object classes in `pages/` directory
2. **Test Logic**: Update test methods in `tests/` directory
3. **Test Data**: Add test data to `fixtures/` directory
4. **Configuration**: Update `conftest.py` for custom setup

## Notes
- Tests are generated with TODO comments for manual implementation
- Screenshots are captured automatically on test failures
- TestRail integration is optional but recommended for reporting
- All generated code includes proper error handling and logging

## Support
For issues with generated tests, check:
1. CSV data format and completeness
2. Environment configuration
3. TestRail connectivity (if enabled)
4. Playwright browser installation
