#!/usr/bin/env python3
"""
Create Actual BO TestRail Cases
This script actually creates the test cases in TestRail, not just local mappings
"""

import os
import sys
import json
import time
from datetime import datetime

# Add the parent directory to the path to import our configs
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from configs.testrail_config import TestRailConfig

def main():
    """Create actual BO test cases in TestRail"""
    print("🚀 Creating Actual BO Test Cases in TestRail")
    print("="*60)
    
    # Initialize config
    config = TestRailConfig()
    project_id = config.project_id
    suite_id = 139  # Use existing comprehensive suite
    
    print(f"📊 Project ID: {project_id}")
    print(f"📝 Suite ID: {suite_id}")
    print(f"🔗 TestRail URL: {config.url}")
    
    # Step 1: Create or find BO section
    print("\n📂 Step 1: Creating BO Section...")
    section_id = create_bo_section(config, project_id, suite_id)
    if not section_id:
        print("❌ Failed to create BO section")
        return False
    
    # Step 2: Define BO test cases with detailed information
    bo_test_cases = [
        {
            'title': 'BO Complete Workflow - Login, Relogin, and Sanity Testing',
            'description': '''Complete end-to-end BO workflow validation covering:
1. BO admin authentication with OTP verification
2. Navigation to accounts management page  
3. Account relogin with OTP in new window/tab
4. Comprehensive sanity testing on relogin session using regression framework patterns
5. Integration with existing framework page objects and utilities''',
            'goal': 'Validate complete BO environment workflow including admin login with OTP, account relogin, and regression sanity testing on relogin session',
            'assertions': [
                'assert bo_login_success == True',
                'assert "accounts" in current_url.lower()',
                'assert len(accounts_list) >= 1', 
                'assert relogin_success == True',
                'assert relogin_page is not None',
                'assert sanity_tests_passed >= 3',
                'assert "app.viewz.co" in relogin_page.url',
                'assert no login errors or authentication failures occur'
            ],
            'test_function': 'test_bo_complete_workflow',
            'priority': 4
        },
        {
            'title': 'BO Admin Login with OTP Authentication',
            'description': '''Test BO admin authentication process:
1. Navigate to BO login page (https://bo.viewz.co/login)
2. Enter admin credentials (sharonadmin / password)
3. Handle OTP verification with TOTP secret
4. Verify successful login and redirect to accounts page
5. Validate BO admin dashboard access''',
            'goal': 'Verify BO admin login functionality with username, password, and OTP verification',
            'assertions': [
                'assert login_page.is_loaded() == True',
                'assert username_field.is_filled() == True', 
                'assert password_field.is_filled() == True',
                'assert otp_verification_success == True',
                'assert "settings/accounts" in final_url',
                'assert bo_logged_in_indicators_visible == True'
            ],
            'test_function': 'test_bo_login_only',
            'priority': 4
        },
        {
            'title': 'BO Accounts Navigation and List Verification',
            'description': '''Test BO accounts page functionality:
1. Navigate to accounts management page
2. Verify accounts list is properly loaded and displayed
3. Validate account table structure and data
4. Check account list pagination and sorting
5. Verify account action buttons are available''',
            'goal': 'Validate navigation to BO accounts page and verify account list display functionality',
            'assertions': [
                'assert accounts_page.is_loaded() == True',
                'assert len(accounts_list) >= 1',
                'assert accounts_table.is_visible() == True', 
                'assert relogin_buttons_count > 0',
                'assert account_data_integrity == True'
            ],
            'test_function': 'test_bo_accounts_navigation_only',
            'priority': 3
        },
        {
            'title': 'BO Account Relogin with OTP in New Window',
            'description': '''Test account relogin process:
1. Select an account from the accounts list
2. Click relogin button for selected account
3. Handle new window/tab opening
4. Fill OTP in new window with TOTP verification
5. Verify successful relogin to main application
6. Validate session establishment in main app''',
            'goal': 'Verify account relogin functionality including OTP handling in new browser window/tab',
            'assertions': [
                'assert account_selected == True',
                'assert relogin_button.is_clicked() == True',
                'assert new_window_detected == True',
                'assert otp_filled_in_new_window == True', 
                'assert relogin_redirect_success == True',
                'assert "app.viewz.co" in final_relogin_url',
                'assert relogin_session_active == True'
            ],
            'test_function': 'test_bo_account_relogin',
            'priority': 4
        },
        {
            'title': 'BO Relogin Session - Comprehensive Sanity Testing',
            'description': '''Test relogin session comprehensive validation:
1. Home page verification in relogin session
2. Navigation functionality and menu accessibility  
3. Session functionality and performance testing
4. Framework integration compatibility
5. Regression test pattern compatibility''',
            'goal': 'Ensure relogin session is fully functional and compatible with existing regression framework patterns',
            'assertions': [
                'assert relogin_home_page_verified == True',
                'assert navigation_elements_functional == True',
                'assert session_performance_acceptable == True',
                'assert framework_integration_working == True',
                'assert regression_compatibility_verified == True'
            ],
            'test_function': 'test_bo_relogin_sanity_comprehensive',
            'priority': 3
        }
    ]
    
    # Step 3: Create test cases in TestRail
    print(f"\n📝 Step 2: Creating {len(bo_test_cases)} BO test cases...")
    created_cases = {}
    
    for i, case_data in enumerate(bo_test_cases, 1):
        print(f"\n🔄 Creating case {i}/{len(bo_test_cases)}: {case_data['title']}")
        
        # Build enhanced test steps
        enhanced_steps = build_enhanced_test_steps(case_data)
        
        # Prepare test case data for TestRail
        data = {
            'title': case_data['title'],
            'section_id': section_id,
            'template_id': 1,  # Test Case (Steps)
            'type_id': 1,      # Automated
            'priority_id': case_data['priority'],
            'custom_steps': enhanced_steps,
            'custom_preconds': f"Prerequisites: BO environment accessible at https://bo.viewz.co, Valid admin credentials (sharonadmin), Valid OTP secret configured for {case_data['test_function']}",
            'custom_expected': f"Expected Result: {case_data['goal']} - All assertions pass and test completes successfully"
        }
        
        # Create the test case in TestRail
        result = config._send_request('POST', f'add_case/{section_id}', data)
        if result:
            case_id = result['id']
            created_cases[case_data['test_function']] = case_id
            print(f"✅ Created: C{case_id} - {case_data['title']}")
        else:
            print(f"❌ Failed to create: {case_data['title']}")
        
        time.sleep(0.5)  # Prevent rate limiting
    
    # Step 4: Update mapping file with actual TestRail case IDs  
    if created_cases:
        print(f"\n📄 Step 3: Updating mapping files with actual TestRail case IDs...")
        update_mapping_files(created_cases, section_id, suite_id, project_id)
        
        # Step 5: Update test files with actual case IDs
        print(f"\n🔧 Step 4: Updating test files with actual TestRail case IDs...")
        update_test_file_with_real_ids(created_cases)
        
        # Step 6: Print summary
        print_success_summary(created_cases, section_id, suite_id, config.url)
        
        return True
    else:
        print("❌ No test cases were created successfully")
        return False

