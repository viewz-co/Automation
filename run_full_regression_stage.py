#!/usr/bin/env python3
"""
Full Regression Test Runner - Stage Environment
Run complete regression suite on stage with TestRail integration
"""

import subprocess
import sys
import os
from pathlib import Path

def run_full_regression_stage():
    """Run full regression tests on stage environment"""
    
    print("🧪 Full Regression Test Runner - STAGE")
    print("Environment: Stage (https://app.stage.viewz.co)")
    print("=" * 60)
    
    # Set stage environment
    env = os.environ.copy()
    env["TEST_ENV"] = "stage"
    
    # Set TestRail environment
    env["TESTRAIL_ENABLED"] = "true"
    env["TESTRAIL_URL"] = "https://viewz.testrail.io"
    env["TESTRAIL_USERNAME"] = "automation@viewz.co"
    env["TESTRAIL_PASSWORD"] = "e.fJg:z5q5mnAdL"
    
    print("🚀 Running STAGE Full Regression")
    print("=" * 60)
    
    # Run all tests with TestRail integration
    cmd = [
        "python3", "-m", "pytest", 
        "tests/", 
        "-v", "-s", "--tb=short",
        "--headless"
    ]
    
    print(f"Executing: {' '.join(cmd)}")
    print("-" * 60)
    
    try:
        # Run the tests
        result = subprocess.run(cmd, env=env, check=False)
        
        if result.returncode == 0:
            print("\n✅ STAGE Full Regression - COMPLETED SUCCESSFULLY!")
        else:
            print(f"\n⚠️ STAGE Full Regression - COMPLETED WITH ISSUES (exit code: {result.returncode})")
        
        # Also run BO stage tests (with correct basic auth)
        print("\n" + "=" * 60)
        print("🏢 Running BO STAGE Tests")
        print("=" * 60)
        
        bo_cmd = ["python3", "run_bo_stage_tests.py", "all", "--headless"]
        print(f"Executing: {' '.join(bo_cmd)}")
        print("-" * 60)
        
        bo_result = subprocess.run(bo_cmd, env=env, check=False)
        
        if bo_result.returncode == 0:
            print("\n✅ BO STAGE Tests - COMPLETED SUCCESSFULLY!")
        else:
            print(f"\n⚠️ BO STAGE Tests - COMPLETED WITH ISSUES (exit code: {bo_result.returncode})")
        
        # Overall result
        overall_success = result.returncode == 0 and bo_result.returncode == 0
        
        print("\n" + "=" * 60)
        print("📊 STAGE REGRESSION SUMMARY")
        print("=" * 60)
        print(f"Main App Tests: {'✅ PASSED' if result.returncode == 0 else '❌ FAILED'}")
        print(f"BO Tests: {'✅ PASSED' if bo_result.returncode == 0 else '❌ FAILED'}")
        print(f"Overall Result: {'✅ SUCCESS' if overall_success else '⚠️ ISSUES FOUND'}")
        
        return overall_success
        
    except Exception as e:
        print(f"❌ Error running stage regression: {str(e)}")
        return False

if __name__ == "__main__":
    # Run the tests
    success = run_full_regression_stage()
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)
