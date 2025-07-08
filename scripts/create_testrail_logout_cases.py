#!/usr/bin/env python3
"""
TestRail Logout Test Cases Creator

This script provides the test case definitions for the logout tests
to be created in TestRail with case IDs 348-352.

Usage:
    python scripts/create_testrail_logout_cases.py
"""

import json
from datetime import datetime

def generate_testrail_cases():
    """Generate TestRail test case definitions for logout tests"""
    
    test_cases = [
        {
            "case_id": 348,
            "title": "C348: Login with 2FA + Logout",
            "section": "Authentication Tests",
            "priority": "High",
            "type": "Functional",
            "template": "Test Case (Steps)",
            "description": "Complete end-to-end test that performs login with Two-Factor Authentication followed by comprehensive logout verification. This test mirrors the existing login test but adds logout functionality.",
            "preconditions": [
                "User has valid login credentials",
                "TOTP secret is configured for 2FA",
                "Application is accessible at login page"
            ],
            "steps": [
                {
                    "step": 1,
                    "action": "Navigate to login page",
                    "expected": "Login page loads successfully"
                },
                {
                    "step": 2,
                    "action": "Enter valid username and password",
                    "expected": "Credentials are accepted"
                },
                {
                    "step": 3,
                    "action": "Submit login form",
                    "expected": "2FA page appears"
                },
                {
                    "step": 4,
                    "action": "Generate and enter TOTP code",
                    "expected": "2FA is accepted and user is logged in"
                },
                {
                    "step": 5,
                    "action": "Verify successful login",
                    "expected": "User is on authenticated page, login indicators visible"
                },
                {
                    "step": 6,
                    "action": "Perform comprehensive logout",
                    "expected": "Logout is initiated successfully"
                },
                {
                    "step": 7,
                    "action": "Verify logout completion",
                    "expected": "User is redirected to login page, session terminated"
                }
            ],
            "automated": True,
            "test_file": "tests/e2e/test_logout.py::test_logout_after_2fa_login"
        },
        {
            "case_id": 349,
            "title": "C349: Direct Logout Test",
            "section": "Authentication Tests",
            "priority": "Medium",
            "type": "Functional",
            "template": "Test Case (Steps)",
            "description": "Test logout functionality using direct logout buttons or links without menu navigation.",
            "preconditions": [
                "User is logged into the application",
                "Direct logout elements are available on the page"
            ],
            "steps": [
                {
                    "step": 1,
                    "action": "Perform quick login to authenticated state",
                    "expected": "User is successfully logged in"
                },
                {
                    "step": 2,
                    "action": "Look for direct logout buttons/links on the page",
                    "expected": "Logout elements are found and visible"
                },
                {
                    "step": 3,
                    "action": "Click direct logout element",
                    "expected": "Logout process is initiated"
                },
                {
                    "step": 4,
                    "action": "Verify logout completion",
                    "expected": "User is logged out and redirected to login page"
                }
            ],
            "automated": True,
            "test_file": "tests/e2e/test_logout.py::test_logout_direct_method"
        },
        {
            "case_id": 350,
            "title": "C350: Menu-based Logout Test",
            "section": "Authentication Tests",
            "priority": "Medium",
            "type": "Functional",
            "template": "Test Case (Steps)",
            "description": "Test logout functionality via user menu dropdown or profile menu navigation.",
            "preconditions": [
                "User is logged into the application",
                "User menu/profile menu is available"
            ],
            "steps": [
                {
                    "step": 1,
                    "action": "Perform quick login to authenticated state",
                    "expected": "User is successfully logged in"
                },
                {
                    "step": 2,
                    "action": "Locate and click user menu/profile menu",
                    "expected": "User menu dropdown opens"
                },
                {
                    "step": 3,
                    "action": "Look for logout option in the menu",
                    "expected": "Logout option is visible in dropdown"
                },
                {
                    "step": 4,
                    "action": "Click logout option from menu",
                    "expected": "Logout process is initiated"
                },
                {
                    "step": 5,
                    "action": "Verify logout completion",
                    "expected": "User is logged out and redirected to login page"
                }
            ],
            "automated": True,
            "test_file": "tests/e2e/test_logout.py::test_logout_via_menu"
        },
        {
            "case_id": 351,
            "title": "C351: Comprehensive Logout Test",
            "section": "Authentication Tests",
            "priority": "High",
            "type": "Functional",
            "template": "Test Case (Steps)",
            "description": "Most robust logout test that tries multiple logout methods as fallbacks: direct buttons, menu navigation, keyboard shortcuts, and URL-based logout.",
            "preconditions": [
                "User is logged into the application",
                "Various logout mechanisms may be available"
            ],
            "steps": [
                {
                    "step": 1,
                    "action": "Perform login to authenticated state",
                    "expected": "User is successfully logged in"
                },
                {
                    "step": 2,
                    "action": "Attempt direct logout method",
                    "expected": "Try to find and click direct logout elements"
                },
                {
                    "step": 3,
                    "action": "If direct fails, attempt menu-based logout",
                    "expected": "Try user menu dropdown logout options"
                },
                {
                    "step": 4,
                    "action": "If menu fails, attempt keyboard shortcuts",
                    "expected": "Try common logout keyboard shortcuts (Ctrl+Shift+L, Alt+L)"
                },
                {
                    "step": 5,
                    "action": "If shortcuts fail, attempt URL-based logout",
                    "expected": "Navigate to logout endpoints (/logout, /signout, etc.)"
                },
                {
                    "step": 6,
                    "action": "Verify logout success with any working method",
                    "expected": "User is logged out successfully regardless of method used"
                }
            ],
            "automated": True,
            "test_file": "tests/e2e/test_logout.py::test_logout_comprehensive_fallback"
        },
        {
            "case_id": 352,
            "title": "C352: Session Validation Logout Test",
            "section": "Authentication Tests",
            "priority": "High",
            "type": "Security",
            "template": "Test Case (Steps)",
            "description": "Test logout with session validation to ensure the user session is properly terminated and cannot access protected resources after logout.",
            "preconditions": [
                "User is logged into the application",
                "Protected pages are available after login"
            ],
            "steps": [
                {
                    "step": 1,
                    "action": "Perform login to authenticated state",
                    "expected": "User is successfully logged in"
                },
                {
                    "step": 2,
                    "action": "Record the current protected page URL",
                    "expected": "Protected page URL is captured"
                },
                {
                    "step": 3,
                    "action": "Perform logout using comprehensive method",
                    "expected": "Logout is completed successfully"
                },
                {
                    "step": 4,
                    "action": "Verify initial logout indicators",
                    "expected": "User appears to be logged out (login form visible, URL changed)"
                },
                {
                    "step": 5,
                    "action": "Attempt to navigate back to protected page",
                    "expected": "Access to protected page should be denied"
                },
                {
                    "step": 6,
                    "action": "Verify session termination",
                    "expected": "User is redirected to login page, cannot access protected resources"
                }
            ],
            "automated": True,
            "test_file": "tests/e2e/test_logout.py::test_logout_session_validation"
        }
    ]
    
    return test_cases

