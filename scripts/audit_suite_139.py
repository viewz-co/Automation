#!/usr/bin/env python3
"""
Complete Audit of Suite 139 - Find all cases and check automation coverage
"""

import os
import requests
import json
from base64 import b64encode
import re

class Suite139Auditor:
    def __init__(self):
        self.url = os.getenv('TESTRAIL_URL', 'https://viewz.testrail.io')
        self.username = os.getenv('TESTRAIL_USERNAME', 'automation@viewz.co')
        self.password = os.getenv('TESTRAIL_PASSWORD', 'e.fJg:z5q5mnAdL')
        self.project_id = 1
        self.suite_id = 139
        
        self.auth = b64encode(f"{self.username}:{self.password}".encode()).decode()
        self.headers = {
            'Authorization': f'Basic {self.auth}',
            'Content-Type': 'application/json'
        }
    
    def _send_request(self, uri):
        """Send GET request to TestRail API"""
        url = f"{self.url}/index.php?/api/v2/{uri}"
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            return response.json() if response.content else None
        except Exception as e:
            print(f"❌ API error: {e}")
            return None
    
    def get_all_sections(self):
        """Get all sections in Suite 139"""
        result = self._send_request(f'get_sections/{self.project_id}&suite_id={self.suite_id}')
        if result and isinstance(result, dict):
            return result.get('sections', [])
        return result or []
    
    def get_all_cases(self):
        """Get all test cases in Suite 139"""
        cases = []
        offset = 0
        limit = 250
        
        while True:
            result = self._send_request(
                f'get_cases/{self.project_id}&suite_id={self.suite_id}&offset={offset}&limit={limit}'
            )
            
            if result:
                if isinstance(result, dict):
                    batch = result.get('cases', [])
                else:
                    batch = result
                
                if not batch:
                    break
                    
                cases.extend(batch)
                
                if len(batch) < limit:
                    break
                    
                offset += limit
            else:
                break
        
        return cases
    
    def get_conftest_mappings(self):
        """Extract all mappings from conftest.py"""
        with open('tests/conftest.py', 'r') as f:
            content = f.read()
        
        # Extract case_mapping
        match = re.search(r'case_mapping = \{(.*?)\}', content, re.DOTALL)
        if not match:
            return {}
        
        mapping_text = match.group(1)
        mappings = re.findall(r"'([^']+)':\s*(\d+)", mapping_text)
        
        # Build mapping dict
        case_to_tests = {}
        test_to_case = {}
        
        for test_name, case_id in mappings:
            case_id = int(case_id)
            test_to_case[test_name] = case_id
            
            if case_id not in case_to_tests:
                case_to_tests[case_id] = []
            case_to_tests[case_id].append(test_name)
        
        return {
            'case_to_tests': case_to_tests,
            'test_to_case': test_to_case
        }
    
    def audit(self):
        """Complete audit of Suite 139"""
        print("=" * 80)
        print("SUITE 139 - COMPLETE AUDIT")
        print("=" * 80)
        
        # Get sections
        sections = self.get_all_sections()
        print(f"\n📁 Found {len(sections)} sections in Suite 139\n")
        
        section_map = {s['id']: s['name'] for s in sections}
        
        # Get all cases
        all_cases = self.get_all_cases()
        print(f"📊 Found {len(all_cases)} total test cases in Suite 139\n")
        
        # Get conftest mappings
        mappings = self.get_conftest_mappings()
        case_to_tests = mappings['case_to_tests']
        
        # Organize by section
        cases_by_section = {}
        for case in all_cases:
            section_id = case.get('section_id')
            if section_id not in cases_by_section:
                cases_by_section[section_id] = []
            cases_by_section[section_id].append(case)
        
        # Analyze each section
        print("=" * 80)
        print("AUTOMATION COVERAGE BY SECTION")
        print("=" * 80)
        
        total_with_automation = 0
        total_without_automation = 0
        
        for section_id in sorted(cases_by_section.keys()):
            section_name = section_map.get(section_id, f"Section {section_id}")
            cases = cases_by_section[section_id]
            
            with_automation = []
            without_automation = []
            
            for case in cases:
                case_id = case['id']
                if case_id in case_to_tests:
                    with_automation.append(case)
                else:
                    without_automation.append(case)
            
            total_with_automation += len(with_automation)
            total_without_automation += len(without_automation)
            
            print(f"\n📂 {section_name}")
            print(f"   Total Cases: {len(cases)}")
            print(f"   ✅ With Automation: {len(with_automation)}")
            print(f"   ❌ Without Automation: {len(without_automation)}")
            
            if without_automation:
                print(f"   \n   Missing Automation:")
                for case in without_automation[:5]:  # Show first 5
                    print(f"      C{case['id']}: {case['title']}")
                if len(without_automation) > 5:
                    print(f"      ... and {len(without_automation) - 5} more")
        
        # Summary
        print("\n" + "=" * 80)
        print("SUMMARY")
        print("=" * 80)
        print(f"Total Cases in Suite 139: {len(all_cases)}")
        print(f"✅ With Automation: {total_with_automation} ({total_with_automation/len(all_cases)*100:.1f}%)")
        print(f"❌ Without Automation: {total_without_automation} ({total_without_automation/len(all_cases)*100:.1f}%)")
        
        # Save detailed report
        report = {
            'suite_id': 139,
            'total_cases': len(all_cases),
            'with_automation': total_with_automation,
            'without_automation': total_without_automation,
            'sections': {}
        }
        
        for section_id, cases in cases_by_section.items():
            section_name = section_map.get(section_id, f"Section {section_id}")
            
            report['sections'][section_name] = {
                'section_id': section_id,
                'total_cases': len(cases),
                'cases': []
            }
            
            for case in cases:
                case_id = case['id']
                report['sections'][section_name]['cases'].append({
                    'id': case_id,
                    'title': case['title'],
                    'has_automation': case_id in case_to_tests,
                    'test_functions': case_to_tests.get(case_id, [])
                })
        
        with open('suite_139_audit_report.json', 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"\n💾 Detailed report saved to: suite_139_audit_report.json")
        
        return report

if __name__ == "__main__":
    auditor = Suite139Auditor()
    auditor.audit()

