#!/usr/bin/env python3
"""
Add Snapshot Tests to TestRail Suite
Adds the new snapshot testing capabilities to the existing TestRail suite
"""

import os
import sys
import json
import time
from typing import Dict, List
from datetime import datetime

# Add the parent directory to the path to import our configs
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from configs.testrail_config import TestRailConfig

class SnapshotTestsAdder:
    def __init__(self):
        self.config = TestRailConfig()
        self.project_id = self.config.project_id
        
        # Existing suite ID (from previous creation)
        self.suite_id = 139  # The comprehensive suite we created earlier
        
        self.new_section_id = None
        self.new_case_mappings = {}
        
    def add_snapshot_section(self):
        """Add the Snapshot Regression section to the existing suite"""
        print(f"📸 Adding Snapshot Regression section to suite {self.suite_id}...")
        
        section_data = {
            'suite_id': self.suite_id,
            'name': '📸 Snapshot Regression',
            'description': 'Visual, DOM, and API snapshot testing for regression detection and change monitoring'
        }
        
        result = self.config._send_request('POST', f'add_section/{self.project_id}', section_data)
        if result:
            self.new_section_id = result['id']
            print(f"✅ Created section: 📸 Snapshot Regression (ID: {self.new_section_id})")
            return True
        else:
            print(f"❌ Failed to create snapshot section")
            return False
    
    def add_snapshot_test_cases(self):
        """Add all snapshot test cases to the new section"""
        print("\n📝 Creating snapshot test cases...")
        
        # Define snapshot test cases
        snapshot_tests = [
            {
                'title': 'Visual Snapshots - Key Application Pages',
                'description': '''Visual regression testing through full-page screenshots of critical application pages.
                
Test Steps:
1. Navigate to Home page and capture visual snapshot
2. Navigate to Reconciliation page and capture visual snapshot  
3. Navigate to Ledger page and capture visual snapshot
4. Compare screenshots against baseline images

Expected Result: 
- Screenshots captured successfully for all key pages
- No unexpected visual differences detected
- Snapshots stored in organized directory structure

TestRail Case ID: Mapped to test_visual_snapshots_key_pages''',
                'priority': 2,
                'type_id': 1  # Automated test
            },
            {
                'title': 'DOM Snapshots - Critical Page Elements',
                'description': '''DOM structure monitoring for critical page elements to detect markup changes.
                
Test Steps:
1. Navigate to application pages
2. Extract HTML content from main content areas
3. Extract HTML content from navigation headers
4. Normalize DOM content (remove dynamic attributes)
5. Save DOM snapshots as HTML files

Expected Result:
- DOM snapshots captured for critical elements
- Content properly normalized for stable comparison
- Snapshots saved to dom/ directory
- Structural consistency validated

TestRail Case ID: Mapped to test_dom_snapshots_critical_elements''',
                'priority': 2,
                'type_id': 1  # Automated test
            },
            {
                'title': 'API Response Snapshots',
                'description': '''API response pattern validation for contract change detection.
                
Test Steps:
1. Intercept network requests during user workflows
2. Capture API response metadata (status, headers, content-type)
3. Group responses by endpoint patterns
4. Create normalized response snapshots
5. Save API snapshots as JSON files

Expected Result:
- API responses captured during test execution
- Response patterns properly normalized
- Endpoint groups identified and stored
- Contract consistency validated

TestRail Case ID: Mapped to test_api_response_snapshots''',
                'priority': 3,
                'type_id': 1  # Automated test
            },
            {
                'title': 'Component Snapshots - UI Components',
                'description': '''Individual UI component visual testing for design consistency validation.
                
Test Steps:
1. Navigate to pages containing target components
2. Locate specific UI components (forms, navigation, tables, KPIs)
3. Capture isolated screenshots of each component
4. Store component screenshots in organized structure

Expected Result:
- Individual component screenshots captured
- Components properly isolated from page context
- Screenshots saved with descriptive naming
- Component consistency validated

TestRail Case ID: Mapped to test_component_snapshots''',
                'priority': 2,
                'type_id': 1  # Automated test
            },
            {
                'title': 'Snapshot Comparison Workflow',
                'description': '''Validation of the snapshot comparison and workflow process.
                
Test Steps:
1. Capture initial baseline snapshot
2. Simulate page changes (scroll, interact)
3. Capture modified state snapshot
4. Reset page to original state
5. Capture final snapshot for comparison

Expected Result:
- Workflow process executes successfully
- Different states properly captured
- Change detection mechanisms working
- Comparison process validated

TestRail Case ID: Mapped to test_snapshot_comparison_workflow''',
                'priority': 2,
                'type_id': 1  # Automated test
            }
        ]
        
        created_cases = []
        
        for test_case in snapshot_tests:
            case_data = {
                'title': test_case['title'],
                'section_id': self.new_section_id,
                'template_id': 1,  # Test Case (Steps)
                'type_id': test_case['type_id'],
                'priority_id': test_case['priority'],
                'custom_steps_separated': [
                    {
                        'content': test_case['description'],
                        'expected': 'Test executes successfully with all snapshots captured and validated'
                    }
                ]
            }
            
            result = self.config._send_request('POST', f'add_case/{self.new_section_id}', case_data)
            if result:
                case_id = result['id']
                created_cases.append({
                    'title': test_case['title'],
                    'case_id': case_id,
                    'testrail_id': f"C{case_id}"
                })
                print(f"✅ Created test case: {test_case['title']} (C{case_id})")
                time.sleep(0.5)  # Prevent rate limiting
            else:
                print(f"❌ Failed to create test case: {test_case['title']}")
        
        return created_cases
    
    def generate_conftest_mappings(self, created_cases):
        """Generate the conftest.py mappings for the new test cases"""
        print("\n🔧 Generating conftest.py mappings...")
        
        # Create mapping dictionary
        test_method_mappings = {
            'Visual Snapshots - Key Application Pages': 'test_visual_snapshots_key_pages',
            'DOM Snapshots - Critical Page Elements': 'test_dom_snapshots_critical_elements',
            'API Response Snapshots': 'test_api_response_snapshots',
            'Component Snapshots - UI Components': 'test_component_snapshots',
            'Snapshot Comparison Workflow': 'test_snapshot_comparison_workflow'
        }
        
        mappings = {}
        for case in created_cases:
            method_name = test_method_mappings.get(case['title'])
            if method_name:
                mappings[method_name] = case['case_id']
        
        # Save mappings to file
        mappings_data = {
            'section_id': self.new_section_id,
            'section_name': '📸 Snapshot Regression',
            'test_cases': created_cases,
            'conftest_mappings': mappings,
            'created_at': datetime.now().isoformat()
        }
        
        with open('snapshot_testrail_mappings.json', 'w') as f:
            json.dump(mappings_data, f, indent=2)
        
        print(f"💾 Saved mappings to: snapshot_testrail_mappings.json")
        return mappings
    
    def print_conftest_update(self, mappings):
        """Print the conftest.py update instructions"""
        print("\n📝 Update conftest.py with these mappings:")
        print("="*60)
        print("# Replace the existing snapshot test mappings with:")
        print()
        print("        # Snapshot Tests")
        for method_name, case_id in mappings.items():
            print(f"        '{method_name}': {case_id},  # C{case_id}")
        print()
        print("="*60)
    
    def run(self):
        """Execute the complete process"""
        print("🚀 Adding Snapshot Tests to TestRail Suite")
        print(f"📋 Target Suite ID: {self.suite_id}")
        print(f"🎯 Project ID: {self.project_id}")
        
        # Step 1: Add section
        if not self.add_snapshot_section():
            print("❌ Failed to create section. Exiting.")
            return False
        
        # Step 2: Add test cases
        created_cases = self.add_snapshot_test_cases()
        if not created_cases:
            print("❌ No test cases were created. Exiting.")
            return False
        
        # Step 3: Generate mappings
        mappings = self.generate_conftest_mappings(created_cases)
        
        # Step 4: Print update instructions
        self.print_conftest_update(mappings)
        
        # Summary
        print(f"\n🎉 Successfully added snapshot tests to TestRail!")
        print(f"   📸 Section: 📸 Snapshot Regression (ID: {self.new_section_id})")
        print(f"   📝 Test Cases: {len(created_cases)}")
        print(f"   🗂️ Suite: {self.suite_id}")
        print(f"   💾 Mappings saved: snapshot_testrail_mappings.json")
        
        return True

def main():
    """Main execution function"""
    adder = SnapshotTestsAdder()
    success = adder.run()
    
    if success:
        print("\n✅ Snapshot tests successfully added to TestRail!")
        print("📚 Next steps:")
        print("   1. Update tests/conftest.py with the new mappings (shown above)")
        print("   2. Run snapshot tests to verify TestRail integration")
        print("   3. Review test cases in TestRail web interface")
    else:
        print("\n❌ Failed to add snapshot tests to TestRail")
        sys.exit(1)

if __name__ == "__main__":
    main() 