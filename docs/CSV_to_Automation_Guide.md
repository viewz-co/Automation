# CSV to Automation Generator Guide

## Overview
The CSV to Automation Generator is a powerful tool that converts CSV test cases into complete Python Playwright automation code with TestRail integration. This guide explains how to use it effectively.

## Features

### 🚀 Core Capabilities
- **CSV Parsing**: Automatically parses CSV files with test case data
- **Page Object Generation**: Creates Page Object Model (POM) classes for each section
- **Test Code Generation**: Generates complete Playwright test methods
- **TestRail Integration**: Automatic TestRail case mapping and reporting
- **Documentation**: Generates comprehensive README and documentation
- **Error Handling**: Built-in error handling and screenshot capture

### 📊 Supported CSV Format
The generator expects CSV files with the following columns:

| Column | Description | Required |
|--------|-------------|----------|
| Title | Test case title | ✅ |
| Section | Test section/category | ✅ |
| Steps | Test steps (semicolon separated) | ✅ |
| Expected Steps | Expected results (semicolon separated) | ✅ |
| Precondition | Test preconditions | ❌ |
| Priority | Test priority (Low/Medium/High/Critical) | ❌ |
| Goals | Test objectives | ❌ |
| Expected Result | Overall expected result | ❌ |
| Created By | Test author | ❌ |
| Suite | Test suite name | ❌ |

## Quick Start

### 1. Prepare Your CSV File
Create a CSV file with your test cases. Here's a sample format:

```csv
Title,Section,Steps,Expected Steps,Precondition,Priority,Goals
"Login Test","Authentication","Navigate to login page; Enter credentials; Click login","Page loads; Credentials accepted; User logged in","Valid credentials available","High","Verify login functionality"
"Upload File","File Management","Click upload button; Select file; Confirm upload","Upload dialog opens; File selected; Upload successful","User is logged in","Medium","Test file upload"
```

### 2. Generate Automation Code
```bash
# Using the generator script directly
python3 scripts/csv_to_automation_generator.py your_test_cases.csv

# Using the demo script
python3 demo_csv_to_automation.py
```

### 3. Review Generated Code
The generator creates a complete test suite structure:
```
generated_tests/
├── pages/           # Page Object classes
├── tests/           # Test files with pytest methods
├── fixtures/        # TestRail mappings and test data
└── README.md        # Generated documentation
```

### 4. Customize and Run
1. Review generated page objects and customize locators
2. Implement TODO sections in test methods
3. Configure environment settings
4. Run tests: `pytest generated_tests/tests/ -v`

## Detailed Usage

### Command Line Interface
```bash
# Basic usage
python3 scripts/csv_to_automation_generator.py input.csv

# Custom output directory
python3 scripts/csv_to_automation_generator.py input.csv --output my_tests

# Show help
python3 scripts/csv_to_automation_generator.py --help
```

### Demo Script Options
```bash
# Generate tests from sample CSV
python3 demo_csv_to_automation.py

# Run generated tests
python3 demo_csv_to_automation.py --run-tests

# Show help
python3 demo_csv_to_automation.py --help
```

## Generated Components

### 1. Page Objects
**File**: `pages/section_name_page.py`

Each section gets its own page object class with:
- Navigation methods
- Common element interactions
- Action methods based on test steps
- Screenshot capabilities
- Section-specific methods

**Example**:
```python
class PayablesSectionPage:
    def __init__(self, page: Page):
        self.page = page
    
    async def navigate_to_section(self):
        # Navigation logic
    
    async def click_upload_button(self):
        # Upload button interaction
    
    async def verify_invoice_list(self):
        # Invoice list verification
```

### 2. Test Methods
**File**: `tests/test_section_name.py`

Each test case becomes a pytest method with:
- TestRail case ID decoration
- Comprehensive docstring
- Step-by-step execution
- Error handling and screenshots
- Precondition verification

**Example**:
```python
@testrail_case("C401")
async def test_verify_invoice_list_is_displayed(self, page: Page, section_page: PayablesSectionPage):
    """
    Test Case: Verify invoice list is displayed
    Priority: Medium
    Section: Payables Section
    """
    # Test implementation with TODO comments
```

### 3. TestRail Integration
**Files**: 
- `fixtures/testrail_csv_mapping.json` - Test name to case ID mapping
- `fixtures/testrail_csv_cases.json` - Complete case definitions

**Features**:
- Automatic case ID assignment (starting from C401)
- Priority mapping
- Step-by-step case definitions
- Result reporting integration

### 4. Configuration
**File**: `tests/conftest.py`

Includes:
- Playwright browser setup
- TestRail integration hooks
- Screenshot capture on failure
- Environment configuration

## TestRail Integration

### Case ID Assignment
- **Starting ID**: C401 (configurable)
- **Increment**: Sequential (C401, C402, C403, ...)
- **Mapping**: Stored in `fixtures/testrail_csv_mapping.json`

### Priority Mapping
| CSV Priority | TestRail Priority ID |
|--------------|---------------------|
| Low | 1 |
| Medium | 2 |
| High | 3 |
| Critical | 4 |

