#!/usr/bin/env python3
"""
Script to create TestRail test cases for DOM Structure tests.
Adds test cases for all 14 pages being monitored.
"""

import os
import requests
from base64 import b64encode

# TestRail configuration
TESTRAIL_URL = os.getenv('TESTRAIL_URL', 'https://viewz.testrail.io')
TESTRAIL_USERNAME = os.getenv('TESTRAIL_USERNAME', 'automation@viewz.co')
TESTRAIL_PASSWORD = os.getenv('TESTRAIL_PASSWORD', 'e.fJg:z5q5mnAdL')

PROJECT_ID = 1
SUITE_ID = 139

# Authentication
auth = b64encode(f"{TESTRAIL_USERNAME}:{TESTRAIL_PASSWORD}".encode()).decode()
headers = {
    'Authorization': f'Basic {auth}',
    'Content-Type': 'application/json'
}

def send_request(method, uri, data=None):
    """Send request to TestRail API"""
    url = f"{TESTRAIL_URL}/index.php?/api/v2/{uri}"
    
    try:
        if method == 'GET':
            response = requests.get(url, headers=headers, timeout=30)
        elif method == 'POST':
            response = requests.post(url, headers=headers, json=data, timeout=30)
        
        if response.status_code == 400:
            print(f"   Response: {response.text[:500]}")
        
        response.raise_for_status()
        return response.json() if response.content else None
    except requests.exceptions.RequestException as e:
        print(f"❌ API error: {e}")
        return None

def get_sections(suite_id):
    """Get all sections in a suite"""
    result = send_request('GET', f'get_sections/{PROJECT_ID}&suite_id={suite_id}')
    if result:
        if isinstance(result, dict) and 'sections' in result:
            return result['sections']
        return result
    return []

def find_or_create_section(suite_id, name, description=""):
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
    
    result = send_request('POST', f'add_section/{PROJECT_ID}', data)
    if result:
        print(f"✅ Created section: {name} (ID: {result.get('id')})")
        return result
    return None

def create_test_case(section_id, test_case):
    """Create a single test case"""
    result = send_request('POST', f'add_case/{section_id}', test_case)
    if result:
        print(f"   ✅ C{result['id']} - {test_case['title']}")
        return result['id']
    return None

