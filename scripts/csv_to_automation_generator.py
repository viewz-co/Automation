#!/usr/bin/env python3
"""
CSV to Automation Generator
Converts CSV test cases to Python Playwright automation code with TestRail integration
"""

import csv
import json
import os
import re
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from pathlib import Path

@dataclass
class TestCaseData:
    """Data class to represent a test case from CSV"""
    title: str
    attachments: str
    created_by: str
    created_on: str
    estimate: str
    expected_result: str
    forecast: str
    goals: str
    precondition: str
    priority: str
    references: str
    section: str
    section_depth: str
    section_description: str
    steps: str
    expected_steps: str
    suite: str
    
    def __post_init__(self):
        """Clean and validate data after initialization"""
        # Clean whitespace from all string fields
        for field_name, field_value in asdict(self).items():
            if isinstance(field_value, str):
                setattr(self, field_name, field_value.strip())
    
    @property
    def test_method_name(self) -> str:
        """Generate a valid Python test method name from title"""
        # Remove special characters and convert to snake_case
        name = re.sub(r'[^\w\s]', '', self.title.lower())
        name = re.sub(r'\s+', '_', name)
        name = re.sub(r'_+', '_', name)  # Remove multiple underscores
        return f"test_{name}"
    
    @property
    def page_object_name(self) -> str:
        """Generate page object class name from section"""
        # Convert section to PascalCase
        words = re.findall(r'\b\w+', self.section)
        return ''.join(word.capitalize() for word in words) + 'Page'
    
    @property
    def test_steps_list(self) -> List[str]:
        """Parse steps into a list"""
        if not self.steps:
            return []
        # Split by common delimiters
        steps = re.split(r'[;\n]', self.steps)
        return [step.strip() for step in steps if step.strip()]
    
    @property
    def expected_results_list(self) -> List[str]:
        """Parse expected results into a list"""
        if not self.expected_steps:
            return []
        # Split by common delimiters
        results = re.split(r'[;\n]', self.expected_steps)
        return [result.strip() for result in results if result.strip()]
    
    @property
    def priority_level(self) -> int:
        """Convert priority to TestRail priority ID"""
        priority_map = {
            'low': 1,
            'medium': 2,
            'high': 3,
            'critical': 4
        }
        return priority_map.get(self.priority.lower(), 2)

