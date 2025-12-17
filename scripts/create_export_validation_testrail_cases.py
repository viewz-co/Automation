"""
Script to create Export Validation test cases in TestRail Suite 139
- Payables Export Data Validation
- Receivables Export Data Validation
"""

import requests
import json
from datetime import datetime

# Import TestRail Config
import sys
sys.path.insert(0, '/Users/sharonhoffman/Desktop/Automation/playwright_python_framework')
from configs.testrail_config import TestRailConfig

# Get config
config = TestRailConfig()
TESTRAIL_URL = config.url
TESTRAIL_USER = config.username
TESTRAIL_API_KEY = config.password
SUITE_ID = config.suite_id

def get_or_create_section(headers, auth, project_id, section_name, description):
    """Get existing section or create new one"""
    
    # Get sections
    sections_url = f"{TESTRAIL_URL}/index.php?/api/v2/get_sections/{project_id}&suite_id={SUITE_ID}"
    response = requests.get(sections_url, headers=headers, auth=auth)
    
    if response.status_code != 200:
        print(f"❌ Failed to get sections: {response.text}")
        return None
    
    sections = response.json().get("sections", response.json()) if isinstance(response.json(), dict) else response.json()
    
    # Find existing section
    for section in sections:
        if section_name.lower() in section.get("name", "").lower():
            print(f"✅ Found existing section: {section['name']} (ID: {section['id']})")
            return section["id"]
    
    # Create new section
    create_section_url = f"{TESTRAIL_URL}/index.php?/api/v2/add_section/{project_id}"
    section_data = {
        "suite_id": SUITE_ID,
        "name": section_name,
        "description": description
    }
    response = requests.post(create_section_url, headers=headers, auth=auth, json=section_data)
    
    if response.status_code == 200:
        section_id = response.json()["id"]
        print(f"✅ Created new section: {section_name} (ID: {section_id})")
        return section_id
    else:
        print(f"⚠️ Could not create section: {response.text}")
        return sections[0]["id"] if sections else None


def create_payables_export_case(headers, auth, section_id):
    """Create Payables Export Data Validation test case"""
    
    test_case = {
        "title": "Payables Export Data Validation",
        "section_id": section_id,
        "template_id": 1,  # Test Case (Steps)
        "type_id": 1,  # Automated
        "priority_id": 2,  # High
        "refs": "Export Validation",
        "custom_preconds": """**Preconditions:**
1. User is logged into the application
2. Payables section has data available (date filter set to 1/1/2020)
3. Export functionality is enabled
4. openpyxl library is installed for Excel file reading""",
        "custom_steps_separated": [
            {
                "content": "**STEP 1: Navigate to Payables**\n- Navigate to /reconciliation/payables\n- Verify page loads successfully",
                "expected": "Payables page loads, URL contains 'payables'"
            },
            {
                "content": "**STEP 2: Set Date Filter**\n- Locate the 'From' date filter\n- Set date to 01/01/2020\n- Wait for table to refresh",
                "expected": "Date filter is set to 1/1/2020, table shows historical data"
            },
            {
                "content": "**STEP 3: Get UI Row Count**\n- Count visible rows in the table\n- Note total count from pagination if available",
                "expected": "Row count is captured (should be > 0)"
            },
            {
                "content": "**STEP 4: Extract UI Table Data**\n- Read all visible rows from the table\n- Capture cell values for each row\n- Handle truncated text (ellipsis)",
                "expected": "Table data extracted successfully"
            },
            {
                "content": "**STEP 5: Click Export Button**\n- Locate Export button\n- Click to initiate download\n- Wait for file download to complete",
                "expected": "Excel/CSV file downloaded successfully"
            },
            {
                "content": "**STEP 6: Read Exported File**\n- Open downloaded file (XLSX format)\n- Extract headers and data rows\n- Note total row count in export",
                "expected": "File read successfully, data extracted"
            },
            {
                "content": "**STEP 7: Compare Data**\n- Compare UI data with exported data\n- Normalize dates (MM/DD/YYYY ↔ YYYY-MM-DD)\n- Normalize numbers (handle currency symbols, negative formats)\n- Handle truncated text comparison",
                "expected": "Data comparison completed"
            },
            {
                "content": "**STEP 8: Validate Results**\n- Verify export row count >= UI visible rows\n- Verify data match percentage >= 95%",
                "expected": "Row count valid, data match >= 95%"
            }
        ],
        "custom_expected": """**Expected Results:**
1. Payables page loads successfully
2. Date filter set to historical date
3. Data is visible in the table
4. Export downloads successfully
5. Exported data matches UI data >= 95%

**Assertions:**
- assert 'payables' in page.url
- assert export_row_count >= ui_visible_rows
- assert data_match_percentage >= 95%

**Known Issues:**
- Status column may show different values in UI vs Export (bug)
- UI shows: 'Pending Approval', 'Sent to Bank', 'Approved'
- Export shows: 'New', 'Matched', 'AI Recommended'"""
    }
    
    create_case_url = f"{TESTRAIL_URL}/index.php?/api/v2/add_case/{section_id}"
    response = requests.post(create_case_url, headers=headers, auth=auth, json=test_case)
    
    if response.status_code == 200:
        case_data = response.json()
        case_id = case_data["id"]
        print(f"\n✅ Created Payables Export Test Case: C{case_id}")
        return case_id
    else:
        print(f"❌ Failed to create Payables test case: {response.text}")
        return None