# Define test cases for each page
DOM_TEST_CASES = [
    {
        "title": "DOM Structure - Home Page",
        "custom_preconds": "User is logged in to the application\nEntity is selected",
        "custom_steps_separated": [
            {"content": "Navigate to Home page", "expected": "Home page loads successfully"},
            {"content": "Verify Viewz Logo is present", "expected": "Logo element is visible"},
            {"content": "Verify Entity Selector is present", "expected": "Entity selector button is visible"},
            {"content": "Verify Main Dashboard Content is present", "expected": "Dashboard grid is rendered"},
            {"content": "Verify Navigation Menu is present", "expected": "Navigation/sidebar is visible"},
        ],
        "custom_expected": "All required DOM elements are present on the Home page",
        "refs": "test_page_dom_structure[home-page_config0]",
        "type_id": 1,
        "priority_id": 2,
    },
    {
        "title": "DOM Structure - Invoicing Page",
        "custom_preconds": "User is logged in\nEntity is selected",
        "custom_steps_separated": [
            {"content": "Navigate to Invoicing page", "expected": "Page loads successfully"},
            {"content": "Verify Add Customer Button", "expected": "Button is visible"},
            {"content": "Verify Customer Table", "expected": "Table is rendered"},
            {"content": "Verify Search Input", "expected": "Search field is visible"},
            {"content": "Verify Export Button", "expected": "Export button is visible"},
        ],
        "custom_expected": "All required DOM elements are present",
        "refs": "test_page_dom_structure[invoicing-page_config1]",
        "type_id": 1,
        "priority_id": 2,
    },
    {
        "title": "DOM Structure - Purchasing Page",
        "custom_preconds": "User is logged in\nEntity is selected",
        "custom_steps_separated": [
            {"content": "Navigate to Purchasing page", "expected": "Page loads successfully"},
            {"content": "Verify Add Vendor Button", "expected": "Button is visible"},
            {"content": "Verify Vendor Table", "expected": "Table is rendered"},
            {"content": "Verify Search Input", "expected": "Search field is visible"},
            {"content": "Verify Export Button", "expected": "Export button is visible"},
        ],
        "custom_expected": "All required DOM elements are present",
        "refs": "test_page_dom_structure[purchasing-page_config2]",
        "type_id": 1,
        "priority_id": 2,
    },
    {
        "title": "DOM Structure - Budgeting Page",
        "custom_preconds": "User is logged in\nEntity is selected",
        "custom_steps_separated": [
            {"content": "Navigate to Budgeting page via sidebar", "expected": "Page loads"},
            {"content": "Verify Sidebar Link is present", "expected": "Link is visible"},
            {"content": "Verify Budget Content", "expected": "Content is rendered"},
            {"content": "Verify Action Buttons", "expected": "Buttons are visible"},
        ],
        "custom_expected": "All required DOM elements are present",
        "refs": "test_page_dom_structure[budgeting-page_config3]",
        "type_id": 1,
        "priority_id": 2,
    },
    {
        "title": "DOM Structure - Ledger Page",
        "custom_preconds": "User is logged in\nEntity is selected",
        "custom_steps_separated": [
            {"content": "Navigate to Ledger page via sidebar", "expected": "Page loads"},
            {"content": "Verify Sidebar Link is present", "expected": "Link is visible"},
            {"content": "Verify Accounts Table", "expected": "Table is rendered"},
            {"content": "Verify Search Input", "expected": "Search field is visible"},
        ],
        "custom_expected": "All required DOM elements are present",
        "refs": "test_page_dom_structure[ledger-page_config4]",
        "type_id": 1,
        "priority_id": 2,
    },
    {
        "title": "DOM Structure - Reconciliation Page",
        "custom_preconds": "User is logged in\nEntity is selected",
        "custom_steps_separated": [
            {"content": "Navigate to Reconciliation page", "expected": "Page loads"},
            {"content": "Verify Sidebar Link is present", "expected": "Link is visible"},
            {"content": "Verify Sub Navigation", "expected": "Sub-nav is visible"},
            {"content": "Verify Content Area", "expected": "Content is rendered"},
        ],
        "custom_expected": "All required DOM elements are present",
        "refs": "test_page_dom_structure[reconciliation-page_config5]",
        "type_id": 1,
        "priority_id": 2,
    },
    {
        "title": "DOM Structure - Payables Page",
        "custom_preconds": "User is logged in\nEntity is selected",
        "custom_steps_separated": [
            {"content": "Navigate to Payables page", "expected": "Page loads"},
            {"content": "Verify Payables Content", "expected": "Content is rendered"},
            {"content": "Verify Status Filter", "expected": "Filter is visible"},
            {"content": "Verify Action Buttons", "expected": "Buttons are visible"},
        ],
        "custom_expected": "All required DOM elements are present",
        "refs": "test_page_dom_structure[payables-page_config6]",
        "type_id": 1,
        "priority_id": 2,
    },
    {
        "title": "DOM Structure - Receivables Tab",
        "custom_preconds": "User is logged in\nEntity is selected",
        "custom_steps_separated": [
            {"content": "Navigate to Reconciliation", "expected": "Page loads"},
            {"content": "Click Receivables tab", "expected": "Tab is selected"},
            {"content": "Verify Data Content", "expected": "Data is rendered"},
            {"content": "Verify Action Buttons", "expected": "Buttons are visible"},
        ],
        "custom_expected": "All required DOM elements are present",
        "refs": "test_page_dom_structure[receivables-page_config7]",
        "type_id": 1,
        "priority_id": 2,
    },
    {
        "title": "DOM Structure - Credit Cards Tab",
        "custom_preconds": "User is logged in\nEntity is selected",
        "custom_steps_separated": [
            {"content": "Navigate to Reconciliation", "expected": "Page loads"},
            {"content": "Click Credit Cards tab", "expected": "Tab is selected"},
            {"content": "Verify Data Content", "expected": "Data is rendered"},
            {"content": "Verify Action Buttons", "expected": "Buttons are visible"},
        ],
        "custom_expected": "All required DOM elements are present",
        "refs": "test_page_dom_structure[credit_cards-page_config8]",
        "type_id": 1,
        "priority_id": 2,
    },
    {
        "title": "DOM Structure - Banks Tab",
        "custom_preconds": "User is logged in\nEntity is selected",
        "custom_steps_separated": [
            {"content": "Navigate to Reconciliation", "expected": "Page loads"},
            {"content": "Click Banks tab", "expected": "Tab is selected"},
            {"content": "Verify Banks Content", "expected": "Data is rendered"},
            {"content": "Verify Action Buttons", "expected": "Buttons are visible"},
        ],
        "custom_expected": "All required DOM elements are present",
        "refs": "test_page_dom_structure[banks-page_config9]",
        "type_id": 1,
        "priority_id": 2,
    },
    {
        "title": "DOM Structure - BI Analysis Page",
        "custom_preconds": "User is logged in\nEntity is selected",
        "custom_steps_separated": [
            {"content": "Navigate to BI Analysis via sidebar", "expected": "Page loads"},
            {"content": "Verify BI Analysis Link", "expected": "Link is visible"},
            {"content": "Verify BI Content", "expected": "Content is rendered"},
            {"content": "Verify Dashboard Elements", "expected": "Widgets are visible"},
        ],
        "custom_expected": "All required DOM elements are present",
        "refs": "test_page_dom_structure[bi_analysis-page_config10]",
        "type_id": 1,
        "priority_id": 2,
    },
    {
        "title": "DOM Structure - Vizion AI Page",
        "custom_preconds": "User is logged in\nEntity is selected",
        "custom_steps_separated": [
            {"content": "Navigate to Vizion AI via sidebar", "expected": "Page loads"},
            {"content": "Verify Vizion AI Link", "expected": "Link is visible"},
            {"content": "Verify AI Content", "expected": "Content is rendered"},
            {"content": "Verify Input Area", "expected": "Input is visible"},
        ],
        "custom_expected": "All required DOM elements are present",
        "refs": "test_page_dom_structure[vizion_ai-page_config11]",
        "type_id": 1,
        "priority_id": 2,
    },
    {
        "title": "DOM Structure - Journal Entries Page",
        "custom_preconds": "User is logged in\nEntity is selected",
        "custom_steps_separated": [
            {"content": "Navigate to Journal Entries", "expected": "Page loads"},
            {"content": "Verify Journal Content", "expected": "Content is rendered"},
            {"content": "Verify Action Buttons", "expected": "Buttons are visible"},
        ],
        "custom_expected": "All required DOM elements are present",
        "refs": "test_page_dom_structure[journal_entries-page_config12]",
        "type_id": 1,
        "priority_id": 2,
    },
    {
        "title": "DOM Structure - Chart of Accounts Page",
        "custom_preconds": "User is logged in\nEntity is selected",
        "custom_steps_separated": [
            {"content": "Navigate to Chart of Accounts", "expected": "Page loads"},
            {"content": "Verify Accounts Table", "expected": "Table is rendered"},
            {"content": "Verify Add GL Button", "expected": "Button is visible"},
            {"content": "Verify Search Input", "expected": "Search is visible"},
        ],
        "custom_expected": "All required DOM elements are present",
        "refs": "test_page_dom_structure[chart_of_accounts-page_config13]",
        "type_id": 1,
        "priority_id": 2,
    },
    {
        "title": "DOM Structure - Full Snapshot Capture",
        "custom_preconds": "User is logged in\nEntity is selected",
        "custom_steps_separated": [
            {"content": "Navigate through all 14 pages", "expected": "All pages load"},
            {"content": "Capture DOM snapshot of each page", "expected": "Snapshots captured"},
            {"content": "Compare against baseline", "expected": "No unexpected changes"},
            {"content": "Save new baseline snapshot", "expected": "Baseline saved"},
        ],
        "custom_expected": "All pages pass DOM validation with no missing elements",
        "refs": "test_capture_all_pages_snapshot",
        "type_id": 1,
        "priority_id": 1,
    },
]

def main():
    print("=" * 60)
    print("🧪 Creating DOM Structure Test Cases in TestRail")
    print("=" * 60)
    
    # Find or create section
    section = find_or_create_section(
        SUITE_ID, 
        "DOM Structure Tests",
        "Tests to detect UI changes and missing components"
    )
    
    if not section:
        print("❌ Failed to find/create section")
        return
    
    section_id = section.get('id')
    print(f"\n📝 Creating {len(DOM_TEST_CASES)} test cases in section {section_id}...")
    
    created_cases = []
    for test_case in DOM_TEST_CASES:
        case_id = create_test_case(section_id, test_case)
        if case_id:
            created_cases.append({
                "id": case_id,
                "refs": test_case.get("refs", "")
            })
    
    print(f"\n{'=' * 60}")
    print(f"✅ Created {len(created_cases)}/{len(DOM_TEST_CASES)} test cases")
    print(f"{'=' * 60}")
    
    # Output case mapping
    print("\n📋 Add to conftest.py case_mapping:")
    print("-" * 40)
    for case in created_cases:
        if case["refs"]:
            print(f'    "{case["refs"]}": {case["id"]},')
    
    print("\n✅ Done!")

if __name__ == "__main__":
    main()
