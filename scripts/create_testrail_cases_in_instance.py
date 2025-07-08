#!/usr/bin/env python3
"""
Create TestRail Cases in TestRail Instance
This script will create the actual test cases in your TestRail instance
"""

import os
import sys
import json
import requests
from base64 import b64encode

class TestRailCaseCreator:
    def __init__(self):
        # TestRail connection settings
        self.url = os.getenv('TESTRAIL_URL', 'https://viewz.testrail.io')
        self.username = os.getenv('TESTRAIL_USERNAME', 'automation@viewz.co')
        self.password = os.getenv('TESTRAIL_PASSWORD', 'e.fJg:z5q5mnAdL')
        
        # Project and suite configuration
        self.project_id = int(os.getenv('TESTRAIL_PROJECT_ID', '1'))
        self.suite_id = int(os.getenv('TESTRAIL_SUITE_ID', '4'))
        
        # Setup authentication
        self.auth = b64encode(f"{self.username}:{self.password}".encode()).decode()
        self.headers = {
            'Authorization': f'Basic {self.auth}',
            'Content-Type': 'application/json'
        }
    
    def _send_request(self, method, uri, data=None):
        """Send request to TestRail API"""
        url = f"{self.url}/index.php?/api/v2/{uri}"
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=self.headers)
            elif method == 'POST':
                response = requests.post(url, headers=self.headers, json=data)
            elif method == 'PUT':
                response = requests.put(url, headers=self.headers, json=data)
            
            if response.status_code == 403:
                print("❌ Authentication failed. Please check credentials.")
                return None
            elif response.status_code == 401:
                print("❌ Invalid credentials.")
                return None
            
            response.raise_for_status()
            return response.json() if response.content else None
        except requests.exceptions.RequestException as e:
            print(f"TestRail API error: {e}")
            return None
    
    def test_connection(self):
        """Test TestRail connection"""
        print("🔍 Testing TestRail connection...")
        result = self._send_request('GET', f'get_project/{self.project_id}')
        if result:
            print(f"✅ Connected to project: {result.get('name', 'Unknown')}")
            return True
        else:
            print("❌ Failed to connect to TestRail")
            return False
    
    def get_existing_cases(self):
        """Get existing test cases"""
        print("📋 Fetching existing test cases...")
        result = self._send_request('GET', f'get_cases/{self.project_id}&suite_id={self.suite_id}')
        if result:
            print(f"📊 Found {len(result)} existing cases")
            return result
        return []
    
    def create_test_case(self, title, description, steps, priority_id=3, type_id=1):
        """Create a single test case"""
        # Convert steps to TestRail format
        formatted_steps = []
        for i, step in enumerate(steps, 1):
            formatted_steps.append({
                'content': step['step'],
                'expected': step['expected']
            })
        
        data = {
            'title': title,
            'type_id': type_id,  # 1 = Automated
            'priority_id': priority_id,  # 3 = Medium, 4 = High
            'custom_steps_separated': formatted_steps,
            'custom_preconds': description
        }
        
        result = self._send_request('POST', f'add_case/{self.suite_id}', data)
        return result
    
    def create_all_test_cases(self):
        """Create all test cases from our definitions"""
        # Load case definitions
        fixtures_path = os.path.join(os.path.dirname(__file__), "../fixtures/testrail_all_cases.json")
        
        if not os.path.exists(fixtures_path):
            print("❌ Case definitions file not found. Please run create_testrail_all_cases.py first.")
            return False
        
        with open(fixtures_path, 'r') as f:
            case_definitions = json.load(f)
        
        print(f"🚀 Creating {len(case_definitions)} test cases in TestRail...")
        print("=" * 60)
        
        created_cases = []
        failed_cases = []
        
        for case_id, case_data in case_definitions.items():
            print(f"\n📝 Creating {case_id}: {case_data['title']}")
            
            result = self.create_test_case(
                title=case_data['title'],
                description=case_data['preconditions'],
                steps=case_data['test_steps'],
                priority_id=case_data['priority_id'],
                type_id=case_data['type_id']
            )
            
            if result:
                created_cases.append({
                    'original_id': case_id,
                    'testrail_id': result['id'],
                    'title': case_data['title']
                })
                print(f"✅ Created case ID: {result['id']}")
            else:
                failed_cases.append({
                    'original_id': case_id,
                    'title': case_data['title']
                })
                print(f"❌ Failed to create {case_id}")
        
        # Print summary
        print("\n" + "=" * 60)
        print("CREATION SUMMARY")
        print("=" * 60)
        print(f"✅ Successfully created: {len(created_cases)} cases")
        print(f"❌ Failed to create: {len(failed_cases)} cases")
        
        if created_cases:
            print("\n📊 CREATED CASES:")
            for case in created_cases:
                print(f"  {case['original_id']} → TestRail ID: {case['testrail_id']}")
                print(f"    Title: {case['title']}")
        
        if failed_cases:
            print("\n❌ FAILED CASES:")
            for case in failed_cases:
                print(f"  {case['original_id']}: {case['title']}")
        
        # Generate updated mapping
        if created_cases:
            self.generate_updated_mapping(created_cases)
        
        return len(created_cases) > 0
    
    def generate_updated_mapping(self, created_cases):
        """Generate updated case mapping for conftest.py"""
        print("\n" + "=" * 60)
        print("UPDATED CASE MAPPING FOR conftest.py")
        print("=" * 60)
        
        # Create mapping from original IDs to actual TestRail IDs
        id_mapping = {
            'C345': 'test_login',
            'C346': ['test_tab_navigation[text=Home-HomePage]', 
                    'test_tab_navigation[text=Vizion AI-VizionAIPage]',
                    'test_tab_navigation[text=Reconciliation-ReconciliationPage]',
                    'test_tab_navigation[text=Ledger-LedgerPage]',
                    'test_tab_navigation[text=BI Analysis-BIAnalysisPage]',
                    'test_tab_navigation[text=Connections-ConnectionPage]'],
            'C347': 'test_tabs_navigation_single_login',
            'C348': 'test_logout_after_2fa_login',
            'C349': 'test_logout_direct_method',
            'C350': 'test_logout_via_menu',
            'C351': 'test_logout_comprehensive_fallback',
            'C352': 'test_logout_session_validation',
            'C353': 'test_scenario_1_valid_login',
            'C354': 'test_scenario_2_logout_user'
        }
        
        # Find actual TestRail IDs
        case_mapping_code = "        case_mapping = {\n"
        
        for case in created_cases:
            original_id = case['original_id']
            testrail_id = case['testrail_id']
            
            if original_id in id_mapping:
                test_names = id_mapping[original_id]
                if isinstance(test_names, list):
                    # Multiple tests map to same case (like navigation)
                    for test_name in test_names:
                        case_mapping_code += f"            '{test_name}': {testrail_id},  # {original_id}: {case['title']}\n"
                else:
                    # Single test maps to case
                    case_mapping_code += f"            '{test_names}': {testrail_id},  # {original_id}: {case['title']}\n"
        
        case_mapping_code += "        }"
        
        print(case_mapping_code)
        
        # Save to file
        mapping_file = os.path.join(os.path.dirname(__file__), "../fixtures/updated_case_mapping.py")
        with open(mapping_file, 'w') as f:
            f.write("# Updated TestRail Case Mapping\n")
            f.write("# Copy this to your tests/conftest.py file\n\n")
            f.write(case_mapping_code)
        
        print(f"\n💾 Updated mapping saved to: {mapping_file}")
        print("\n📋 NEXT STEPS:")
        print("1. Copy the case_mapping above to your tests/conftest.py")
        print("2. Replace the existing case_mapping in the pytest_runtest_makereport function")
        print("3. Run your tests with TESTRAIL_ENABLED=true")
        print("4. Verify results appear in TestRail")

def main():
    print("🚀 TestRail Case Creator")
    print("=" * 50)
    
    creator = TestRailCaseCreator()
    
    # Test connection first
    if not creator.test_connection():
        print("\n❌ Cannot connect to TestRail. Please check:")
        print("1. TESTRAIL_URL environment variable")
        print("2. TESTRAIL_USERNAME environment variable")
        print("3. TESTRAIL_PASSWORD environment variable (should be API key)")
        print("4. Network connectivity")
        print("5. TestRail instance accessibility")
        return False
    
    # Get existing cases
    existing_cases = creator.get_existing_cases()
    
    # Create all test cases
    success = creator.create_all_test_cases()
    
    if success:
        print("\n🎉 Test cases created successfully!")
        print("Your TestRail instance now has the test cases.")
        print("Update your conftest.py with the new case IDs shown above.")
    else:
        print("\n❌ Failed to create test cases.")
        print("Please check the errors above and try again.")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 