#!/usr/bin/env python3
"""
Script to add Budget Builder test cases to TestRail Suite 139
"""

import requests
import json
import os
from base64 import b64encode

# TestRail configuration - use same credentials as testrail_config.py
TESTRAIL_URL = os.getenv('TESTRAIL_URL', 'https://viewz.testrail.io')
TESTRAIL_USERNAME = os.getenv('TESTRAIL_USERNAME', 'automation@viewz.co')
TESTRAIL_PASSWORD = os.getenv('TESTRAIL_PASSWORD', 'e.fJg:z5q5mnAdL')
SUITE_ID = 139

# Find Budget section ID (or create one)
BUDGET_SECTION_NAME = "Budget Builder"

# Setup authentication
auth = b64encode(f"{TESTRAIL_USERNAME}:{TESTRAIL_PASSWORD}".encode()).decode()
HEADERS = {
    'Authorization': f'Basic {auth}',
    'Content-Type': 'application/json'
}

def get_auth():
    return (TESTRAIL_USERNAME, TESTRAIL_PASSWORD)

def get_sections():
    """Get all sections in suite 139"""
    url = f"{TESTRAIL_URL}/index.php?/api/v2/get_sections/1&suite_id={SUITE_ID}"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        return response.json()
    print(f"Error getting sections: {response.status_code} - {response.text}")
    return []

def create_section(name, parent_id=None):
    """Create a new section"""
    url = f"{TESTRAIL_URL}/index.php?/api/v2/add_section/1"
    data = {
        "suite_id": SUITE_ID,
        "name": name
    }
    if parent_id:
        data["parent_id"] = parent_id
    
    response = requests.post(url, headers=HEADERS, json=data)
    if response.status_code == 200:
        return response.json()
    print(f"Error creating section: {response.status_code} - {response.text}")
    return None

def find_or_create_section(name):
    """Find existing section or create new one"""
    sections = get_sections()
    
    # Look for existing Budget Builder section
    for section in sections.get('sections', sections) if isinstance(sections, dict) else sections:
        if section.get('name') == name:
            print(f"Found existing section: {name} (ID: {section['id']})")
            return section['id']
    
    # Create new section
    print(f"Creating new section: {name}")
    new_section = create_section(name)
    if new_section:
        print(f"Created section: {name} (ID: {new_section['id']})")
        return new_section['id']
    return None

def create_test_case(section_id, title, steps, expected, preconditions="", priority=2):
    """Create a test case in TestRail"""
    url = f"{TESTRAIL_URL}/index.php?/api/v2/add_case/{section_id}"
    
    # Format steps for TestRail
    steps_separated = []
    for i, step in enumerate(steps, 1):
        steps_separated.append({
            "content": step,
            "expected": expected[i-1] if i <= len(expected) else ""
        })
    
    data = {
        "title": title,
        "custom_steps_separated": steps_separated,
        "custom_preconds": preconditions,
        "priority_id": priority,
        "type_id": 1,  # Automated
    }
    
    response = requests.post(url, headers=HEADERS, json=data)
    if response.status_code == 200:
        case = response.json()
        print(f"✅ Created: {title} (C{case['id']})")
        return case
    else:
        print(f"❌ Failed to create: {title}")
        print(f"   Error: {response.status_code} - {response.text}")
        return None

