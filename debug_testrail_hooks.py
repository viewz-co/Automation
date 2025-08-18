#!/usr/bin/env python3
"""
Debug TestRail Integration Hooks
Test the pytest hooks that should be updating TestRail case results
"""

import os
import sys

# Set TestRail environment
os.environ['TESTRAIL_ENABLED'] = 'true'
os.environ['TESTRAIL_URL'] = 'https://viewz.testrail.io'
os.environ['TESTRAIL_USERNAME'] = 'automation@viewz.co'
os.environ['TESTRAIL_PASSWORD'] = 'e.fJg:z5q5mnAdL'

sys.path.append('/Users/sharonhoffman/Desktop/Automation/playwright_python_framework')

from utils.testrail_integration import testrail, testrail_case

print("🔍 Debug TestRail Hooks")
print("="*50)

# Test the decorator and case ID
@testrail_case(27980)
def mock_test_function():
    """Mock test function"""
    pass

print(f"Function: {mock_test_function.__name__}")
print(f"Has case ID: {hasattr(mock_test_function, 'testrail_case_id')}")
if hasattr(mock_test_function, 'testrail_case_id'):
    print(f"Case ID: {mock_test_function.testrail_case_id}")
    print(f"Case ID type: {type(mock_test_function.testrail_case_id)}")

# Test TestRail integration status
print(f"\nTestRail Integration:")
print(f"  Enabled: {testrail._is_enabled()}")
print(f"  Run ID: {testrail.run_id}")

# Test manual update
print(f"\nTesting manual case update...")
if testrail._is_enabled():
    # Create a test run first
    case_ids = [27980]
    run_id = testrail.setup_test_run(case_ids)
    print(f"  Created run: {run_id}")
    
    if run_id:
        # Try to update the case result
        result = testrail.update_test_result(27980, 1, "Manual test - PASSED", "5.0s")
        print(f"  Update result: {result}")
        
        # Close the run
        testrail.finalize_test_run()
        print(f"  Run finalized")
else:
    print("  TestRail not enabled")
