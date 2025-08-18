#!/usr/bin/env python3
"""
BO Stage Environment Test Runner
Run BO tests against the stage environment (https://bo.stage.viewz.co)
"""

import subprocess
import sys
import os
from pathlib import Path

def run_bo_stage_tests(test_mode="quick"):
    """
    Run BO tests in stage environment
    
    Available modes:
    - complete: Run complete BO workflow test
    - login: Run BO login test only
    - accounts: Run BO accounts navigation test only
    - relogin: Run BO relogin tests
    - sanity: Run BO sanity tests
    - snapshots: Run all BO snapshot tests
    - visual: Run BO visual snapshots only
    - workflow: Run BO workflow snapshots
    - components: Run BO component snapshots
    - dom: Run BO DOM snapshots
    - quick: Run essential BO tests (login + accounts)
    - all: Run all BO tests
    """
    
    print("🎯 BO Stage Environment Test Runner")
    print("Environment: BO Stage (https://bo.stage.viewz.co)")
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
    
    print("🚀 Running BO Stage Tests")
    print("=" * 50)
    
    if test_mode == "complete":
        # Run complete BO workflow
        cmd = [
            "python3", "-m", "pytest", 
            "tests/e2e/bo/test_bo_complete_flow.py::TestBOCompleteFlow::test_bo_complete_workflow",
            "-v", "-s", "--tb=short"
        ]
    elif test_mode == "login":
        # Run BO login only
        cmd = [
            "python3", "-m", "pytest", 
            "tests/e2e/bo/test_bo_complete_flow.py::TestBOCompleteFlow::test_bo_login_only",
            "-v", "-s", "--tb=short"
        ]
    elif test_mode == "accounts":
        # Run BO accounts navigation only
        cmd = [
            "python3", "-m", "pytest", 
            "tests/e2e/bo/test_bo_complete_flow.py::TestBOCompleteFlow::test_bo_accounts_navigation_only",
            "-v", "-s", "--tb=short"
        ]
    elif test_mode == "relogin":
        # Run BO relogin tests
        cmd = [
            "python3", "-m", "pytest", 
            "tests/e2e/bo/test_bo_complete_flow.py::TestBOCompleteFlow::test_bo_account_relogin",
            "tests/e2e/bo/test_bo_complete_flow.py::TestBOCompleteFlow::test_bo_relogin_sanity_comprehensive",
            "-v", "-s", "--tb=short"
        ]
    elif test_mode == "sanity":
        # Run BO sanity test
        cmd = [
            "python3", "-m", "pytest", 
            "tests/e2e/bo/test_bo_complete_flow.py::TestBOCompleteFlow::test_bo_relogin_sanity_comprehensive",
            "-v", "-s", "--tb=short"
        ]
    elif test_mode == "snapshots":
        # Run all BO snapshot tests
        cmd = [
            "python3", "-m", "pytest", 
            "tests/e2e/bo/test_bo_snapshots.py",
            "-v", "-s", "--tb=short"
        ]
    elif test_mode == "visual":
        # Run BO visual snapshots only
        cmd = [
            "python3", "-m", "pytest", 
            "tests/e2e/bo/test_bo_snapshots.py::TestBOSnapshots::test_bo_visual_snapshots",
            "-v", "-s", "--tb=short"
        ]
    elif test_mode == "workflow":
        # Run BO workflow snapshots
        cmd = [
            "python3", "-m", "pytest", 
            "tests/e2e/bo/test_bo_snapshots.py::TestBOSnapshots::test_bo_workflow_snapshots",
            "-v", "-s", "--tb=short"
        ]
    elif test_mode == "components":
        # Run BO component snapshots
        cmd = [
            "python3", "-m", "pytest", 
            "tests/e2e/bo/test_bo_snapshots.py::TestBOSnapshots::test_bo_component_snapshots",
            "-v", "-s", "--tb=short"
        ]
    elif test_mode == "dom":
        # Run BO DOM snapshots
        cmd = [
            "python3", "-m", "pytest", 
            "tests/e2e/bo/test_bo_snapshots.py::TestBOSnapshots::test_bo_dom_snapshots",
            "-v", "-s", "--tb=short"
        ]
    elif test_mode == "quick":
        # Run essential BO tests (login + accounts)
        cmd = [
            "python3", "-m", "pytest", 
            "tests/e2e/bo/test_bo_complete_flow.py::TestBOCompleteFlow::test_bo_login_only",
            "tests/e2e/bo/test_bo_complete_flow.py::TestBOCompleteFlow::test_bo_accounts_navigation_only",
            "-v", "-s", "--tb=short"
        ]
    elif test_mode == "all":
        # Run all BO tests
        cmd = [
            "python3", "-m", "pytest", 
            "tests/e2e/bo/",
            "-v", "-s", "--tb=short"
        ]
    else:
        print(f"❌ Unknown test mode: {test_mode}")
        print("Available modes: complete, login, accounts, relogin, sanity, snapshots, visual, workflow, components, dom, quick, all")
        return False
    
    print(f"Executing: {' '.join(cmd)}")
    print("-" * 50)
    
    try:
        # Run the tests
        result = subprocess.run(cmd, env=env, check=False)
        
        if result.returncode == 0:
            print("\n✅ BO Stage Tests - COMPLETED SUCCESSFULLY!")
        else:
            print(f"\n⚠️ BO Stage Tests - COMPLETED WITH ISSUES (exit code: {result.returncode})")
        
        return result.returncode == 0
        
    except Exception as e:
        print(f"❌ Error running BO stage tests: {str(e)}")
        return False

if __name__ == "__main__":
    # Get test mode from command line argument
    test_mode = sys.argv[1] if len(sys.argv) > 1 else "quick"
    
    # Run the tests
    success = run_bo_stage_tests(test_mode)
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)
