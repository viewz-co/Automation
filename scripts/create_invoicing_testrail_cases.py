#!/usr/bin/env python3
"""
Script to create Invoicing test cases in TestRail Suite 9
Playwright Python Framework - Complete Test Suite
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
SUITE_ID = 9  # Suite 9: Playwright Python Framework - Complete Test Suite

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
        # Handle both paginated and non-paginated responses
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

def get_cases(suite_id, section_id=None):
    """Get test cases from a suite/section"""
    uri = f'get_cases/{PROJECT_ID}&suite_id={suite_id}'
    if section_id:
        uri += f'&section_id={section_id}'
    
    result = send_request('GET', uri)
    if result:
        # Handle paginated response
        if isinstance(result, dict) and 'cases' in result:
            return result['cases']
        return result
    return []

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

def get_sample_case_format(suite_id):
    """Get a sample case to understand the format"""
    cases = get_cases(suite_id)
    if cases and len(cases) > 0:
        print("\n📋 Sample case format from Suite 9:")
        sample = cases[0]
        print(json.dumps(sample, indent=2, default=str))
        return sample
    return None

def get_suites():
    """Get all suites in the project"""
    result = send_request('GET', f'get_suites/{PROJECT_ID}')
    if result:
        # Handle paginated response
        if isinstance(result, dict) and 'suites' in result:
            return result['suites']
        return result
    return []

def main():
    print("=" * 60)
    print("🚀 Creating Invoicing Test Cases in TestRail")
    print("=" * 60)
    
    # First, list all available suites
    print("\n📋 Getting available suites...")
    suites = get_suites()
    
    if suites:
        print("\n📁 Available Suites:")
        for suite in suites:
            print(f"   Suite {suite.get('id')}: {suite.get('name')}")
        
        # Ask which suite to use or find the correct one
        target_suite = None
        for suite in suites:
            if 'playwright' in suite.get('name', '').lower() or suite.get('id') == 139:
                target_suite = suite
                break
        
        if not target_suite and suites:
            target_suite = suites[0]  # Use first suite as fallback
        
        if target_suite:
            global SUITE_ID
            SUITE_ID = target_suite.get('id')
            print(f"\n✅ Using Suite {SUITE_ID}: {target_suite.get('name')}")
    else:
        print("❌ No suites found")
        return
    
    # First, get existing sections to see if Invoicing section exists
    print("\n📁 Checking existing sections...")
    sections = get_sections(SUITE_ID)
    
    invoicing_section_id = None
    for section in sections:
        print(f"   Section: {section.get('name')} (ID: {section.get('id')})")
        if 'invoicing' in section.get('name', '').lower():
            invoicing_section_id = section.get('id')
            print(f"   ✅ Found existing Invoicing section: {invoicing_section_id}")
    
    # Get a sample case to see the format
    print("\n📋 Getting sample case format...")
    sample = get_sample_case_format(SUITE_ID)
    
    # Create Invoicing section if it doesn't exist
    if not invoicing_section_id:
        print("\n📁 Creating Invoicing section...")
        section_result = create_section(
            SUITE_ID, 
            "Invoicing", 
            "Tests for Invoicing Management - Customer, Product, and Invoice operations"
        )
        if section_result:
            invoicing_section_id = section_result.get('id')
        else:
            print("❌ Failed to create Invoicing section")
            return
    
    # Define the 17 invoicing test cases
    invoicing_tests = [
        {
            'title': 'Verify Invoicing page loads successfully',
            'custom_automation_id': 'test_invoicing_page_loads',
            'custom_preconds': '1. User is logged in\n2. User has access to Invoicing module',
            'custom_steps': '1. Navigate to Invoicing page (/invoicing)\n2. Wait for page to load\n3. Verify page elements are visible',
            'custom_expected': '1. Page loads without errors\n2. "Invoicing Management" title is displayed\n3. Customer list or empty state is shown',
            'type_id': 1,  # Automated
            'priority_id': 2,  # Medium
        },
        {
            'title': 'Verify Invoicing navigation elements are visible',
            'custom_automation_id': 'test_invoicing_navigation_elements',
            'custom_preconds': '1. User is logged in\n2. User is on Invoicing page',
            'custom_steps': '1. Check for Customers section\n2. Check for Products section (via Actions menu)\n3. Check for Invoices section (via Actions menu)',
            'custom_expected': '1. Customers section is visible\n2. Products option available in customer Actions menu\n3. Invoices option available in customer Actions menu',
            'type_id': 1,
            'priority_id': 2,
        },
        {
            'title': 'Verify Customer creation form is accessible',
            'custom_automation_id': 'test_customer_form_visibility',
            'custom_preconds': '1. User is logged in\n2. User is on Invoicing page',
            'custom_steps': '1. Click "Add Customer" button\n2. Verify form opens\n3. Check all required fields are present',
            'custom_expected': '1. Add Customer form opens successfully\n2. Customer Name field is visible\n3. Email, Address, Country fields are visible\n4. Required dropdowns (Income Account, Payment Terms) are present',
            'type_id': 1,
            'priority_id': 2,
        },
        {
            'title': 'Create a new customer with valid data',
            'custom_automation_id': 'test_create_customer',
            'custom_preconds': '1. User is logged in\n2. User is on Invoicing page',
            'custom_steps': '1. Click "Add Customer"\n2. Fill Customer Name\n3. Select Income Account\n4. Fill Email\n5. Select Country\n6. Fill City, Address, Zip Code\n7. Fill Registration Number, Tax ID\n8. Select Payment Terms\n9. Click "Create Customer"',
            'custom_expected': '1. Customer is created successfully\n2. Success message is displayed\n3. Customer appears in the customer list',
            'type_id': 1,
            'priority_id': 1,  # High
        },
        {
            'title': 'Verify Customer form validation',
            'custom_automation_id': 'test_customer_validation',
            'custom_preconds': '1. User is logged in\n2. User is on Add Customer form',
            'custom_steps': '1. Leave required fields empty\n2. Click "Create Customer"\n3. Observe validation messages',
            'custom_expected': '1. Form is not submitted\n2. Validation errors shown for required fields:\n   - Customer Name\n   - Income Account\n   - Email\n   - Country\n   - Payment Terms',
            'type_id': 1,
            'priority_id': 2,
        },
        {
            'title': 'Verify Product creation form is accessible',
            'custom_automation_id': 'test_product_form_visibility',
            'custom_preconds': '1. User is logged in\n2. At least one customer exists',
            'custom_steps': '1. Go to Invoicing page\n2. Click "..." on customer row\n3. Click "Products"\n4. Click "Add Product"\n5. Verify form fields',
            'custom_expected': '1. Products section opens\n2. Add Product form is accessible\n3. Product Name, Price fields are visible',
            'type_id': 1,
            'priority_id': 2,
        },
        {
            'title': 'Create a new product for a customer',
            'custom_automation_id': 'test_create_product',
            'custom_preconds': '1. User is logged in\n2. Customer exists\n3. User is in Products section for a customer',
            'custom_steps': '1. Click "Add Product"\n2. Fill Product Name\n3. Fill other required fields\n4. Click "Create Product"',
            'custom_expected': '1. Product is created successfully\n2. Product appears in the products list',
            'type_id': 1,
            'priority_id': 1,
        },
        {
            'title': 'Verify Product price field validation',
            'custom_automation_id': 'test_product_price_validation',
            'custom_preconds': '1. User is logged in\n2. User is on Add Product form',
            'custom_steps': '1. Enter invalid price (negative number)\n2. Try to submit form\n3. Observe validation',
            'custom_expected': '1. Invalid price is rejected\n2. Validation error is shown',
            'type_id': 1,
            'priority_id': 3,  # Low
        },
        {
            'title': 'Verify Invoice creation form is accessible',
            'custom_automation_id': 'test_invoice_form_visibility',
            'custom_preconds': '1. User is logged in\n2. Customer and Product exist',
            'custom_steps': '1. Go to Invoicing page\n2. Click "..." on customer row\n3. Click "Invoices"\n4. Click "Generate Invoice"\n5. Verify form fields',
            'custom_expected': '1. Invoices section opens\n2. Generate Invoice form is accessible\n3. Month selection dropdown is visible',
            'type_id': 1,
            'priority_id': 2,
        },
        {
            'title': 'Verify Invoice list displays correctly',
            'custom_automation_id': 'test_invoice_list_display',
            'custom_preconds': '1. User is logged in\n2. User is in Invoices section for a customer',
            'custom_steps': '1. View invoice list\n2. Check table columns\n3. Check pagination if applicable',
            'custom_expected': '1. Invoice list is displayed\n2. Columns include: Invoice Number, Email, Status, Actions\n3. Empty state shown if no invoices',
            'type_id': 1,
            'priority_id': 2,
        },
        {
            'title': 'Complete end-to-end invoice flow',
            'custom_automation_id': 'test_complete_invoice_flow',
            'custom_preconds': '1. User is logged in\n2. User has access to Invoicing module',
            'custom_steps': '1. Navigate to Invoicing\n2. Create new customer\n3. Navigate to Products (via Actions menu)\n4. Create new product\n5. Navigate to Invoices (via Actions menu)\n6. Generate invoice',
            'custom_expected': '1. Customer created successfully\n2. Product created for customer\n3. Invoice generated successfully\n4. All data is saved correctly',
            'type_id': 1,
            'priority_id': 1,
        },
        {
            'title': 'Verify invoice appears in Receivables page',
            'custom_automation_id': 'test_invoice_appears_in_receivables',
            'custom_preconds': '1. User is logged in\n2. Invoice has been generated',
            'custom_steps': '1. Generate an invoice\n2. Navigate to Receivables page\n3. Search for the invoice/customer',
            'custom_expected': '1. Invoice is visible in Receivables\n2. Customer name matches\n3. Amount is correct',
            'type_id': 1,
            'priority_id': 1,
        },
        {
            'title': 'Verify duplicate customer handling',
            'custom_automation_id': 'test_duplicate_customer_handling',
            'custom_preconds': '1. User is logged in\n2. Customer already exists',
            'custom_steps': '1. Try to create customer with same email\n2. Observe system behavior',
            'custom_expected': '1. System prevents duplicate or shows warning\n2. Data integrity is maintained',
            'type_id': 1,
            'priority_id': 3,
        },
        {
            'title': 'Verify invoice creation without customer validation',
            'custom_automation_id': 'test_invoice_without_customer',
            'custom_preconds': '1. User is logged in\n2. User is on Invoice creation form',
            'custom_steps': '1. Try to create invoice without selecting customer\n2. Observe validation',
            'custom_expected': '1. Form validation prevents submission\n2. Error message is displayed',
            'type_id': 1,
            'priority_id': 2,
        },
        {
            'title': 'Verify invoice with zero quantity validation',
            'custom_automation_id': 'test_invoice_with_zero_quantity',
            'custom_preconds': '1. User is logged in\n2. User is on Invoice creation form',
            'custom_steps': '1. Enter zero or negative quantity\n2. Try to submit',
            'custom_expected': '1. Validation error is shown\n2. Invoice is not created with invalid quantity',
            'type_id': 1,
            'priority_id': 3,
        },
        {
            'title': 'Verify Invoicing page responsiveness',
            'custom_automation_id': 'test_invoicing_page_responsiveness',
            'custom_preconds': '1. User is logged in\n2. User is on Invoicing page',
            'custom_steps': '1. Test page at desktop viewport (1920x1080)\n2. Test at laptop viewport (1366x768)\n3. Test at tablet viewport (768x1024)',
            'custom_expected': '1. Page layout adapts to each viewport\n2. All elements remain accessible\n3. No horizontal scrolling on smaller screens',
            'type_id': 1,
            'priority_id': 3,
        },
        {
            'title': 'Verify form keyboard tab navigation',
            'custom_automation_id': 'test_invoicing_form_tab_navigation',
            'custom_preconds': '1. User is logged in\n2. User is on Add Customer form',
            'custom_steps': '1. Use Tab key to navigate through form fields\n2. Verify focus moves correctly\n3. Test Enter key submission',
            'custom_expected': '1. Tab navigation works through all fields\n2. Focus indicator is visible\n3. Form is accessible via keyboard',
            'type_id': 1,
            'priority_id': 3,
        },
    ]
    
    # Create test cases
    print(f"\n📝 Creating {len(invoicing_tests)} test cases in section {invoicing_section_id}...")
    print("-" * 60)
    
    created_cases = []
    for test in invoicing_tests:
        title = test.pop('title')
        case = create_case(invoicing_section_id, title, **test)
        if case:
            created_cases.append(case)
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 SUMMARY")
    print("=" * 60)
    print(f"✅ Created {len(created_cases)} test cases in Suite 9")
    print(f"📁 Section: Invoicing (ID: {invoicing_section_id})")
    print("\n📋 Case IDs created:")
    for case in created_cases:
        print(f"   C{case.get('id')}: {case.get('title')[:50]}...")
    
    # Output mappings for conftest.py
    print("\n" + "=" * 60)
    print("📝 TESTRAIL MAPPINGS FOR conftest.py")
    print("=" * 60)
    print("\n# Add these mappings to tests/conftest.py:")
    print("\n# Invoicing Tests (Suite 9)")
    for case in created_cases:
        automation_id = None
        # Try to get the custom field
        for key in case:
            if 'automation' in key.lower():
                automation_id = case[key]
                break
        
        # Fallback to extracting from title
        if not automation_id:
            for test in invoicing_tests + [{'title': case.get('title'), 'custom_automation_id': None}]:
                if test.get('title') == case.get('title'):
                    automation_id = test.get('custom_automation_id', f"test_{case.get('id')}")
                    break
        
        print(f"'{automation_id}': {case.get('id')},  # C{case.get('id')}")

if __name__ == "__main__":
    main()

