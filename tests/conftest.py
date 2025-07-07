import pytest
import pytest_asyncio
from playwright.async_api import async_playwright
from playwright.sync_api import sync_playwright
import pyotp
import json
import os
import asyncio
import traceback
from datetime import datetime
from pages.login_page import LoginPage

# Import TestRail integration
from utils.testrail_integration import testrail, TestRailStatus
from utils.screenshot_helper import screenshot_helper

# ---------- ENV CONFIG ---------- #
def load_config():
    env = os.getenv("ENV", "dev")  # export ENV=stage
    with open("configs/env_config.json") as f:
        return json.load(f)[env]

@pytest.fixture(scope="session")
def env_config():
    return load_config()

# ---------- ASYNC PAGE FIXTURE ---------- #
@pytest_asyncio.fixture
async def page(env_config):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, slow_mo=200, args=["--start-maximized"])
        context = await browser.new_context(base_url=env_config["base_url"], viewport=None)
        page = await context.new_page()
        yield page
        await context.close()
        await browser.close()

# ---------- SYNC CONTEXT FIXTURE (optional) ---------- #
@pytest.fixture(scope="session")
def sync_browser_context():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        yield context
        browser.close()

# ---------- LOGIN DATA FIXTURE ---------- #
@pytest.fixture
def login_data():
    fixture_path = os.path.join(
        os.path.dirname(__file__), "../fixtures/test_data.json"
    )
    with open(fixture_path) as f:
        return json.load(f)["login"]

# ---------- PERFORM LOGIN WITH OTP FIXTURE ---------- #
@pytest_asyncio.fixture
async def perform_login(page, login_data):
    login = LoginPage(page)
    await login.goto()
    await login.login(login_data["username"], login_data["password"])

    # הזנת OTP
    secret = "HA2ECLBIKYUEEI2GPUUSMN3XIMXFETRQ"  # החלף אם צריך
    otp = pyotp.TOTP(secret).now()

    await page.wait_for_selector("text=Two-Factor Authentication", timeout=5000)
    await page.get_by_role("textbox").fill(otp)
    await asyncio.sleep(1)
    #await page.get_by_role("button", name="Verify").click()
    await page.wait_for_selector("text=SuccessOTP verified successfully", timeout=5000)

    return page

# ---------- SCREENSHOT FIXTURE ---------- #
@pytest.fixture
def screenshot_on_failure(request):
    """Fixture to capture screenshots on test failure"""
    yield
    
    if request.node.rep_call.failed:
        # Get page from test fixtures
        page = None
        if hasattr(request, 'getfixturevalue'):
            try:
                page = request.getfixturevalue('page')
            except:
                try:
                    page = request.getfixturevalue('perform_login')
                except:
                    pass
        
        if page:
            test_name = request.node.name
            filename, info = screenshot_helper.capture_sync_screenshot(page, test_name)
            if filename:
                print(f"\n📸 Screenshot saved: {filename}")
            else:
                print(f"\n⚠️ Screenshot failed: {info}")

