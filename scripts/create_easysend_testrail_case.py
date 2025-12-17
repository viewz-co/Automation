"""
Script to create EasySend Email to Payables test case in TestRail Suite 139
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

def create_testrail_case():
    """Create EasySend Email to Payables test case"""
    
    # First, find or create a section for EasySend tests
    headers = {
        "Content-Type": "application/json"
    }
    auth = (TESTRAIL_USER, TESTRAIL_API_KEY)
    
    # Get project ID from suite
    suite_url = f"{TESTRAIL_URL}/index.php?/api/v2/get_suite/{SUITE_ID}"
    response = requests.get(suite_url, headers=headers, auth=auth)
    
    if response.status_code != 200:
        print(f"❌ Failed to get suite: {response.text}")
        return None
    
    suite_data = response.json()
    project_id = suite_data.get("project_id")
    print(f"✅ Found Suite {SUITE_ID} in Project {project_id}")
    
    # Get sections to find or create EasySend section
    sections_url = f"{TESTRAIL_URL}/index.php?/api/v2/get_sections/{project_id}&suite_id={SUITE_ID}"
    response = requests.get(sections_url, headers=headers, auth=auth)
    
    if response.status_code != 200:
        print(f"❌ Failed to get sections: {response.text}")
        return None
    
    sections = response.json().get("sections", response.json()) if isinstance(response.json(), dict) else response.json()
    
    # Find EasySend section or use existing one
    easysend_section_id = None
    for section in sections:
        if "easysend" in section.get("name", "").lower() or "email" in section.get("name", "").lower():
            easysend_section_id = section["id"]
            print(f"✅ Found existing section: {section['name']} (ID: {easysend_section_id})")
            break
    
    # If no section found, create one
    if not easysend_section_id:
        create_section_url = f"{TESTRAIL_URL}/index.php?/api/v2/add_section/{project_id}"
        section_data = {
            "suite_id": SUITE_ID,
            "name": "📧 EasySend Integration Tests",
            "description": "End-to-end tests for EasySend email to payables flow"
        }
        response = requests.post(create_section_url, headers=headers, auth=auth, json=section_data)
        
        if response.status_code == 200:
            easysend_section_id = response.json()["id"]
            print(f"✅ Created new section: EasySend Integration Tests (ID: {easysend_section_id})")
        else:
            print(f"⚠️ Could not create section, using first available section")
            easysend_section_id = sections[0]["id"] if sections else None
    
    if not easysend_section_id:
        print("❌ No section available")
        return None
    
    # Create the test case
    test_case = {
        "title": "EasySend Email to Payables - Complete E2E Flow",
        "section_id": easysend_section_id,
        "template_id": 1,  # Test Case (Steps)
        "type_id": 1,  # Automated
        "priority_id": 2,  # High
        "refs": "EasySend Integration",
        "custom_preconds": """**Preconditions:**
1. Gmail account (viewzqa0@gmail.com) is accessible
2. BO account (sharonadmin) has access to account 71
3. Test PDF file exists at: uploaded_test_files/PI25007981 - הדפסת חשבונית עסקה 1.1.pdf
4. EasySend email processing is configured for easysend@viewz.co
5. HTTP Basic Auth credentials configured for both BO and App domains""",
        "custom_steps_separated": [
            {
                "content": "**STEP 1: Login to Gmail**\n- Navigate to gmail.com\n- Enter email: viewzqa0@gmail.com\n- Enter password\n- Handle any CAPTCHA or verification if required",
                "expected": "Successfully logged into Gmail inbox"
            },
            {
                "content": "**STEP 2: Compose and Send Email**\n- Click 'Compose' button\n- Enter recipient: easysend@viewz.co\n- Enter subject with timestamp\n- Attach PDF file: PI25007981 - הדפסת חשבונית עסקה 1.1.pdf\n- Click 'Send'",
                "expected": "Email sent successfully, compose window closes"
            },
            {
                "content": "**STEP 3: Wait for Processing**\n- Wait 60 seconds for EasySend to process the email",
                "expected": "Wait completes"
            },
            {
                "content": "**STEP 4: Login to BO**\n- Navigate to bo.stage.viewz.co\n- Enter username: sharonadmin\n- Enter password\n- Enter OTP code",
                "expected": "Successfully logged into BO, redirected to settings/accounts"
            },
            {
                "content": "**STEP 5: Search for Account 71**\n- Navigate to /settings/accounts\n- Search for account ID: 71",
                "expected": "Account 71 is displayed in the accounts list"
            },
            {
                "content": "**STEP 6: Relogin to Account 71**\n- Hover over account 71 row\n- Click the relogin arrow button (→)\n- Enter OTP in new window\n- Wait for redirect to app",
                "expected": "New window opens with app.stage.viewz.co, user is logged in as account 71"
            },
            {
                "content": "**STEP 7: Navigate to Payables**\n- Navigate to /reconciliation/payables",
                "expected": "Payables page loads successfully (not redirected to login)"
            },
            {
                "content": "**STEP 8: Verify File in Payables**\n- Search for the uploaded file (PI25007981)\n- Verify the file appears in the payables list",
                "expected": "The sent PDF file appears in the payables list"
            },
            {
                "content": "**STEP 9: Delete File from Payables**\n- Select the uploaded file\n- Delete the file",
                "expected": "File is deleted successfully from payables"
            }
        ],
        "custom_expected": """**Expected Results:**
1. Gmail login successful
2. Email with PDF attachment sent to easysend@viewz.co
3. BO login and 2FA successful
4. Account 71 found and relogin successful
5. Payables page accessible after relogin
6. Uploaded file appears in payables
7. File can be deleted from payables

**Assertions:**
- assert gmail_login_success == True
- assert email_sent == True
- assert bo_login_success == True
- assert account_71_found == True
- assert relogin_success == True
- assert payables_page_loaded == True (URL contains /reconciliation/payables)
- assert file_found_in_payables == True
- assert file_deleted == True"""
    }
    
    # Create the test case
    create_case_url = f"{TESTRAIL_URL}/index.php?/api/v2/add_case/{easysend_section_id}"
    response = requests.post(create_case_url, headers=headers, auth=auth, json=test_case)
    
    if response.status_code == 200:
        case_data = response.json()
        case_id = case_data["id"]
        print(f"\n✅ Created Test Case: C{case_id}")
        print(f"   Title: {test_case['title']}")
        print(f"   Section ID: {easysend_section_id}")
        print(f"\n📋 Add this mapping to conftest.py:")
        print(f"   'test_easysend_email_to_payables_flow': {case_id},  # C{case_id} - EasySend Email to Payables")
        return case_id
    else:
        print(f"❌ Failed to create test case: {response.text}")
        return None


if __name__ == "__main__":
    print("="*60)
    print("Creating EasySend Test Case in TestRail Suite 139")
    print("="*60)
    
    case_id = create_testrail_case()
    
    if case_id:
        print("\n" + "="*60)
        print("✅ SUCCESS!")
        print("="*60)
        print(f"\nTest Case ID: C{case_id}")
        print(f"\nNext steps:")
        print(f"1. Add mapping to tests/conftest.py:")
        print(f"   'test_easysend_email_to_payables_flow': {case_id},")
        print(f"\n2. Run the test to verify mapping works")
    else:
        print("\n❌ Failed to create test case")

