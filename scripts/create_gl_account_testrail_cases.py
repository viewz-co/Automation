#!/usr/bin/env python3
"""
Script to create GL Account (Chart of Accounts) test cases in TestRail Suite 139
Playwright Python Framework - Complete Test Suite

Creates test cases for:
- Chart of Accounts page navigation
- GL Account creation (Trade Receivables, different currencies)
- GL Account search/verification
- Inline edit row functionality
"""

import os
import requests
import json
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

def create_section(suite_id, name, description="", parent_id=None):
    """Create a new section in the suite"""
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

def main():
    print("=" * 60)
    print("🚀 Creating GL Account Test Cases in TestRail Suite 139")
    print("=" * 60)
    
    # Get existing sections
    print("\n📁 Checking existing sections in Suite 139...")
    sections = get_sections(SUITE_ID)
    
    gl_section_id = None
    ledger_section_id = None
    
    for section in sections:
        section_name = section.get('name', '').lower()
        print(f"   Section: {section.get('name')} (ID: {section.get('id')})")
        if 'gl account' in section_name or 'chart of accounts' in section_name:
            gl_section_id = section.get('id')
            print(f"   ✅ Found existing GL Account section: {gl_section_id}")
        elif 'ledger' in section_name and not section.get('parent_id'):
            ledger_section_id = section.get('id')
    
    # Create GL Account section if it doesn't exist
    if not gl_section_id:
        print("\n📁 Creating GL Account / Chart of Accounts section...")
        section_result = create_section(
            SUITE_ID, 
            "GL Account Operations",
            "Tests for GL Account creation in Chart of Accounts - Precondition for Invoicing",
            parent_id=ledger_section_id  # Under Ledger if exists
        )
        if section_result:
            gl_section_id = section_result.get('id')
        else:
            print("❌ Failed to create GL Account section")
            return
    
    # Define the GL Account test cases (matching test_gl_account_operations.py)
    gl_account_tests = [
        # Page Load & Navigation Tests
        {
            'title': 'Verify Chart of Accounts page loads successfully',
            'custom_automation_id': 'test_chart_of_accounts_page_loads',
            'custom_preconds': '1. User is logged in with valid credentials\n2. User has completed 2FA authentication\n3. Entity is selected (Viewz Demo INC)',
            'custom_steps': '1. Navigate to /ledger/chart-of-accounts\n2. Wait for page to load\n3. Verify page title "Chart of Accounts" is visible\n4. Verify URL contains /ledger/chart-of-accounts',
            'custom_expected': '1. Page loads without errors\n2. "Chart of Accounts" title is displayed\n3. GL Account table is visible\n4. Add GL Account button is present',
            'type_id': 1,  # Automated
            'priority_id': 2,  # Medium
        },
        {
            'title': 'Verify Add GL Account button is visible',
            'custom_automation_id': 'test_add_gl_account_button_visible',
            'custom_preconds': '1. User is logged in\n2. User is on Chart of Accounts page',
            'custom_steps': '1. Navigate to Chart of Accounts page\n2. Look for "Add GL Account" button\n3. Verify button is clickable',
            'custom_expected': '1. "Add GL Account" button is visible\n2. Button has purple/primary color styling\n3. Button is enabled and clickable',
            'type_id': 1,
            'priority_id': 2,
        },
        
        # GL Account Creation Tests
        {
            'title': 'Create GL Account - Trade Receivables (USD, Balance Sheet, Current Assets)',
            'custom_automation_id': 'test_create_gl_account_trade_receivables',
            'custom_preconds': '1. User is logged in\n2. User is on Chart of Accounts page\n3. User has permission to create GL accounts',
            'custom_steps': '1. Click "Add GL Account" button\n2. Verify new inline row appears with "Auto-generated" Account ID\n3. Fill Account Name: "AR Test Account [random]"\n4. Select Currency: USD\n5. Select Report Type: Balance Sheet\n6. Select Account Type: Current Assets\n7. Select Account Group: Trade Receivables\n8. Click Save (green button)',
            'custom_expected': '1. Inline edit row is created\n2. All dropdown fields are selectable (Radix UI comboboxes)\n3. Account is saved successfully\n4. Account appears in the list with auto-generated Account ID\n5. All selected values are persisted correctly',
            'type_id': 1,
            'priority_id': 1,  # High - Critical for Invoicing precondition
        },
        {
            'title': 'Create GL Account for Invoicing Precondition',
            'custom_automation_id': 'test_create_gl_account_for_invoicing_precondition',
            'custom_preconds': '1. User is logged in\n2. User is on Chart of Accounts page\n3. This is a precondition step before Invoicing customer creation',
            'custom_steps': '1. Navigate to Chart of Accounts\n2. Use create_ar_account_for_invoicing() method\n3. Verify account is created with:\n   - Currency: USD\n   - Report Type: Balance Sheet\n   - Account Type: Current Assets\n   - Account Group: Trade Receivables',
            'custom_expected': '1. AR account is created for Invoicing use\n2. Account name contains "AR" or "Invoicing"\n3. Account can be used in Customer creation Income Account dropdown',
            'type_id': 1,
            'priority_id': 1,  # High - Invoicing dependency
        },
        {
            'title': 'Create GL Accounts with different currencies (USD, EUR)',
            'custom_automation_id': 'test_create_gl_account_different_currencies',
            'custom_preconds': '1. User is logged in\n2. User is on Chart of Accounts page',
            'custom_steps': '1. Create GL Account with USD currency\n2. Verify USD account is saved\n3. Create GL Account with EUR currency\n4. Verify EUR account is saved\n5. Verify both accounts appear in the list',
            'custom_expected': '1. USD account created successfully\n2. EUR account created successfully\n3. Both accounts are visible in Chart of Accounts\n4. Currency displays correctly for each account',
            'type_id': 1,
            'priority_id': 2,
        },
        
        # Search & Verification Tests
        {
            'title': 'Search for GL Account by name',
            'custom_automation_id': 'test_search_gl_account',
            'custom_preconds': '1. User is logged in\n2. User is on Chart of Accounts page\n3. At least one GL account exists',
            'custom_steps': '1. Create a GL account with unique name\n2. Use search input field\n3. Enter account name\n4. Verify search results',
            'custom_expected': '1. Search input accepts text\n2. Account appears in filtered results\n3. Search is case-insensitive\n4. Partial name matching works',
            'type_id': 1,
            'priority_id': 2,
        },
        
        # Inline Edit Row Tests
        {
            'title': 'Verify Add GL Account creates inline edit row',
            'custom_automation_id': 'test_add_gl_account_creates_inline_row',
            'custom_preconds': '1. User is logged in\n2. User is on Chart of Accounts page',
            'custom_steps': '1. Click "Add GL Account" button\n2. Verify new row appears at top of table\n3. Check row contains "Auto-generated" text\n4. Verify all editable fields are present:\n   - Account ID (auto-generated)\n   - Name (text input)\n   - Currency (dropdown)\n   - Report Type (dropdown)\n   - Type (dropdown)\n   - Group (dropdown)\n   - Save/Cancel buttons',
            'custom_expected': '1. New inline row appears immediately\n2. "Auto-generated" shown in Account ID field\n3. Name field is focused and editable\n4. All dropdown fields show placeholder "Select"\n5. Save (green) and Cancel buttons visible',
            'type_id': 1,
            'priority_id': 2,
        },
        {
            'title': 'Cancel GL Account creation',
            'custom_automation_id': 'test_cancel_gl_account_creation',
            'custom_preconds': '1. User is logged in\n2. User is on Chart of Accounts page\n3. Inline edit row is open',
            'custom_steps': '1. Click "Add GL Account" to open inline row\n2. Fill some fields partially\n3. Click Cancel button (or press Escape)\n4. Verify row is removed',
            'custom_expected': '1. Inline edit row is removed\n2. No account is created\n3. Table returns to previous state\n4. No error messages shown',
            'type_id': 1,
            'priority_id': 3,  # Low
        },
    ]
    
    # Create test cases
    print(f"\n📝 Creating {len(gl_account_tests)} test cases in section {gl_section_id}...")
    print("-" * 60)
    
    created_cases = []
    for test in gl_account_tests:
        title = test.pop('title')
        case = create_case(gl_section_id, title, **test)
        if case:
            created_cases.append({
                'id': case.get('id'),
                'title': title,
                'automation_id': test.get('custom_automation_id', '')
            })
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 SUMMARY")
    print("=" * 60)
    print(f"✅ Created {len(created_cases)} test cases in Suite 139")
    print(f"📁 Section: GL Account Operations (ID: {gl_section_id})")
    
    print("\n📋 Case IDs created:")
    for case in created_cases:
        print(f"   C{case['id']}: {case['title'][:50]}...")
    
    # Output mappings for conftest.py
    print("\n" + "=" * 60)
    print("📝 TESTRAIL MAPPINGS FOR conftest.py")
    print("=" * 60)
    print("\n# Add these mappings to tests/conftest.py case_mapping dict:")
    print("\n# ===== GL ACCOUNT / CHART OF ACCOUNTS TESTS =====")
    print(f"# GL Account Section (ID: {gl_section_id}) - Chart of Accounts operations")
    
    for case in created_cases:
        automation_id = case.get('automation_id', f"test_{case['id']}")
        print(f"'{automation_id}': {case['id']},  # C{case['id']}")
    
    # Also output as a dict that can be directly copied
    print("\n\n# Copy-paste ready mapping:")
    print("gl_account_mapping = {")
    for case in created_cases:
        automation_id = case.get('automation_id', f"test_{case['id']}")
        print(f"    '{automation_id}': {case['id']},  # C{case['id']}")
    print("}")
    
    return created_cases

if __name__ == "__main__":
    main()