# ---------- TESTRAIL INTEGRATION HOOKS ---------- #
def pytest_configure(config):
    """Setup TestRail integration at the start of test session"""
    if testrail._is_enabled():
        print("\n🔗 TestRail integration enabled")
        # Setup test run
        testrail.setup_test_run()

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Create test report and update TestRail with screenshots and detailed failure info"""
    outcome = yield
    report = outcome.get_result()
    
    # Store report in item for screenshot fixture
    setattr(item, f"rep_{call.when}", report)
    
    if call.when == 'call':
        # Get test case ID mapping - Updated with actual TestRail case IDs
        test_name = item.nodeid.split("::")[-1]
        print(f"\n🔍 Processing test: {test_name}")
        
        case_mapping = {
            'test_login': 345,  # C345: Login
            'test_tab_navigation[text=Home-HomePage]': 346,  # C346: test tabs navigation
            'test_tab_navigation[text=Vizion AI-VizionAIPage]': 346,  # C346: test tabs navigation
            'test_tab_navigation[text=Reconciliation-ReconciliationPage]': 346,  # C346: test tabs navigation
            'test_tab_navigation[text=Ledger-LedgerPage]': 346,  # C346: test tabs navigation
            'test_tab_navigation[text=BI Analysis-BIAnalysisPage]': 346,  # C346: test tabs navigation
            'test_tab_navigation[text=Connections-ConnectionPage]': 346,  # C346: test tabs navigation
            'test_tabs_navigation_single_login': 347,  # C347: test tabs single login
        }
        
        case_id = case_mapping.get(test_name)
        
        # Get page object if available for screenshots
        page = None
        if hasattr(item, 'funcargs'):
            # Try to get page from different fixture names
            page = item.funcargs.get('page') or item.funcargs.get('perform_login')
        
        # Always capture screenshot on failure, regardless of TestRail mapping
        if not report.passed and page:
            print(f"📸 Attempting to capture screenshot for failed test: {test_name}")
            try:
                filename, info = screenshot_helper.capture_sync_screenshot(page, test_name)
                if filename:
                    print(f"✅ Screenshot captured: {filename}")
                else:
                    print(f"❌ Screenshot failed: {info}")
            except Exception as e:
                print(f"❌ Screenshot exception: {str(e)}")
        
        # Only update TestRail if test is mapped
        if case_id and testrail._is_enabled():
            # Determine test status and create detailed comment
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            if report.passed:
                status = TestRailStatus.PASSED
                comment = f"✅ **Test PASSED** - {timestamp}\n\n"
                comment += f"**Test**: {test_name}\n"
                comment += f"**Duration**: {report.duration:.2f}s\n"
                comment += "**Result**: All assertions passed successfully"
                
            else:
                status = TestRailStatus.FAILED
                comment = f"❌ **Test FAILED** - {timestamp}\n\n"
                comment += f"**Test**: {test_name}\n"
                comment += f"**Duration**: {report.duration:.2f}s\n\n"
                
                # Add detailed failure information
                if report.longrepr:
                    failure_info = str(report.longrepr)
                    # Extract the actual error message
                    if "AssertionError:" in failure_info:
                        error_lines = failure_info.split('\n')
                        for line in error_lines:
                            if "AssertionError:" in line:
                                comment += f"**Error**: {line.strip()}\n\n"
                                break
                    elif "TimeoutError:" in failure_info:
                        error_lines = failure_info.split('\n')
                        for line in error_lines:
                            if "TimeoutError:" in line:
                                comment += f"**Timeout Error**: {line.strip()}\n\n"
                                break
                    else:
                        # Get the last few lines which usually contain the error
                        error_lines = failure_info.split('\n')[-8:]
                        comment += "**Error Details**:\n```\n"
                        comment += '\n'.join([line for line in error_lines if line.strip()])
                        comment += "\n```\n\n"
                
                # Add page context information
                if page:
                    try:
                        context = screenshot_helper.get_page_context(page)
                        comment += f"**Current URL**: {context.get('url', 'Unknown')}\n"
                        comment += f"**Page Title**: {context.get('title', 'Unknown')}\n\n"
                        
                        # Try to capture screenshot
                        filename, info = screenshot_helper.capture_sync_screenshot(page, test_name)
                        if filename:
                            comment += f"📸 **Screenshot**: {filename}\n"
                            comment += f"**Screenshot Location**: screenshots/{filename}\n\n"
                        else:
                            comment += f"⚠️ **Screenshot Error**: {info}\n\n"
                    except Exception as e:
                        comment += f"⚠️ **Context Error**: Could not capture page context - {str(e)}\n\n"
            
            # Calculate elapsed time
            elapsed = f"{report.duration:.2f}s" if hasattr(report, 'duration') else None
            
            # Update TestRail
            testrail.update_test_result(case_id, status, comment, elapsed)
            screenshot_msg = "with screenshot" if status == TestRailStatus.FAILED and page else ""
            print(f"📊 Updated TestRail case {case_id}: {status} {screenshot_msg}")
        else:
            print(f"ℹ️ Test '{test_name}' not mapped to TestRail or TestRail disabled")

def pytest_sessionfinish(session, exitstatus):
    """Finalize TestRail integration at the end of test session"""
    if testrail._is_enabled():
        testrail.finalize_test_run()
        print("🏁 TestRail test run completed")
