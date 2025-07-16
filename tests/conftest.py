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

# ---------- PYTEST CONFIGURATION ---------- #
def pytest_addoption(parser):
    parser.addoption(
        "--headless", 
        action="store_true", 
        default=False, 
        help="Run tests in headless mode (without browser UI)"
    )

@pytest.fixture(scope="session")
def headless_mode(request):
    return request.config.getoption("--headless")

# ---------- ENV CONFIG ---------- #
def load_config():
    with open("configs/env_config.json") as f:
        config = json.load(f)
        # Handle both flat config structure and environment-based structure
        env = os.getenv("ENV", "dev")
        if env in config:
            return config[env]
        else:
            # Return the flat config directly
            return config

@pytest.fixture(scope="session")
def env_config():
    return load_config()

# ---------- ASYNC PAGE FIXTURE ---------- #
@pytest_asyncio.fixture
async def page(env_config, headless_mode):
    async with async_playwright() as p:
        # Use headless_mode parameter, but keep slow_mo and args for non-headless
        launch_options = {
            "headless": headless_mode,
        }
        if not headless_mode:
            launch_options.update({
                "slow_mo": 200,
                "args": ["--start-maximized"]
            })
        
        browser = await p.chromium.launch(**launch_options)
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
    secret = os.getenv('TEST_TOTP_SECRET')  # החלף אם צריך
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
            # Login Tests - Using existing TestRail cases
            'test_login': 345,  # C345: Login (existing case)
            
            # Navigation Tests - Using existing TestRail cases
            'test_tab_navigation[text=Home-HomePage]': 346,  # C346: test tabs navigation (existing case)
            'test_tab_navigation[text=Vizion AI-VizionAIPage]': 346,  # C346: test tabs navigation (existing case)
            'test_tab_navigation[text=Reconciliation-ReconciliationPage]': 346,  # C346: test tabs navigation (existing case)
            'test_tab_navigation[text=Ledger-LedgerPage]': 346,  # C346: test tabs navigation (existing case)
            'test_tab_navigation[text=BI Analysis-BIAnalysisPage]': 346,  # C346: test tabs navigation (existing case)
            'test_tab_navigation[text=Connections-ConnectionPage]': 346,  # C346: test tabs navigation (existing case)
            'test_tabs_navigation_single_login': 347,  # C347: test tabs single login (existing case)
            
            # Logout Tests - Using existing logout case for now
            'test_logout_after_2fa_login': 357,  # C357: Logout (existing case)
            'test_logout_direct_method': 357,  # C357: Logout (existing case)
            'test_logout_via_menu': 357,  # C357: Logout (existing case)
            'test_logout_comprehensive_fallback': 357,  # C357: Logout (existing case)
            'test_logout_session_validation': 357,  # C357: Logout (existing case)
            
            # Login Scenarios Tests - Map to existing login case for now
            'test_scenario_1_valid_login': 345,  # C345: Login (existing case)
            'test_scenario_2_logout_user': 357,  # C357: Logout (existing case)
            
            # ===== PAYABLES TESTS - MAPPED TO ACTUAL TESTRAIL CASES 428-447 =====
            
            # Basic Navigation & Display Tests
            'test_verify_invoice_list_is_displayed': 428,  # Case 428: Verify invoices list is displayed
            'test_view_invoice_in_new_view': 445,  # Case 445: View invoice in new tab
            
            # File Upload Tests
            'test_upload_invoice_file': 429,  # Case 429: Upload a valid invoice file
            'test_upload_invalid_file_type': 430,  # Case 430: Upload invalid file type
            'test_upload_duplicate_invoice': 431,  # Case 431: Upload duplicate invoice
            
            # Delete Operations Tests
            'test_delete_invoice_in_new_status': 432,  # Case 432: Delete invoice in New status
            'test_attempt_to_delete_invoice': 433,  # Case 433: Attempt to delete invoice in Recorded status
            'test_delete_invoice_dialog': 447,  # Case 447: Delete confirmation dialog actions
            
            # Menu & Context Operations Tests
            'test_menu_options_for_new_status': 434,  # Case 434: Menu options for New status
            'test_menu_options_for_matched_status': 435,  # Case 435: Menu options for Matched status
            'test_menu_options_for_reconciled_status': 436,  # Case 436: Menu options for Recorded status
            'test_payables_menu_operations': 434,  # Case 434: Menu options for New status (general menu test)
            
            # Form & Popup Operations Tests
            'test_open_edit_popup_layout': 437,  # Case 437: Open Edit popup layout
            'test_mandatory_validation': 438,  # Case 438: Mandatory fields validation in Edit popup
            'test_payables_form_validation': 438,  # Case 438: Mandatory fields validation in Edit popup
            'test_line_totals_equal_before_validation': 439,  # Case 439: Line totals equal Before VAT validation
            'test_verify_je_amount_and_description': 446,  # Case 446: Verify JE amount and description fields are read-only
            
            # Dropdown & Selection Tests
            'test_gl_account_dropdown': 440,  # Case 440: GL Account dropdown search
            'test_recognition_timing_single_date': 441,  # Case 441: Recognition timing Single Date
            'test_recognition_timing_default': 442,  # Case 442: Recognition timing Deferred Period
            
            # Record & Status Operations
            'test_record_invoice_and_status': 443,  # Case 443: Record invoice and status change
            'test_show_journal_entry_for_record': 444,  # Case 444: Show Journal Entry for Recorded invoice
            
            # Additional Payables Tests (using the new page object methods)
            'test_payables_edit_delete_buttons': 432,  # Case 432: Delete invoice in New status (edit/delete buttons)
            'test_payables_status_dropdowns': 434,  # Case 434: Menu options for New status (status dropdowns)
            'test_payables_search_filter_options': 440,  # Case 440: GL Account dropdown search (search/filter)
            
            # ===== API DATE FORMAT VALIDATION TESTS - UPDATED CASE IDs =====
            # These tests validate that all API endpoints use YYYY-MM-DD date format
            
            # Date Format Validation Tests - Updated with C951-C957 mappings
            'test_get_journal_entries_valid_date_format_request': 951,  # C951: Verify date format in GET /api/v2/accounting/getJournalEntries response
            'test_create_journal_entry_valid_date_format': 952,  # C952: Verify date format in POST /api/v2/accounting/createJournalEntry request
            'test_create_journal_entry_invalid_date_format': 953,  # C953: Validate rejection of invalid date format in POST /api/v2/accounting/createJournalEntry
            'test_get_bank_uploaded_files_date_format': 954,  # C954: Verify date format in GET /api/v2/banks/getBankUploadedFiles
            'test_get_bank_transactions_data_date_format': 955,  # C955: Verify date format in GET /api/v2/banks/getBankTransactionsData
            'test_get_entity_documents_date_format': 956,  # C956: Verify date format in GET /api/v2/docs/getEntityDocuments
            'test_get_accounting_uploaded_files_date_format': 957,  # C957: Verify date format in GET /api/v2/accounting/getAccountingUploadedFiles
            
            # ===== BANK OPERATIONS TESTS - NEW BANK FUNCTIONALITY =====
            # Comprehensive tests for bank reconciliation functionality
            
            # Bank Navigation & Display Tests
            'test_verify_bank_page_loads': 2173,  # C2173: Verify bank page loads correctly
            'test_verify_transactions_display': 2175,  # C2175: Verify transaction table structure
            
            # Bank Account Management Tests
            'test_bank_account_selection': 2192,  # C2192: Select different bank accounts
            
            # Transaction Management Tests
            'test_transaction_filtering_by_date': 2178,  # C2178: Filter transactions by date range
            'test_transaction_search': 2179,  # C2179: Search transactions by description/amount
            
            # Bank File Upload Tests
            'test_verify_upload_area': 2182,  # C2182: Upload bank statement files (CSV, Excel, OFX)
            'test_upload_statement_file_validation': 2183,  # C2183: Validate file format restrictions
            
            # Bank Reconciliation Tests
            'test_reconciliation_status_display': 2188,  # C2188: Mark transactions as reconciled
            'test_transaction_reconciliation': 2187,  # C2187: Match transactions with journal entries
            
            # Bank Action Buttons Tests
            'test_transaction_action_buttons': 2190,  # C2190: Bulk reconciliation operations
            
            # Bank Workflow Tests
            'test_complete_bank_workflow': 2190,  # C2190: Bulk reconciliation operations
            'test_empty_state_handling': 2175,  # C2175: Verify transaction table structure
            'test_bank_page_responsiveness': 2173,  # C2173: Verify bank page loads correctly
            
            # Additional Bank Test Cases - Mapped to specific TestRail cases
            'test_check_bank_account_list_display': 2174,  # C2174: Check bank account list display
            'test_view_bank_transactions_list': 2177,  # C2177: View bank transactions list
            'test_sort_transactions_by_columns': 2180,  # C2180: Sort transactions by different columns
            'test_handle_duplicate_uploads': 2184,  # C2184: Handle duplicate uploads
            'test_process_uploaded_statements': 2185,  # C2185: Process uploaded statements
            'test_handle_unmatched_transactions': 2189,  # C2189: Handle unmatched transactions
            'test_view_account_balances': 2193,  # C2193: View account balances
            'test_account_settings_configuration': 2194,  # C2194: Account settings and configuration
            
            # ===== POTENTIAL FUTURE CSV TESTS =====
            # Template for additional CSV-generated tests
            # 'test_csv_generated_<functionality>': <appropriate_case_id>,
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
