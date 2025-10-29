#!/usr/bin/env python3
"""Find Credit Cards Operations in Suite 139"""

import os
import requests
import json
from base64 import b64encode

url = os.getenv('TESTRAIL_URL', 'https://viewz.testrail.io')
username = os.getenv('TESTRAIL_USERNAME', 'automation@viewz.co')
password = os.getenv('TESTRAIL_PASSWORD', 'e.fJg:z5q5mnAdL')
project_id = 1
suite_id = 139  # The correct suite!

auth = b64encode(f"{username}:{password}".encode()).decode()
headers = {'Authorization': f'Basic {auth}', 'Content-Type': 'application/json'}

print("\n🔍 Searching Suite 139 for Credit Cards Operations...\n")

# Get sections
sections_response = requests.get(
    f"{url}/index.php?/api/v2/get_sections/{project_id}&suite_id={suite_id}",
    headers=headers
)

credit_card_section = None
if sections_response.status_code == 200:
    sections_result = sections_response.json()
    sections = sections_result.get('sections', [])
    
    print("📁 SECTIONS IN SUITE 139:\n")
    for section in sections:
        section_id = section.get('id')
        name = section.get('name')
        depth = section.get('depth', 0)
        indent = "  " * depth
        
        print(f"{indent}[{section_id}] {name}")
        
        if 'credit' in name.lower() and 'card' in name.lower():
            credit_card_section = section
            print(f"{indent}     ⭐⭐⭐ FOUND IT! ⭐⭐⭐")

# Get cases in Credit Card section
if credit_card_section:
    section_id = credit_card_section['id']
    print(f"\n{'='*80}")
    print(f"✅ Found Credit Cards Operations Section: ID {section_id}")
    print(f"{'='*80}\n")
    
    # Get all cases in this section
    cases_response = requests.get(
        f"{url}/index.php?/api/v2/get_cases/{project_id}&suite_id={suite_id}&section_id={section_id}",
        headers=headers
    )
    
    if cases_response.status_code == 200:
        cases_result = cases_response.json()
        cases = cases_result.get('cases', [])
        
        print(f"📊 Found {len(cases)} Credit Card test cases:\n")
        
        case_list = []
        for i, case in enumerate(cases, 1):
            case_id = case.get('id')
            title = case.get('title')
            priority = case.get('priority_id')
            type_id = case.get('type_id')
            
            priority_name = {1: 'Low', 2: 'Medium', 3: 'High', 4: 'Critical'}.get(priority, 'Unknown')
            
            print(f"{i}. C{case_id}: {title}")
            print(f"   Priority: {priority_name}")
            
            case_list.append({
                'case_id': case_id,
                'title': title,
                'priority': priority_name
            })
            
            # Show preconditions if available
            if case.get('custom_preconds'):
                preconds = case.get('custom_preconds')
                print(f"   Preconditions: {preconds[:100]}{'...' if len(preconds) > 100 else ''}")
            print()
        
        # Save to file
        output = {
            'suite_id': suite_id,
            'section': credit_card_section,
            'total_cases': len(cases),
            'case_ids': [c['case_id'] for c in case_list],
            'case_id_range': f"C{min(c['case_id'] for c in case_list)}-C{max(c['case_id'] for c in case_list)}" if case_list else 'N/A',
            'cases': case_list,
            'full_cases': cases
        }
        
        with open('credit_card_suite_139_cases.json', 'w') as f:
            json.dump(output, f, indent=2)
        
        print(f"{'='*80}")
        print(f"✅ SUMMARY:")
        print(f"   Suite: 139")
        print(f"   Section: {credit_card_section['name']} (ID: {section_id})")
        print(f"   Total Cases: {len(cases)}")
        print(f"   Case IDs: C{min(c['case_id'] for c in case_list)}-C{max(c['case_id'] for c in case_list)}")
        print(f"{'='*80}")
        
        print(f"\n💾 Full details saved to: credit_card_suite_139_cases.json")
        
        print("\n🚀 NEXT STEPS:")
        print("  1. Review the cases above")
        print("  2. I'll create automation tests for each case")
        print("  3. Create page object: pages/credit_card_page.py")
        print("  4. Map tests to TestRail cases in conftest.py")
        print("  5. Run tests with TestRail integration")
    else:
        print(f"❌ Failed to get cases: {cases_response.status_code}")
else:
    print("\n⚠️  Credit Cards Operations section not found in Suite 139")
    print("Available sections are listed above.")

