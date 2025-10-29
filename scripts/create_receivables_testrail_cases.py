#!/usr/bin/env python3
"""
Create Receivables TestRail Cases Automatically
Creates 13 TestRail cases (C8066-C8078) for receivables testing
"""

import os
import sys
import requests
from base64 import b64encode

class ReceivablesTestRailCreator:
    def __init__(self):
        # TestRail connection settings
        self.url = os.getenv('TESTRAIL_URL', 'https://viewz.testrail.io')
        self.username = os.getenv('TESTRAIL_USERNAME', 'automation@viewz.co')
        self.password = os.getenv('TESTRAIL_PASSWORD', 'e.fJg:z5q5mnAdL')
        
        # Project and suite configuration
        self.project_id = int(os.getenv('TESTRAIL_PROJECT_ID', '1'))
        self.suite_id = int(os.getenv('TESTRAIL_SUITE_ID', '4'))
        
        # Section ID for Receivables (will need to find or create this)
        self.receivables_section_id = None
        
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
            
            if response.status_code in [403, 401]:
                print(f"❌ Authentication failed (Status {response.status_code})")
                return None
            
            response.raise_for_status()
            return response.json() if response.content else None
        except requests.exceptions.RequestException as e:
            print(f"❌ TestRail API error: {e}")
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
        """Find or create Receivables section"""
        print("📁 Looking for Receivables section...")
        
        # Get all sections
        sections = self._send_request('GET', f'get_sections/{self.project_id}&suite_id={self.suite_id}')
        
        print(f"🔍 Debug: sections type = {type(sections)}, content = {sections if sections else 'None'}")
        
        if sections:
            # Handle both dict and list responses
            if isinstance(sections, dict) and 'sections' in sections:
                sections = sections['sections']
            
            if isinstance(sections, list):
                # Look for Reconciliation section first
                reconciliation_section = None
                receivables_section = None
                
                print(f"📊 Found {len(sections)} sections")
                
                for section in sections:
                    if not isinstance(section, dict):
                        continue
                    section_name = section.get('name', '')
                    print(f"  - {section_name} (ID: {section.get('id')})")
                    if 'Reconciliation' in section_name:
                        reconciliation_section = section
                    if 'Receivables' in section_name:
                        receivables_section = section
                
                if receivables_section:
                    print(f"✅ Found existing Receivables section: ID {receivables_section['id']}")
                    self.receivables_section_id = receivables_section['id']
                    return True
                
                # Create Receivables section
                print(f"📁 Creating new Receivables section...")
                if reconciliation_section:
                    print(f"   Under Reconciliation section ID: {reconciliation_section['id']}")
                    data = {
                        'suite_id': self.suite_id,
                        'parent_id': reconciliation_section['id'],
                        'name': 'Receivables',
                        'description': 'Automated tests for Receivables functionality'
                    }
                else:
                    print(f"   As top-level section")
                    data = {
                        'suite_id': self.suite_id,
                        'name': 'Reconciliation - Receivables',
                        'description': 'Automated tests for Receivables functionality'
                    }
                
                result = self._send_request('POST', f'add_section/{self.project_id}', data)
                if result:
                    self.receivables_section_id = result['id']
                    print(f"✅ Created Receivables section: ID {self.receivables_section_id}")
                    return True
                else:
                    print(f"❌ Failed to create section")
        
        # If no sections exist, create without parent
        print("📁 No sections found, creating Receivables as new section...")
        data = {
            'suite_id': self.suite_id,
            'name': 'Receivables',
            'description': 'Receivables test cases'
        }
        result = self._send_request('POST', f'add_section/{self.project_id}', data)
        if result:
            self.receivables_section_id = result['id']
            print(f"✅ Created Receivables section: ID {self.receivables_section_id}")
            return True
        
        return False
    
    def create_test_case(self, section_id, case_data):
        """Create a single test case"""
        data = {
            'title': case_data['title'],
            'type_id': case_data.get('type_id', 1),  # 1 = Automated
            'priority_id': case_data.get('priority_id', 3),  # 3 = Medium, 4 = High
            'estimate': case_data.get('estimate', '5m'),
            'refs': case_data.get('refs', ''),
            'custom_preconds': case_data.get('preconditions', ''),
            'custom_steps': case_data.get('steps', ''),
            'custom_expected': case_data.get('expected', ''),
            'custom_automation_type': 1  # Automated
        }
        
        result = self._send_request('POST', f'add_case/{section_id}', data)
        return result
    
    def get_receivables_case_definitions(self):
        """Define all 13 receivables test cases"""
        return [
            {
                'title': 'Verify Receivable List is Displayed',
                'type_id': 1,  # Functional
                'priority_id': 4,  # High
                'estimate': '5m',
                'refs': 'C8066',
                'preconditions': 'User is logged in\nEntity is selected\nUser has access to Reconciliation module',
                'steps': '1. Navigate to Reconciliation section\n2. Click on Receivables tab\n3. Wait for page to load\n4. Verify receivables list/table is visible',
                'expected': 'Receivables list table is displayed\nTable shows receivables with proper columns (Date, Customer, Amount, Status)\nData loads without errors'
            },
            {
                'title': 'Upload Valid Receivable File',
                'type_id': 1,  # Functional
                'priority_id': 4,  # High
                'estimate': '5m',
                'refs': 'C8067',
                'preconditions': 'User is on the Receivables page\nUpload functionality is available\nTest receivable PDF file exists',
                'steps': '1. Navigate to Receivables page\n2. Click Upload button\n3. Select valid PDF file\n4. Confirm upload',
                'expected': 'File uploads successfully\nReceivable appears in the list\nSuccess message is displayed'
            },
            {
                'title': 'Upload Invalid File Type',
                'type_id': 2,  # Negative
                'priority_id': 3,  # Medium
                'estimate': '3m',
                'refs': 'C8068',
                'preconditions': 'User is on the Receivables page\nUpload functionality is available',
                'steps': '1. Navigate to Receivables page\n2. Click Upload button\n3. Attempt to select .txt or other non-PDF file\n4. Observe system response',
                'expected': 'System rejects invalid file type\nError message displayed\nFile is not uploaded'
            },
            {
                'title': 'Upload Duplicate Receivable',
                'type_id': 2,  # Negative
                'priority_id': 3,  # Medium
                'estimate': '3m',
                'refs': 'C8069',
                'preconditions': 'User is on the Receivables page\nReceivable file already exists in system',
                'steps': '1. Upload a receivable file\n2. Attempt to upload the same file again\n3. Observe system response',
                'expected': 'System detects duplicate\nWarning/error message displayed\nDuplicate is not created'
            },
            {
                'title': 'Edit/Delete Buttons Functionality',
                'type_id': 1,  # Functional
                'priority_id': 4,  # High
                'estimate': '5m',
                'refs': 'C8070',
                'preconditions': 'User is on the Receivables page\nReceivables exist in the list',
                'steps': '1. Navigate to Receivables page\n2. Locate receivable row\n3. Verify Edit button exists\n4. Verify Delete button exists\n5. Check button accessibility',
                'expected': 'Edit button is visible\nDelete button is visible\nButtons are clickable and functional'
            },
            {
                'title': 'Status Dropdowns',
                'type_id': 1,  # Functional
                'priority_id': 3,  # Medium
                'estimate': '3m',
                'refs': 'C8071',
                'preconditions': 'User is on the Receivables page\nReceivables with various statuses exist',
                'steps': '1. Navigate to Receivables page\n2. Locate status dropdown\n3. Open dropdown\n4. Select different status options\n5. Verify filtering works',
                'expected': 'Status dropdown is visible\nDropdown opens correctly\nStatus options are available (New, Matched, Recorded)\nFiltering by status works'
            },
            {
                'title': 'Search/Filter and Menu Operations',
                'type_id': 1,  # Functional
                'priority_id': 3,  # Medium
                'estimate': '5m',
                'refs': 'C8072',
                'preconditions': 'User is on the Receivables page\nMultiple receivables exist',
                'steps': '1. Test search functionality:\n  - Enter search term\n  - Verify results filter correctly\n2. Test context menu:\n  - Right-click receivable\n  - Verify menu appears\n  - Check menu options',
                'expected': 'Search filters results correctly\nContext menu appears on right-click\nMenu options are appropriate'
            },
            {
                'title': 'Form Validation',
                'type_id': 1,  # Functional
                'priority_id': 4,  # High
                'estimate': '10m',
                'refs': 'C8073',
                'preconditions': 'User can open edit receivable form',
                'steps': '1. Open edit form for a receivable\n2. Test mandatory field validation:\n  - Leave required fields empty\n  - Attempt to submit\n  - Verify validation messages\n3. Test field format validation\n4. Test form popup layout',
                'expected': 'Mandatory fields are validated\nValidation messages are clear\nForm layout is correct\nInvalid data is rejected'
            },
            {
                'title': 'Form Calculations and Recognition Timing',
                'type_id': 1,  # Functional
                'priority_id': 3,  # Medium
                'estimate': '10m',
                'refs': 'C8074',
                'preconditions': 'User can edit receivables\nGL accounts are configured',
                'steps': '1. Test line totals calculation\n2. Test GL Account dropdown\n3. Test recognition timing:\n  - Select "Single Date" option\n  - Select "Deferred Period" option\n  - Verify timing options work',
                'expected': 'Line totals calculate correctly\nGL account dropdown works\nRecognition timing options function properly\nCalculations are accurate'
            },
            {
                'title': 'Recording and Journal Entries',
                'type_id': 1,  # Functional
                'priority_id': 4,  # High
                'estimate': '10m',
                'refs': 'C8075',
                'preconditions': 'Receivable exists in "New" or "Matched" status\nUser has permission to record receivables',
                'steps': '1. Select a receivable\n2. Click Record button\n3. Verify status changes to "Recorded"\n4. View journal entry:\n  - Click "Show Journal Entry"\n  - Verify JE details display\n  - Confirm JE amounts are read-only\n5. Verify JE description fields',
                'expected': 'Receivable is recorded successfully\nStatus updates to "Recorded"\nJournal entry is created\nJE display shows correct information\nJE amount and description fields are read-only'
            },
            {
                'title': 'Delete Operations',
                'type_id': 1,  # Functional
                'priority_id': 3,  # Medium
                'estimate': '5m',
                'refs': 'C8076',
                'preconditions': 'Receivables exist with different statuses',
                'steps': '1. Test delete confirmation:\n  - Click delete on a "New" receivable\n  - Verify confirmation dialog appears\n  - Test Cancel and Confirm options\n2. Test delete prevention:\n  - Attempt to delete "Recorded" receivable\n  - Verify system prevents deletion\n  - Check for appropriate message',
                'expected': 'Delete confirmation dialog appears\nDialog has Cancel and Confirm buttons\nRecorded receivables cannot be deleted\nSystem shows appropriate message'
            },
            {
                'title': 'View Operations',
                'type_id': 1,  # Functional
                'priority_id': 2,  # Low
                'estimate': '3m',
                'refs': 'C8077',
                'preconditions': 'Receivables exist in the list',
                'steps': '1. Locate a receivable in the list\n2. Right-click or use action menu\n3. Select "View in New Tab" option\n4. Verify new tab opens\n5. Verify receivable details display correctly',
                'expected': 'Option to view in new tab is available\nNew tab/window opens\nReceivable details are displayed correctly\nAll information is readable'
            },
            {
                'title': 'Context Menu by Status',
                'type_id': 1,  # Functional
                'priority_id': 3,  # Medium
                'estimate': '10m',
                'refs': 'C8078',
                'preconditions': 'Receivables exist with different statuses (New, Matched, Recorded)',
                'steps': '1. Test "New" status menu:\n  - Right-click receivable with "New" status\n  - Verify menu options (Edit, Delete, Match, Record)\n2. Test "Matched" status menu:\n  - Right-click receivable with "Matched" status\n  - Verify menu options (Edit, Unmatch, Record)\n3. Test "Recorded" status menu:\n  - Right-click receivable with "Recorded" status\n  - Verify menu options (View JE, View Only)\n  - Confirm Delete is NOT available',
                'expected': 'Context menus display correctly for each status\nMenu options are appropriate for status\nRecorded receivables have limited options\nMenu actions function correctly'
            }
        ]
    
    def create_all_receivables_cases(self):
        """Create all 13 receivables test cases"""
        if not self.receivables_section_id:
            print("❌ No section ID available")
            return False
        
        cases = self.get_receivables_case_definitions()
        
        print(f"\n🚀 Creating {len(cases)} receivables test cases...")
        print("=" * 60)
        
        created_cases = []
        failed_cases = []
        
        for i, case_data in enumerate(cases, 1):
            print(f"\n📝 [{i}/{len(cases)}] Creating: {case_data['title']}")
            
            result = self.create_test_case(self.receivables_section_id, case_data)
            
            if result:
                created_cases.append({
                    'testrail_id': result['id'],
                    'title': case_data['title'],
                    'refs': case_data.get('refs', '')
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
            print("\n🎯 CREATED CASES:")
            for case in created_cases:
                print(f"  C{case['testrail_id']}: {case['title']}")
        
        if failed_cases:
            print("\n❌ FAILED CASES:")
            for title in failed_cases:
                print(f"  - {title}")
        
        # Print next steps
        if created_cases:
            print("\n" + "=" * 60)
            print("📋 NEXT STEPS")
            print("=" * 60)
            print("1. ✅ TestRail cases created successfully!")
            print("2. 📝 Note the case IDs shown above")
            print("3. 🔄 If case IDs don't match C8066-C8078:")
            print("   - Update conftest.py with actual case IDs")
            print("   - Run: scripts/update_receivables_testrail_ids.py")
            print("4. 🧪 Run tests with TestRail integration:")
            print("   TESTRAIL_ENABLED=true python -m pytest tests/e2e/reconciliation/receivables/ -v --headless")
            print("5. ✅ Verify results appear in TestRail")
        
        return len(created_cases) > 0

def main():
    print("🎯 Receivables TestRail Case Creator")
    print("=" * 60)
    print("This script will create 13 TestRail cases for Receivables")
    print("=" * 60)
    
    creator = ReceivablesTestRailCreator()
    
    # Test connection
    if not creator.test_connection():
        print("\n❌ Cannot connect to TestRail. Please check:")
        print("1. TESTRAIL_URL environment variable")
        print("2. TESTRAIL_USERNAME environment variable")
        print("3. TESTRAIL_PASSWORD environment variable")
        print("4. Network connectivity")
        return False
    
    # Find or create section
    if not creator.find_or_create_section():
        print("\n❌ Failed to find/create Receivables section")
        return False
    
    # Create all test cases
    success = creator.create_all_receivables_cases()
    
    if success:
        print("\n🎉 SUCCESS! Receivables test cases created in TestRail!")
        print("\nYou can now run your tests with TestRail integration.")
    else:
        print("\n❌ Failed to create test cases. Check errors above.")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