def print_testrail_cases():
    """Print TestRail case definitions in a readable format"""
    cases = generate_testrail_cases()
    
    print("🔗 TestRail Logout Test Cases")
    print("=" * 50)
    print(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Total cases: {len(cases)}")
    print()
    
    for case in cases:
        print(f"📋 {case['title']}")
        print(f"   Section: {case['section']}")
        print(f"   Priority: {case['priority']}")
        print(f"   Type: {case['type']}")
        print(f"   Automated: {case['automated']}")
        print(f"   Test File: {case['test_file']}")
        print()
        print(f"   Description:")
        print(f"   {case['description']}")
        print()
        print(f"   Preconditions:")
        for precondition in case['preconditions']:
            print(f"   • {precondition}")
        print()
        print(f"   Test Steps:")
        for step in case['steps']:
            print(f"   {step['step']}. {step['action']}")
            print(f"      Expected: {step['expected']}")
        print()
        print("-" * 50)
        print()

def save_testrail_cases():
    """Save TestRail cases to JSON file"""
    cases = generate_testrail_cases()
    
    output_file = "fixtures/testrail_logout_cases.json"
    with open(output_file, 'w') as f:
        json.dump(cases, f, indent=2)
    
    print(f"💾 TestRail cases saved to: {output_file}")
    return output_file

def main():
    """Main function"""
    print("🚀 TestRail Logout Cases Generator")
    print("=" * 40)
    
    # Print cases to console
    print_testrail_cases()
    
    # Save to file
    output_file = save_testrail_cases()
    
    print("📋 Summary:")
    print("=" * 20)
    print("✅ Case C348: Login with 2FA + Logout (High Priority)")
    print("✅ Case C349: Direct Logout Test (Medium Priority)")
    print("✅ Case C350: Menu-based Logout Test (Medium Priority)")  
    print("✅ Case C351: Comprehensive Logout Test (High Priority)")
    print("✅ Case C352: Session Validation Test (High Priority)")
    print()
    print("📝 Next Steps:")
    print("1. Create these test cases in your TestRail instance")
    print("2. Use the case IDs 348-352 as specified")
    print("3. Copy the descriptions and steps from above")
    print("4. Enable TestRail integration: export TESTRAIL_ENABLED=true")
    print("5. Run tests: pytest tests/e2e/test_logout.py -v")
    print()
    print(f"📁 Detailed case definitions saved to: {output_file}")

if __name__ == "__main__":
    main() 