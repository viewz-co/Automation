#!/usr/bin/env python3
"""
Debug TestRail Payables Integration
Check what's being reported to TestRail for payables tests
"""

import os
import sys
from utils.testrail_integration import testrail

def debug_testrail_payables():
    """Debug TestRail integration for payables tests"""
    
    print("🔍 DEBUGGING TESTRAIL PAYABLES INTEGRATION")
    print("=" * 50)
    
    # Check if TestRail is enabled
    if not testrail._is_enabled():
        print("❌ TestRail integration is not enabled")
        print("💡 Set TESTRAIL_ENABLED=true to enable")
        return
    
    print("✅ TestRail integration is enabled")
    
    # Get TestRail connection info
    print(f"🔗 TestRail URL: {testrail.client.url}")
    print(f"📊 Project ID: {testrail.project_id}")
    print(f"📋 Suite ID: {testrail.suite_id}")
    
    # Test connection
    try:
        projects = testrail.client.send_get('get_projects')
        print(f"✅ TestRail connection successful - Found {len(projects)} projects")
    except Exception as e:
        print(f"❌ TestRail connection failed: {e}")
        return
    
    # Get current test cases
    try:
        cases = testrail.client.send_get(f'get_cases/{testrail.project_id}&suite_id={testrail.suite_id}')
        print(f"📋 Found {len(cases)} test cases in suite")
        
        # Show relevant cases
        payables_cases = [345, 346, 347, 357]  # Our mapped cases
        for case in cases:
            if case['id'] in payables_cases:
                print(f"   C{case['id']}: {case['title']}")
        
    except Exception as e:
        print(f"❌ Error getting test cases: {e}")
    
    # Get recent test runs
    try:
        runs = testrail.client.send_get(f'get_runs/{testrail.project_id}')
        print(f"🏃 Found {len(runs)} test runs")
        
        # Show recent runs
        for run in runs[:5]:  # Show last 5 runs
            print(f"   Run {run['id']}: {run['name']} - {run['passed_count']} passed, {run['failed_count']} failed")
            
            # Get results for this run
            try:
                results = testrail.client.send_get(f'get_results_for_run/{run["id"]}')
                print(f"     └─ {len(results)} results")
                
                # Show payables-related results
                for result in results[:10]:  # Show first 10 results
                    case_id = result['case_id']
                    status = result['status_id']
                    status_name = {1: 'PASSED', 5: 'FAILED', 3: 'UNTESTED'}.get(status, f'STATUS_{status}')
                    
                    if case_id in payables_cases:
                        print(f"       C{case_id}: {status_name}")
                        if result.get('comment'):
                            # Show first line of comment
                            comment_line = result['comment'].split('\n')[0]
                            print(f"         Comment: {comment_line}")
                        
            except Exception as e:
                print(f"     └─ Error getting results: {e}")
        
    except Exception as e:
        print(f"❌ Error getting test runs: {e}")
    
    # Show current mapping
    print(f"\n📋 CURRENT TESTRAIL MAPPING")
    print("-" * 30)
    
    # Import the case mapping
    payables_mapping = {
        'test_verify_invoice_list_is_displayed': 346,
        'test_upload_invoice_file': 346,
        'test_payables_edit_delete_buttons': 346,
        'test_payables_status_dropdowns': 346,
        'test_payables_search_filter_options': 346,
    }
    
    for test_name, case_id in payables_mapping.items():
        print(f"   {test_name} → C{case_id}")
    
    print(f"\n💡 RECOMMENDATIONS")
    print("-" * 20)
    print("1. Check TestRail web interface at: https://viewz.testrail.io")
    print("2. Look for recent test runs in Project 1, Suite 4")
    print("3. All payables tests should report to case C346 (Navigation)")
    print("4. If tests are passing but not showing in TestRail, check network connectivity")

if __name__ == "__main__":
    debug_testrail_payables() 