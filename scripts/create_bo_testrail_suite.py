#!/usr/bin/env python3
"""
Create BO TestRail Test Suite
Creates TestRail test cases for the BO (Back Office) environment tests
Including detailed goals and assertions for each test case
"""

import os
import sys
import json
import time
from typing import Dict, List
from datetime import datetime

# Add the parent directory to the path to import our configs
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from configs.testrail_config import TestRailConfig

class BOTestRailSuiteCreator:
    def __init__(self):
        self.config = TestRailConfig()
        self.project_id = self.config.project_id
        self.suite_id = 139  # Use existing comprehensive suite
        
        # BO Test Cases with detailed goals and assertions
        self.bo_test_cases = {
            # Main BO Workflow Test
            'test_bo_complete_workflow': {
                'title': 'BO Complete Workflow - Login, Account Relogin, and Sanity Testing',
                'goal': 'Validate complete BO environment workflow including admin login with OTP, account relogin, and regression sanity testing on relogin session',
                'section': '🔐 BO Environment Testing',
                'priority': 4,
                'description': '''Complete end-to-end BO workflow validation covering:
1. BO admin authentication with OTP verification
2. Navigation to accounts management page
3. Account relogin with OTP in new window/tab
4. Comprehensive sanity testing on relogin session using regression framework patterns
5. Integration with existing framework page objects and utilities''',
                'preconditions': 'BO environment accessible at https://bo.viewz.co, Valid admin credentials (sharonadmin), Valid OTP secret configured',
                'assertions': [
                    'assert bo_login_success == True',
                    'assert "accounts" in current_url.lower()',
                    'assert len(accounts_list) >= 1',
                    'assert relogin_success == True',
                    'assert relogin_page is not None',
                    'assert sanity_tests_passed >= 3',
                    'assert "app.viewz.co" in relogin_page.url',
                    'assert no login errors or authentication failures occur'
                ]
            },
            
            # BO Login Test
            'test_bo_login_only': {
                'title': 'BO Admin Login with OTP Authentication',
                'goal': 'Verify BO admin login functionality with username, password, and OTP verification',
                'section': '🔐 BO Environment Testing',
                'priority': 4,
                'description': '''Test BO admin authentication process:
1. Navigate to BO login page (https://bo.viewz.co/login)
2. Enter admin credentials (sharonadmin / password)
3. Handle OTP verification with TOTP secret
4. Verify successful login and redirect to accounts page
5. Validate BO admin dashboard access''',
                'preconditions': 'BO environment accessible, Valid admin credentials, OTP secret configured correctly',
                'assertions': [
                    'assert login_page.is_loaded() == True',
                    'assert username_field.is_filled() == True',
                    'assert password_field.is_filled() == True',
                    'assert otp_verification_success == True',
                    'assert "settings/accounts" in final_url',
                    'assert bo_logged_in_indicators_visible == True'
                ]
            },
            
            # BO Account Navigation Test
            'test_bo_accounts_navigation': {
                'title': 'BO Accounts Page Navigation and List Verification',
                'goal': 'Validate navigation to BO accounts page and verify account list display functionality',
                'section': '🔐 BO Environment Testing',
                'priority': 3,
                'description': '''Test BO accounts page functionality:
1. Navigate to accounts management page
2. Verify accounts list is properly loaded and displayed
3. Validate account table structure and data
4. Check account list pagination and sorting
5. Verify account action buttons are available''',
                'preconditions': 'User successfully logged into BO environment, Accounts page accessible',
                'assertions': [
                    'assert accounts_page.is_loaded() == True',
                    'assert len(accounts_list) >= 1',
                    'assert accounts_table.is_visible() == True',
                    'assert relogin_buttons_count > 0',
                    'assert account_data_integrity == True'
                ]
            },
            
            # BO Account Relogin Test
            'test_bo_account_relogin': {
                'title': 'BO Account Relogin with OTP in New Window',
                'goal': 'Verify account relogin functionality including OTP handling in new browser window/tab',
                'section': '🔐 BO Environment Testing',
                'priority': 4,
                'description': '''Test account relogin process:
1. Select an account from the accounts list
2. Click relogin button for selected account
3. Handle new window/tab opening
4. Fill OTP in new window with TOTP verification
5. Verify successful relogin to main application
6. Validate session establishment in main app''',
                'preconditions': 'User logged into BO with access to accounts list, At least one account available for relogin',
                'assertions': [
                    'assert account_selected == True',
                    'assert relogin_button.is_clicked() == True',
                    'assert new_window_detected == True',
                    'assert otp_filled_in_new_window == True',
                    'assert relogin_redirect_success == True',
                    'assert "app.viewz.co" in final_relogin_url',
                    'assert relogin_session_active == True'
                ]
            }
        }
        
        # Relogin Sanity Tests with detailed goals
        self.bo_sanity_test_cases = {
            'test_relogin_sanity_home_verification': {
                'title': 'Relogin Session - Home Page Verification',
                'goal': 'Validate that relogin session successfully loads main application home page with proper indicators',
                'section': '🔐 BO Environment Testing',
                'priority': 3,
                'description': '''Test relogin session home page functionality:
1. Verify relogin session URL is correct (app.viewz.co)
2. Check for main application indicators (main, nav, dashboard)
3. Validate home page elements are properly loaded
4. Verify ViewZ logo and branding elements
5. Confirm navigation header is functional''',
                'preconditions': 'Successful account relogin completed, New window/tab with active session',
                'assertions': [
                    'assert "app.viewz.co" in relogin_page.url',
                    'assert main_app_indicators_found >= 1',
                    'assert home_page_verified == True',
                    'assert navigation_elements_visible == True'
                ]
            },
            
            'test_relogin_sanity_navigation': {
                'title': 'Relogin Session - Main App Navigation Testing',
                'goal': 'Verify navigation functionality and menu accessibility in relogin session',
                'section': '🔐 BO Environment Testing',
                'priority': 3,
                'description': '''Test navigation in relogin session:
1. Verify navigation header and menu elements
2. Check availability of main navigation links
3. Test navigation responsiveness and functionality
4. Validate access to dashboard, ledger, bank, payables modules
5. Confirm menu state and active page indicators''',
                'preconditions': 'Active relogin session with main application loaded',
                'assertions': [
                    'assert navigation_elements_count >= 2',
                    'assert header_navigation.is_visible() == True',
                    'assert dashboard_link.is_accessible() == True',
                    'assert main_modules_accessible == True'
                ]
            },
            
            'test_relogin_sanity_session_functionality': {
                'title': 'Relogin Session - Session Functionality and Performance',
                'goal': 'Validate relogin session remains active, responsive, and performs within acceptable limits',
                'section': '🔐 BO Environment Testing',
                'priority': 3,
                'description': '''Test session functionality in relogin:
1. Test session persistence after page reload
2. Measure page load performance and responsiveness
3. Verify session doesn't redirect to login
4. Check session timeout handling
5. Validate network connectivity and API responses''',
                'preconditions': 'Active relogin session established',
                'assertions': [
                    'assert page_reload_success == True',
                    'assert load_time < 15.0',
                    'assert no_login_redirect == True',
                    'assert session_remains_valid == True'
                ]
            },
            
            'test_relogin_sanity_framework_integration': {
                'title': 'Relogin Session - Framework Integration Testing',
                'goal': 'Verify relogin session compatibility with existing framework page objects and test patterns',
                'section': '🔐 BO Environment Testing',
                'priority': 2,
                'description': '''Test framework integration:
1. Test compatibility with existing page objects
2. Verify interactive elements accessibility
3. Check form elements and button functionality
4. Validate framework utilities work with relogin session
5. Test screenshot capture and error handling''',
                'preconditions': 'Relogin session active with framework utilities available',
                'assertions': [
                    'assert interactive_elements_count >= 10',
                    'assert framework_compatibility == True',
                    'assert page_objects_functional == True',
                    'assert utilities_accessible == True'
                ]
            },
            
            'test_relogin_sanity_regression_compatibility': {
                'title': 'Relogin Session - Regression Test Compatibility',
                'goal': 'Ensure relogin session is compatible with existing regression test patterns and indicators',
                'section': '🔐 BO Environment Testing',
                'priority': 2,
                'description': '''Test regression compatibility:
1. Check for positive application indicators
2. Verify absence of error states and messages
3. Test content integrity and data consistency
4. Validate application state is stable
5. Confirm regression test patterns work correctly''',
                'preconditions': 'Relogin session with main application loaded and functional',
                'assertions': [
                    'assert positive_indicators >= 2',
                    'assert negative_indicators == 0',
                    'assert content_integrity == True',
                    'assert regression_patterns_compatible == True'
                ]
            }
        }
    
    def create_bo_section(self):
        """Create BO section in TestRail if it doesn't exist"""
        print("📂 Creating/Checking BO Environment Testing section...")
        
        # Check if section already exists
        sections = self.config._send_request('GET', f'get_sections/{self.project_id}&suite_id={self.suite_id}')
        if sections and isinstance(sections, list):
            for section in sections:
                if isinstance(section, dict) and '🔐 BO Environment Testing' in section.get('name', ''):
                    print(f"✅ BO section already exists: ID {section['id']}")
                    return section['id']
        
        # Create new section
        data = {
            'suite_id': self.suite_id,
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
        
        result = self.config._send_request('POST', f'add_section/{self.project_id}', data)
        if result:
            section_id = result['id']
            print(f"✅ Created BO section: ID {section_id}")
            return section_id
        else:
            print("❌ Failed to create BO section")
            return None
    
    def create_test_case_with_goals(self, case_data, section_id):
        """Create a test case with enhanced goals and assertions"""
        
        # Build comprehensive test steps with goals and assertions
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

        # Prepare test case data
        data = {
            'title': case_data['title'],
            'section_id': section_id,
            'template_id': 1,  # Test Case (Steps)
            'type_id': 1,      # Automated
            'priority_id': case_data['priority'],
            'custom_steps': enhanced_steps,
            'custom_preconds': case_data['preconditions'],
            'custom_expected': f"Expected Result: {case_data['goal']} - All assertions pass and test completes successfully"
        }
        
        # Create the test case
        result = self.config._send_request('POST', f'add_case/{section_id}', data)
        if result:
            case_id = result['id']
            print(f"✅ Created: {case_data['title']} (C{case_id})")
            return case_id
        else:
            print(f"❌ Failed to create: {case_data['title']}")
            return None
    
    def create_all_bo_test_cases(self):
        """Create all BO test cases in TestRail"""
        print("🚀 Creating BO test cases in TestRail...")
        print("="*80)
        
        # Create BO section
        section_id = self.create_bo_section()
        if not section_id:
            print("❌ Cannot proceed without BO section")
            return False
        
        created_cases = {}
        total_cases = 0
        
        # Create main BO workflow test cases
        print(f"\n📝 Creating main BO workflow test cases...")
        for test_function, case_data in self.bo_test_cases.items():
            case_id = self.create_test_case_with_goals(case_data, section_id)
            if case_id:
                created_cases[test_function] = case_id
                total_cases += 1
            time.sleep(0.5)  # Prevent rate limiting
        
        # Create BO sanity test cases
        print(f"\n📝 Creating BO sanity test cases...")
        for test_function, case_data in self.bo_sanity_test_cases.items():
            case_id = self.create_test_case_with_goals(case_data, section_id)
            if case_id:
                created_cases[test_function] = case_id
                total_cases += 1
            time.sleep(0.5)  # Prevent rate limiting
        
        print(f"\n🎉 Successfully created {total_cases} BO test cases!")
        return created_cases, section_id
    
    def generate_bo_mapping_file(self, created_cases, section_id):
        """Generate mapping file for BO test cases"""
        print("\n📄 Generating BO test case mapping file...")
        
        mapping_data = {
            'bo_suite_info': {
                'suite_id': self.suite_id,
                'section_id': section_id,
                'section_name': '🔐 BO Environment Testing',
                'project_id': self.project_id,
                'created_date': datetime.now().isoformat(),
                'total_bo_cases': len(created_cases),
                'environment': 'BO (https://bo.viewz.co)',
                'framework': 'Playwright + pytest + TestRail'
            },
            'bo_case_mappings': created_cases,
            'bo_framework_mappings': {
                'test_function_to_case_id': created_cases
            },
            'bo_test_goals_assertions': {
                **self.bo_test_cases,
                **self.bo_sanity_test_cases
            }
        }
        
        # Save BO mapping file
        mapping_file = 'bo_testrail_mappings.json'
        with open(mapping_file, 'w') as f:
            json.dump(mapping_data, f, indent=2)
        
        print(f"✅ Created BO mapping file: {mapping_file}")
        return mapping_file
    
    def update_conftest_with_bo_mappings(self, created_cases):
        """Update conftest.py to include BO test mappings"""
        print("\n🔧 Updating conftest.py with BO test mappings...")
        
        # Read current conftest.py
        conftest_path = '/Users/sharonhoffman/Desktop/Automation/playwright_python_framework/tests/conftest.py'
        
        try:
            with open(conftest_path, 'r') as f:
                conftest_content = f.read()
            
            # Add BO test mappings to the existing mapping function
            bo_mappings = []
            for test_function, case_id in created_cases.items():
                bo_mappings.append(f"        '{test_function}': 'C{case_id}',  # BO: {test_function}")
            
            bo_mapping_section = f"""
        # BO Environment Test Mappings
{chr(10).join(bo_mappings)}"""
            
            # Check if BO mappings already exist
            if "# BO Environment Test Mappings" not in conftest_content:
                # Find the mapping dictionary and add BO mappings
                if "def get_testrail_case_mapping():" in conftest_content:
                    # Add before the closing brace of the mapping dictionary
                    conftest_content = conftest_content.replace(
                        "    }\n    return mapping",
                        f"{bo_mapping_section}\n    }}\n    return mapping"
                    )
                    
                    with open(conftest_path, 'w') as f:
                        f.write(conftest_content)
                    
                    print("✅ Updated conftest.py with BO test mappings")
                else:
                    print("⚠️ Could not find mapping function in conftest.py")
            else:
                print("ℹ️ BO mappings already exist in conftest.py")
                
        except Exception as e:
            print(f"⚠️ Could not update conftest.py: {str(e)}")
    
    def print_bo_summary(self, created_cases, section_id):
        """Print summary of BO TestRail integration"""
        print("\n" + "="*80)
        print("🎉 BO TESTRAIL INTEGRATION COMPLETE!")
        print("="*80)
        print(f"📊 Suite ID: {self.suite_id}")
        print(f"📂 BO Section ID: {section_id}")
        print(f"📝 BO Test Cases Created: {len(created_cases)}")
        print(f"🏗️ Project ID: {self.project_id}")
        
        print("\n📝 BO Test Cases Summary:")
        for test_function, case_id in created_cases.items():
            print(f"   C{case_id}: {test_function}")
        
        print(f"\n🔗 TestRail URL: {self.config.url}/index.php?/suites/view/{self.suite_id}")
        print(f"🔗 BO Section URL: {self.config.url}/index.php?/suites/view/{self.suite_id}&group_by=cases:section_id&group_id={section_id}")
        
        print("\n✅ Next Steps:")
        print("   1. BO tests are now integrated with TestRail")
        print("   2. Run BO tests to see results in TestRail")
        print("   3. conftest.py has been updated with BO mappings")
        print("   4. Screenshots and evidence will be captured automatically")

def main():
    """Main execution function"""
    print("🚀 Starting BO TestRail Integration...")
    print("This will create comprehensive BO test cases with goals and assertions in TestRail")
    
    # Ask for confirmation
    confirm = input("\nDo you want to proceed? (y/N): ").strip().lower()
    if confirm != 'y':
        print("❌ Operation cancelled")
        return
    
    creator = BOTestRailSuiteCreator()
    
    try:
        # Create all BO test cases
        created_cases, section_id = creator.create_all_bo_test_cases()
        
        if not created_cases:
            print("❌ No test cases were created. Exiting.")
            return
        
        # Generate mapping file
        creator.generate_bo_mapping_file(created_cases, section_id)
        
        # Update conftest.py
        creator.update_conftest_with_bo_mappings(created_cases)
        
        # Print summary
        creator.print_bo_summary(created_cases, section_id)
        
    except KeyboardInterrupt:
        print("\n❌ Operation cancelled by user")
    except Exception as e:
        print(f"❌ Error occurred: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
