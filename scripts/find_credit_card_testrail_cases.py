#!/usr/bin/env python3
"""
Search TestRail for existing Credit Card test cases
"""

import os
import requests
from base64 import b64encode

class TestRailSearcher:
    def __init__(self):
        self.url = os.getenv('TESTRAIL_URL', 'https://viewz.testrail.io')
        self.username = os.getenv('TESTRAIL_USERNAME', 'automation@viewz.co')
        self.password = os.getenv('TESTRAIL_PASSWORD', 'e.fJg:z5q5mnAdL')
        self.project_id = int(os.getenv('TESTRAIL_PROJECT_ID', '1'))
        self.suite_id = int(os.getenv('TESTRAIL_SUITE_ID', '4'))
        
        self.auth = b64encode(f"{self.username}:{self.password}".encode()).decode()
        self.headers = {
            'Authorization': f'Basic {self.auth}',
            'Content-Type': 'application/json'
        }
    
    def _send_request(self, method, uri):
        """Send request to TestRail API"""
        url = f"{self.url}/index.php?/api/v2/{uri}"
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=self.headers, timeout=10)
            
            response.raise_for_status()
            return response.json() if response.content else None
        except requests.exceptions.RequestException as e:
            print(f"❌ API error: {e}")
            return None
    
    def find_credit_card_cases(self):
        """Search for Credit Card test cases"""
        print("🔍 Searching for Credit Card test cases in TestRail...\n")
        
        # Get all cases
        result = self._send_request('GET', f'get_cases/{self.project_id}&suite_id={self.suite_id}')
        
        if not result:
            print("❌ Failed to retrieve test cases")
            return
        
        # Handle pagination
        cases = result.get('cases', []) if isinstance(result, dict) else result
        
        # Search for credit card related cases
        credit_card_cases = []
        keywords = ['credit card', 'creditcard', 'cc', 'card']
        
        for case in cases:
            if not isinstance(case, dict):
                continue
            
            title = case.get('title', '').lower()
            section_id = case.get('section_id')
            
            # Check if title contains credit card keywords
            if any(keyword in title for keyword in keywords):
                credit_card_cases.append(case)
        
        # Get sections to find Credit Card section
        sections_result = self._send_request('GET', f'get_sections/{self.project_id}&suite_id={self.suite_id}')
        
        credit_card_section = None
        if sections_result:
            sections = sections_result.get('sections', []) if isinstance(sections_result, dict) else sections_result
            
            for section in sections:
                if not isinstance(section, dict):
                    continue
                
                section_name = section.get('name', '').lower()
                if 'credit' in section_name or 'card' in section_name:
                    credit_card_section = section
                    print(f"✅ Found Credit Card section: '{section.get('name')}' (ID: {section.get('id')})\n")
                    
                    # Get cases in this section
                    for case in cases:
                        if case.get('section_id') == section.get('id'):
                            if case not in credit_card_cases:
                                credit_card_cases.append(case)
        
        if not credit_card_cases:
            print("⚠️  No Credit Card test cases found in TestRail")
            print("\n📋 Options:")
            print("  1. Cases might exist in a different section")
            print("  2. Cases need to be created (we can do this automatically!)")
            print("  3. Cases might use different naming convention")
            return []
        
        # Display found cases
        print(f"📊 Found {len(credit_card_cases)} Credit Card test case(s):\n")
        print("=" * 80)
        
        for i, case in enumerate(credit_card_cases, 1):
            case_id = case.get('id')
            title = case.get('title')
            section_id = case.get('section_id')
            type_id = case.get('type_id')
            priority_id = case.get('priority_id')
            
            print(f"\n{i}. Case C{case_id}: {title}")
            print(f"   Section ID: {section_id}")
            print(f"   Type: {self._get_type_name(type_id)}")
            print(f"   Priority: {self._get_priority_name(priority_id)}")
            
            # Show any custom fields or steps if available
            if case.get('custom_preconds'):
                print(f"   Preconditions: {case.get('custom_preconds')[:100]}...")
        
        print("\n" + "=" * 80)
        print(f"\n✅ Total Credit Card cases found: {len(credit_card_cases)}")
        
        # Save to file
        import json
        output_file = 'credit_card_testrail_cases_found.json'
        with open(output_file, 'w') as f:
            json.dump({
                'total_cases': len(credit_card_cases),
                'section': credit_card_section,
                'cases': credit_card_cases
            }, f, indent=2)
        
        print(f"💾 Details saved to: {output_file}")
        
        return credit_card_cases
    
    def _get_type_name(self, type_id):
        types = {
            1: "Automated",
            2: "Functional",
            3: "Regression",
            4: "Smoke",
            5: "Performance",
            6: "Security"
        }
        return types.get(type_id, f"Type {type_id}")
    
    def _get_priority_name(self, priority_id):
        priorities = {
            1: "Low",
            2: "Medium",
            3: "High",
            4: "Critical"
        }
        return priorities.get(priority_id, f"Priority {priority_id}")

def main():
    print("🚀 Credit Card TestRail Case Finder")
    print("=" * 80)
    
    searcher = TestRailSearcher()
    cases = searcher.find_credit_card_cases()
    
    if cases:
        print("\n🎯 Next Steps:")
        print("  1. Review the cases found above")
        print("  2. We'll create automation tests for each case")
        print("  3. Tests will automatically map to these TestRail cases")
        print("  4. Results will post to TestRail when tests run")
    else:
        print("\n🎯 Next Steps:")
        print("  1. Provide the TestRail case IDs manually, OR")
        print("  2. We can create the TestRail cases automatically (like Receivables!)")

if __name__ == "__main__":
    main()

