#!/usr/bin/env python3
"""
Script to update DOM Structure TestRail cases with detailed assertions and success criteria.
"""

import os
import requests
from base64 import b64encode

# TestRail configuration
TESTRAIL_URL = os.getenv('TESTRAIL_URL', 'https://viewz.testrail.io')
TESTRAIL_USERNAME = os.getenv('TESTRAIL_USERNAME', 'automation@viewz.co')
TESTRAIL_PASSWORD = os.getenv('TESTRAIL_PASSWORD', 'e.fJg:z5q5mnAdL')

# Authentication
auth = b64encode(f"{TESTRAIL_USERNAME}:{TESTRAIL_PASSWORD}".encode()).decode()
headers = {
    'Authorization': f'Basic {auth}',
    'Content-Type': 'application/json'
}

def update_case(case_id, data):
    """Update an existing test case"""
    url = f"{TESTRAIL_URL}/index.php?/api/v2/update_case/{case_id}"
    try:
        response = requests.post(url, headers=headers, json=data, timeout=30)
        response.raise_for_status()
        print(f"   ✅ Updated C{case_id}")
        return True
    except requests.exceptions.RequestException as e:
        print(f"   ❌ Failed C{case_id}: {e}")
        return False

# Define detailed updates for each case
CASE_UPDATES = {
    194169: {  # Home Page
        "title": "DOM Structure - Home Page",
        "custom_preconds": """Pre-conditions:
1. User is logged in to the application
2. Entity (Viewz Demo INC) is selected
3. Browser is Chrome/Firefox/Edge latest version
4. Network connection is stable""",
        "custom_steps_separated": [
            {"content": "Navigate to Home page (/home)", "expected": "Home page loads within 5 seconds with HTTP 200 status"},
            {"content": "Verify Viewz Logo element exists using selector: a[href*='/home'] svg", "expected": "Logo SVG element is found and visible in the DOM"},
            {"content": "Verify Entity Selector using selector: button:has-text('Viewz')", "expected": "Entity selector button displays current entity name"},
            {"content": "Verify Main Dashboard Content using selector: [class*='grid']", "expected": "Dashboard grid layout is rendered with child elements"},
            {"content": "Verify Navigation Menu using selector: nav, [class*='nav'], [class*='sidebar']", "expected": "Navigation sidebar/menu is present and contains navigation links"},
        ],
        "custom_expected": """Success Criteria:
✅ All 5 required DOM elements are found
✅ Element count > 0 for each selector
✅ No console errors related to missing components
✅ Page URL matches expected pattern: /home?entityId=*

Assertions Verified:
- Logo element exists (count >= 1)
- Entity selector button is clickable
- Dashboard grid has multiple child elements
- Navigation contains links to other pages
- No 'Required element not found' errors in test output""",
    },
    194170: {  # Invoicing Page
        "title": "DOM Structure - Invoicing Page",
        "custom_preconds": """Pre-conditions:
1. User is logged in to the application
2. Entity is selected
3. User has permissions to view Invoicing page""",
        "custom_steps_separated": [
            {"content": "Navigate to Invoicing page (/invoicing)", "expected": "Invoicing page loads successfully"},
            {"content": "Verify Add Customer Button: button:has-text('Add Customer')", "expected": "Add Customer button is visible and clickable"},
            {"content": "Verify Customer Table: table tbody", "expected": "Customer data table is rendered with rows"},
            {"content": "Verify Search Input: input[placeholder*='Search' i]", "expected": "Search input field accepts text input"},
            {"content": "Verify Export Button: button:has-text('Export')", "expected": "Export button is present for data export"},
            {"content": "Verify Sidebar Link: a[href*='/invoicing']", "expected": "Invoicing link in sidebar is active/highlighted"},
        ],
        "custom_expected": """Success Criteria:
✅ All 5 required DOM elements are found
✅ Add Customer button is functional
✅ Table renders customer data
✅ Search and Export features are accessible

Assertions Verified:
- Add Customer button count = 1
- Table body exists with data rows
- Search placeholder contains 'Search'
- Export button is visible
- Sidebar link href contains '/invoicing'""",
    },
    194171: {  # Purchasing Page
        "title": "DOM Structure - Purchasing Page",
        "custom_preconds": """Pre-conditions:
1. User is logged in to the application
2. Entity is selected
3. User has permissions to view Purchasing page""",
        "custom_steps_separated": [
            {"content": "Navigate to Purchasing page (/purchasing)", "expected": "Purchasing page loads successfully"},
            {"content": "Verify Add Vendor Button: button:has-text('Add Vendor')", "expected": "Add Vendor button is visible and clickable"},
            {"content": "Verify Vendor Table: table tbody", "expected": "Vendor data table is rendered"},
            {"content": "Verify Search Input: input[placeholder*='Search' i]", "expected": "Search input field is present"},
            {"content": "Verify Export Button: button:has-text('Export')", "expected": "Export button is accessible"},
            {"content": "Verify Sidebar Link: a[href*='/purchasing']", "expected": "Purchasing link in sidebar is active"},
        ],
        "custom_expected": """Success Criteria:
✅ All 5 required DOM elements are found
✅ Add Vendor functionality is accessible
✅ Vendor list table is rendered
✅ Search and Export features work

Assertions Verified:
- Add Vendor button count = 1
- Table body contains vendor rows
- Search input is interactable
- Export button is clickable
- Sidebar purchasing link is highlighted""",
    },
    194172: {  # Budgeting Page
        "title": "DOM Structure - Budgeting Page",
        "custom_preconds": """Pre-conditions:
1. User is logged in to the application
2. Entity is selected
3. Budgeting feature is enabled for the entity""",
        "custom_steps_separated": [
            {"content": "Click Budgeting link in sidebar: a[href*='/budgeting']", "expected": "Navigation to Budgeting page initiated"},
            {"content": "Wait for page load", "expected": "Budgeting page loads at /budgeting/chart-of-budget"},
            {"content": "Verify Sidebar Budgeting Link is present", "expected": "Link is visible and marked as active"},
            {"content": "Verify Budget Content: table, [class*='budget'], [class*='chart']", "expected": "Budget table or chart is rendered"},
            {"content": "Verify Action Buttons: button", "expected": "Action buttons are available for budget operations"},
        ],
        "custom_expected": """Success Criteria:
✅ All 3 required DOM elements are found
✅ Sidebar navigation works correctly
✅ Budget content area is rendered
✅ User can interact with budget controls

Assertions Verified:
- Sidebar link count >= 1
- Budget table/chart is visible
- At least one action button exists
- Page URL contains '/budgeting'""",
    },
    194173: {  # Ledger Page
        "title": "DOM Structure - Ledger Page",
        "custom_preconds": """Pre-conditions:
1. User is logged in to the application
2. Entity is selected
3. Ledger module is accessible""",
        "custom_steps_separated": [
            {"content": "Click Ledger link in sidebar: a[href*='/ledger']", "expected": "Navigation to Ledger page initiated"},
            {"content": "Wait for page load", "expected": "Ledger page loads at /ledger/general-ledger"},
            {"content": "Verify Sidebar Ledger Link is present", "expected": "Link is visible and active"},
            {"content": "Verify Accounts Table: table tbody", "expected": "GL accounts table is rendered"},
            {"content": "Verify Search Input: input[placeholder*='Search' i]", "expected": "Search functionality is available"},
            {"content": "Verify Action Buttons: button", "expected": "Add/Edit buttons are present"},
        ],
        "custom_expected": """Success Criteria:
✅ All 4 required DOM elements are found
✅ GL account table displays data
✅ Search input filters accounts
✅ Action buttons are clickable

Assertions Verified:
- Sidebar link is highlighted
- Table body has account rows
- Search input accepts text
- Multiple action buttons exist
- Page URL matches /ledger/*""",
    },
    194174: {  # Reconciliation Page
        "title": "DOM Structure - Reconciliation Page",
        "custom_preconds": """Pre-conditions:
1. User is logged in to the application
2. Entity is selected
3. Reconciliation module is enabled""",
        "custom_steps_separated": [
            {"content": "Click Reconciliation link in sidebar: a[href*='/reconciliation']", "expected": "Navigation to Reconciliation initiated"},
            {"content": "Wait for page load", "expected": "Reconciliation page loads"},
            {"content": "Verify Sidebar Reconciliation Link", "expected": "Link is present and active"},
            {"content": "Verify Sub Navigation: a[href*='/reconciliation/']", "expected": "Sub-navigation tabs are visible (Payables, Receivables, etc.)"},
            {"content": "Verify Content Area: [class*='content'], main", "expected": "Main content area is rendered"},
        ],
        "custom_expected": """Success Criteria:
✅ All 3 required DOM elements are found
✅ Sub-navigation tabs are accessible
✅ Content area loads based on selected tab
✅ No layout issues

Assertions Verified:
- Sidebar link count >= 1
- Sub-navigation links exist for different reconciliation types
- Content area is not empty
- Page responds to tab clicks""",
    },
    194175: {  # Payables Page
        "title": "DOM Structure - Payables Page",
        "custom_preconds": """Pre-conditions:
1. User is logged in to the application
2. Entity is selected
3. Payables data exists""",
        "custom_steps_separated": [
            {"content": "Navigate to Payables: /reconciliation/payables", "expected": "Payables page loads"},
            {"content": "Verify Payables Content: table, [class*='payable']", "expected": "Payables table or content is rendered"},
            {"content": "Verify Status Filter: [class*='filter'], button:has-text('Status')", "expected": "Status filter dropdown is available"},
            {"content": "Verify Action Buttons: button", "expected": "Action buttons (Delete, Edit) are present"},
        ],
        "custom_expected": """Success Criteria:
✅ All 3 required DOM elements are found
✅ Payables list is displayed
✅ Status filter can filter records
✅ Action buttons are functional

Assertions Verified:
- Payables table/content exists
- Filter controls are interactive
- Action buttons count >= 1
- Page URL is /reconciliation/payables""",
    },
    194176: {  # Receivables Tab
        "title": "DOM Structure - Receivables Tab",
        "custom_preconds": """Pre-conditions:
1. User is logged in to the application
2. Entity is selected
3. Receivables data exists""",
        "custom_steps_separated": [
            {"content": "Navigate to Reconciliation page via sidebar", "expected": "Reconciliation page loads"},
            {"content": "Click Receivables tab: button:has-text('Receivables')", "expected": "Receivables tab is selected"},
            {"content": "Verify Data Content: table, [class*='data']", "expected": "Receivables data table is displayed"},
            {"content": "Verify Action Buttons: button", "expected": "Export and action buttons are available"},
        ],
        "custom_expected": """Success Criteria:
✅ All 2 required DOM elements are found
✅ Tab navigation works
✅ Receivables data is displayed
✅ Export functionality is accessible

Assertions Verified:
- Data table/content exists after tab click
- Action buttons are clickable
- Tab is visually selected/active
- Data corresponds to Receivables type""",
    },
    194177: {  # Credit Cards Tab
        "title": "DOM Structure - Credit Cards Tab",
        "custom_preconds": """Pre-conditions:
1. User is logged in to the application
2. Entity is selected
3. Credit card transactions exist""",
        "custom_steps_separated": [
            {"content": "Navigate to Reconciliation page via sidebar", "expected": "Reconciliation page loads"},
            {"content": "Click Credit Cards tab: button:has-text('Credit Cards')", "expected": "Credit Cards tab is selected"},
            {"content": "Verify Data Content: table, [class*='data']", "expected": "Credit card transactions table is displayed"},
            {"content": "Verify Action Buttons: button", "expected": "Export and action buttons are available"},
        ],
        "custom_expected": """Success Criteria:
✅ All 2 required DOM elements are found
✅ Tab switch works correctly
✅ Credit card data is displayed
✅ Actions are accessible

Assertions Verified:
- Data table exists after tab selection
- Buttons are present and clickable
- Tab is marked as active
- Correct data type is shown""",
    },
    194178: {  # Banks Tab
        "title": "DOM Structure - Banks Tab",
        "custom_preconds": """Pre-conditions:
1. User is logged in to the application
2. Entity is selected
3. Bank connections exist""",
        "custom_steps_separated": [
            {"content": "Navigate to Reconciliation page via sidebar", "expected": "Reconciliation page loads"},
            {"content": "Click Banks tab: button:has-text('Banks')", "expected": "Banks tab is selected"},
            {"content": "Verify Banks Content: table, [class*='bank'], [class*='data']", "expected": "Bank transactions/accounts are displayed"},
            {"content": "Verify Action Buttons: button", "expected": "Bank-related action buttons are available"},
        ],
        "custom_expected": """Success Criteria:
✅ All 2 required DOM elements are found
✅ Banks tab navigation works
✅ Bank data is rendered
✅ Actions are functional

Assertions Verified:
- Banks content area is populated
- Action buttons exist
- Tab is active state
- Bank-specific UI elements present""",
    },
    194179: {  # BI Analysis Page
        "title": "DOM Structure - BI Analysis Page",
        "custom_preconds": """Pre-conditions:
1. User is logged in to the application
2. Entity is selected
3. BI Analysis feature is enabled""",
        "custom_steps_separated": [
            {"content": "Click BI Analysis link in sidebar: a[href*='/bi']", "expected": "Navigation to BI Analysis initiated"},
            {"content": "Wait for page load", "expected": "BI Analysis page loads"},
            {"content": "Verify BI Analysis Link: a[href*='/bi']", "expected": "Sidebar link is present"},
            {"content": "Verify BI Content: [class*='bi'], [class*='analysis'], [class*='chart'], main", "expected": "BI dashboard or charts are rendered"},
            {"content": "Verify Dashboard Elements: [class*='dashboard'], [class*='widget'], [class*='card']", "expected": "Dashboard widgets/cards are displayed"},
        ],
        "custom_expected": """Success Criteria:
✅ All 3 required DOM elements are found
✅ BI dashboard loads completely
✅ Charts/widgets render correctly
✅ Interactive elements work

Assertions Verified:
- BI link in sidebar exists
- Main BI content area is populated
- Dashboard widgets/cards are present
- No chart rendering errors""",
    },
    194180: {  # Vizion AI Page
        "title": "DOM Structure - Vizion AI Page",
        "custom_preconds": """Pre-conditions:
1. User is logged in to the application
2. Entity is selected
3. Vizion AI feature is enabled""",
        "custom_steps_separated": [
            {"content": "Click Vizion AI link in sidebar: a[href*='/vizion']", "expected": "Navigation to Vizion AI initiated"},
            {"content": "Wait for page load", "expected": "Vizion AI page loads"},
            {"content": "Verify Vizion AI Link: a[href*='/vizion']", "expected": "Sidebar link is present and active"},
            {"content": "Verify AI Content: [class*='vizion'], [class*='ai'], [class*='chat'], main", "expected": "AI chat interface or content is rendered"},
            {"content": "Verify Input Area: input, textarea, [class*='input']", "expected": "User input field is available for queries"},
        ],
        "custom_expected": """Success Criteria:
✅ All 3 required DOM elements are found
✅ AI interface loads completely
✅ Input area is interactive
✅ Chat/response area is visible

Assertions Verified:
- Vizion AI link exists in sidebar
- AI content area is rendered
- Input field/textarea is present
- Interface is ready for user interaction""",
    },
    194181: {  # Journal Entries Page
        "title": "DOM Structure - Journal Entries Page",
        "custom_preconds": """Pre-conditions:
1. User is logged in to the application
2. Entity is selected
3. Journal entries exist""",
        "custom_steps_separated": [
            {"content": "Navigate to Journal Entries: /ledger/journal-entries", "expected": "Journal Entries page loads"},
            {"content": "Verify Journal Content: table, [class*='journal'], main", "expected": "Journal entries table/list is rendered"},
            {"content": "Verify Action Buttons: button", "expected": "Create/Edit buttons are available"},
        ],
        "custom_expected": """Success Criteria:
✅ All 2 required DOM elements are found
✅ Journal entries list is displayed
✅ Create new entry option is available
✅ Existing entries can be viewed

Assertions Verified:
- Journal content area exists
- Action buttons are present
- Table/list has journal data
- Page URL matches /ledger/journal-entries""",
    },
    194182: {  # Chart of Accounts Page
        "title": "DOM Structure - Chart of Accounts Page",
        "custom_preconds": """Pre-conditions:
1. User is logged in to the application
2. Entity is selected
3. GL accounts are configured""",
        "custom_steps_separated": [
            {"content": "Navigate to Chart of Accounts: /ledger/chart-of-accounts", "expected": "Chart of Accounts page loads"},
            {"content": "Verify Accounts Table: table tbody", "expected": "GL accounts table is rendered with account data"},
            {"content": "Verify Add GL Button: button:has-text('Add GL')", "expected": "Add GL Account button is visible and clickable"},
            {"content": "Verify Search Input: input[placeholder*='Search' i]", "expected": "Search input for filtering accounts is present"},
        ],
        "custom_expected": """Success Criteria:
✅ All 3 required DOM elements are found
✅ GL accounts table displays accounts
✅ Add GL Account functionality works
✅ Search filters accounts correctly

Assertions Verified:
- Accounts table body has rows
- Add GL button count = 1
- Search input accepts text
- Table columns show account details (ID, Name, Type, etc.)""",
    },
    194183: {  # Full Snapshot Capture
        "title": "DOM Structure - Full Snapshot Capture",
        "custom_preconds": """Pre-conditions:
1. User is logged in to the application
2. Entity is selected
3. All 14 pages are accessible
4. UPDATE_BASELINE environment variable set appropriately""",
        "custom_steps_separated": [
            {"content": "Navigate through all 14 pages in sequence", "expected": "Each page loads without errors"},
            {"content": "For each page, capture DOM element snapshot", "expected": "All required elements found for each page"},
            {"content": "Compare current snapshot against baseline (if exists)", "expected": "No unexpected missing elements"},
            {"content": "Save new baseline snapshot to baselines directory", "expected": "JSON snapshot file saved with timestamp"},
            {"content": "Generate summary report", "expected": "Summary shows 14 pages checked, 0 with issues"},
        ],
        "custom_expected": """Success Criteria:
✅ All 14 pages are successfully checked
✅ No pages have missing required elements
✅ Baseline snapshot is saved
✅ Summary shows '0 pages with issues'

Assertions Verified:
- home: 5/5 elements found
- invoicing: 5/5 elements found
- purchasing: 5/5 elements found
- budgeting: 3/3 elements found
- ledger: 4/4 elements found
- reconciliation: 3/3 elements found
- payables: 3/3 elements found
- receivables: 2/2 elements found
- credit_cards: 2/2 elements found
- banks: 2/2 elements found
- bi_analysis: 3/3 elements found
- vizion_ai: 3/3 elements found
- journal_entries: 2/2 elements found
- chart_of_accounts: 3/3 elements found

Total Elements Verified: 45 elements across 14 pages
Snapshot saved to: tests/e2e/dom_structure/baselines/""",
    },
}

def main():
    print("=" * 60)
    print("🔄 Updating DOM Structure Test Cases with Assertions")
    print("=" * 60)
    
    success_count = 0
    for case_id, data in CASE_UPDATES.items():
        print(f"\n📝 Updating C{case_id}: {data.get('title', 'Unknown')}")
        if update_case(case_id, data):
            success_count += 1
    
    print(f"\n{'=' * 60}")
    print(f"✅ Updated {success_count}/{len(CASE_UPDATES)} test cases")
    print("=" * 60)

if __name__ == "__main__":
    main()

