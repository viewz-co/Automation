#!/usr/bin/env python3
"""
Script to create Navigation test cases in TestRail Suite 139
Adds Purchasing and Budgeting navigation tests with all steps, goals, and assertions
"""

import os
import requests
from base64 import b64encode

# TestRail configuration
TESTRAIL_URL = os.getenv('TESTRAIL_URL', 'https://viewz.testrail.io')
TESTRAIL_USERNAME = os.getenv('TESTRAIL_USERNAME', 'automation@viewz.co')
TESTRAIL_PASSWORD = os.getenv('TESTRAIL_PASSWORD', 'e.fJg:z5q5mnAdL')

PROJECT_ID = 1
SUITE_ID = 139  # Suite 139: Main automation suite

# Authentication
auth = b64encode(f"{TESTRAIL_USERNAME}:{TESTRAIL_PASSWORD}".encode()).decode()
headers = {
    'Authorization': f'Basic {auth}',
    'Content-Type': 'application/json'
}

def send_request(method, uri, data=None):
    """Send request to TestRail API"""
    url = f"{TESTRAIL_URL}/index.php?/api/v2/{uri}"
    
    print(f"🔗 {method} {url}")
    
    try:
        if method == 'GET':
            response = requests.get(url, headers=headers, timeout=30)
        elif method == 'POST':
            response = requests.post(url, headers=headers, json=data, timeout=30)
        
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 400:
            print(f"   Response: {response.text[:500]}")
        
        response.raise_for_status()
        return response.json() if response.content else None
    except requests.exceptions.RequestException as e:
        print(f"❌ API error: {e}")
        if hasattr(e, 'response') and e.response:
            print(f"   Response: {e.response.text[:500]}")
        return None

def get_sections(suite_id):
    """Get all sections in a suite"""
    result = send_request('GET', f'get_sections/{PROJECT_ID}&suite_id={suite_id}')
    if result:
        if isinstance(result, dict) and 'sections' in result:
            return result['sections']
        return result
    return []

def find_or_create_section(suite_id, name, description="", parent_id=None):
    """Find existing section or create new one"""
    sections = get_sections(suite_id)
    
    for section in sections:
        if section.get('name') == name:
            print(f"📁 Found existing section: {name} (ID: {section.get('id')})")
            return section
    
    # Create new section
    data = {
        'suite_id': suite_id,
        'name': name,
        'description': description
    }
    if parent_id:
        data['parent_id'] = parent_id
    
    result = send_request('POST', f'add_section/{PROJECT_ID}', data)
    if result:
        print(f"✅ Created section: {name} (ID: {result.get('id')})")
        return result
    return None

def create_case(section_id, title, **kwargs):
    """Create a new test case"""
    data = {
        'title': title,
        **kwargs
    }
    
    result = send_request('POST', f'add_case/{section_id}', data)
    if result:
        print(f"✅ Created case C{result.get('id')}: {title}")
        return result
    else:
        print(f"❌ Failed to create case: {title}")
    return None