def create_bo_section(config, project_id, suite_id):
    """Create or find BO section in TestRail"""
    print("🔍 Checking for existing BO section...")
    
    # Get existing sections
    sections = config._send_request('GET', f'get_sections/{project_id}&suite_id={suite_id}')
    if sections and isinstance(sections, list):
        for section in sections:
            if isinstance(section, dict) and 'BO Environment Testing' in section.get('name', ''):
                print(f"✅ Found existing BO section: ID {section['id']}")
                return section['id']
    
    print("📂 Creating new BO section...")
    # Create new section
    data = {
        'suite_id': suite_id,
        'name': '🔐 BO Environment Testing',
        'description': '''Back Office (BO) environment testing suite covering:

🎯 **BO Testing Scope:**
- BO admin authentication with OTP verification
- Account management and navigation
- Account relogin functionality with new window handling  
- Sanity testing on relogin sessions
- Integration with existing regression framework
- Performance and compatibility validation

🔧 **Technical Coverage:**
- Multi-window/tab browser automation
- TOTP-based OTP generation and verification
- Session management across windows
- Framework integration testing
- Regression pattern compatibility

🌐 **Environment Details:**
- BO URL: https://bo.viewz.co
- Main App URL: https://app.viewz.co
- Authentication: Username/Password + TOTP OTP
- Test Framework: Playwright + pytest + TestRail'''
    }
    
    result = config._send_request('POST', f'add_section/{project_id}', data)
    if result:
        section_id = result['id']
        print(f"✅ Created BO section: ID {section_id}")
        return section_id
    else:
        print("❌ Failed to create BO section")
        return None