### Environment Variables
```bash
export TESTRAIL_ENABLED=true
export TESTRAIL_URL=https://your-instance.testrail.io
export TESTRAIL_USERNAME=your-username
export TESTRAIL_PASSWORD=your-password
export TESTRAIL_PROJECT_ID=1
export TESTRAIL_SUITE_ID=1
```

## Customization Guide

### 1. Page Object Customization
After generation, customize page objects:

```python
# Add specific locators
class PayablesSectionPage:
    # Locators
    UPLOAD_BUTTON = "button[data-testid='upload-btn']"
    INVOICE_LIST = ".invoice-list-container"
    
    async def click_upload_button(self):
        await self.page.locator(self.UPLOAD_BUTTON).click()
    
    async def verify_invoice_list_displayed(self):
        await expect(self.page.locator(self.INVOICE_LIST)).to_be_visible()
```

### 2. Test Method Implementation
Replace TODO comments with actual test logic:

```python
async def test_upload_invoice_file(self, page: Page, section_page: PayablesSectionPage):
    # Step 1: Click Upload button
    await section_page.click_upload_button()
    
    # Step 2: Select PDF file
    await page.set_input_files("input[type='file']", "test_invoice.pdf")
    
    # Step 3: Verify upload success
    await section_page.verify_upload_success()
```

### 3. Environment Configuration
Create `configs/env_config.json`:

```json
{
  "dev": {
    "base_url": "https://dev.example.com",
    "username": "test@example.com",
    "password": "testpass123"
  },
  "stage": {
    "base_url": "https://stage.example.com",
    "username": "stage@example.com",
    "password": "stagepass123"
  }
}
```

## Best Practices

### 1. CSV Preparation
- **Clear Titles**: Use descriptive test case titles
- **Logical Sections**: Group related tests in sections
- **Detailed Steps**: Break down complex actions into steps
- **Specific Expected Results**: Define clear success criteria
- **Consistent Format**: Use consistent terminology and structure

### 2. Test Organization
- **One Section per Page Object**: Keep page objects focused
- **Meaningful Test Names**: Use descriptive method names
- **Proper Assertions**: Add specific verification steps
- **Error Handling**: Implement proper exception handling

### 3. Maintenance
- **Regular Updates**: Keep generated code updated with CSV changes
- **Version Control**: Track changes to both CSV and generated code
- **Documentation**: Update README files with customizations
- **Testing**: Regularly run generated tests to ensure functionality

## Troubleshooting

### Common Issues

#### 1. CSV Parsing Errors
**Problem**: CSV file not parsed correctly
**Solution**: 
- Check CSV format and encoding (UTF-8 recommended)
- Ensure required columns are present
- Verify data doesn't contain special characters

#### 2. Generated Code Errors
**Problem**: Syntax errors in generated code
**Solution**:
- Check for special characters in CSV data
- Verify section names are valid Python identifiers
- Review generated file structure

#### 3. TestRail Integration Issues
**Problem**: TestRail cases not created/updated
**Solution**:
- Verify TestRail credentials and permissions
- Check project and suite IDs
- Ensure TestRail API is accessible

#### 4. Test Execution Failures
**Problem**: Generated tests fail to run
**Solution**:
- Implement TODO sections in test methods
- Add proper locators to page objects
- Configure environment settings
- Install required dependencies

### Debug Mode
Enable debug logging:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Examples

### Sample CSV Data
See `sample_test_cases.csv` for a complete example with 19 test cases covering:
- Invoice list verification
- File upload functionality
- Menu operations
- Form validation
- Status updates

### Generated Output
Run the demo to see complete generated output:
```bash
python3 demo_csv_to_automation.py
```

### Integration Example
```python
# Custom integration in your existing framework
from scripts.csv_to_automation_generator import CSVToAutomationGenerator

generator = CSVToAutomationGenerator("my_tests.csv", "custom_output")
generator.generate_all()

# Access generated data
test_cases = generator.test_cases
sections = generator.sections
```

## Advanced Features

### 1. Custom Templates
Modify the generator to use custom templates:
```python
def _generate_custom_page_object(self, class_name, section_name, test_cases):
    # Custom page object template
    return custom_template
```

### 2. Multiple CSV Files
Process multiple CSV files:
```python
for csv_file in csv_files:
    generator = CSVToAutomationGenerator(csv_file, f"output_{csv_file}")
    generator.generate_all()
```

### 3. Custom TestRail Mapping
Override default TestRail case ID assignment:
```python
def custom_case_id_generator(test_case, index):
    return f"CUSTOM_{index:03d}"
```

## Support and Contribution

### Getting Help
1. Check this documentation
2. Review generated README files
3. Examine sample CSV and generated output
4. Check troubleshooting section

### Contributing
1. Fork the repository
2. Create feature branch
3. Add tests for new functionality
4. Submit pull request

### Reporting Issues
Include:
- CSV file sample (anonymized)
- Error messages
- Generated code output
- Environment details

---

**Note**: This generator is designed to create a solid foundation for automation tests. Manual customization is expected and encouraged to match your specific application requirements. 