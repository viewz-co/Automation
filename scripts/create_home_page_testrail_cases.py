#!/usr/bin/env python3
"""
Script to create TestRail test cases for Home Page tests.
Adds 34 test cases covering dashboard elements, filters, KPIs, charts, and navigation.
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
    
    result = send_request('POST', f'add_section/{PROJECT_ID}', {
        'suite_id': suite_id,
        'name': name,
        'description': description
    })
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

# Define test cases
HOME_PAGE_TESTS = [
    # === TestHomePageElements (6 tests) ===
    {
        "title": "Home Page - Page Loads Successfully",
        "custom_preconds": "User is logged in\nEntity is selected",
        "custom_steps_separated": [
            {"content": "Navigate to home page", "expected": "Home page loads"},
            {"content": "Verify URL contains /home", "expected": "URL matches pattern"},
            {"content": "Verify dashboard title visible", "expected": "Title is displayed"},
        ],
        "custom_expected": "✅ Home page loads with Financial Overview Dashboard\n✅ URL contains /home\n✅ Dashboard is fully rendered",
        "refs": "test_home_page_loads",
        "type_id": 1, "priority_id": 1,
    },
    {
        "title": "Home Page - Dashboard Title Visible",
        "custom_preconds": "User is on home page",
        "custom_steps_separated": [
            {"content": "Locate h1 element with 'Financial Overview Dashboard'", "expected": "Element found"},
            {"content": "Verify title text", "expected": "Text matches expected"},
        ],
        "custom_expected": "✅ 'Financial Overview Dashboard' title is visible",
        "refs": "test_dashboard_title_visible",
        "type_id": 1, "priority_id": 2,
    },
    {
        "title": "Home Page - Dashboard Subtitle Visible",
        "custom_preconds": "User is on home page",
        "custom_steps_separated": [
            {"content": "Locate subtitle element", "expected": "Subtitle found"},
            {"content": "Verify subtitle contains 'Real-time insights'", "expected": "Text visible"},
        ],
        "custom_expected": "✅ Dashboard subtitle with description is displayed",
        "refs": "test_dashboard_subtitle_visible",
        "type_id": 1, "priority_id": 3,
    },
    {
        "title": "Home Page - Viewz Logo Visible",
        "custom_preconds": "User is on home page",
        "custom_steps_separated": [
            {"content": "Locate Viewz logo SVG in header", "expected": "Logo element found"},
            {"content": "Verify logo is visible", "expected": "Logo displayed"},
        ],
        "custom_expected": "✅ Viewz logo is visible in header",
        "refs": "test_viewz_logo_visible",
        "type_id": 1, "priority_id": 2,
    },
    {
        "title": "Home Page - Entity Selector Visible",
        "custom_preconds": "User is on home page",
        "custom_steps_separated": [
            {"content": "Locate entity selector dropdown", "expected": "Dropdown found"},
            {"content": "Verify shows entity name (e.g., 'Viewz Demo INC')", "expected": "Entity name displayed"},
        ],
        "custom_expected": "✅ Entity selector is visible\n✅ Shows current entity name",
        "refs": "test_entity_selector_visible",
        "type_id": 1, "priority_id": 2,
    },
    {
        "title": "Home Page - User Avatar Visible",
        "custom_preconds": "User is on home page",
        "custom_steps_separated": [
            {"content": "Locate user avatar/profile indicator", "expected": "Avatar found"},
            {"content": "Verify avatar is visible", "expected": "Avatar displayed"},
        ],
        "custom_expected": "✅ User avatar is visible indicating logged-in state",
        "refs": "test_user_avatar_visible",
        "type_id": 1, "priority_id": 3,
    },
    
    # === TestHomePageFilters (9 tests) ===
    {
        "title": "Home Page - Date Range Filter Visible",
        "custom_preconds": "User is on home page",
        "custom_steps_separated": [
            {"content": "Locate date range filter", "expected": "Date range element found"},
            {"content": "Verify shows date range (e.g., 'Jan 1, 2025 - Jan 7, 2026')", "expected": "Dates displayed"},
        ],
        "custom_expected": "✅ Date range filter is visible with current range",
        "refs": "test_date_range_filter_visible",
        "type_id": 1, "priority_id": 2,
    },
    {
        "title": "Home Page - Period Buttons (Y/Q/M) Visible",
        "custom_preconds": "User is on home page",
        "custom_steps_separated": [
            {"content": "Locate Year (Y) button", "expected": "Y button visible"},
            {"content": "Locate Quarter (Q) button", "expected": "Q button visible"},
            {"content": "Locate Month (M) button", "expected": "M button visible"},
        ],
        "custom_expected": "✅ All period buttons (Y/Q/M) are visible",
        "refs": "test_period_buttons_visible",
        "type_id": 1, "priority_id": 2,
    },
    {
        "title": "Home Page - Period Selection Year",
        "custom_preconds": "User is on home page",
        "custom_steps_separated": [
            {"content": "Click Year (Y) period button", "expected": "Button is clicked"},
            {"content": "Wait for data refresh", "expected": "Dashboard updates"},
            {"content": "Verify KPI section still visible", "expected": "KPIs displayed"},
        ],
        "custom_expected": "✅ Year period selected\n✅ Dashboard data updates\n✅ KPIs remain visible",
        "refs": "test_period_selection_year",
        "type_id": 1, "priority_id": 2,
    },
    {
        "title": "Home Page - Period Selection Quarter",
        "custom_preconds": "User is on home page",
        "custom_steps_separated": [
            {"content": "Click Quarter (Q) period button", "expected": "Button is clicked"},
            {"content": "Wait for data refresh", "expected": "Dashboard updates"},
            {"content": "Verify KPI section still visible", "expected": "KPIs displayed"},
        ],
        "custom_expected": "✅ Quarter period selected\n✅ Dashboard data updates",
        "refs": "test_period_selection_quarter",
        "type_id": 1, "priority_id": 2,
    },
    {
        "title": "Home Page - Period Selection Month",
        "custom_preconds": "User is on home page",
        "custom_steps_separated": [
            {"content": "Click Month (M) period button", "expected": "Button is clicked"},
            {"content": "Wait for data refresh", "expected": "Dashboard updates"},
            {"content": "Verify KPI section still visible", "expected": "KPIs displayed"},
        ],
        "custom_expected": "✅ Month period selected\n✅ Dashboard data updates",
        "refs": "test_period_selection_month",
        "type_id": 1, "priority_id": 2,
    },
    {
        "title": "Home Page - Entity Filter Visible",
        "custom_preconds": "User is on home page",
        "custom_steps_separated": [
            {"content": "Locate 'All Entities' filter", "expected": "Filter found"},
            {"content": "Verify filter is visible", "expected": "Filter displayed"},
        ],
        "custom_expected": "✅ All Entities filter dropdown is visible",
        "refs": "test_entity_filter_visible",
        "type_id": 1, "priority_id": 3,
    },
    {
        "title": "Home Page - Transactions Filter Visible",
        "custom_preconds": "User is on home page",
        "custom_steps_separated": [
            {"content": "Locate 'All Transactions' filter", "expected": "Filter found"},
            {"content": "Verify filter is visible", "expected": "Filter displayed"},
        ],
        "custom_expected": "✅ All Transactions filter is visible",
        "refs": "test_transactions_filter_visible",
        "type_id": 1, "priority_id": 3,
    },
    {
        "title": "Home Page - Include Recurring Checkbox",
        "custom_preconds": "User is on home page",
        "custom_steps_separated": [
            {"content": "Locate 'Include Recurring' checkbox", "expected": "Checkbox found"},
            {"content": "Verify checkbox is visible", "expected": "Checkbox displayed"},
        ],
        "custom_expected": "✅ Include Recurring checkbox is visible and functional",
        "refs": "test_include_recurring_checkbox",
        "type_id": 1, "priority_id": 3,
    },
    {
        "title": "Home Page - Tag Filters Visible",
        "custom_preconds": "User is on home page",
        "custom_steps_separated": [
            {"content": "Locate Tag 1 filter", "expected": "Tag 1 filter found"},
            {"content": "Locate Tag 2 filter", "expected": "Tag 2 filter found"},
        ],
        "custom_expected": "✅ Both Tag 1 and Tag 2 filters are visible",
        "refs": "test_tag_filters_visible",
        "type_id": 1, "priority_id": 3,
    },
    
    # === TestHomePageKPIs (4 tests) ===
    {
        "title": "Home Page - KPI Section Visible",
        "custom_preconds": "User is on home page",
        "custom_steps_separated": [
            {"content": "Locate 'Key Performance Indicators' section", "expected": "Section found"},
            {"content": "Verify section header is visible", "expected": "Header displayed"},
        ],
        "custom_expected": "✅ KPI section with header is visible",
        "refs": "test_kpi_section_visible",
        "type_id": 1, "priority_id": 1,
    },
    {
        "title": "Home Page - KPI Cards Count",
        "custom_preconds": "User is on home page",
        "custom_steps_separated": [
            {"content": "Count KPI card elements", "expected": "Count >= 5"},
            {"content": "Verify multiple KPI metrics displayed", "expected": "Multiple cards visible"},
        ],
        "custom_expected": "✅ At least 5 KPI cards are displayed\n✅ Cards show: Total Income, Gross Profit, EBITDA, Net margins, etc.",
        "refs": "test_kpi_cards_count",
        "type_id": 1, "priority_id": 2,
    },
    {
        "title": "Home Page - KPI Values Displayed",
        "custom_preconds": "User is on home page",
        "custom_steps_separated": [
            {"content": "Locate monetary values in KPI section", "expected": "Values found"},
            {"content": "Verify at least 3 monetary values displayed", "expected": "Values like $0.60M, $605K visible"},
        ],
        "custom_expected": "✅ KPI cards show monetary values (e.g., $0.60M, $2.82M)\n✅ At least 3 values displayed",
        "refs": "test_kpi_values_displayed",
        "type_id": 1, "priority_id": 2,
    },
    {
        "title": "Home Page - KPI Trend Indicators",
        "custom_preconds": "User is on home page",
        "custom_steps_separated": [
            {"content": "Locate trend indicators (up/down arrows)", "expected": "Indicators found"},
            {"content": "Verify trend icons are displayed", "expected": "Arrows visible"},
        ],
        "custom_expected": "✅ KPI cards show trend indicators (↑ green for positive, ↓ red for negative)",
        "refs": "test_kpi_trend_indicators",
        "type_id": 1, "priority_id": 3,
    },
    
    # === TestHomePageCharts (3 tests) ===
    {
        "title": "Home Page - Total Income Chart Visible",
        "custom_preconds": "User is on home page",
        "custom_steps_separated": [
            {"content": "Locate 'Total income' chart section", "expected": "Chart section found"},
            {"content": "Verify chart displays value (e.g., $605K)", "expected": "Value displayed"},
        ],
        "custom_expected": "✅ Total Income chart is visible\n✅ Shows income value and trends",
        "refs": "test_total_income_chart_visible",
        "type_id": 1, "priority_id": 2,
    },
    {
        "title": "Home Page - Gross Profit Chart Visible",
        "custom_preconds": "User is on home page",
        "custom_steps_separated": [
            {"content": "Locate 'Gross Profit' chart section", "expected": "Chart section found"},
            {"content": "Verify chart shows profit margin trends", "expected": "Chart displayed"},
        ],
        "custom_expected": "✅ Gross Profit chart is visible\n✅ Shows profit margin and percentage trends",
        "refs": "test_gross_profit_chart_visible",
        "type_id": 1, "priority_id": 2,
    },
    {
        "title": "Home Page - Chart Dropdown Selector",
        "custom_preconds": "User is on home page",
        "custom_steps_separated": [
            {"content": "Locate dropdown near Total Income chart", "expected": "Dropdown found"},
            {"content": "Verify dropdown can change metric", "expected": "Selector functional"},
        ],
        "custom_expected": "✅ Chart has dropdown to change displayed metric",
        "refs": "test_chart_dropdown_selector",
        "type_id": 1, "priority_id": 3,
    },
    
    # === TestHomePageNavigation (5 tests) ===
    {
        "title": "Home Page - Sidebar Visible",
        "custom_preconds": "User is on home page",
        "custom_steps_separated": [
            {"content": "Locate sidebar navigation", "expected": "Sidebar found"},
            {"content": "Verify sidebar is visible", "expected": "Sidebar displayed"},
        ],
        "custom_expected": "✅ Sidebar navigation is visible on left side",
        "refs": "test_sidebar_visible",
        "type_id": 1, "priority_id": 1,
    },
    {
        "title": "Home Page - Sidebar Links Count",
        "custom_preconds": "User is on home page",
        "custom_steps_separated": [
            {"content": "Count navigation links in sidebar", "expected": "Count >= 5"},
            {"content": "Verify main navigation items present", "expected": "Links visible"},
        ],
        "custom_expected": "✅ At least 5 navigation links\n✅ Includes: Home, Invoicing, Purchasing, Ledger, Reconciliation, etc.",
        "refs": "test_sidebar_links_count",
        "type_id": 1, "priority_id": 2,
    },
    {
        "title": "Home Page - Navigate to Invoicing",
        "custom_preconds": "User is on home page",
        "custom_steps_separated": [
            {"content": "Click Invoicing link in sidebar", "expected": "Link clicked"},
            {"content": "Wait for navigation", "expected": "Page loads"},
            {"content": "Verify URL contains /invoicing", "expected": "URL correct"},
        ],
        "custom_expected": "✅ Successfully navigates to Invoicing page",
        "refs": "test_navigate_to_invoicing",
        "type_id": 1, "priority_id": 2,
    },
    {
        "title": "Home Page - Navigate to Purchasing",
        "custom_preconds": "User is on home page",
        "custom_steps_separated": [
            {"content": "Click Purchasing link in sidebar", "expected": "Link clicked"},
            {"content": "Wait for navigation", "expected": "Page loads"},
            {"content": "Verify URL contains /purchasing", "expected": "URL correct"},
        ],
        "custom_expected": "✅ Successfully navigates to Purchasing page",
        "refs": "test_navigate_to_purchasing",
        "type_id": 1, "priority_id": 2,
    },
    {
        "title": "Home Page - Navigate Back to Home",
        "custom_preconds": "User is on another page",
        "custom_steps_separated": [
            {"content": "Click Home link or logo", "expected": "Link clicked"},
            {"content": "Wait for navigation", "expected": "Page loads"},
            {"content": "Verify URL contains /home", "expected": "URL correct"},
        ],
        "custom_expected": "✅ Successfully returns to home page",
        "refs": "test_navigate_back_to_home",
        "type_id": 1, "priority_id": 2,
    },
    
    # === TestHomePageEntitySwitching (2 tests) ===
    {
        "title": "Home Page - Entity Dropdown Opens",
        "custom_preconds": "User is on home page",
        "custom_steps_separated": [
            {"content": "Click entity selector dropdown", "expected": "Dropdown opens"},
            {"content": "Verify dropdown menu appears", "expected": "Options visible"},
            {"content": "Close dropdown", "expected": "Dropdown closes"},
        ],
        "custom_expected": "✅ Entity dropdown opens and shows options",
        "refs": "test_entity_dropdown_opens",
        "type_id": 1, "priority_id": 2,
    },
    {
        "title": "Home Page - Current Entity Displayed",
        "custom_preconds": "User is on home page",
        "custom_steps_separated": [
            {"content": "Read entity selector text", "expected": "Text retrieved"},
            {"content": "Verify shows entity name", "expected": "Name like 'Viewz Demo INC' displayed"},
        ],
        "custom_expected": "✅ Current entity name is displayed in selector",
        "refs": "test_current_entity_displayed",
        "type_id": 1, "priority_id": 2,
    },
    
    # === TestHomePageRefresh (1 test) ===
    {
        "title": "Home Page - Refresh Reloads Data",
        "custom_preconds": "User is on home page",
        "custom_steps_separated": [
            {"content": "Refresh the page", "expected": "Page reloads"},
            {"content": "Wait for data to load", "expected": "Dashboard loads"},
            {"content": "Verify KPI section visible", "expected": "KPIs displayed"},
        ],
        "custom_expected": "✅ Page refresh reloads dashboard data\n✅ All elements remain visible",
        "refs": "test_page_refresh_reloads_data",
        "type_id": 1, "priority_id": 2,
    },
    
    # === TestHomePageResponsiveness (1 test) ===
    {
        "title": "Home Page - Elements Load Within Timeout",
        "custom_preconds": "User navigates to home page",
        "custom_steps_separated": [
            {"content": "Navigate to home page", "expected": "Navigation starts"},
            {"content": "Wait for dashboard title (max 10s)", "expected": "Title visible"},
            {"content": "Wait for entity selector (max 10s)", "expected": "Selector visible"},
            {"content": "Wait for KPI section (max 10s)", "expected": "KPIs visible"},
        ],
        "custom_expected": "✅ All critical elements load within 10 seconds\n✅ Page is responsive",
        "refs": "test_elements_load_within_timeout",
        "type_id": 1, "priority_id": 2,
    },
    
    # === TestHomePageDataValidation (2 tests) ===
    {
        "title": "Home Page - KPI Values Are Numeric",
        "custom_preconds": "User is on home page",
        "custom_steps_separated": [
            {"content": "Find monetary values (matching $X.XXM/K pattern)", "expected": "Values found"},
            {"content": "Verify at least 1 valid monetary value", "expected": "Valid format"},
        ],
        "custom_expected": "✅ KPI values contain valid numeric data\n✅ Format: $X.XXM, $XXXK, etc.",
        "refs": "test_kpi_values_are_numeric",
        "type_id": 1, "priority_id": 2,
    },
    {
        "title": "Home Page - Percentage Values Displayed",
        "custom_preconds": "User is on home page",
        "custom_steps_separated": [
            {"content": "Find percentage values (matching X.XX% pattern)", "expected": "Values found"},
            {"content": "Count percentage values", "expected": "Multiple found"},
        ],
        "custom_expected": "✅ Percentage values displayed correctly (e.g., 81.50%, 32.18%)",
        "refs": "test_percentage_values_displayed",
        "type_id": 1, "priority_id": 3,
    },
]

def main():
    print("=" * 60)
    print("🏠 Creating Home Page Test Cases in TestRail")
    print("=" * 60)
    
    section = find_or_create_section(
        SUITE_ID,
        "Home Page Tests",
        "Tests for Financial Overview Dashboard - elements, filters, KPIs, charts, navigation"
    )
    
    if not section:
        print("❌ Failed to find/create section")
        return
    
    section_id = section.get('id')
    print(f"\n📝 Creating {len(HOME_PAGE_TESTS)} test cases in section {section_id}...")
    
    created_cases = []
    for test_case in HOME_PAGE_TESTS:
        case_id = create_test_case(section_id, test_case)
        if case_id:
            created_cases.append({
                "id": case_id,
                "refs": test_case.get("refs", "")
            })
    
    print(f"\n{'=' * 60}")
    print(f"✅ Created {len(created_cases)}/{len(HOME_PAGE_TESTS)} test cases")
    print("=" * 60)
    
    print("\n📋 Add to conftest.py case_mapping:")
    print("-" * 40)
    for case in created_cases:
        if case["refs"]:
            print(f'    "{case["refs"]}": {case["id"]},')
    
    print("\n✅ Done!")

if __name__ == "__main__":
    main()

