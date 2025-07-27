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
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

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
    """Load configuration from environment variables"""
    return {
        "base_url": os.getenv("BASE_URL", "https://new.viewz.co"),
        "username": os.getenv("TEST_USERNAME", ""),
        "password": os.getenv("TEST_PASSWORD", ""),
        "otp_secret": os.getenv("TEST_TOTP_SECRET", ""),
        "api_base_url": os.getenv("API_BASE_URL", "https://new.viewz.co"),
        "jwt_token": os.getenv("JWT_TOKEN", "")
    }

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
    """Load login data from environment variables"""
    return {
        "username": os.getenv("TEST_USERNAME", ""),
        "password": os.getenv("TEST_PASSWORD", "")
    }

# ---------- PERFORM LOGIN WITH OTP FIXTURE ---------- #
@pytest_asyncio.fixture
async def perform_login(page, login_data):
    login = LoginPage(page)
    await login.goto()
    await login.login(login_data["username"], login_data["password"])

    # הזנת OTP
    secret = os.getenv('TEST_TOTP_SECRET')
    if not secret:
        raise ValueError("TEST_TOTP_SECRET environment variable is required")
    otp = pyotp.TOTP(secret).now()

    await page.wait_for_selector("text=Two-Factor Authentication", timeout=5000)
    await page.get_by_role("textbox").fill(otp)
    await asyncio.sleep(1)
    #await page.get_by_role("button", name="Verify").click()
    await page.wait_for_selector("text=SuccessOTP verified successfully", timeout=5000)

    return page

