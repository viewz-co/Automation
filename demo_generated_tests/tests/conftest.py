"""
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
        print("\n🔗 TestRail integration enabled for CSV-generated tests")
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
                
                comment = f"{'✅' if report.passed else '❌'} **CSV-Generated Test** - {timestamp}\n\n"
                comment += f"**Test**: {test_name}\n"
                comment += f"**Duration**: {report.duration:.2f}s\n"
                
                if not report.passed and report.longrepr:
                    comment += f"**Error**: {str(report.longrepr)[:500]}..."
                
                testrail.update_test_result(case_number, status, comment)

def pytest_sessionfinish(session, exitstatus):
    """Finalize TestRail integration"""
    if testrail._is_enabled():
        print("\n🏁 Finalizing TestRail integration for CSV-generated tests")
        testrail.finalize_test_run()
