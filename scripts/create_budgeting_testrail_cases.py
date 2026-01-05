#!/usr/bin/env python3
"""
Script to create Budgeting test cases in TestRail Suite 139
Adds Budget Group and Budget Builder tests with all steps, goals, and assertions
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
        if section.get('name').strip() == name.strip():
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

# Budgeting Test Cases
BUDGETING_TEST_CASES = [
    # Budget Group Tests
    {
        'title': 'Budgeting - Add Budget Group',
        'template_id': 2,  # Test Case (Steps)
        'type_id': 1,  # Functional
        'priority_id': 2,  # Medium
        'custom_preconds': '''**Environment**: Stage or Production
**User**: Logged in with valid credentials and entity selected
**Page**: Budgeting page accessible via sidebar''',
        'custom_steps_separated': [
            {
                'content': 'Navigate to Budgeting page via sidebar menu',
                'expected': 'Budgeting page loads with "Chart Of Budget" tab visible'
            },
            {
                'content': 'Click "Add Budget Group" button',
                'expected': 'Create Budget Group modal/dialog opens'
            },
            {
                'content': 'Fill Budget ID field (e.g., QA-001)',
                'expected': 'Budget ID is entered'
            },
            {
                'content': 'Fill Name field (e.g., QA Budget Test)',
                'expected': 'Name is entered'
            },
            {
                'content': 'Select Report Type from dropdown',
                'expected': 'Report Type is selected (e.g., Balance Sheet)'
            },
            {
                'content': 'Select Account Type from dropdown',
                'expected': 'Account Type is selected (e.g., Current Assets)'
            },
            {
                'content': 'Select Group from dropdown',
                'expected': 'Group is selected'
            },
            {
                'content': 'Click "Create Group" button',
                'expected': 'Budget group is created and appears in the list'
            },
            {
                'content': 'Verify budget group exists in the Chart of Budget list',
                'expected': 'New budget group is visible in the table'
            }
        ],
        'custom_automation_type': 1,
        'refs': 'test_add_budget_group'
    },
    {
        'title': 'Budgeting - Add Budget Group with Custom Name',
        'template_id': 2,
        'type_id': 1,
        'priority_id': 2,
        'custom_preconds': '''**Environment**: Stage or Production
**User**: Logged in with entity selected
**Goal**: Verify custom names work for budget groups''',
        'custom_steps_separated': [
            {
                'content': 'Navigate to Budgeting page',
                'expected': 'Budgeting page loads'
            },
            {
                'content': 'Click Add Budget Group',
                'expected': 'Form opens'
            },
            {
                'content': 'Enter specific custom name "QA Test Budget 2026"',
                'expected': 'Custom name is entered'
            },
            {
                'content': 'Fill required fields and save',
                'expected': 'Budget group created with custom name'
            },
            {
                'content': 'Verify group name matches exactly',
                'expected': 'Group name is "QA Test Budget 2026"'
            }
        ],
        'custom_automation_type': 1,
        'refs': 'test_add_budget_group_with_custom_name'
    },
    
    # Budget Builder Tests
    {
        'title': 'Budgeting - Open Budget Builder',
        'template_id': 2,
        'type_id': 1,
        'priority_id': 2,
        'custom_preconds': '''**Environment**: Stage or Production
**User**: Logged in with entity selected
**Prerequisite**: At least one budget group exists''',
        'custom_steps_separated': [
            {
                'content': 'Navigate to Budgeting page',
                'expected': 'Budgeting page with Chart of Budget tab'
            },
            {
                'content': 'Create or select an existing budget group',
                'expected': 'Budget group is available'
            },
            {
                'content': 'Click on "Budget Builder" tab or link',
                'expected': 'Budget Builder view opens'
            },
            {
                'content': 'Verify Budget Builder is loaded',
                'expected': 'Budget Builder UI with GL accounts and amount fields visible'
            }
        ],
        'custom_automation_type': 1,
        'refs': 'test_open_budget_builder'
    },
    {
        'title': 'Budgeting - Budget Builder Add Line',
        'template_id': 2,
        'type_id': 1,
        'priority_id': 2,
        'custom_preconds': '''**Environment**: Stage or Production
**User**: Logged in with entity selected
**Prerequisite**: Budget group exists, Budget Builder is open''',
        'custom_steps_separated': [
            {
                'content': 'Create a budget group',
                'expected': 'Budget group created'
            },
            {
                'content': 'Open Budget Builder for the group',
                'expected': 'Budget Builder opens'
            },
            {
                'content': 'Add a budget line with amount (e.g., $25,000)',
                'expected': 'Budget line is added to the builder'
            },
            {
                'content': 'Save the budget',
                'expected': 'Budget is saved successfully'
            }
        ],
        'custom_automation_type': 1,
        'refs': 'test_budget_builder_add_line'
    },
    {
        'title': 'Budgeting - Build Complete Budget with Multiple Lines',
        'template_id': 2,
        'type_id': 1,
        'priority_id': 1,  # High
        'custom_preconds': '''**Environment**: Stage or Production
**User**: Logged in with entity selected
**Goal**: Create complete budget with quarterly breakdown''',
        'custom_steps_separated': [
            {
                'content': 'Create a budget group "Complete Budget Test"',
                'expected': 'Budget group created'
            },
            {
                'content': 'Open Budget Builder',
                'expected': 'Builder opens'
            },
            {
                'content': 'Add budget line for Q1: $50,000',
                'expected': 'Q1 budget line added'
            },
            {
                'content': 'Add budget line for Q2: $75,000',
                'expected': 'Q2 budget line added'
            },
            {
                'content': 'Add budget line for Q3: $60,000',
                'expected': 'Q3 budget line added'
            },
            {
                'content': 'Add budget line for Q4: $80,000',
                'expected': 'Q4 budget line added'
            },
            {
                'content': 'Save complete budget',
                'expected': 'Total budget of $265,000 is saved'
            },
            {
                'content': 'Verify all lines are saved',
                'expected': 'Budget is complete with all 4 quarters'
            }
        ],
        'custom_automation_type': 1,
        'refs': 'test_build_complete_budget'
    },
    
    # E2E Integration Test
    {
        'title': 'Budgeting - E2E Budget to GL Account Integration',
        'template_id': 2,
        'type_id': 1,
        'priority_id': 1,  # High
        'custom_preconds': '''**Environment**: Stage or Production
**User**: Logged in with entity selected
**Goal**: Verify budget groups appear in GL Account budget selection''',
        'custom_steps_separated': [
            {
                'content': 'Navigate to Budgeting page',
                'expected': 'Budgeting page loads'
            },
            {
                'content': 'Create a new budget group "E2E Test Budget"',
                'expected': 'Budget group is created'
            },
            {
                'content': 'Navigate to Ledger > Chart of Accounts',
                'expected': 'Chart of Accounts page loads'
            },
            {
                'content': 'Click on a GL Account to edit',
                'expected': 'GL Account edit mode opens'
            },
            {
                'content': 'Find the Budget dropdown/column',
                'expected': 'Budget selection field is visible'
            },
            {
                'content': 'Verify "E2E Test Budget" appears in the dropdown',
                'expected': 'Created budget group is available for selection'
            },
            {
                'content': 'Cleanup: Delete test budget group',
                'expected': 'Test data cleaned up'
            }
        ],
        'custom_automation_type': 1,
        'refs': 'test_budget_appears_in_gl_account_dropdown'
    },
    
    # Validation Tests
    {
        'title': 'Budgeting - Page Elements Validation',
        'template_id': 2,
        'type_id': 1,
        'priority_id': 3,  # Low
        'custom_preconds': '''**Environment**: Stage or Production
**User**: Logged in with entity selected''',
        'custom_steps_separated': [
            {
                'content': 'Navigate to Budgeting page',
                'expected': 'Page loads'
            },
            {
                'content': 'Verify "Budgeting" heading is visible',
                'expected': 'Heading is displayed'
            },
            {
                'content': 'Verify Add Budget Group button exists',
                'expected': 'Button is visible'
            },
            {
                'content': 'Verify table/list for budget groups exists',
                'expected': 'Data grid is displayed'
            }
        ],
        'custom_automation_type': 1,
        'refs': 'test_budgeting_page_elements'
    },
    {
        'title': 'Budgeting - Budget Groups List Display',
        'template_id': 2,
        'type_id': 1,
        'priority_id': 3,
        'custom_preconds': '''**Environment**: Stage or Production
**User**: Logged in with entity selected''',
        'custom_steps_separated': [
            {
                'content': 'Navigate to Budgeting page',
                'expected': 'Page loads'
            },
            {
                'content': 'Get list of existing budget groups',
                'expected': 'Groups are retrieved'
            },
            {
                'content': 'Verify list is accessible and displays data',
                'expected': 'Budget groups are visible in the table'
            }
        ],
        'custom_automation_type': 1,
        'refs': 'test_budget_group_list_display'
    }
]

def main():
    print("=" * 70)
    print("🧪 Creating Budgeting Test Cases in TestRail Suite 139")
    print("=" * 70)
    
    # Find or create Budgeting section (use existing one if available)
    # Looking for existing "Budgeting" or similar section
    sections = get_sections(SUITE_ID)
    budgeting_section = None
    
    for section in sections:
        name = section.get('name', '').strip().lower()
        if 'budget' in name:
            budgeting_section = section
            print(f"📁 Found existing section: {section.get('name')} (ID: {section.get('id')})")
            break
    
    if not budgeting_section:
        budgeting_section = find_or_create_section(
            SUITE_ID,
            'Budgeting Operations',
            'Tests for Budget Group creation and Budget Builder functionality'
        )
    
    if not budgeting_section:
        print("❌ Failed to find/create Budgeting section")
        return
    
    section_id = budgeting_section.get('id')
    print(f"\n📁 Using section ID: {section_id}")
    
    # Create test cases
    created_cases = []
    
    print("\n" + "=" * 70)
    print("📝 Creating Budgeting Test Cases")
    print("=" * 70)
    
    for i, test_case in enumerate(BUDGETING_TEST_CASES, 1):
        print(f"\n[{i}/{len(BUDGETING_TEST_CASES)}] Creating: {test_case['title']}")
        
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
            print(f'    "{case["refs"]}": {case["id"]},')
    
    print("\n✅ Done!")

if __name__ == "__main__":
    main()

