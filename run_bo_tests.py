#!/usr/bin/env python3
"""
BO Tests Runner
Quick runner for BO environment tests with different execution modes
"""

import subprocess
import sys
import os

def run_bo_tests(test_mode="complete"):
    """
    Run BO tests with different modes
    
    Args:
        test_mode: "complete", "login", "accounts", "quick", "snapshots", "visual", "workflow", "components", "dom"
    """
    
    base_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(base_dir)
    
    print(f"🚀 Running BO Tests - Mode: {test_mode}")
    print("="*50)
    
    if test_mode == "complete":
        # Run complete workflow test
        cmd = [
            "python3", "-m", "pytest", 
            "tests/e2e/bo/test_bo_complete_flow.py::TestBOCompleteFlow::test_bo_complete_workflow",
            "-v", "-s", "--tb=short"
        ]
    elif test_mode == "login":
        # Run login only test
        cmd = [
            "python3", "-m", "pytest", 
            "tests/e2e/bo/test_bo_complete_flow.py::TestBOCompleteFlow::test_bo_login_only",
            "-v", "-s", "--tb=short"
        ]
    elif test_mode == "accounts":
        # Run accounts navigation test
        cmd = [
            "python3", "-m", "pytest", 
            "tests/e2e/bo/test_bo_complete_flow.py::TestBOCompleteFlow::test_bo_accounts_navigation_only",
            "-v", "-s", "--tb=short"
        ]
    elif test_mode == "quick":
        # Run all BO tests
        cmd = [
            "python3", "-m", "pytest", 
            "tests/e2e/bo/",
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
    else:
        print(f"❌ Unknown test mode: {test_mode}")
        print("Available modes: complete, login, accounts, quick, snapshots, visual, workflow, components, dom")
        return False
    
    print(f"Executing: {' '.join(cmd)}")
    print("-"*50)
    
    try:
        result = subprocess.run(cmd, capture_output=False)
        return result.returncode == 0
    except Exception as e:
        print(f"❌ Error running tests: {str(e)}")
        return False

def main():
    """Main execution function"""
    if len(sys.argv) > 1:
        test_mode = sys.argv[1]
    else:
        test_mode = "complete"
    
    print("🎯 BO Test Runner")
    print(f"Environment: BO (https://bo.viewz.co)")
    print(f"Test Mode: {test_mode}")
    print("="*50)
    
    success = run_bo_tests(test_mode)
    
    if success:
        print("\n✅ BO Tests - COMPLETED SUCCESSFULLY!")
    else:
        print("\n❌ BO Tests - FAILED!")
        sys.exit(1)

if __name__ == "__main__":
    main()
