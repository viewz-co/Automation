#!/usr/bin/env python3
"""
Create BO Snapshot TestRail Cases
Add BO snapshot test cases to TestRail with detailed goals and assertions
"""

import os
import sys
import json
import time
from datetime import datetime

# Add the parent directory to the path to import our configs
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from configs.testrail_config import TestRailConfig

def main():
    """Create BO snapshot test cases in TestRail"""
    print("🚀 Creating BO Snapshot Test Cases in TestRail")
    print("="*60)
    
    # Initialize config
    config = TestRailConfig()
    project_id = config.project_id
    suite_id = 139  # Use existing comprehensive suite
    
    print(f"📊 Project ID: {project_id}")
    print(f"📝 Suite ID: {suite_id}")
    
    # Find existing BO section
    sections = config._send_request('GET', f'get_sections/{project_id}&suite_id={suite_id}')
    bo_section_id = None
    
    if sections and isinstance(sections, list):
        print(f"🔍 Found {len(sections)} sections total")
        for section in sections:
            if isinstance(section, dict):
                section_name = section.get('name', '')
                section_id = section.get('id', 'N/A')
                print(f"   📂 Section: '{section_name}' (ID: {section_id})")
                if 'BO Environment Testing' in section_name or section_name == '🔐 BO Environment Testing':
                    bo_section_id = section['id']
                    print(f"✅ Found existing BO section: ID {bo_section_id}")
                    break
    else:
        print(f"⚠️ Sections response: {type(sections)} - {sections}")
        # Try direct section ID approach
        bo_section_id = 1860  # Use the section ID we know was created
        print(f"🔧 Using known BO section ID: {bo_section_id}")
    
    if not bo_section_id:
        print("❌ BO section not found. Available sections listed above.")
        print("Please run: python3 scripts/create_actual_bo_testrail_cases.py first")
        return False
    
    # BO Snapshot test cases with detailed information
    bo_snapshot_cases = [
        {
            'title': 'BO Visual Snapshots - Key Pages',
            'description': '''Test visual snapshots of key BO pages for regression detection:
1. BO Login page visual state
2. BO Accounts management page after login
3. BO Account detail views
4. Full page screenshot comparisons for UI changes
5. Visual regression detection across BO workflow''',
            'goal': 'Capture and verify visual snapshots of key BO pages to detect UI regressions and layout changes',
            'assertions': [
                'assert login_page_snapshot_captured == True',
                'assert accounts_page_snapshot_captured == True',
                'assert account_detail_snapshot_captured == True',
                'assert successful_snapshots >= total_snapshots / 2',
                'assert all_snapshot_files_exist == True',
                'assert no_critical_visual_regressions_detected == True'
            ],
            'test_function': 'test_bo_visual_snapshots',
            'priority': 3,
            'case_id': 27985
        },
        {
            'title': 'BO DOM Snapshots - Critical Elements',
            'description': '''Test DOM snapshots of critical BO page elements:
1. BO navigation header structure
2. BO accounts table HTML structure
3. BO main content area DOM
4. BO sidebar navigation elements
5. BO action buttons and form elements
6. DOM structure consistency validation''',
            'goal': 'Capture and verify DOM snapshots of critical BO elements to detect structural changes',
            'assertions': [
                'assert header_dom_snapshot_captured == True',
                'assert accounts_table_dom_captured == True',
                'assert main_content_dom_captured == True',
                'assert sidebar_navigation_dom_captured == True',
                'assert action_buttons_dom_captured == True',
                'assert dom_content_normalized == True',
                'assert successful_dom_snapshots > 0'
            ],
            'test_function': 'test_bo_dom_snapshots',
            'priority': 3,
            'case_id': 27986
        },
        {
            'title': 'BO Workflow Snapshots - Complete Process',
            'description': '''Test snapshots throughout the complete BO workflow:
1. BO login page initial state
2. BO accounts page after successful login
3. BO account selection and highlighting
4. BO relogin process (if successful)
5. Step-by-step workflow visual documentation
6. Process flow regression detection''',
            'goal': 'Document and verify the complete BO workflow through visual snapshots for process consistency',
            'assertions': [
                'assert login_workflow_snapshot_captured == True',
                'assert accounts_workflow_snapshot_captured == True',
                'assert selection_workflow_snapshot_captured == True',
                'assert relogin_workflow_documented == True',
                'assert workflow_steps_complete >= 2',
                'assert process_consistency_verified == True'
            ],
            'test_function': 'test_bo_workflow_snapshots',
            'priority': 3,
            'case_id': 27987
        },
        {
            'title': 'BO Component Snapshots - UI Elements',
            'description': '''Test snapshots of specific BO UI components:
1. BO login form component
2. BO navigation header component
3. BO accounts table component
4. BO action buttons component
5. BO user menu component
6. Individual component regression testing''',
            'goal': 'Capture and verify individual BO UI components for granular regression detection',
            'assertions': [
                'assert login_form_component_captured == True',
                'assert navigation_header_component_captured == True',
                'assert accounts_table_component_captured == True',
                'assert action_buttons_component_captured == True',
                'assert component_isolation_successful == True',
                'assert component_snapshots_documented == True'
            ],
            'test_function': 'test_bo_component_snapshots',
            'priority': 2,
            'case_id': 27988
        }
    ]
    
    # Create test cases in TestRail
    print(f"\n📝 Creating {len(bo_snapshot_cases)} BO snapshot test cases...")
    created_cases = {}
    
    for i, case_data in enumerate(bo_snapshot_cases, 1):
        print(f"\n🔄 Creating case {i}/{len(bo_snapshot_cases)}: {case_data['title']}")
        
        # Build enhanced test steps
        enhanced_steps = f"""🎯 **TEST GOAL:**
{case_data['goal']}

📋 **TEST DESCRIPTION:**
{case_data['description']}

🔧 **TEST EXECUTION STEPS:**
1. Setup: Initialize BO environment and page objects
2. Login: Authenticate to BO with OTP verification
3. Navigation: Navigate to required BO pages/sections
4. Snapshot: Capture visual/DOM/component snapshots
5. Validation: Verify snapshot capture and integrity
6. Storage: Save snapshots to designated directories
7. Cleanup: Take final screenshots for evidence

✅ **ASSERTIONS VERIFIED:**
"""
        
        for i, assertion in enumerate(case_data['assertions'], 1):
            enhanced_steps += f"{i}. {assertion}\n"

        enhanced_steps += f"""

📊 **SUCCESS CRITERIA:**
- All snapshot captures complete successfully
- Visual/DOM snapshots stored in correct directories
- No critical errors during snapshot process
- Evidence captured for regression comparison
- Test goal achieved with proper documentation

🔧 **AUTOMATION DETAILS:**
- Test Function: {case_data['test_function']}
- Framework: Playwright + pytest + BO Framework
- Environment: BO (https://bo.viewz.co)
- TestRail Integration: Enabled with case ID {case_data['case_id']}
- Screenshot Storage: snapshots/visual/, snapshots/dom/, screenshots/
- Snapshot Types: Visual, DOM, Component, Workflow

📱 **SNAPSHOT COVERAGE:**
- Browser: Chromium-based browsers
- Viewport: 1280x720 (configurable)
- Full Page: Yes for workflow snapshots
- Component Level: Yes for UI element snapshots
- DOM Structure: Yes for element snapshots
- Regression Detection: Visual comparison ready"""

        # Prepare test case data for TestRail
        data = {
            'title': case_data['title'],
            'section_id': bo_section_id,
            'template_id': 1,  # Test Case (Steps)
            'type_id': 1,      # Automated
            'priority_id': case_data['priority'],
            'custom_steps': enhanced_steps,
            'custom_preconds': f"Prerequisites: BO environment accessible, BO admin credentials available, OTP secret configured, Snapshot directories writable for {case_data['test_function']}",
            'custom_expected': f"Expected Result: {case_data['goal']} - All snapshot captures complete successfully with proper evidence"
        }
        
        # Create the test case in TestRail
        result = config._send_request('POST', f'add_case/{bo_section_id}', data)
        if result:
            case_id = result['id']
            # Verify the case ID matches our expectation
            if case_id == case_data['case_id']:
                print(f"✅ Created: C{case_id} - {case_data['title']} (ID matches expectation)")
            else:
                print(f"✅ Created: C{case_id} - {case_data['title']} (Expected: C{case_data['case_id']})")
            
            created_cases[case_data['test_function']] = case_id
        else:
            print(f"❌ Failed to create: {case_data['title']}")
        
        time.sleep(0.5)  # Prevent rate limiting
    
    # Update mapping file with actual TestRail case IDs  
    if created_cases:
        print(f"\n📄 Updating BO snapshot mapping files...")
        
        # Load existing BO mappings
        try:
            with open('bo_testrail_mappings_actual.json', 'r') as f:
                existing_mappings = json.load(f)
        except FileNotFoundError:
            existing_mappings = {
                'bo_suite_info': {
                    'suite_id': suite_id,
                    'section_id': bo_section_id,
                    'project_id': project_id
                },
                'bo_testrail_cases': {},
                'bo_framework_mappings': {}
            }
        
        # Add snapshot cases
        for test_function, case_id in created_cases.items():
            existing_mappings['bo_testrail_cases'][test_function] = f"C{case_id}"
            existing_mappings['bo_framework_mappings'][test_function] = f"C{case_id}"
        
        # Update metadata
        existing_mappings['bo_suite_info']['total_bo_cases'] = len(existing_mappings['bo_testrail_cases'])
        existing_mappings['bo_suite_info']['last_updated'] = datetime.now().isoformat()
        existing_mappings['bo_suite_info']['status'] = 'BO Snapshot TestRail cases created successfully'
        
        # Save updated mapping file
        with open('bo_testrail_mappings_actual.json', 'w') as f:
            json.dump(existing_mappings, f, indent=2)
        
        print("✅ Updated bo_testrail_mappings_actual.json with snapshot cases")
        
        # Print summary
        print("\n" + "="*80)
        print("🎉 BO SNAPSHOT TESTRAIL CASES CREATED SUCCESSFULLY!")
        print("="*80)
        print(f"📊 Suite ID: {suite_id}")
        print(f"📂 BO Section ID: {bo_section_id}")
        print(f"📝 Snapshot Test Cases Created: {len(created_cases)}")
        
        print("\n📝 Created BO Snapshot TestRail Cases:")
        for test_function, case_id in created_cases.items():
            print(f"   C{case_id}: {test_function}")
        
        print(f"\n🔗 TestRail URLs:")
        print(f"   📋 Suite: https://viewz.testrail.io/index.php?/suites/view/{suite_id}")
        print(f"   📂 BO Section: https://viewz.testrail.io/index.php?/suites/view/{suite_id}&group_by=cases:section_id&group_id={bo_section_id}")
        
        print("\n✅ Next Steps:")
        print("   1. BO snapshot test cases are now created in TestRail")
        print("   2. Run BO snapshot tests to verify functionality")
        print("   3. Check snapshots directory for captured evidence")
        print("   4. Review TestRail for detailed test execution results")
        
        return True
    else:
        print("❌ No snapshot test cases were created successfully")
        return False

if __name__ == "__main__":
    main()
