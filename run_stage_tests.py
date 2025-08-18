#!/usr/bin/env python3
"""
Stage Environment Test Runner
Run tests against the stage environment (https://app.stage.viewz.co)
"""

import subprocess
import sys
import os
from pathlib import Path

def run_stage_tests(test_mode="all"):
    """
    Run tests in stage environment
    
    Available modes:
    - all: Run all tests
    - login: Run login tests only
    - navigation: Run navigation tests only
    - payables: Run payables tests only
    - ledger: Run ledger tests only
    - reconciliation: Run reconciliation tests only
    - performance: Run performance tests only
    - snapshot: Run snapshot tests only
    - bo: Run BO tests only
    - quick: Run a quick subset of tests
    """
    
    print("🎯 Stage Environment Test Runner")
    print("Environment: Stage (https://app.stage.viewz.co)")
    print(f"Test Mode: {test_mode}")
    print("=" * 50)
    
    # Set stage environment
    env = os.environ.copy()
    env["TEST_ENV"] = "stage"
    
    # Set TestRail environment (same for both prod and stage)
    env["TESTRAIL_ENABLED"] = "true"
    env["TESTRAIL_URL"] = "https://viewz.testrail.io"
    env["TESTRAIL_USERNAME"] = "automation@viewz.co"
    env["TESTRAIL_PASSWORD"] = "e.fJg:z5q5mnAdL"
    
    print("🚀 Running Stage Tests")
    print("=" * 50)
    
    if test_mode == "all":
        # Run all tests
        cmd = [
            "python3", "-m", "pytest", 
            "tests/", 
            "-v", "-s", "--tb=short"
        ]
    elif test_mode == "login":
        # Run login tests only
        cmd = [
            "python3", "-m", "pytest", 
            "tests/e2e/login/",
            "-v", "-s", "--tb=short"
        ]
    elif test_mode == "navigation":
        # Run navigation tests
        cmd = [
            "python3", "-m", "pytest", 
            "tests/e2e/navigation/",
            "-v", "-s", "--tb=short"
        ]
    elif test_mode == "payables":
        # Run payables tests
        cmd = [
            "python3", "-m", "pytest", 
            "tests/e2e/payables/",
            "-v", "-s", "--tb=short"
        ]
    elif test_mode == "ledger":
        # Run ledger tests
        cmd = [
            "python3", "-m", "pytest", 
            "tests/e2e/ledger/",
            "-v", "-s", "--tb=short"
        ]
    elif test_mode == "reconciliation":
        # Run reconciliation tests
        cmd = [
            "python3", "-m", "pytest", 
            "tests/e2e/reconciliation/",
            "-v", "-s", "--tb=short"
        ]
    elif test_mode == "performance":
        # Run performance tests
        cmd = [
            "python3", "-m", "pytest", 
            "tests/performance/",
            "-v", "-s", "--tb=short"
        ]
    elif test_mode == "snapshot":
        # Run snapshot tests
        cmd = [
            "python3", "-m", "pytest", 
            "tests/e2e/snapshot/",
            "-v", "-s", "--tb=short"
        ]
    elif test_mode == "bo":
        # Run BO tests
        cmd = [
            "python3", "-m", "pytest", 
            "tests/e2e/bo/",
            "-v", "-s", "--tb=short"
        ]
    elif test_mode == "quick":
        # Run a quick subset of important tests
        cmd = [
            "python3", "-m", "pytest", 
            "tests/e2e/login/test_login.py",
            "tests/e2e/navigation/test_tabs_navigation.py",
            "tests/e2e/bo/test_bo_complete_flow.py::TestBOCompleteFlow::test_bo_login_only",
            "-v", "-s", "--tb=short"
        ]
    else:
        print(f"❌ Unknown test mode: {test_mode}")
        print("Available modes: all, login, navigation, payables, ledger, reconciliation, performance, snapshot, bo, quick")
        return False
    
    print(f"Executing: {' '.join(cmd)}")
    print("-" * 50)
    
    try:
        # Run the tests
        result = subprocess.run(cmd, env=env, check=False)
        
        if result.returncode == 0:
            print("\n✅ Stage Tests - COMPLETED SUCCESSFULLY!")
        else:
            print(f"\n⚠️ Stage Tests - COMPLETED WITH ISSUES (exit code: {result.returncode})")
        
        return result.returncode == 0
        
    except Exception as e:
        print(f"❌ Error running stage tests: {str(e)}")
        return False

if __name__ == "__main__":
    # Get test mode from command line argument
    test_mode = sys.argv[1] if len(sys.argv) > 1 else "quick"
    
    # Run the tests
    success = run_stage_tests(test_mode)
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)