# Navigation Test Cases
NAVIGATION_TEST_CASES = [
    # Purchasing Navigation Tests
    {
        'title': 'Navigation - Purchasing Page Load',
        'template_id': 2,  # Test Case (Steps)
        'type_id': 1,  # Functional
        'priority_id': 2,  # Medium
        'custom_preconds': '''**Environment**: Stage or Production
**User**: Logged in with valid credentials and entity selected
**Menu**: Sidebar navigation is accessible''',
        'custom_steps_separated': [
            {
                'content': 'Login to the application with valid credentials',
                'expected': 'Login successful, OTP verified, redirected to home page'
            },
            {
                'content': 'Select an entity (e.g., Viewz Demo INC)',
                'expected': 'Entity is selected and displayed in the header'
            },
            {
                'content': 'Hover over the Viewz logo to open the sidebar menu',
                'expected': 'Sidebar menu expands showing all navigation options'
            },
            {
                'content': 'Click the pin button to keep menu open (optional)',
                'expected': 'Menu stays open for navigation'
            },
            {
                'content': 'Click on "Purchasing" in the sidebar menu',
                'expected': 'Purchasing page loads successfully'
            },
            {
                'content': 'Verify the page heading shows "Purchasing"',
                'expected': 'Heading "Purchasing" is visible on the page'
            },
            {
                'content': 'Verify the URL contains "purchasing"',
                'expected': 'URL includes /purchasing path'
            }
        ],
        'custom_automation_type': 1,
        'refs': 'test_navigate_to_purchasing'
    },
    {
        'title': 'Navigation - Purchasing Tab Navigation (Parametrized)',
        'template_id': 2,
        'type_id': 1,
        'priority_id': 2,
        'custom_preconds': '''**Environment**: Stage or Production
**User**: Logged in with valid credentials
**Entity**: Selected''',
        'custom_steps_separated': [
            {
                'content': 'Login and select entity',
                'expected': 'User is logged in with entity context'
            },
            {
                'content': 'Open sidebar menu',
                'expected': 'Menu is visible with all tabs'
            },
            {
                'content': 'Click "Purchasing" tab',
                'expected': 'Navigation initiated to Purchasing'
            },
            {
                'content': 'Wait for page to load',
                'expected': 'Page loads within timeout'
            },
            {
                'content': 'Verify PurchasingPage.is_loaded() returns True',
                'expected': 'Page object confirms successful load'
            }
        ],
        'custom_automation_type': 1,
        'refs': 'test_tab_navigation[text=Purchasing-PurchasingPage]'
    },
    
    # Budgeting Navigation Tests
    {
        'title': 'Navigation - Budgeting Page Load',
        'template_id': 2,
        'type_id': 1,
        'priority_id': 2,
        'custom_preconds': '''**Environment**: Stage or Production
**User**: Logged in with valid credentials and entity selected
**Menu**: Sidebar navigation is accessible''',
        'custom_steps_separated': [
            {
                'content': 'Login to the application with valid credentials',
                'expected': 'Login successful, OTP verified, redirected to home page'
            },
            {
                'content': 'Select an entity (e.g., Viewz Demo INC)',
                'expected': 'Entity is selected and displayed in the header'
            },
            {
                'content': 'Hover over the Viewz logo to open the sidebar menu',
                'expected': 'Sidebar menu expands showing all navigation options'
            },
            {
                'content': 'Click the pin button to keep menu open (optional)',
                'expected': 'Menu stays open for navigation'
            },
            {
                'content': 'Click on "Budgeting" in the sidebar menu',
                'expected': 'Budgeting page loads successfully'
            },
            {
                'content': 'Verify the page heading shows "Budgeting"',
                'expected': 'Heading "Budgeting" is visible on the page'
            },
            {
                'content': 'Verify the URL contains "budget"',
                'expected': 'URL includes /budget path'
            }
        ],
        'custom_automation_type': 1,
        'refs': 'test_navigate_to_budgeting'
    },
    {
        'title': 'Navigation - Budgeting Tab Navigation (Parametrized)',
        'template_id': 2,
        'type_id': 1,
        'priority_id': 2,
        'custom_preconds': '''**Environment**: Stage or Production
**User**: Logged in with valid credentials
**Entity**: Selected''',
        'custom_steps_separated': [
            {
                'content': 'Login and select entity',
                'expected': 'User is logged in with entity context'
            },
            {
                'content': 'Open sidebar menu',
                'expected': 'Menu is visible with all tabs'
            },
            {
                'content': 'Click "Budgeting" tab',
                'expected': 'Navigation initiated to Budgeting'
            },
            {
                'content': 'Wait for page to load',
                'expected': 'Page loads within timeout'
            },
            {
                'content': 'Verify BudgetingPage.is_loaded() returns True',
                'expected': 'Page object confirms successful load'
            }
        ],
        'custom_automation_type': 1,
        'refs': 'test_tab_navigation[text=Budgeting-BudgetingPage]'
    },
    
    # Combined Navigation Test
    {
        'title': 'Navigation - All Tabs Single Login (Including Purchasing & Budgeting)',
        'template_id': 2,
        'type_id': 1,
        'priority_id': 1,  # High
        'custom_preconds': '''**Environment**: Stage or Production
**User**: Logged in with valid credentials
**Entity**: Selected
**Goal**: Verify all navigation tabs work in a single session''',
        'custom_steps_separated': [
            {
                'content': 'Login and select entity',
                'expected': 'User is logged in with entity context'
            },
            {
                'content': 'Open sidebar menu and pin it',
                'expected': 'Menu is pinned open'
            },
            {
                'content': 'Navigate to Home tab',
                'expected': 'Home page loads successfully'
            },
            {
                'content': 'Navigate to Vizion AI tab',
                'expected': 'Vizion AI page loads successfully'
            },
            {
                'content': 'Navigate to Reconciliation tab',
                'expected': 'Reconciliation page loads successfully'
            },
            {
                'content': 'Navigate to Ledger tab',
                'expected': 'Ledger page loads successfully'
            },
            {
                'content': 'Navigate to Invoicing tab',
                'expected': 'Invoicing page loads successfully'
            },
            {
                'content': 'Navigate to Purchasing tab',
                'expected': 'Purchasing page loads successfully'
            },
            {
                'content': 'Navigate to BI Analysis tab',
                'expected': 'BI Analysis page loads successfully'
            },
            {
                'content': 'Navigate to Budgeting tab',
                'expected': 'Budgeting page loads successfully'
            },
            {
                'content': 'Verify all tabs passed navigation',
                'expected': 'All 8 tabs load correctly with no failures'
            }
        ],
        'custom_automation_type': 1,
        'refs': 'test_tabs_navigation_single_login_with_entity'
    }
]