# ---------- PERFORM LOGIN WITH ENTITY SELECTION FIXTURE ---------- #
@pytest_asyncio.fixture
async def perform_login_with_entity(page, login_data):
    """Enhanced login fixture that includes entity selection after login"""
    from pages.entity_selector_page import EntitySelectorPage
    
    login = LoginPage(page)
    await login.goto()
    await login.login(login_data["username"], login_data["password"])

    # הזנת OTP
    secret = "HA2ECLBIKYUEEI2GPUUSMN3XIMXFETRQ"  # החלף אם צריך
    otp = pyotp.TOTP(secret).now()

    await page.wait_for_selector("text=Two-Factor Authentication", timeout=5000)
    await page.get_by_role("textbox").fill(otp)
    await asyncio.sleep(3)
    
    # Try to wait for various success indicators, don't fail if timeout
    try:
        await page.wait_for_selector("text=SuccessOTP verified successfully", timeout=5000)
    except:
        try:
            # Alternative success indicators
            await page.wait_for_selector("text=Success", timeout=2000)
        except:
            try:
                # Check if we're redirected (indicates success)
                await page.wait_for_url("**/home**", timeout=3000)
            except:
                # Continue anyway - some 2FA flows don't show success message
                await asyncio.sleep(2)

    # Entity Selection Step
    print("🏢 Starting entity selection...")
    entity_selector = EntitySelectorPage(page)
    entity_selected = await entity_selector.select_entity("Viewz Demo INC")
    
    if entity_selected:
        print("✅ Entity selection completed successfully")
    else:
        print("⚠️ Entity selection failed or not required")
    
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
        # ===== COMPLETE COMPREHENSIVE SUITE MAPPINGS =====
        # Suite ID: 139
        # Total Cases Mapped: 133

        # API Tests
        'test_account_activity_report': 8024,  # C8024
        'test_account_balance_display': 8017,  # C8017
        'test_account_details_popup': 8018,  # C8018
        'test_account_selection_functionality': 8016,  # C8016
        'test_account_settings_configuration': 7973,  # C7973
        'test_all_endpoints_reject_invalid_date_formats': 7944,  # C7944
        'test_api_response_times': 8059,  # C8059
        'test_concurrent_user_simulation': 8058,  # C8058
        'test_create_journal_entry_invalid_date_format': 7939,  # C7939
        'test_create_journal_entry_valid_date_format': 7938,  # C7938
        'test_date_format_consistency_across_endpoints': 7945,  # C7945
        'test_date_format_validation_demo': 7946,  # C7946
        'test_date_preset_functionality': 8042,  # C8042
        'test_empty_state_handling': 7969,  # C7969
        'test_export_functionality': 8025,  # C8025
        'test_get_accounting_uploaded_files_date_format': 7943,  # C7943
        'test_get_bank_transactions_data_date_format': 7941,  # C7941
        'test_get_bank_uploaded_files_date_format': 7940,  # C7940
        'test_get_entity_documents_date_format': 7942,  # C7942
        'test_get_gross_profit_value': 8038,  # C8038
        'test_get_journal_entries_invalid_date_format_request': 7937,  # C7937
        'test_get_journal_entries_valid_date_format_request': 7936,  # C7936
        'test_get_total_income_value': 8037,  # C8037
        'test_gl_account_dropdown': 8001,  # C8001
        'test_handle_unmatched_transactions': 7985,  # C7985
        'test_journal_entries_filtering_by_account': 8020,  # C8020
        'test_journal_entries_filtering_by_date': 8019,  # C8019
        'test_journal_entries_search': 8021,  # C8021
        'test_journal_entry_posting': 8029,  # C8029
        'test_journal_entry_reversal': 8030,  # C8030
        'test_journal_entry_validation': 8028,  # C8028
        'test_large_dataset_handling': 8060,  # C8060
        'test_line_totals_equal_before_validation': 7999,  # C7999
        'test_mandatory_validation': 7998,  # C7998
        'test_manual_journal_entry_creation': 8027,  # C8027
        'test_menu_options_for_matched_status': 7995,  # C7995
        'test_menu_options_for_new_status': 7994,  # C7994
        'test_menu_options_for_reconciled_status': 7996,  # C7996
        'test_no_data_states_handling': 8044,  # C8044
        'test_open_edit_popup_layout': 7997,  # C7997
        'test_password_requirements': 8053,  # C8053
        'test_period_filter_impact': 8043,  # C8043
        'test_period_selection': 8026,  # C8026
        'test_period_selection_functionality': 8041,  # C8041
        'test_recognition_timing_default': 8003,  # C8003
        'test_recognition_timing_single_date': 8002,  # C8002
        'test_reconciliation_status_display': 7983,  # C7983
        'test_secure_headers': 8055,  # C8055
        'test_session_timeout_handling': 8050,  # C8050
        'test_show_journal_entry_for_record': 8005,  # C8005
        'test_sort_transactions_by_columns': 7977,  # C7977
        'test_transaction_action_buttons': 7978,  # C7978
        'test_transaction_drill_down': 8022,  # C8022
        'test_transaction_filtering_by_date': 7974,  # C7974
        'test_transaction_reconciliation': 7984,  # C7984
        'test_transaction_search': 7975,  # C7975
        'test_trial_balance_display': 8023,  # C8023
        'test_verify_account_hierarchy_display': 8013,  # C8013
        'test_verify_filter_controls_display': 8036,  # C8036
        'test_verify_je_amount_and_description': 8000,  # C8000
        'test_verify_transactions_display': 7967,  # C7967
        'test_view_account_balances': 7972,  # C7972

        # Authentication Tests
        'test_invalid_login_attempts': 8049,  # C8049
        'test_login': 7947,  # C7947
        'test_logout_after_2fa_login': 7961,  # C7961
        'test_scenario_1_valid_login': 7948,  # C7948
        'test_scenario_2_logout_user': 7949,  # C7949
        'test_tabs_navigation_single_login': 7956,  # C7956
        'test_tabs_navigation_single_login_with_entity': 7959,  # C7959

        # Navigation Tests
        'test_chart_of_accounts_navigation': 8015,  # C8015
        'test_entity_selection_validation': 7958,  # C7958
        'test_tab_navigation[text=BI Analysis-BIAnalysisPage]': 7954,  # C7954
        'test_tab_navigation[text=Connections-ConnectionPage]': 7955,  # C7955
        'test_tab_navigation[text=Home-HomePage]': 7950,  # C7950
        'test_tab_navigation[text=Ledger-LedgerPage]': 7953,  # C7953
        'test_tab_navigation[text=Reconciliation-ReconciliationPage]': 7952,  # C7952
        'test_tab_navigation[text=Vizion AI-VizionAIPage]': 7951,  # C7951
        'test_tab_navigation_with_entity[text=BI Analysis-BIAnalysisPage]': 7957,  # C7957
        'test_tab_navigation_with_entity[text=Connections-ConnectionPage]': 7957,  # C7957
        'test_tab_navigation_with_entity[text=Home-HomePage]': 7957,  # C7957
        'test_tab_navigation_with_entity[text=Ledger-LedgerPage]': 7957,  # C7957
        'test_tab_navigation_with_entity[text=Reconciliation-ReconciliationPage]': 7957,  # C7957
        'test_tab_navigation_with_entity[text=Vizion AI-VizionAIPage]': 7957,  # C7957

        # Logout Tests
        'test_logout_comprehensive_workflow': 7965,  # C7965
        'test_logout_direct_method': 7962,  # C7962
        'test_logout_keyboard_method': 7964,  # C7964
        'test_logout_via_menu': 7963,  # C7963

        # Bank Tests
        'test_bank_account_selection': 7970,  # C7970
        'test_bank_page_responsiveness': 7968,  # C7968
        'test_bank_reconciliation_integration': 8031,  # C8031
        'test_check_bank_account_list_display': 7971,  # C7971
        'test_complete_bank_workflow': 7986,  # C7986
        'test_verify_bank_page_loads': 7966,  # C7966
        'test_view_bank_transactions_list': 7976,  # C7976

        # Payables Tests
        'test_attempt_to_delete_invoice': 8010,  # C8010
        'test_delete_invoice_dialog': 8009,  # C8009
        'test_payables_edit_delete_buttons': 8006,  # C8006
        'test_payables_form_validation': 7993,  # C7993
        'test_payables_integration': 8032,  # C8032
        'test_payables_menu_operations': 7992,  # C7992
        'test_payables_search_filter_options': 8008,  # C8008
        'test_payables_status_dropdowns': 8007,  # C8007
        'test_record_invoice_and_status': 8004,  # C8004
        'test_upload_duplicate_invoice': 7990,  # C7990
        'test_upload_invoice_file': 7988,  # C7988
        'test_verify_invoice_list_is_displayed': 7987,  # C7987
        'test_view_invoice_in_new_view': 7991,  # C7991

        # Ledger Tests
        'test_complete_dashboard_workflow': 8046,  # C8046
        'test_complete_ledger_workflow': 8033,  # C8033
        'test_dashboard_edge_cases': 8048,  # C8048
        'test_dashboard_responsiveness': 8047,  # C8047
        'test_dashboard_url_parameters': 8045,  # C8045
        'test_get_all_kpi_values': 8039,  # C8039
        'test_kpi_data_consistency': 8040,  # C8040
        'test_ledger_page_responsiveness': 8014,  # C8014
        'test_verify_financial_kpis_display': 8035,  # C8035
        'test_verify_general_ledger_entries_display': 8012,  # C8012
        'test_verify_ledger_dashboard_loads': 8034,  # C8034
        'test_verify_ledger_page_loads': 8011,  # C8011

        # Security Tests
        'test_csrf_protection': 8054,  # C8054
        'test_sql_injection_prevention': 8051,  # C8051
        'test_xss_prevention': 8052,  # C8052

        # Performance Tests
        'test_handle_duplicate_uploads': 7981,  # C7981
        'test_memory_usage_monitoring': 8057,  # C8057
        'test_page_load_performance': 8056,  # C8056
        'test_process_uploaded_statements': 7982,  # C7982
        'test_upload_invalid_file_type': 7989,  # C7989
        'test_upload_statement_file_validation': 7980,  # C7980
        'test_verify_upload_area': 7979,  # C7979

        # Compatibility Tests
        'test_mobile_viewport_compatibility': 8062,  # C8062
        'test_print_stylesheet_compatibility': 8065,  # C8065
        'test_responsive_design_elements': 8063,  # C8063
        'test_touch_interface_compatibility': 8064,  # C8064

        # Snapshot Tests
        'test_visual_snapshots_key_pages': 12865,  # C12865
        'test_dom_snapshots_critical_elements': 12866,  # C12866
        'test_api_response_snapshots': 12867,  # C12867
        'test_component_snapshots': 12868,  # C12868
        'test_snapshot_comparison_workflow': 12869,  # C12869
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
            result = testrail.update_test_result(case_id, status, comment, elapsed)
            screenshot_msg = "with screenshot" if status == TestRailStatus.FAILED and page else ""
            
            # Only show success message if TestRail update actually worked
            if result:
                print(f"📊 Updated TestRail case {case_id}: {status} {screenshot_msg}")
            else:
                print(f"❌ Failed to update TestRail case {case_id}: {status} {screenshot_msg}")
        else:
            print(f"ℹ️ Test '{test_name}' not mapped to TestRail or TestRail disabled")

def pytest_sessionfinish(session, exitstatus):
    """Finalize TestRail integration at the end of test session"""
    if testrail._is_enabled():
        # Add a small delay to ensure all test results are processed
        import time
        time.sleep(2)
        testrail.finalize_test_run()
        print("🏁 TestRail test run completed")
