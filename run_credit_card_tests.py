#!/usr/bin/env python3
"""
Run Credit Card Tests with TestRail Integration (Suite 139)
"""

import os
import sys
import subprocess

def run_credit_card_tests(headless=False):
    """Run Credit Card tests with TestRail integration"""
    
    print("🏦 Credit Card Tests Runner")
    print("=" * 60)
    print(f"Suite: 139 (Credit Cards Operations)")
    print(f"Headless: {headless}")
    print("=" * 60)
    
    # Set environment variables for Suite 139
    env = os.environ.copy()
    env['TESTRAIL_SUITE_ID'] = '139'
    env['TESTRAIL_ENABLED'] = 'true'
    
    # Build pytest command
    cmd = [
        "python3", "-m", "pytest",
        "tests/e2e/reconciliation/credit_cards/",
        "-v", "-s", "--tb=short"
    ]
    
    if headless:
        cmd.append("--headless")
    
    print(f"\n🚀 Running command: {' '.join(cmd)}")
    print(f"   Using TESTRAIL_SUITE_ID=139\n")
    
    # Run tests
    try:
        result = subprocess.run(cmd, env=env)
        
        if result.returncode == 0:
            print("\n✅ Credit Card tests completed successfully!")
            print("📊 Check TestRail Suite 139 for results")
            return True
        else:
            print(f"\n⚠️ Tests completed with exit code: {result.returncode}")
            return False
            
    except KeyboardInterrupt:
        print("\n⚠️ Tests interrupted by user")
        return False
    except Exception as e:
        print(f"\n❌ Error running tests: {e}")
        return False

def main():
    """Main function"""
    headless = "--headless" in sys.argv
    
    print("\n" + "=" * 60)
    print("CREDIT CARD TEST SUITE")
    print("TestRail Suite: 139")
    print("Test Cases: 22 (C51886-C52146)")
    print("=" * 60 + "\n")
    
    success = run_credit_card_tests(headless=headless)
    
    if success:
        print("\n🎉 All tests completed!")
        print("\n📋 Next Steps:")
        print("  1. Go to https://viewz.testrail.io")
        print("  2. Navigate to Suite 139")
        print("  3. View test results in the latest run")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

