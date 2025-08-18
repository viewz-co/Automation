#!/usr/bin/env python3
"""
Debug TestRail Integration
Quick script to test TestRail integration and case ID detection
"""

import os
from utils.testrail_integration import testrail_case

# Set TestRail environment
os.environ['TESTRAIL_ENABLED'] = 'true'

# Test the decorator
@testrail_case(27980)
def test_function():
    """Test function with TestRail case ID"""
    pass

# Check if the decorator worked
print("🔍 Debug TestRail Integration")
print("="*50)
print(f"Function name: {test_function.__name__}")
print(f"Has testrail_case_id: {hasattr(test_function, 'testrail_case_id')}")
if hasattr(test_function, 'testrail_case_id'):
    print(f"Case ID: {test_function.testrail_case_id}")
    print(f"Case ID type: {type(test_function.testrail_case_id)}")

# Test TestRail integration settings
from utils.testrail_integration import testrail
print(f"\nTestRail enabled: {testrail._is_enabled()}")
print(f"TESTRAIL_ENABLED env: {os.getenv('TESTRAIL_ENABLED')}")

# Test configuration
from configs.testrail_config import TestRailConfig
config = TestRailConfig()
print(f"TestRail URL: {config.url}")
print(f"TestRail Username: {config.username}")
print(f"Project ID: {config.project_id}")
print(f"Suite ID: {config.suite_id}")
