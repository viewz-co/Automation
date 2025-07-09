#!/usr/bin/env python3
"""
Check TestRail Results
Simple guide to find your payables test results in TestRail
"""

import os
from configs.testrail_config import TestRailConfig

def check_testrail_results():
    """Show where to find TestRail results"""
    
    print("🔍 TESTRAIL RESULTS LOCATION")
    print("=" * 50)
    
    # Check if TestRail is enabled
    if not os.getenv('TESTRAIL_ENABLED', 'false').lower() == 'true':
        print("❌ TestRail integration is not enabled")
        print("💡 Run tests with: TESTRAIL_ENABLED=true python -m pytest")
        return
    
    print("✅ TestRail integration is enabled")
    
    # Get TestRail configuration
    config = TestRailConfig()
    
    print(f"\n📋 TESTRAIL CONFIGURATION")
    print("-" * 30)
    print(f"🔗 TestRail URL: {config.url}")
    print(f"📊 Project ID: {config.project_id}")
    print(f"📋 Suite ID: {config.suite_id}")
    print(f"👤 Username: {config.username}")
    
    print(f"\n🎯 WHERE TO FIND YOUR PAYABLES TEST RESULTS")
    print("-" * 50)
    print("1. Go to: https://viewz.testrail.io")
    print("2. Login with your credentials")
    print("3. Navigate to: Projects → Project 1 → Test Runs")
    print("4. Look for recent runs named: 'Automated Test Run - Playwright Framework'")
    print("5. Click on the most recent run to see results")
    
    print(f"\n📊 PAYABLES TEST MAPPING")
    print("-" * 30)
    print("All payables tests report to these TestRail cases:")
    print("• C345 (Login) - Status update tests")
    print("• C346 (Navigation) - Most payables tests")
    print("• C357 (Logout) - Delete operation tests")
    
    payables_tests = [
        "test_verify_invoice_list_is_displayed → C346",
        "test_upload_invoice_file → C346",
        "test_payables_edit_delete_buttons → C346",
        "test_payables_status_dropdowns → C346",
        "test_payables_search_filter_options → C346"
    ]
    
    print(f"\n📝 SPECIFIC PAYABLES TESTS")
    print("-" * 30)
    for test in payables_tests:
        print(f"• {test}")
    
    print(f"\n🚀 HOW TO RUN PAYABLES TESTS")
    print("-" * 30)
    print("# Run all payables tests:")
    print("TESTRAIL_ENABLED=true python -m pytest tests/e2e/reconciliation/payables/ -v")
    print()
    print("# Run single payables test:")
    print("TESTRAIL_ENABLED=true python -m pytest tests/e2e/reconciliation/payables/test_complete_payables_operations.py::TestCompletePayablesOperations::test_verify_invoice_list_is_displayed -v")
    
    print(f"\n💡 TROUBLESHOOTING")
    print("-" * 20)
    print("If you don't see results in TestRail:")
    print("1. Check that tests are PASSING (failed tests also report)")
    print("2. Verify network connection to TestRail")
    print("3. Check TestRail permissions for automation@viewz.co")
    print("4. Look for 'Updated TestRail case XXX' messages in test output")
    
    print(f"\n✅ RECENT TEST RUNS")
    print("-" * 20)
    print("Based on recent test executions, you should see:")
    print("• TestRail Run 21, 22, 23, 24 (recent runs)")
    print("• Results for C346 (Navigation case)")
    print("• Test comments with timestamps and results")

if __name__ == "__main__":
    check_testrail_results() 