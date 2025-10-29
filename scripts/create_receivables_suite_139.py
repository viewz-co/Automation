#!/usr/bin/env python3
"""
Create Receivables TestRail Cases in Suite 139
"""

import os
import requests
from base64 import b64encode

class ReceivablesTestRailCreatorSuite139:
    def __init__(self):
        self.url = os.getenv('TESTRAIL_URL', 'https://viewz.testrail.io')
        self.username = os.getenv('TESTRAIL_USERNAME', 'automation@viewz.co')
        self.password = os.getenv('TESTRAIL_PASSWORD', 'e.fJg:z5q5mnAdL')
        self.project_id = int(os.getenv('TESTRAIL_PROJECT_ID', '1'))
        self.suite_id = 139  # Suite 139
        
        self.receivables_section_id = None
        
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
                response = requests.get(url, headers=self.headers, timeout=10)
            elif method == 'POST':
                response = requests.post(url, headers=self.headers, json=data, timeout=10)
            
            if response.status_code in [403, 401]:
                print(f"❌ Authentication failed (Status {response.status_code})")
                return None
            
            response.raise_for_status()
            return response.json() if response.content else None
        except requests.exceptions.RequestException as e:
            print(f"❌ API error: {e}")
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
    
    def find_or_create_section(self):
        """Find or create Receivables Operations section in Suite 139"""
        print("📁 Looking for Receivables Operations section in Suite 139...")
        
        sections = self._send_request('GET', f'get_sections/{self.project_id}&suite_id={self.suite_id}')
        
        if sections:
            if isinstance(sections, dict) and 'sections' in sections:
                sections = sections['sections']
            
            if isinstance(sections, list):
                print(f"📊 Found {len(sections)} sections in Suite 139")
                
                for section in sections:
                    if not isinstance(section, dict):
                        continue
                    section_name = section.get('name', '')
                    print(f"  - {section_name} (ID: {section.get('id')})")
                    if 'Receivables Operations' in section_name:
                        print(f"✅ Found existing Receivables Operations section: ID {section['id']}")
                        self.receivables_section_id = section['id']
                        return True
                
                # Create Receivables Operations section
                print(f"📁 Creating new Receivables Operations section...")
                data = {
                    'suite_id': self.suite_id,
                    'name': 'Receivables Operations',
                    'description': 'Automated tests for Receivables functionality'
                }
                
                result = self._send_request('POST', f'add_section/{self.project_id}', data)
                if result:
                    self.receivables_section_id = result['id']
                    print(f"✅ Created Receivables Operations section: ID {self.receivables_section_id}")
                    return True
        
        return False
    
    def create_test_case(self, section_id, case_data):
        """Create a single test case"""
        data = {
            'title': case_data['title'],
            'type_id': case_data.get('type_id', 1),
            'priority_id': case_data.get('priority_id', 3),
            'estimate': case_data.get('estimate', '5m'),
            'refs': case_data.get('refs', ''),
            'custom_preconds': case_data.get('preconditions', ''),
            'custom_steps': case_data.get('steps', ''),
            'custom_expected': case_data.get('expected', ''),
            'custom_automation_type': 1
        }
        
        result = self._send_request('POST', f'add_case/{section_id}', data)
        return result
    
    def get_receivables_case_definitions(self):
        """Define all 13 receivables test cases"""
        return [
            {
                'title': 'Verify Receivable List is Displayed',
                'type_id': 1,
                'priority_id': 4,
                'estimate': '5m',
                'preconditions': 'User is logged in\nEntity is selected\nUser has access to Reconciliation module',
                'steps': '1. Navigate to Reconciliation section\n2. Click on Receivables tab\n3. Wait for page to load\n4. Verify receivables list/table is visible',
                'expected': 'Receivables list table is displayed\nTable shows receivables with proper columns\nData loads without errors'
            },
            {
                'title': 'Upload Valid Receivable File',
                'type_id': 1,
                'priority_id': 4,
                'estimate': '5m',
                'preconditions': 'User is on the Receivables page\nUpload functionality is available',
                'steps': '1. Navigate to Receivables page\n2. Click Upload button\n3. Select valid PDF file\n4. Confirm upload',
                'expected': 'File uploads successfully\nReceivable appears in the list\nSuccess message is displayed'
            },
            {
                'title': 'Upload Invalid File Type',
                'type_id': 2,
                'priority_id': 3,
                'estimate': '3m',
                'preconditions': 'User is on the Receivables page',
                'steps': '1. Navigate to Receivables page\n2. Click Upload button\n3. Attempt to select invalid file type\n4. Observe system response',
                'expected': 'System rejects invalid file type\nError message displayed'
            },
            {
                'title': 'Upload Duplicate Receivable',
                'type_id': 2,
                'priority_id': 3,
                'estimate': '3m',
                'preconditions': 'Receivable file already exists in system',
                'steps': '1. Upload a receivable file\n2. Attempt to upload the same file again',
                'expected': 'System detects duplicate\nWarning message displayed'
            },
            {
                'title': 'Edit/Delete Buttons Functionality',
                'type_id': 1,
                'priority_id': 4,
                'estimate': '5m',
                'preconditions': 'Receivables exist in the list',
                'steps': '1. Navigate to Receivables page\n2. Locate receivable row\n3. Verify Edit button exists\n4. Verify Delete button exists',
                'expected': 'Edit button is visible\nDelete button is visible\nButtons are functional'
            },
            {
                'title': 'Status Dropdowns',
                'type_id': 1,
                'priority_id': 3,
                'estimate': '3m',
                'preconditions': 'Receivables with various statuses exist',
                'steps': '1. Navigate to Receivables page\n2. Locate status dropdown\n3. Open dropdown\n4. Select different status options',
                'expected': 'Status dropdown opens correctly\nStatus options available\nFiltering works'
            },
            {
                'title': 'Search/Filter and Menu Operations',
                'type_id': 1,
                'priority_id': 3,
                'estimate': '5m',
                'preconditions': 'Multiple receivables exist',
                'steps': '1. Test search functionality\n2. Test context menu\n3. Verify menu options',
                'expected': 'Search filters correctly\nContext menu appears\nMenu options appropriate'
            },
            {
                'title': 'Form Validation',
                'type_id': 1,
                'priority_id': 4,
                'estimate': '10m',
                'preconditions': 'User can open edit receivable form',
                'steps': '1. Open edit form\n2. Test mandatory field validation\n3. Test field format validation',
                'expected': 'Mandatory fields validated\nValidation messages clear\nInvalid data rejected'
            },
            {
                'title': 'Form Calculations and Recognition Timing',
                'type_id': 1,
                'priority_id': 3,
                'estimate': '10m',
                'preconditions': 'GL accounts configured',
                'steps': '1. Test line totals calculation\n2. Test GL Account dropdown\n3. Test recognition timing options',
                'expected': 'Calculations accurate\nGL dropdown works\nTiming options function'
            },
            {
                'title': 'Recording and Journal Entries',
                'type_id': 1,
                'priority_id': 4,
                'estimate': '10m',
                'preconditions': 'Receivable exists in New/Matched status',
                'steps': '1. Select receivable\n2. Click Record\n3. Verify status changes\n4. View journal entry',
                'expected': 'Receivable recorded\nStatus updated\nJournal entry created\nJE details correct'
            },
            {
                'title': 'Delete Operations',
                'type_id': 1,
                'priority_id': 3,
                'estimate': '5m',
                'preconditions': 'Receivables exist with different statuses',
                'steps': '1. Test delete confirmation\n2. Test delete prevention for recorded items',
                'expected': 'Delete confirmation appears\nRecorded items cannot be deleted'
            },
            {
                'title': 'View Operations',
                'type_id': 1,
                'priority_id': 2,
                'estimate': '3m',
                'preconditions': 'Receivables exist',
                'steps': '1. Right-click receivable\n2. Select View in New Tab\n3. Verify details display',
                'expected': 'New tab opens\nDetails displayed correctly'
            },
            {
                'title': 'Context Menu by Status',
                'type_id': 1,
                'priority_id': 3,
                'estimate': '10m',
                'preconditions': 'Receivables with different statuses exist',
                'steps': '1. Test New status menu\n2. Test Matched status menu\n3. Test Recorded status menu',
                'expected': 'Menu options appropriate for each status\nRecorded has limited options'
            }
        ]
    
    def create_all_receivables_cases(self):
        """Create all 13 receivables test cases"""
        if not self.receivables_section_id:
            print("❌ No section ID available")
            return False
        
        cases = self.get_receivables_case_definitions()
        
        print(f"\n🚀 Creating {len(cases)} receivables test cases in Suite 139...")
        print("=" * 60)
        
        created_cases = []
        failed_cases = []
        
        for i, case_data in enumerate(cases, 1):
            print(f"\n📝 [{i}/{len(cases)}] Creating: {case_data['title']}")
            
            result = self.create_test_case(self.receivables_section_id, case_data)
            
            if result:
                created_cases.append({
                    'testrail_id': result['id'],
                    'title': case_data['title']
                })
                print(f"✅ Created TestRail case ID: C{result['id']}")
            else:
                failed_cases.append(case_data['title'])
                print(f"❌ Failed to create: {case_data['title']}")
        
        # Print summary
        print("\n" + "=" * 60)
        print("📊 CREATION SUMMARY")
        print("=" * 60)
        print(f"✅ Successfully created: {len(created_cases)} cases")
        print(f"❌ Failed to create: {len(failed_cases)} cases")
        
        if created_cases:
            print("\n🎯 CREATED CASES IN SUITE 139:")
            for case in created_cases:
                print(f"  C{case['testrail_id']}: {case['title']}")
            
            # Save mapping
            import json
            mapping = {str(i+1): case['testrail_id'] for i, case in enumerate(created_cases)}
            with open('receivables_suite_139_mapping.json', 'w') as f:
                json.dump({
                    'suite_id': 139,
                    'section_id': self.receivables_section_id,
                    'total_cases': len(created_cases),
                    'case_ids': [c['testrail_id'] for c in created_cases],
                    'mapping': mapping,
                    'cases': created_cases
                }, f, indent=2)
            
            print(f"\n💾 Mapping saved to: receivables_suite_139_mapping.json")
        
        return len(created_cases) > 0

def main():
    print("🎯 Receivables TestRail Case Creator - Suite 139")
    print("=" * 60)
    
    creator = ReceivablesTestRailCreatorSuite139()
    
    if not creator.test_connection():
        print("\n❌ Cannot connect to TestRail")
        return False
    
    if not creator.find_or_create_section():
        print("\n❌ Failed to find/create Receivables Operations section")
        return False
    
    success = creator.create_all_receivables_cases()
    
    if success:
        print("\n🎉 SUCCESS! Receivables cases created in Suite 139!")
    else:
        print("\n❌ Failed to create test cases")
    
    return success

if __name__ == "__main__":
    import sys
    success = main()
    sys.exit(0 if success else 1)

