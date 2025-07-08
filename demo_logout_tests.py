#!/usr/bin/env python3
"""
🚪 Logout Tests Demo

This script demonstrates all available logout tests that build on your test_login.py
Run this to see all logout test options.

Usage:
    python demo_logout_tests.py
"""

import os
import sys
import subprocess
from pathlib import Path

def main():
    """Demo all available logout tests"""
    print("🚪 Logout Tests Demo")
    print("=" * 30)
    
    # Check if we're in the right directory
    if not Path("tests/e2e/test_logout.py").exists():
        print("❌ Please run this script from the project root directory")
        return
    
    print("📋 Available Logout Tests:")
    print("=" * 40)
    
    tests = [
        {
            "name": "🔐 2FA Login + Logout Test",
            "test": "test_logout_after_2fa_login",
            "description": "Complete test: Login with 2FA → Logout (mirrors your test_login.py)"
        },
        {
            "name": "🎯 Direct Logout Test",
            "test": "test_logout_direct_method", 
            "description": "Tests direct logout buttons/links"
        },
        {
            "name": "📱 Menu Logout Test",
            "test": "test_logout_via_menu",
            "description": "Tests logout via user menu dropdown"
        },
        {
            "name": "🛡️ Comprehensive Logout Test",
            "test": "test_logout_comprehensive_fallback",
            "description": "Tries all logout methods (most robust)"
        },
        {
            "name": "🔒 Session Validation Test",
            "test": "test_logout_session_validation",
            "description": "Validates session termination after logout"
        }
    ]
    
    for i, test in enumerate(tests, 1):
        print(f"\n{i}. {test['name']}")
        print(f"   Test: {test['test']}")
        print(f"   Description: {test['description']}")
    
    print(f"\n6. 🎯 Run ALL logout tests")
    print(f"0. ❌ Exit")
    
    print("\n" + "=" * 40)
    
    while True:
        choice = input("🤔 Choose a test to run (0-6): ").strip()
        
        if choice == "0":
            print("👋 Goodbye!")
            return
        
        if choice == "6":
            print("\n🚀 Running ALL logout tests...")
            run_all_tests()
            break
        
        try:
            test_index = int(choice) - 1
            if 0 <= test_index < len(tests):
                selected_test = tests[test_index]
                print(f"\n🚀 Running: {selected_test['name']}")
                run_single_test(selected_test['test'])
                break
            else:
                print("❌ Invalid choice. Please enter 0-6.")
        except ValueError:
            print("❌ Invalid input. Please enter a number.")

def run_single_test(test_name):
    """Run a single logout test"""
    print(f"🔄 Executing: {test_name}")
    print("=" * 50)
    
    try:
        # Set PYTHONPATH and run the test
        env = os.environ.copy()
        env['PYTHONPATH'] = f"{os.getcwd()}:{env.get('PYTHONPATH', '')}"
        
        result = subprocess.run([
            sys.executable, 
            "-m", "pytest", 
            f"tests/e2e/test_logout.py::{test_name}",
            "-v", "-s"
        ], env=env, capture_output=False, text=True)
        
        print("\n" + "=" * 50)
        if result.returncode == 0:
            print("✅ Test completed successfully!")
            print("\n📁 Check these files for results:")
            print("   📸 screenshots/ - All screenshots from the test")
            print("   📊 Test output above shows detailed results")
        else:
            print("❌ Test completed with issues")
            print("   Check the output above for details")
            
    except Exception as e:
        print(f"❌ Error running test: {str(e)}")

def run_all_tests():
    """Run all logout tests"""
    print("🔄 Running ALL logout tests...")
    print("=" * 50)
    
    try:
        # Set PYTHONPATH and run all tests
        env = os.environ.copy()
        env['PYTHONPATH'] = f"{os.getcwd()}:{env.get('PYTHONPATH', '')}"
        
        result = subprocess.run([
            sys.executable, 
            "-m", "pytest", 
            "tests/e2e/test_logout.py",
            "-v", "-s"
        ], env=env, capture_output=False, text=True)
        
        print("\n" + "=" * 50)
        if result.returncode == 0:
            print("✅ All tests completed successfully!")
            print("\n📁 Check these files for results:")
            print("   📸 screenshots/ - All screenshots from all tests")
            print("   📊 Test output above shows detailed results")
        else:
            print("❌ Some tests completed with issues")
            print("   Check the output above for details")
            
    except Exception as e:
        print(f"❌ Error running tests: {str(e)}")

if __name__ == "__main__":
    main() 