class CSVToAutomationGenerator:
    """Main class for converting CSV test cases to automation code"""
    
    def __init__(self, csv_file_path: str, output_dir: str = "generated_tests"):
        self.csv_file_path = csv_file_path
        self.output_dir = Path(output_dir)
        self.test_cases: List[TestCaseData] = []
        self.sections: Dict[str, List[TestCaseData]] = {}
        self.testrail_cases: Dict[str, int] = {}
        
        # Create output directory
        self.output_dir.mkdir(exist_ok=True)
        (self.output_dir / "pages").mkdir(exist_ok=True)
        (self.output_dir / "tests").mkdir(exist_ok=True)
        (self.output_dir / "fixtures").mkdir(exist_ok=True)
    
    def parse_csv(self) -> List[TestCaseData]:
        """Parse CSV file and extract test case data"""
        print(f"🔍 Parsing CSV file: {self.csv_file_path}")
        
        try:
            with open(self.csv_file_path, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                
                for row in reader:
                    # Map CSV columns to TestCaseData fields
                    test_case = TestCaseData(
                        title=row.get('Title', ''),
                        attachments=row.get('Attachments', ''),
                        created_by=row.get('Created By', ''),
                        created_on=row.get('Created On', ''),
                        estimate=row.get('Estimate', ''),
                        expected_result=row.get('Expected Result', ''),
                        forecast=row.get('Forecast', ''),
                        goals=row.get('Goals', ''),
                        precondition=row.get('Precondition', ''),
                        priority=row.get('Priority', 'medium'),
                        references=row.get('References', ''),
                        section=row.get('Section', ''),
                        section_depth=row.get('Section Depth', ''),
                        section_description=row.get('Section Description', ''),
                        steps=row.get('Steps', ''),
                        expected_steps=row.get('Expected Steps', ''),
                        suite=row.get('Suite', '')
                    )
                    
                    if test_case.title:  # Only add if title exists
                        self.test_cases.append(test_case)
                        
                        # Group by section
                        section = test_case.section or 'General'
                        if section not in self.sections:
                            self.sections[section] = []
                        self.sections[section].append(test_case)
            
            print(f"✅ Parsed {len(self.test_cases)} test cases from CSV")
            print(f"📁 Found {len(self.sections)} sections: {list(self.sections.keys())}")
            
            return self.test_cases
            
        except Exception as e:
            print(f"❌ Error parsing CSV: {str(e)}")
            return []
    
    def generate_page_objects(self) -> None:
        """Generate page object classes for each section"""
        print(f"🏗️ Generating page objects for {len(self.sections)} sections...")
        
        for section_name, test_cases in self.sections.items():
            page_class_name = test_cases[0].page_object_name
            file_name = f"{section_name.lower().replace(' ', '_')}_page.py"
            file_path = self.output_dir / "pages" / file_name
            
            # Generate page object code
            page_code = self._generate_page_object_code(page_class_name, section_name, test_cases)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(page_code)
            
            print(f"✅ Generated page object: {file_path}")
    
    def _generate_page_object_code(self, class_name: str, section_name: str, test_cases: List[TestCaseData]) -> str:
        """Generate page object class code"""
        
        # Extract unique actions from test steps
        actions = set()
        for test_case in test_cases:
            for step in test_case.test_steps_list:
                # Extract action verbs
                action_words = re.findall(r'\b(click|navigate|enter|verify|select|upload|delete|confirm|open|close|submit|login|logout)\b', step.lower())
                actions.update(action_words)
        
        # Generate method signatures
        methods = []
        for action in sorted(actions):
            method_name = f"{action}_element"
            methods.append(f"""
    async def {method_name}(self, locator: str, value: str = None):
        \"\"\"Perform {action} action on element\"\"\"
        element = self.page.locator(locator)
        await element.wait_for(state="visible", timeout=5000)
        
        if "{action}" == "click":
            await element.click()
        elif "{action}" == "enter" and value:
            await element.fill(value)
        elif "{action}" == "select" and value:
            await element.select_option(value)
        elif "{action}" == "verify":
            await expect(element).to_be_visible()
        # Add more action implementations as needed
        
        await self.page.wait_for_timeout(1000)  # Brief pause for stability""")
        
        return f'''"""
{class_name} - Page Object for {section_name} section
Generated from CSV test cases on {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
"""

from playwright.async_api import Page, expect
from typing import Optional
import asyncio

class {class_name}:
    """Page Object for {section_name} functionality"""
    
    def __init__(self, page: Page):
        self.page = page
        self.section_name = "{section_name}"
    
    async def navigate_to_section(self, base_url: str = None):
        """Navigate to {section_name} section"""
        if base_url:
            section_url = f"{{base_url}}/{section_name.lower().replace(' ', '-')}"
            await self.page.goto(section_url)
        else:
            # Try to find and click navigation link
            nav_locator = f"text={section_name}"
            try:
                await self.page.locator(nav_locator).click()
            except:
                print(f"⚠️ Could not find navigation for {section_name}")
    
    async def wait_for_page_load(self):
        """Wait for page to fully load"""
        await self.page.wait_for_load_state("networkidle")
        await self.page.wait_for_timeout(1000)
    
    async def take_screenshot(self, name: str = None):
        """Take screenshot of current page state"""
        screenshot_name = name or f"{section_name.lower().replace(' ', '_')}_screenshot.png"
        await self.page.screenshot(path=f"screenshots/{{screenshot_name}}")
        return screenshot_name
    
    # Common element interactions
    async def click_button(self, button_text: str):
        """Click button by text"""
        await self.page.get_by_role("button", name=button_text).click()
    
    async def fill_input(self, label: str, value: str):
        """Fill input field by label"""
        await self.page.get_by_label(label).fill(value)
    
    async def verify_text_visible(self, text: str):
        """Verify text is visible on page"""
        await expect(self.page.locator(f"text={{text}}")).to_be_visible()
    
    async def verify_element_visible(self, locator: str):
        """Verify element is visible"""
        await expect(self.page.locator(locator)).to_be_visible()
    
    # Generated action methods
    {''.join(methods)}
    
    # Section-specific methods (customize as needed)
    async def perform_section_action(self, action: str, **kwargs):
        """Perform section-specific action"""
        # Implement section-specific logic here
        print(f"Performing {action} in {section_name} section")
        await self.page.wait_for_timeout(1000)
'''
    
    def generate_test_files(self) -> None:
        """Generate test files for each section"""
        print(f"🧪 Generating test files for {len(self.sections)} sections...")
        
        for section_name, test_cases in self.sections.items():
            file_name = f"test_{section_name.lower().replace(' ', '_')}.py"
            file_path = self.output_dir / "tests" / file_name
            
            # Generate test code
            test_code = self._generate_test_code(section_name, test_cases)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(test_code)
            
            print(f"✅ Generated test file: {file_path}")
    
    def _generate_test_code(self, section_name: str, test_cases: List[TestCaseData]) -> str:
        """Generate test code for a section"""
        
        page_class_name = test_cases[0].page_object_name
        page_import = f"from pages.{section_name.lower().replace(' ', '_')}_page import {page_class_name}"
        
        # Generate individual test methods
        test_methods = []
        for i, test_case in enumerate(test_cases, 1):
            method_code = self._generate_test_method(test_case, page_class_name, i)
            test_methods.append(method_code)
        
        return f'''"""
Test Suite for {section_name} Section
Generated from CSV test cases on {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

Total test cases: {len(test_cases)}
"""

import pytest
import pytest_asyncio
from playwright.async_api import Page, expect
import asyncio
from datetime import datetime

{page_import}
from utils.testrail_integration import testrail_case
from utils.screenshot_helper import screenshot_helper

class Test{section_name.replace(' ', '')}:
    """Test class for {section_name} functionality"""
    
    @pytest_asyncio.fixture
    async def section_page(self, page: Page):
        """Initialize section page object"""
        page_obj = {page_class_name}(page)
        await page_obj.navigate_to_section()
        await page_obj.wait_for_page_load()
        return page_obj
    
    {''.join(test_methods)}
    
    # Helper methods
    async def _verify_test_preconditions(self, test_case_title: str, preconditions: str):
        """Verify test preconditions are met"""
        print(f"🔍 Verifying preconditions for: {{test_case_title}}")
        if preconditions:
            print(f"📋 Preconditions: {{preconditions}}")
        # Add specific precondition checks here
    
    async def _capture_test_evidence(self, page: Page, test_name: str, step: str):
        """Capture screenshots and evidence during test execution"""
        screenshot_name = f"{{test_name}}_{{step.replace(' ', '_').lower()}}.png"
        try:
            await page.screenshot(path=f"screenshots/{{screenshot_name}}")
            print(f"📸 Screenshot captured: {{screenshot_name}}")
        except Exception as e:
            print(f"⚠️ Screenshot failed: {{str(e)}}")
'''
    
    def _generate_test_method(self, test_case: TestCaseData, page_class_name: str, case_number: int) -> str:
        """Generate individual test method"""
        
        # Generate TestRail case ID (you can customize this logic)
        testrail_case_id = f"C{400 + case_number}"  # Starting from C401
        
        # Generate test steps
        test_steps = []
        for i, (step, expected) in enumerate(zip(test_case.test_steps_list, test_case.expected_results_list), 1):
            step_code = f"""
        # Step {i}: {step}
        print(f"📝 Step {i}: {step}")
        await self._capture_test_evidence(page, "{test_case.test_method_name}", "step_{i}")
        
        # TODO: Implement step logic based on: {step}
        # Expected: {expected}
        await section_page.perform_section_action("step_{i}")
        
        # Verify expected result
        # TODO: Add specific verification for: {expected}
        await asyncio.sleep(1)  # Brief pause for stability"""
            test_steps.append(step_code)
        
        return f'''
    @testrail_case("{testrail_case_id}")
    async def {test_case.test_method_name}(self, page: Page, section_page: {page_class_name}):
        """
        Test Case: {test_case.title}
        
        Priority: {test_case.priority}
        Section: {test_case.section}
        
        Preconditions: {test_case.precondition}
        
        Goals: {test_case.goals}
        
        Expected Result: {test_case.expected_result}
        
        Generated TestRail Case ID: {testrail_case_id}
        """
        
        # Verify preconditions
        await self._verify_test_preconditions("{test_case.title}", "{test_case.precondition}")
        
        # Test execution
        start_time = datetime.now()
        print(f"🚀 Starting test: {test_case.title}")
        
        try:
            {''.join(test_steps)}
            
            # Final verification
            print(f"✅ Test completed successfully: {test_case.title}")
            
        except Exception as e:
            print(f"❌ Test failed: {test_case.title} - {{str(e)}}")
            await self._capture_test_evidence(page, "{test_case.test_method_name}", "failure")
            raise
        
        finally:
            duration = (datetime.now() - start_time).total_seconds()
            print(f"⏱️ Test duration: {{duration:.2f}}s")
'''
    
    def generate_testrail_mapping(self) -> None:
        """Generate TestRail case mapping file"""
        print("🔗 Generating TestRail case mapping...")
        
        mapping = {}
        case_definitions = {}
        
        for i, test_case in enumerate(self.test_cases, 1):
            case_id = f"C{400 + i}"  # Starting from C401
            
            mapping[test_case.test_method_name] = case_id
            
            case_definitions[case_id] = {
                "title": test_case.title,
                "section": test_case.section,
                "priority": test_case.priority_level,
                "description": test_case.goals or test_case.title,
                "preconditions": test_case.precondition,
                "expected_result": test_case.expected_result,
                "steps": test_case.test_steps_list,
                "expected_steps": test_case.expected_results_list,
                "created_from_csv": True,
                "csv_row_number": i
            }
        
        # Save mapping file
        mapping_file = self.output_dir / "fixtures" / "testrail_csv_mapping.json"
        with open(mapping_file, 'w', encoding='utf-8') as f:
            json.dump(mapping, f, indent=2, ensure_ascii=False)
        
        # Save case definitions
        cases_file = self.output_dir / "fixtures" / "testrail_csv_cases.json"
        with open(cases_file, 'w', encoding='utf-8') as f:
            json.dump(case_definitions, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Generated TestRail mapping: {mapping_file}")
        print(f"✅ Generated case definitions: {cases_file}")
    
    def generate_conftest(self) -> None:
        """Generate conftest.py for the generated tests"""
        print("⚙️ Generating conftest.py...")
        
        conftest_code = '''"""
Generated conftest.py for CSV-based test automation
"""

import pytest
import pytest_asyncio
from playwright.async_api import async_playwright
import json
import os
from datetime import datetime
from pathlib import Path

# Import TestRail integration
from utils.testrail_integration import testrail, TestRailStatus
from utils.screenshot_helper import screenshot_helper

# ---------- ENV CONFIG ---------- #
def load_config():
    """Load environment configuration"""
    env = os.getenv("ENV", "dev")
    config_path = Path(__file__).parent.parent / "configs" / "env_config.json"
    
    if config_path.exists():
        with open(config_path) as f:
            return json.load(f)[env]
    else:
        # Default configuration
        return {
            "base_url": "https://example.com",
            "username": "test@example.com",
            "password": "password123"
        }

@pytest.fixture(scope="session")
def env_config():
    return load_config()

# ---------- ASYNC PAGE FIXTURE ---------- #
@pytest_asyncio.fixture
async def page(env_config):
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=False, 
            slow_mo=200, 
            args=["--start-maximized"]
        )
        context = await browser.new_context(
            base_url=env_config["base_url"], 
            viewport=None
        )
        page = await context.new_page()
        
        # Create screenshots directory
        screenshots_dir = Path("screenshots")
        screenshots_dir.mkdir(exist_ok=True)
        
        yield page
        await context.close()
        await browser.close()

# ---------- TESTRAIL INTEGRATION ---------- #
def pytest_configure(config):
    """Setup TestRail integration"""
    if testrail._is_enabled():
        print("\\n🔗 TestRail integration enabled for CSV-generated tests")
        testrail.setup_test_run()

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Update TestRail with test results"""
    outcome = yield
    report = outcome.get_result()
    
    if call.when == 'call':
        # Load CSV-generated TestRail mapping
        mapping_file = Path(__file__).parent / "fixtures" / "testrail_csv_mapping.json"
        
        if mapping_file.exists():
            with open(mapping_file) as f:
                case_mapping = json.load(f)
            
            test_name = item.nodeid.split("::")[-1]
            case_id = case_mapping.get(test_name)
            
            if case_id and testrail._is_enabled():
                # Extract case number from case_id (e.g., "C401" -> 401)
                case_number = int(case_id[1:])
                
                # Get page object for screenshots
                page = None
                if hasattr(item, 'funcargs'):
                    page = item.funcargs.get('page')
                
                # Capture screenshot on failure
                if not report.passed and page:
                    try:
                        filename, info = screenshot_helper.capture_sync_screenshot(page, test_name)
                        print(f"📸 Screenshot captured: {filename}")
                    except Exception as e:
                        print(f"❌ Screenshot failed: {str(e)}")
                
                # Update TestRail
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                status = TestRailStatus.PASSED if report.passed else TestRailStatus.FAILED
                
                comment = f"{'✅' if report.passed else '❌'} **CSV-Generated Test** - {timestamp}\\n\\n"
                comment += f"**Test**: {test_name}\\n"
                comment += f"**Duration**: {report.duration:.2f}s\\n"
                
                if not report.passed and report.longrepr:
                    comment += f"**Error**: {str(report.longrepr)[:500]}..."
                
                testrail.update_test_result(case_number, status, comment)

def pytest_sessionfinish(session, exitstatus):
    """Finalize TestRail integration"""
    if testrail._is_enabled():
        print("\\n🏁 Finalizing TestRail integration for CSV-generated tests")
        testrail.finalize_test_run()
'''
        
        conftest_file = self.output_dir / "tests" / "conftest.py"
        with open(conftest_file, 'w', encoding='utf-8') as f:
            f.write(conftest_code)
        
        print(f"✅ Generated conftest.py: {conftest_file}")
    
    def generate_readme(self) -> None:
        """Generate README for the generated test suite"""
        print("📝 Generating README...")
        
        readme_content = f'''# CSV-Generated Test Automation Suite

## Overview
This test suite was automatically generated from CSV test cases on {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}.

## Statistics
- **Total Test Cases**: {len(self.test_cases)}
- **Sections**: {len(self.sections)}
- **Generated Files**: {len(self.sections) * 2 + 3} (page objects + tests + config files)

## Test Sections
{self._generate_section_summary()}

## File Structure
```
generated_tests/
├── pages/              # Page Object classes
│   ├── __init__.py
{self._generate_file_list("pages")}
├── tests/              # Test files
│   ├── __init__.py
│   ├── conftest.py
{self._generate_file_list("tests")}
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
'''
        
        readme_file = self.output_dir / "README.md"
        with open(readme_file, 'w', encoding='utf-8') as f:
            f.write(readme_content)
        
        print(f"✅ Generated README: {readme_file}")
    
    def _generate_section_summary(self) -> str:
        """Generate section summary for README"""
        summary = []
        for section_name, test_cases in self.sections.items():
            summary.append(f"- **{section_name}**: {len(test_cases)} test cases")
        return '\n'.join(summary)
    
    def _generate_file_list(self, directory: str) -> str:
        """Generate file list for README"""
        files = []
        for section_name in self.sections.keys():
            if directory == "pages":
                files.append(f"│   └── {section_name.lower().replace(' ', '_')}_page.py")
            elif directory == "tests":
                files.append(f"│   └── test_{section_name.lower().replace(' ', '_')}.py")
        return '\n'.join(files)
    
    def generate_all(self) -> None:
        """Generate complete test automation suite from CSV"""
        print("🚀 Starting CSV to Automation Generation...")
        print("=" * 60)
        
        # Parse CSV
        if not self.parse_csv():
            print("❌ Failed to parse CSV file")
            return
        
        # Generate all components
        self.generate_page_objects()
        self.generate_test_files()
        self.generate_testrail_mapping()
        self.generate_conftest()
        self.generate_readme()
        
        # Generate __init__.py files
        self._generate_init_files()
        
        print("\n" + "=" * 60)
        print("✅ CSV to Automation Generation Complete!")
        print(f"📁 Output directory: {self.output_dir}")
        print(f"📊 Generated {len(self.test_cases)} test cases")
        print(f"🏗️ Created {len(self.sections)} page objects")
        print(f"🧪 Created {len(self.sections)} test files")
        print("\n📋 Next Steps:")
        print("1. Review generated code and customize as needed")
        print("2. Implement TODO sections in test methods")
        print("3. Configure environment settings")
        print("4. Run tests with: pytest generated_tests/tests/ -v")
    
    def _generate_init_files(self) -> None:
        """Generate __init__.py files for packages"""
        init_files = [
            self.output_dir / "pages" / "__init__.py",
            self.output_dir / "tests" / "__init__.py",
            self.output_dir / "fixtures" / "__init__.py"
        ]
        
        for init_file in init_files:
            init_file.write_text('"""Generated package init file"""')

def main():
    """Main function for command-line usage"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Generate Playwright automation tests from CSV")
    parser.add_argument("csv_file", help="Path to CSV file containing test cases")
    parser.add_argument("--output", "-o", default="generated_tests", help="Output directory")
    
    args = parser.parse_args()
    
    if not os.path.exists(args.csv_file):
        print(f"❌ CSV file not found: {args.csv_file}")
        return
    
    generator = CSVToAutomationGenerator(args.csv_file, args.output)
    generator.generate_all()

if __name__ == "__main__":
    main() 