def main():
    print("=" * 70)
    print("🧪 Creating Navigation Test Cases in TestRail Suite 139")
    print("=" * 70)
    
    # Use existing Navigation section (ID: 531) in Suite 139
    # Don't create a new section - add to existing " Navigation" section
    section_id = 531  # Existing Navigation section
    print(f"📁 Using existing Navigation section (ID: {section_id})")
    section = {'id': section_id}
    
    if not section:
        print("❌ Failed to find/create Navigation section")
        return
    
    section_id = section.get('id')
    print(f"\n📁 Using section ID: {section_id}")
    
    # Create test cases
    created_cases = []
    
    print("\n" + "=" * 70)
    print("📝 Creating Navigation Test Cases")
    print("=" * 70)
    
    for i, test_case in enumerate(NAVIGATION_TEST_CASES, 1):
        print(f"\n[{i}/{len(NAVIGATION_TEST_CASES)}] Creating: {test_case['title']}")
        
        result = create_case(section_id, **test_case)
        if result:
            created_cases.append({
                'id': result.get('id'),
                'title': test_case['title'],
                'refs': test_case.get('refs', '')
            })
    
    # Summary
    print("\n" + "=" * 70)
    print("📊 SUMMARY")
    print("=" * 70)
    print(f"✅ Created {len(created_cases)} test cases")
    
    if created_cases:
        print("\n📋 Created Cases:")
        for case in created_cases:
            print(f"   C{case['id']}: {case['title']}")
            if case['refs']:
                print(f"      └─ Automation ref: {case['refs']}")
    
    # Generate mapping for conftest.py
    print("\n" + "=" * 70)
    print("📝 Add these mappings to tests/conftest.py case_mapping:")
    print("=" * 70)
    for case in created_cases:
        if case['refs']:
            # Extract simple test name
            test_name = case['refs'].split('[')[0] if '[' in case['refs'] else case['refs']
            print(f'    "{test_name}": {case["id"]},')
    
    print("\n✅ Done!")

if __name__ == "__main__":
    main()

