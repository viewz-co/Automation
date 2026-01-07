#!/usr/bin/env python3
"""
Script to create Purchasing test cases in TestRail Suite 139
Adds Vendor, Product, and Purchase Order tests with all steps, goals, and assertions
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

# Purchasing Test Cases
PURCHASING_TEST_CASES = [
    # ==========================================
    # PAGE LOAD & NAVIGATION TESTS
    # ==========================================
    {
        'title': 'Purchasing - Page Loads Successfully',
        'custom_preconds': '''1. User is logged into the application
2. User has access to Purchasing module
3. Entity is selected''',
        'custom_steps_separated': [
            {'content': 'Navigate to the Purchasing page via sidebar menu', 'expected': 'Purchasing page starts loading'},
            {'content': 'Wait for page to fully load', 'expected': 'Page heading "Purchasing" is visible'},
            {'content': 'Verify the page URL contains "purchasing"', 'expected': 'URL includes "purchasing" path'},
        ],
        'custom_expected': '''- Purchasing page loads successfully
- Page heading is visible
- No error messages displayed''',
        'refs': 'test_purchasing_page_loads'
    },
    {
        'title': 'Purchasing - Navigation Elements Present',
        'custom_preconds': '''1. User is logged into the application
2. User is on the Purchasing page''',
        'custom_steps_separated': [
            {'content': 'Check for vendor table visibility', 'expected': 'Vendor table is displayed'},
            {'content': 'Check for Add Vendor button', 'expected': 'Add Vendor button is visible'},
            {'content': 'Check for Actions menu in table rows', 'expected': 'Actions menu (...) is accessible'},
        ],
        'custom_expected': '''- Vendor table is displayed with columns
- Add Vendor button is clickable
- Actions menu is available for each row''',
        'refs': 'test_purchasing_navigation_elements'
    },
    
    # ==========================================
    # VENDOR TESTS
    # ==========================================
    {
        'title': 'Purchasing - Vendor Form Visibility',
        'custom_preconds': '''1. User is logged into the application
2. User is on the Purchasing page
3. Vendors tab is active''',
        'custom_steps_separated': [
            {'content': 'Navigate to Vendors tab', 'expected': 'Vendors section is displayed'},
            {'content': 'Click Add Vendor button', 'expected': 'Vendor creation form opens'},
            {'content': 'Verify form fields are visible', 'expected': 'Name, Email, Address fields visible'},
        ],
        'custom_expected': '''- Vendor creation form is accessible
- All required form fields are present
- Form is ready for data entry''',
        'refs': 'test_vendor_form_visibility'
    },
    {
        'title': 'Purchasing - Create Vendor',
        'custom_preconds': '''1. User is logged into the application
2. User is on the Purchasing page''',
        'custom_steps_separated': [
            {'content': 'Navigate to Vendors tab', 'expected': 'Vendors section is displayed'},
            {'content': 'Click Add Vendor button', 'expected': 'Vendor form opens'},
            {'content': 'Fill in vendor name with unique value', 'expected': 'Name field is filled'},
            {'content': 'Fill in vendor email', 'expected': 'Email field is filled'},
            {'content': 'Fill in city and address', 'expected': 'Location fields are filled'},
            {'content': 'Fill in registration number and tax ID', 'expected': 'Tax fields are filled'},
            {'content': 'Click Create Vendor button', 'expected': 'Vendor is created successfully'},
            {'content': 'Verify vendor appears in list', 'expected': 'Vendor name visible in vendor list'},
        ],
        'custom_expected': '''- Vendor is created successfully
- Vendor appears in the vendor list
- All entered data is saved correctly''',
        'refs': 'test_create_vendor'
    },
    {
        'title': 'Purchasing - Vendor Form Validation',
        'custom_preconds': '''1. User is logged into the application
2. User is on the Purchasing page
3. Add Vendor form is open''',
        'custom_steps_separated': [
            {'content': 'Open Add Vendor form', 'expected': 'Form opens'},
            {'content': 'Leave all required fields empty', 'expected': 'Fields remain empty'},
            {'content': 'Click Create Vendor button', 'expected': 'Form submission attempted'},
            {'content': 'Verify validation errors appear', 'expected': 'Error messages for required fields'},
        ],
        'custom_expected': '''- Form shows validation errors for required fields
- Form is not submitted with empty required fields
- User can see which fields need to be filled''',
        'refs': 'test_vendor_validation'
    },
    {
        'title': 'Purchasing - Vendor List Display',
        'custom_preconds': '''1. User is logged into the application
2. User is on the Purchasing page''',
        'custom_steps_separated': [
            {'content': 'Navigate to Vendors tab', 'expected': 'Vendors section is displayed'},
            {'content': 'Check vendor table is visible', 'expected': 'Table with vendors is displayed'},
            {'content': 'Verify table columns', 'expected': 'Name, Email, and other columns visible'},
        ],
        'custom_expected': '''- Vendor list is displayed
- Table shows vendor information correctly
- Pagination works if multiple pages exist''',
        'refs': 'test_vendor_list_display'
    },
    
    # ==========================================
    # PRODUCT TESTS
    # ==========================================
    {
        'title': 'Purchasing - Product Form Visibility',
        'custom_preconds': '''1. User is logged into the application
2. User is on the Purchasing page
3. At least one vendor exists''',
        'custom_steps_separated': [
            {'content': 'Navigate to Products via Actions menu on a vendor', 'expected': 'Products section opens'},
            {'content': 'Click Add Product button', 'expected': 'Product form opens'},
            {'content': 'Verify form fields are visible', 'expected': 'Name, Price, SKU fields visible'},
        ],
        'custom_expected': '''- Product creation form is accessible
- Form fields for product details are present
- Form is ready for data entry''',
        'refs': 'test_product_form_visibility'
    },
    {
        'title': 'Purchasing - Create Product for Vendor',
        'custom_preconds': '''1. User is logged into the application
2. User is on the Purchasing page
3. A vendor exists or will be created''',
        'custom_steps_separated': [
            {'content': 'Create a new vendor (if needed)', 'expected': 'Vendor is available'},
            {'content': 'Navigate to Products for the vendor', 'expected': 'Products section opens'},
            {'content': 'Click Add Product button', 'expected': 'Product form opens'},
            {'content': 'Fill in product name', 'expected': 'Name field is filled'},
            {'content': 'Fill in product description', 'expected': 'Description is filled'},
            {'content': 'Fill in product price', 'expected': 'Price is set'},
            {'content': 'Fill in SKU', 'expected': 'SKU is filled'},
            {'content': 'Click Create Product button', 'expected': 'Product is created'},
        ],
        'custom_expected': '''- Product is created successfully
- Product is linked to the vendor
- All product details are saved correctly''',
        'refs': 'test_create_product_for_vendor'
    },
    {
        'title': 'Purchasing - Product Price Validation',
        'custom_preconds': '''1. User is logged into the application
2. Product form is open''',
        'custom_steps_separated': [
            {'content': 'Open Add Product form', 'expected': 'Form opens'},
            {'content': 'Enter negative price value (-100)', 'expected': 'Invalid price entered'},
            {'content': 'Try to submit the form', 'expected': 'Form submission attempted'},
            {'content': 'Verify validation error', 'expected': 'Price validation error shown'},
        ],
        'custom_expected': '''- Negative prices are rejected
- Validation message is displayed
- Form is not submitted with invalid price''',
        'refs': 'test_product_price_validation'
    },
    
    # ==========================================
    # PURCHASE ORDER TESTS
    # ==========================================
    {
        'title': 'Purchasing - Purchase Order Form Visibility',
        'custom_preconds': '''1. User is logged into the application
2. User is on the Purchasing page''',
        'custom_steps_separated': [
            {'content': 'Navigate to Purchase Orders tab', 'expected': 'PO section is displayed'},
            {'content': 'Click Create Purchase Order button', 'expected': 'PO form opens'},
            {'content': 'Verify form fields are visible', 'expected': 'Vendor, Product, Quantity fields visible'},
        ],
        'custom_expected': '''- Purchase Order form is accessible
- All required fields are present
- Form is ready for data entry''',
        'refs': 'test_purchase_order_form_visibility'
    },
    {
        'title': 'Purchasing - Purchase Order List Display',
        'custom_preconds': '''1. User is logged into the application
2. User is on the Purchasing page''',
        'custom_steps_separated': [
            {'content': 'Navigate to Purchase Orders tab', 'expected': 'PO section is displayed'},
            {'content': 'Check PO table is visible', 'expected': 'Table with orders is displayed'},
            {'content': 'Verify table columns', 'expected': 'Order details columns visible'},
        ],
        'custom_expected': '''- Purchase Order list is displayed
- Table shows order information correctly
- Orders can be viewed and managed''',
        'refs': 'test_purchase_order_list_display'
    },
    {
        'title': 'Purchasing - Create Purchase Order',
        'custom_preconds': '''1. User is logged into the application
2. User is on the Purchasing page
3. At least one vendor and product exist''',
        'custom_steps_separated': [
            {'content': 'Create a vendor (if needed)', 'expected': 'Vendor is available'},
            {'content': 'Create a product for the vendor', 'expected': 'Product is available'},
            {'content': 'Navigate to Purchase Orders', 'expected': 'PO section opens'},
            {'content': 'Click Create Purchase Order', 'expected': 'PO form opens'},
            {'content': 'Select vendor from dropdown', 'expected': 'Vendor is selected'},
            {'content': 'Select product from dropdown', 'expected': 'Product is selected'},
            {'content': 'Enter quantity', 'expected': 'Quantity is set'},
            {'content': 'Click Create/Submit button', 'expected': 'Purchase Order is created'},
        ],
        'custom_expected': '''- Purchase Order is created successfully
- PO appears in the orders list
- All order details are saved correctly''',
        'refs': 'test_create_purchase_order'
    },
    
    # ==========================================
    # COMPLETE FLOW TESTS
    # ==========================================
    {
        'title': 'Purchasing - Complete Purchase Flow (Vendor → Product → PO)',
        'custom_preconds': '''1. User is logged into the application
2. User has full Purchasing module access''',
        'custom_steps_separated': [
            {'content': 'Navigate to Purchasing page', 'expected': 'Purchasing page loads'},
            {'content': 'Step 1: Create a new vendor with complete data', 'expected': 'Vendor created successfully'},
            {'content': 'Step 2: Create a product for the vendor', 'expected': 'Product created and linked to vendor'},
            {'content': 'Step 3: Create a purchase order', 'expected': 'PO created with vendor and product'},
            {'content': 'Verify all entities are created', 'expected': 'Complete flow successful'},
        ],
        'custom_expected': '''- Complete flow executes successfully
- Vendor is created with all details
- Product is linked to vendor
- Purchase Order references both vendor and product''',
        'refs': 'test_complete_purchase_flow'
    },
    {
        'title': 'Purchasing - PO Appears in Payables',
        'custom_preconds': '''1. User is logged into the application
2. A complete purchase flow has been executed''',
        'custom_steps_separated': [
            {'content': 'Execute complete purchase flow', 'expected': 'PO is created'},
            {'content': 'Navigate to Payables page', 'expected': 'Payables page loads'},
            {'content': 'Search for vendor name', 'expected': 'Search executed'},
            {'content': 'Verify PO appears in payables', 'expected': 'PO/vendor visible in payables'},
        ],
        'custom_expected': '''- Created PO appears in Payables
- Vendor information is visible
- Payment can be processed''',
        'refs': 'test_po_appears_in_payables'
    },
    
    # ==========================================
    # EDGE CASE TESTS
    # ==========================================
    {
        'title': 'Purchasing - Duplicate Vendor Handling',
        'custom_preconds': '''1. User is logged into the application
2. A vendor with specific name already exists''',
        'custom_steps_separated': [
            {'content': 'Create a vendor with a name', 'expected': 'First vendor created'},
            {'content': 'Attempt to create another vendor with same name', 'expected': 'Second creation attempted'},
            {'content': 'Verify system response', 'expected': 'Error or warning displayed'},
        ],
        'custom_expected': '''- System prevents or warns about duplicate vendors
- Clear feedback is provided to user
- Data integrity is maintained''',
        'refs': 'test_duplicate_vendor_handling'
    },
    {
        'title': 'Purchasing - PO Without Vendor Selection',
        'custom_preconds': '''1. User is logged into the application
2. PO creation form is open''',
        'custom_steps_separated': [
            {'content': 'Open Create Purchase Order form', 'expected': 'Form opens'},
            {'content': 'Leave vendor field empty', 'expected': 'No vendor selected'},
            {'content': 'Try to submit the form', 'expected': 'Form submission attempted'},
            {'content': 'Verify validation error', 'expected': 'Vendor required error shown'},
        ],
        'custom_expected': '''- Vendor selection is required
- Validation error is displayed
- PO cannot be created without vendor''',
        'refs': 'test_po_without_vendor'
    },
    {
        'title': 'Purchasing - PO With Zero Quantity',
        'custom_preconds': '''1. User is logged into the application
2. PO creation form is open''',
        'custom_steps_separated': [
            {'content': 'Open Create Purchase Order form', 'expected': 'Form opens'},
            {'content': 'Enter quantity as 0', 'expected': 'Zero quantity entered'},
            {'content': 'Try to submit the form', 'expected': 'Form submission attempted'},
            {'content': 'Verify validation error', 'expected': 'Quantity validation error shown'},
        ],
        'custom_expected': '''- Zero quantity is rejected
- Validation message is displayed
- PO cannot be created with zero quantity''',
        'refs': 'test_po_with_zero_quantity'
    },
    
    # ==========================================
    # UI/UX TESTS
    # ==========================================
    {
        'title': 'Purchasing - Page Responsiveness',
        'custom_preconds': '''1. User is logged into the application
2. User is on the Purchasing page''',
        'custom_steps_separated': [
            {'content': 'View page at Desktop resolution (1920x1080)', 'expected': 'Page displays correctly'},
            {'content': 'Resize to Laptop resolution (1366x768)', 'expected': 'Page adapts to size'},
            {'content': 'Resize to Tablet resolution (768x1024)', 'expected': 'Page remains functional'},
        ],
        'custom_expected': '''- Page is responsive at all viewports
- All elements remain accessible
- Layout adjusts appropriately''',
        'refs': 'test_purchasing_page_responsiveness'
    },
    {
        'title': 'Purchasing - Form Tab Navigation',
        'custom_preconds': '''1. User is logged into the application
2. Vendor creation form is open''',
        'custom_steps_separated': [
            {'content': 'Open vendor creation form', 'expected': 'Form opens'},
            {'content': 'Press Tab key multiple times', 'expected': 'Focus moves through form fields'},
            {'content': 'Verify all fields are reachable', 'expected': 'Tab navigation works correctly'},
        ],
        'custom_expected': '''- Tab navigation works through all form fields
- Focus order is logical
- All fields are keyboard accessible''',
        'refs': 'test_purchasing_form_tab_navigation'
    },
    {
        'title': 'Purchasing - Page Elements Verification',
        'custom_preconds': '''1. User is logged into the application
2. User is on the Purchasing page''',
        'custom_steps_separated': [
            {'content': 'Check for page heading', 'expected': 'Heading is visible'},
            {'content': 'Check for data table', 'expected': 'Table is displayed'},
            {'content': 'Check for navigation tabs', 'expected': 'Tabs are present'},
        ],
        'custom_expected': '''- All key page elements are present
- Page is fully rendered
- No missing components''',
        'refs': 'test_purchasing_page_elements'
    },
    {
        'title': 'Purchasing - Vendor Search Functionality',
        'custom_preconds': '''1. User is logged into the application
2. User is on the Vendors tab
3. Multiple vendors exist''',
        'custom_steps_separated': [
            {'content': 'Navigate to Vendors tab', 'expected': 'Vendors list displayed'},
            {'content': 'Locate search input field', 'expected': 'Search field found'},
            {'content': 'Enter search term', 'expected': 'Search is executed'},
            {'content': 'Verify filtered results', 'expected': 'Results match search term'},
        ],
        'custom_expected': '''- Search functionality is available
- Results are filtered correctly
- Search is responsive''',
        'refs': 'test_vendor_search_functionality'
    },
]


def main():
    """Main function to create Purchasing test cases"""
    print("="*60)
    print("🛒 Creating Purchasing Test Cases in TestRail")
    print("="*60)
    print(f"\nTarget: Suite {SUITE_ID}")
    print(f"Test Cases: {len(PURCHASING_TEST_CASES)}")
    print()
    
    # Find or create Purchasing section
    section = find_or_create_section(
        SUITE_ID,
        "Purchasing",
        "Purchasing page tests - Vendor, Product, and Purchase Order operations"
    )
    
    if not section:
        print("❌ Failed to find or create Purchasing section")
        return
    
    section_id = section.get('id')
    print(f"\n📂 Using section: Purchasing (ID: {section_id})")
    
    # Create test cases
    created_cases = []
    print(f"\n📝 Creating {len(PURCHASING_TEST_CASES)} test cases...\n")
    
    for i, test_case in enumerate(PURCHASING_TEST_CASES, 1):
        print(f"\n[{i}/{len(PURCHASING_TEST_CASES)}] {test_case['title']}")
        
        case = create_case(
            section_id,
            test_case['title'],
            custom_preconds=test_case.get('custom_preconds', ''),
            custom_steps_separated=test_case.get('custom_steps_separated', []),
            custom_expected=test_case.get('custom_expected', ''),
            refs=test_case.get('refs', '')
        )
        
        if case:
            created_cases.append(case)
    
    # Summary
    print("\n" + "="*60)
    print("📊 SUMMARY")
    print("="*60)
    print(f"✅ Created: {len(created_cases)}/{len(PURCHASING_TEST_CASES)} test cases")
    
    if created_cases:
        print("\n📋 Created Case IDs:")
        for case in created_cases:
            print(f"   - C{case.get('id')}: {case.get('title')}")
    
    print("\n✅ Done!")


if __name__ == "__main__":
    main()