def build_enhanced_test_steps(case_data):
    """Build enhanced test steps with goals and assertions"""
    enhanced_steps = f"""🎯 **TEST GOAL:**
{case_data['goal']}

📋 **TEST DESCRIPTION:**
{case_data['description']}

🔧 **TEST EXECUTION STEPS:**
1. Setup: Ensure all preconditions are met
2. Execution: Run the test following the automated workflow
3. Validation: Verify all assertions pass successfully
4. Cleanup: Capture screenshots and test evidence

✅ **ASSERTIONS VERIFIED:**
"""
    
    for i, assertion in enumerate(case_data['assertions'], 1):
        enhanced_steps += f"{i}. {assertion}\n"

    enhanced_steps += f"""

📊 **SUCCESS CRITERIA:**
- All assertions pass successfully
- Test goal is achieved completely
- No unexpected errors or failures occur
- Expected behavior is verified and documented
- Screenshots captured for evidence

🔧 **AUTOMATION DETAILS:**
- Test Function: {case_data['test_function']}
- Framework: Playwright + pytest
- Environment: BO (https://bo.viewz.co)
- TestRail Integration: Enabled
- Screenshot Capture: On success and failure
- OTP Handling: TOTP-based verification
- Multi-window Support: Yes

📱 **COMPATIBILITY:**
- Browser: Chromium-based browsers
- Window Management: Multi-window/tab support
- Session Handling: Cross-window session management
- Framework Integration: Full compatibility with existing test patterns"""

    return enhanced_steps

def update_mapping_files(created_cases, section_id, suite_id, project_id):
    """Update mapping files with actual TestRail case IDs"""
    
    # Update main mapping file
    mapping_data = {
        'bo_suite_info': {
            'suite_id': suite_id,
            'section_id': section_id,
            'project_id': project_id,
            'created_date': datetime.now().isoformat(),
            'total_bo_cases': len(created_cases),
            'environment': 'BO (https://bo.viewz.co)',
            'framework': 'Playwright + pytest + TestRail',
            'status': 'TestRail cases created successfully'
        },
        'bo_testrail_cases': {},
        'bo_framework_mappings': {}
    }
    
    for test_function, case_id in created_cases.items():
        mapping_data['bo_testrail_cases'][test_function] = f"C{case_id}"
        mapping_data['bo_framework_mappings'][test_function] = f"C{case_id}"
    
    # Save updated mapping file
    with open('bo_testrail_mappings_actual.json', 'w') as f:
        json.dump(mapping_data, f, indent=2)
    
    print("✅ Created bo_testrail_mappings_actual.json with real TestRail case IDs")

def update_test_file_with_real_ids(created_cases):
    """Update test file decorators with actual TestRail case IDs"""
    test_file = '/Users/sharonhoffman/Desktop/Automation/playwright_python_framework/tests/e2e/bo/test_bo_complete_flow.py'
    
    try:
        with open(test_file, 'r') as f:
            content = f.read()
        
        # Update decorators with actual case IDs
        for test_function, case_id in created_cases.items():
            if test_function == 'test_bo_complete_workflow':
                content = content.replace(
                    '@testrail_case("C_BO_001")',
                    f'@testrail_case("C{case_id}")'
                )
            elif test_function == 'test_bo_login_only':
                content = content.replace(
                    '@testrail_case("C_BO_002")',
                    f'@testrail_case("C{case_id}")'
                )
            elif test_function == 'test_bo_accounts_navigation_only':
                content = content.replace(
                    '@testrail_case("C_BO_003")',
                    f'@testrail_case("C{case_id}")'
                )
        
        with open(test_file, 'w') as f:
            f.write(content)
        
        print(f"✅ Updated test file with actual TestRail case IDs")
        
    except Exception as e:
        print(f"⚠️ Could not update test file: {str(e)}")

def print_success_summary(created_cases, section_id, suite_id, testrail_url):
    """Print success summary"""
    print("\n" + "="*80)
    print("🎉 BO TESTRAIL CASES CREATED SUCCESSFULLY!")
    print("="*80)
    print(f"📊 Suite ID: {suite_id}")
    print(f"📂 BO Section ID: {section_id}")
    print(f"📝 Test Cases Created: {len(created_cases)}")
    
    print("\n📝 Created TestRail Cases:")
    for test_function, case_id in created_cases.items():
        print(f"   C{case_id}: {test_function}")
    
    print(f"\n🔗 TestRail URLs:")
    print(f"   📋 Suite: {testrail_url}/index.php?/suites/view/{suite_id}")
    print(f"   📂 BO Section: {testrail_url}/index.php?/suites/view/{suite_id}&group_by=cases:section_id&group_id={section_id}")
    
    print("\n✅ Next Steps:")
    print("   1. BO test cases are now created in TestRail")
    print("   2. Test file decorators updated with actual case IDs")
    print("   3. Run BO tests to see results reported to TestRail")
    print("   4. Check TestRail for test execution results")

if __name__ == "__main__":
    main()
