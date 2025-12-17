#!/usr/bin/env python3
"""
Script to update Invoicing test cases in TestRail to match the template format
Based on test case C7966 format
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
        
        response.raise_for_status()
        return response.json() if response.content else None
    except requests.exceptions.RequestException as e:
        print(f"❌ API error: {e}")
        return None

def get_case(case_id):
    """Get a specific test case"""
    return send_request('GET', f'get_case/{case_id}')

def update_case(case_id, data):
    """Update a test case"""
    result = send_request('POST', f'update_case/{case_id}', data)
    if result:
        print(f"✅ Updated case C{case_id}")
    else:
        print(f"❌ Failed to update case C{case_id}")
    return result

def main():
    print("=" * 60)
    print("📝 Updating Invoicing Test Cases Format")
    print("=" * 60)
    
    # First, get the template case C7966 to see its format
    print("\n📋 Getting template case C7966...")
    template_case = get_case(7966)
    if template_case:
        print(f"   Title: {template_case.get('title')}")
        print(f"   Steps format sample:")
        steps = template_case.get('custom_steps', '')[:500]
        print(f"   {steps}...")
    
    # Define the 17 invoicing test cases with proper template format
    invoicing_tests = [
        {
            'case_id': 77366,
            'title': 'Verify Invoicing page loads successfully',
            'test_function': 'test_invoicing_page_loads',
            'goal': 'Verify that the Invoicing Management page loads successfully and displays all expected elements',
            'steps': [
                'Login to the application with valid credentials',
                'Navigate to Invoicing page (/invoicing)',
                'Wait for page to fully load',
                'Verify "Invoicing Management" title is displayed',
                'Verify customer list or empty state is shown'
            ],
            'assertions': [
                'assert page.url contains "/invoicing"',
                'assert "Invoicing Management" title is visible',
                'assert page loads without errors',
                'assert customer table or empty state is displayed'
            ],
            'expected': 'Invoicing page loads successfully with all expected elements visible'
        },
        {
            'case_id': 77367,
            'title': 'Verify Invoicing navigation elements are visible',
            'test_function': 'test_invoicing_navigation_elements',
            'goal': 'Verify that all navigation elements (Customers, Products, Invoices) are accessible in the Invoicing module',
            'steps': [
                'Login and navigate to Invoicing page',
                'Verify Customers section is visible',
                'Click on customer Actions menu (...)',
                'Verify "Products" option is available',
                'Verify "Invoices" option is available'
            ],
            'assertions': [
                'assert Customers section is displayed',
                'assert Actions menu opens on click',
                'assert "Products" menu option is visible',
                'assert "Invoices" menu option is visible'
            ],
            'expected': 'All navigation elements are visible and accessible via the Actions menu'
        },
        {
            'case_id': 77368,
            'title': 'Verify Customer creation form is accessible',
            'test_function': 'test_customer_form_visibility',
            'goal': 'Verify that the Add Customer form opens correctly and displays all required fields',
            'steps': [
                'Login and navigate to Invoicing page',
                'Click "Add Customer" button',
                'Wait for form to open',
                'Verify all required fields are present',
                'Verify dropdowns are functional'
            ],
            'assertions': [
                'assert "Add Customer" button is clickable',
                'assert Customer Name field is visible',
                'assert Email field is visible',
                'assert Income Account dropdown is present',
                'assert Country dropdown is present',
                'assert Payment Terms dropdown is present'
            ],
            'expected': 'Add Customer form opens with all required fields visible and functional'
        },
        {
            'case_id': 77369,
            'title': 'Create a new customer with valid data',
            'test_function': 'test_create_customer',
            'goal': 'Verify that a new customer can be created successfully with all required data',
            'steps': [
                'Login and navigate to Invoicing page',
                'Click "Add Customer" button',
                'Fill Customer Name field',
                'Select Income Account from dropdown',
                'Fill Email address',
                'Select Country',
                'Fill City, Address, Zip Code',
                'Fill Registration Number and Tax ID',
                'Select Payment Terms',
                'Click "Create Customer" button'
            ],
            'assertions': [
                'assert all required fields are filled',
                'assert "Create Customer" button is enabled',
                'assert success message is displayed after creation',
                'assert new customer appears in the customer list'
            ],
            'expected': 'Customer is created successfully and appears in the customer list'
        },
        {
            'case_id': 77370,
            'title': 'Verify Customer form validation',
            'test_function': 'test_customer_validation',
            'goal': 'Verify that the customer form validates required fields and shows appropriate error messages',
            'steps': [
                'Login and navigate to Invoicing page',
                'Click "Add Customer" button',
                'Leave all required fields empty',
                'Click "Create Customer" button',
                'Verify validation errors are displayed'
            ],
            'assertions': [
                'assert form is not submitted with empty fields',
                'assert "Customer Name is required" error is shown',
                'assert "Income Account is required" error is shown',
                'assert "Email is required" error is shown',
                'assert "Country is required" error is shown',
                'assert "Payment Terms is required" error is shown'
            ],
            'expected': 'Form validation prevents submission and displays appropriate error messages'
        },
        {
            'case_id': 77371,
            'title': 'Verify Product creation form is accessible',
            'test_function': 'test_product_form_visibility',
            'goal': 'Verify that the Add Product form is accessible via the customer Actions menu',
            'steps': [
                'Login and navigate to Invoicing page',
                'Ensure at least one customer exists',
                'Click on customer Actions menu (...)',
                'Click "Products" option',
                'Click "Add Product" button',
                'Verify form fields are visible'
            ],
            'assertions': [
                'assert Products section opens',
                'assert "Add Product" button is visible',
                'assert Product Name field is displayed',
                'assert Price field is displayed'
            ],
            'expected': 'Product creation form is accessible and displays all required fields'
        },
        {
            'case_id': 77372,
            'title': 'Create a new product for a customer',
            'test_function': 'test_create_product',
            'goal': 'Verify that a new product can be created for a customer',
            'steps': [
                'Login and navigate to Invoicing page',
                'Navigate to Products section for a customer',
                'Click "Add Product" button',
                'Fill Product Name',
                'Fill other required fields (Price, etc.)',
                'Click "Create Product" button'
            ],
            'assertions': [
                'assert Product Name is filled',
                'assert "Create Product" button is enabled',
                'assert product is created successfully',
                'assert product appears in products list'
            ],
            'expected': 'Product is created successfully and appears in the products list'
        },
        {
            'case_id': 77373,
            'title': 'Verify Product price field validation',
            'test_function': 'test_product_price_validation',
            'goal': 'Verify that the product price field validates input correctly',
            'steps': [
                'Login and navigate to Products section',
                'Click "Add Product" button',
                'Enter invalid price (negative number)',
                'Try to submit the form',
                'Verify validation error is shown'
            ],
            'assertions': [
                'assert negative price is rejected',
                'assert validation error is displayed',
                'assert form is not submitted with invalid price'
            ],
            'expected': 'Invalid price values are rejected with appropriate validation messages'
        },
        {
            'case_id': 77374,
            'title': 'Verify Invoice creation form is accessible',
            'test_function': 'test_invoice_form_visibility',
            'goal': 'Verify that the Generate Invoice form is accessible via the customer Actions menu',
            'steps': [
                'Login and navigate to Invoicing page',
                'Ensure customer and product exist',
                'Click on customer Actions menu (...)',
                'Click "Invoices" option',
                'Click "Generate Invoice" button',
                'Verify form fields are visible'
            ],
            'assertions': [
                'assert Invoices section opens',
                'assert "Generate Invoice" button is visible',
                'assert Invoice Month dropdown is displayed'
            ],
            'expected': 'Invoice creation form is accessible and displays all required fields'
        },
        {
            'case_id': 77375,
            'title': 'Verify Invoice list displays correctly',
            'test_function': 'test_invoice_list_display',
            'goal': 'Verify that the invoice list displays correctly with proper columns',
            'steps': [
                'Login and navigate to Invoicing page',
                'Navigate to Invoices section for a customer',
                'View the invoice list',
                'Verify table columns are present',
                'Check for empty state if no invoices'
            ],
            'assertions': [
                'assert invoice table is displayed',
                'assert "Invoice Number" column is visible',
                'assert "Email" column is visible',
                'assert "Status" column is visible',
                'assert "Actions" column is visible'
            ],
            'expected': 'Invoice list displays with all expected columns and data'
        },
        {
            'case_id': 77376,
            'title': 'Complete end-to-end invoice flow',
            'test_function': 'test_complete_invoice_flow',
            'goal': 'Verify the complete invoice workflow: Create Customer → Create Product → Generate Invoice',
            'steps': [
                'Login and navigate to Invoicing page',
                'Create a new customer with all required data',
                'Navigate to Products via Actions menu',
                'Create a new product for the customer',
                'Navigate to Invoices via Actions menu',
                'Generate a new invoice',
                'Verify invoice is created successfully'
            ],
            'assertions': [
                'assert customer is created successfully',
                'assert product is created for the customer',
                'assert invoice is generated successfully',
                'assert all data is saved correctly'
            ],
            'expected': 'Complete invoice flow executes successfully from customer creation to invoice generation'
        },
        {
            'case_id': 77377,
            'title': 'Verify invoice appears in Receivables page',
            'test_function': 'test_invoice_appears_in_receivables',
            'goal': 'Verify that generated invoices appear in the Receivables page',
            'steps': [
                'Login and create a complete invoice',
                'Navigate to Receivables page',
                'Search for the invoice or customer',
                'Verify invoice is displayed'
            ],
            'assertions': [
                'assert Receivables page loads',
                'assert invoice is found in receivables',
                'assert customer name matches',
                'assert invoice amount is correct'
            ],
            'expected': 'Generated invoice appears in the Receivables page with correct details'
        },
        {
            'case_id': 77378,
            'title': 'Verify duplicate customer handling',
            'test_function': 'test_duplicate_customer_handling',
            'goal': 'Verify that the system handles duplicate customer creation appropriately',
            'steps': [
                'Login and navigate to Invoicing page',
                'Create a customer with specific email',
                'Try to create another customer with same email',
                'Observe system behavior'
            ],
            'assertions': [
                'assert duplicate customer is prevented OR warning is shown',
                'assert data integrity is maintained',
                'assert appropriate error message is displayed'
            ],
            'expected': 'System prevents duplicate customers or shows appropriate warning'
        },
        {
            'case_id': 77379,
            'title': 'Verify invoice creation without customer validation',
            'test_function': 'test_invoice_without_customer',
            'goal': 'Verify that invoice creation requires customer selection',
            'steps': [
                'Login and navigate to Invoice creation form',
                'Try to create invoice without selecting customer',
                'Observe validation behavior'
            ],
            'assertions': [
                'assert form validation prevents submission',
                'assert error message is displayed',
                'assert invoice is not created without customer'
            ],
            'expected': 'Form validation prevents invoice creation without required customer selection'
        },
        {
            'case_id': 77380,
            'title': 'Verify invoice with zero quantity validation',
            'test_function': 'test_invoice_with_zero_quantity',
            'goal': 'Verify that invoice creation validates quantity field',
            'steps': [
                'Login and navigate to Invoice creation form',
                'Enter zero or negative quantity',
                'Try to submit the form',
                'Observe validation behavior'
            ],
            'assertions': [
                'assert zero quantity is rejected',
                'assert negative quantity is rejected',
                'assert validation error is displayed'
            ],
            'expected': 'Invalid quantity values are rejected with appropriate validation messages'
        },
        {
            'case_id': 77381,
            'title': 'Verify Invoicing page responsiveness',
            'test_function': 'test_invoicing_page_responsiveness',
            'goal': 'Verify that the Invoicing page is responsive across different viewport sizes',
            'steps': [
                'Login and navigate to Invoicing page',
                'Test at desktop viewport (1920x1080)',
                'Test at laptop viewport (1366x768)',
                'Test at tablet viewport (768x1024)',
                'Verify page elements are accessible at each size'
            ],
            'assertions': [
                'assert page layout adapts to viewport',
                'assert all elements remain accessible',
                'assert no horizontal scrolling on smaller screens',
                'assert responsive at 2+ viewport sizes'
            ],
            'expected': 'Invoicing page is fully responsive and functional across all viewport sizes'
        },
        {
            'case_id': 77382,
            'title': 'Verify form keyboard tab navigation',
            'test_function': 'test_invoicing_form_tab_navigation',
            'goal': 'Verify that forms support keyboard navigation using Tab key',
            'steps': [
                'Login and open Add Customer form',
                'Use Tab key to navigate through form fields',
                'Verify focus moves correctly',
                'Test Enter key for form submission'
            ],
            'assertions': [
                'assert Tab navigation works through all fields',
                'assert focus indicator is visible',
                'assert Tab count >= 3 fields',
                'assert form is keyboard accessible'
            ],
            'expected': 'Form supports full keyboard navigation and is accessible'
        },
    ]
    
    # Update each test case with the template format
    print(f"\n📝 Updating {len(invoicing_tests)} test cases...")
    print("-" * 60)
    
    for test in invoicing_tests:
        case_id = test['case_id']
        
        # Build the steps in template format
        steps_text = f"""🎯 **TEST GOAL:**
{test['goal']}