def create_receivables_export_case(headers, auth, section_id):
    """Create Receivables Export Data Validation test case"""
    
    test_case = {
        "title": "Receivables Export Data Validation",
        "section_id": section_id,
        "template_id": 1,  # Test Case (Steps)
        "type_id": 1,  # Automated
        "priority_id": 2,  # High
        "refs": "Export Validation",
        "custom_preconds": """**Preconditions:**
1. User is logged into the application
2. Receivables section has data available (date filter set to 1/1/2020)
3. Export functionality is enabled
4. openpyxl library is installed for Excel file reading""",
        "custom_steps_separated": [
            {
                "content": "**STEP 1: Navigate to Receivables**\n- Navigate to /reconciliation/receivables\n- Verify page loads successfully",
                "expected": "Receivables page loads, URL contains 'receivables'"
            },
            {
                "content": "**STEP 2: Set Date Filter**\n- Locate the 'From' date filter\n- Set date to 01/01/2020\n- Wait for table to refresh",
                "expected": "Date filter is set to 1/1/2020, table shows historical data"
            },
            {
                "content": "**STEP 3: Get UI Row Count**\n- Count visible rows in the table\n- Note total count from pagination if available",
                "expected": "Row count is captured (should be > 0)"
            },
            {
                "content": "**STEP 4: Extract UI Table Data**\n- Read all visible rows from the table\n- Capture cell values for each row\n- Handle truncated text (ellipsis)",
                "expected": "Table data extracted successfully"
            },
            {
                "content": "**STEP 5: Click Export Button**\n- Locate Export button\n- Click to initiate download\n- Wait for file download to complete",
                "expected": "Excel/CSV file downloaded successfully"
            },
            {
                "content": "**STEP 6: Read Exported File**\n- Open downloaded file (XLSX format)\n- Extract headers and data rows\n- Note total row count in export",
                "expected": "File read successfully, data extracted"
            },
            {
                "content": "**STEP 7: Compare Data**\n- Compare UI data with exported data\n- Normalize dates (MM/DD/YYYY ↔ YYYY-MM-DD)\n- Normalize numbers (handle currency symbols, negative formats)\n- Handle truncated text comparison",
                "expected": "Data comparison completed"
            },
            {
                "content": "**STEP 8: Validate Results**\n- Verify export row count >= UI visible rows (pagination)\n- Verify data match percentage >= 95%",
                "expected": "Row count valid, data match >= 95%"
            }
        ],
        "custom_expected": """**Expected Results:**
1. Receivables page loads successfully
2. Date filter set to historical date
3. Data is visible in the table
4. Export downloads successfully
5. Exported data matches UI data >= 95%

**Assertions:**
- assert 'receivables' in page.url
- assert export_row_count >= ui_visible_rows
- assert data_match_percentage >= 95%

**Known Issues:**
- Status column may show different values in UI vs Export (bug)
- UI shows: 'Created'
- Export shows: 'New'"""
    }
    
    create_case_url = f"{TESTRAIL_URL}/index.php?/api/v2/add_case/{section_id}"
    response = requests.post(create_case_url, headers=headers, auth=auth, json=test_case)
    
    if response.status_code == 200:
        case_data = response.json()
        case_id = case_data["id"]
        print(f"\n✅ Created Receivables Export Test Case: C{case_id}")
        return case_id
    else:
        print(f"❌ Failed to create Receivables test case: {response.text}")
        return None


def main():
    print("="*60)
    print("Creating Export Validation Test Cases in TestRail Suite 139")
    print("="*60)
    
    headers = {
        "Content-Type": "application/json"
    }
    auth = (TESTRAIL_USER, TESTRAIL_API_KEY)
    
    # Get project ID from suite
    suite_url = f"{TESTRAIL_URL}/index.php?/api/v2/get_suite/{SUITE_ID}"
    response = requests.get(suite_url, headers=headers, auth=auth)
    
    if response.status_code != 200:
        print(f"❌ Failed to get suite: {response.text}")
        return
    
    suite_data = response.json()
    project_id = suite_data.get("project_id")
    print(f"✅ Found Suite {SUITE_ID} in Project {project_id}")
    
    # Get or create Export Validation section
    section_id = get_or_create_section(
        headers, auth, project_id,
        "📊 Export Validation Tests",
        "Tests for validating data export functionality in Payables and Receivables"
    )
    
    if not section_id:
        print("❌ Could not get/create section")
        return
    
    # Create test cases
    payables_case_id = create_payables_export_case(headers, auth, section_id)
    receivables_case_id = create_receivables_export_case(headers, auth, section_id)
    
    # Summary
    print("\n" + "="*60)
    print("✅ SUMMARY")
    print("="*60)
    
    mappings = []
    if payables_case_id:
        mappings.append(f"    'test_payables_export_data_validation': {payables_case_id},  # C{payables_case_id}")
        print(f"✅ Payables Export Test: C{payables_case_id}")
    
    if receivables_case_id:
        mappings.append(f"    'test_receivables_export_data_validation': {receivables_case_id},  # C{receivables_case_id}")
        print(f"✅ Receivables Export Test: C{receivables_case_id}")
    
    if mappings:
        print("\n📋 Add these mappings to tests/conftest.py case_mapping:")
        print("-"*60)
        for mapping in mappings:
            print(mapping)
        print("-"*60)


if __name__ == "__main__":
    main()