def main():
    print("="*60)
    print("Adding Budget Builder Tests to TestRail Suite 139")
    print("="*60)
    
    # Find or create Budget Builder section
    section_id = find_or_create_section(BUDGET_SECTION_NAME)
    if not section_id:
        print("❌ Could not find or create section")
        return
    
    # Define test cases
    test_cases = [
        {
            "title": "Budget Builder - Fiscal Year Filter",
            "steps": [
                "Navigate to Budgeting page",
                "Click on 'Budget Builder' tab",
                "Note current fiscal year displayed",
                "Click on Fiscal Year dropdown",
                "Select a different fiscal year (e.g., 2025 or 2024)",
                "Verify data updates after selection",
                "Change back to original fiscal year"
            ],
            "expected": [
                "Budgeting page loads successfully",
                "Budget Builder opens with table of GL accounts",
                "Current fiscal year is displayed (e.g., 2026)",
                "Dropdown shows available fiscal years",
                "Year changes and data refreshes",
                "Summary statistics (Total, Lines) update for new year",
                "Original data is restored"
            ],
            "preconditions": "User is logged in with valid credentials\nBudget data exists for multiple fiscal years"
        },
        {
            "title": "Budget Builder - Version Selection",
            "steps": [
                "Navigate to Budget Builder page",
                "Locate the Version dropdown",
                "Click to open version options",
                "Note available versions",
                "Select a different version",
                "Verify version change is reflected"
            ],
            "expected": [
                "Budget Builder page loads",
                "Version dropdown is visible",
                "Dropdown shows list of available budget versions",
                "Multiple versions are listed (if available)",
                "Version changes successfully",
                "Data updates to reflect selected version"
            ],
            "preconditions": "User is logged in\nMultiple budget versions exist"
        },
        {
            "title": "Budget Builder - Search Budget Lines",
            "steps": [
                "Navigate to Budget Builder page",
                "Locate the search input (Search budget lines...)",
                "Enter search term 'Income'",
                "Verify filtered results",
                "Clear search input",
                "Enter search term 'Expenses'",
                "Verify different filtered results",
                "Clear search to show all lines"
            ],
            "expected": [
                "Budget Builder loads with all budget lines",
                "Search input is visible and accessible",
                "'Income' search filters to show income-related rows",
                "Only matching budget lines are displayed",
                "All budget lines are shown again",
                "'Expenses' search filters to show expense-related rows",
                "Different set of rows displayed",
                "All budget lines restored"
            ],
            "preconditions": "User is logged in\nBudget Builder has multiple budget line categories"
        },
        {
            "title": "Budget Builder - Balance Indicator Display",
            "steps": [
                "Navigate to Budget Builder page",
                "Locate the balance indicator near the search box",
                "Verify percentage is displayed (e.g., '79% Balanced')",
                "Check indicator color/status",
                "Verify percentage is between 0-100+"
            ],
            "expected": [
                "Budget Builder loads",
                "Balance indicator is visible",
                "Percentage value is displayed clearly",
                "Green indicates balanced, other colors indicate imbalance",
                "Percentage value is valid and reflects actual balance state"
            ],
            "preconditions": "User is logged in\nBudget has allocated amounts"
        },
        {
            "title": "Budget Builder - Summary Statistics Display",
            "steps": [
                "Navigate to Budget Builder page",
                "Locate summary statistics row",
                "Verify 'Total' amount is displayed",
                "Verify 'Avg/mo' (average monthly) is displayed",
                "Verify 'Lines' count is displayed",
                "Verify 'Top' item (highest budget) is displayed",
                "Validate statistics match table data"
            ],
            "expected": [
                "Budget Builder loads with data",
                "Summary statistics are visible above the table",
                "Total shows sum of all budgets (e.g., '$31,560.1K USD')",
                "Average monthly amount is calculated correctly",
                "Lines count matches number of budget rows (e.g., 63)",
                "Top item shows category with highest budget",
                "Statistics are accurate and match visible data"
            ],
            "preconditions": "User is logged in\nBudget Builder has budget data"
        },
        {
            "title": "Budget Builder - Row Expansion/Collapse",
            "steps": [
                "Navigate to Budget Builder page",
                "Find an expandable budget category row (e.g., 'Accrued Income')",
                "Note current row count",
                "Click expand arrow/button on the row",
                "Verify sub-items become visible",
                "Click to collapse the row",
                "Verify sub-items are hidden"
            ],
            "expected": [
                "Budget Builder loads with hierarchical data",
                "Expandable rows have expand/chevron icon",
                "Initial row count is recorded",
                "Row expands to show child/sub-items",
                "Row count increases, sub-items are indented",
                "Row collapses successfully",
                "Sub-items are hidden, original row count restored"
            ],
            "preconditions": "User is logged in\nBudget has hierarchical structure with parent/child categories"
        },
        {
            "title": "Budget Builder - Monthly Value Edit",
            "steps": [
                "Navigate to Budget Builder page",
                "Find a row with $0 values (editable)",
                "Double-click on a monthly value cell (e.g., January)",
                "Enter a new amount (e.g., 5000)",
                "Press Enter to commit the value",
                "Verify the value is updated",
                "Click Save Budget button"
            ],
            "expected": [
                "Budget Builder loads",
                "Zero-value row is identified",
                "Cell enters edit mode with input field",
                "Amount can be typed into the field",
                "Value is committed and displayed",
                "Cell shows new value (e.g., $5.0K)",
                "Budget is saved successfully"
            ],
            "preconditions": "User is logged in\nUser has edit permissions for budget"
        },
        {
            "title": "Budget Builder - Negative Budget Display",
            "steps": [
                "Navigate to Budget Builder page",
                "Scan table for rows with negative values",
                "Identify negative value formatting",
                "Verify negative values are visually distinguished",
                "Check if negative values use parentheses or minus sign",
                "Verify color coding (typically red for negative)"
            ],
            "expected": [
                "Budget Builder loads with data",
                "Rows with negative values are found (if any exist)",
                "Negative values are clearly formatted differently",
                "Negative values stand out from positive values",
                "Format is consistent (e.g., ($4.0K) or -$4.0K)",
                "Negative values may be displayed in red or different color"
            ],
            "preconditions": "User is logged in\nBudget contains categories with negative values (e.g., Employees with expense variances)"
        },
        {
            "title": "Budget Builder - Bulk Actions Functionality",
            "steps": [
                "Navigate to Budget Builder page",
                "Locate the 'Bulk Actions' button",
                "Click Bulk Actions button",
                "Verify menu opens with available options",
                "Note the available bulk action options",
                "Close the menu",
                "Try selecting multiple rows (if checkboxes available)"
            ],
            "expected": [
                "Budget Builder loads",
                "Bulk Actions button is visible",
                "Dropdown menu opens",
                "Menu shows bulk operation options",
                "Options may include: Delete, Update, Export, etc.",
                "Menu closes properly",
                "Multiple rows can be selected for bulk operations"
            ],
            "preconditions": "User is logged in with appropriate permissions"
        },
        {
            "title": "Budget Builder - Table Horizontal Scroll",
            "steps": [
                "Navigate to Budget Builder page",
                "Note which month columns are initially visible",
                "Scroll table horizontally to the right",
                "Verify December column becomes visible",
                "Scroll back to the left",
                "Verify January column is visible again",
                "Confirm all 12 months are accessible"
            ],
            "expected": [
                "Budget Builder loads with monthly columns",
                "Initial months visible (typically Jan-Aug)",
                "Table scrolls smoothly to the right",
                "December (Dec) column is visible and shows data",
                "Table scrolls back to the left",
                "January (Jan) column is visible",
                "All months (Jan-Dec) can be accessed via scroll"
            ],
            "preconditions": "User is logged in\nScreen width doesn't show all 12 months at once"
        }
    ]
    
    # Create all test cases
    created_cases = []
    for tc in test_cases:
        case = create_test_case(
            section_id=section_id,
            title=tc["title"],
            steps=tc["steps"],
            expected=tc["expected"],
            preconditions=tc.get("preconditions", "")
        )
        if case:
            created_cases.append(case)
    
    print("\n" + "="*60)
    print(f"✅ Created {len(created_cases)}/{len(test_cases)} test cases")
    print("="*60)
    
    # Print case IDs for conftest mapping
    print("\n📋 TestRail Case IDs for conftest.py mapping:")
    print("-" * 40)
    test_names = [
        "test_fiscal_year_filter",
        "test_version_selection",
        "test_search_budget_lines",
        "test_balance_indicator",
        "test_summary_statistics",
        "test_row_expansion",
        "test_monthly_value_edit",
        "test_negative_budget_display",
        "test_bulk_actions",
        "test_table_horizontal_scroll"
    ]
    
    for i, case in enumerate(created_cases):
        if i < len(test_names):
            print(f'    "{test_names[i]}": {case["id"]},')

if __name__ == "__main__":
    main()