📋 **TEST STEPS:**
"""
        for i, step in enumerate(test['steps'], 1):
            steps_text += f"{i}. {step}\n"
        
        steps_text += """
✅ **ASSERTIONS VERIFIED:**
"""
        for i, assertion in enumerate(test['assertions'], 1):
            steps_text += f"{i}. {assertion}\n"
        
        steps_text += f"""
📊 **SUCCESS CRITERIA:**
- All assertions pass successfully
- Test goal is achieved
- No unexpected errors occur
- Expected behavior is verified

🔧 **AUTOMATION DETAILS:**
- Test Function: {test['test_function']}
- Framework: Playwright + pytest
- TestRail Integration: Enabled
- Screenshot Capture: On failure"""
        
        # Build preconditions
        preconds = f"""Prerequisites:
1. User is logged in with valid credentials
2. User has access to Invoicing module
3. Environment is properly configured for {test['test_function']}"""
        
        # Build expected result
        expected = f"Expected Result: {test['expected']} - All assertions pass and test completes successfully"
        
        # Update the case
        update_data = {
            'custom_preconds': preconds,
            'custom_steps': steps_text,
            'custom_expected': expected
        }
        
        update_case(case_id, update_data)
    
    print("\n" + "=" * 60)
    print("✅ All test cases updated with template format!")
    print("=" * 60)

if __name__ == "__main__":
    main()



