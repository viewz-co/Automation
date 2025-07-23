#!/usr/bin/env python3
"""
Update conftest.py with New TestRail Mappings
Updates the TESTRAIL_CASE_IDS mapping in conftest.py with new suite case IDs
"""

import json
import re
import os
import sys

def load_mapping_file(mapping_file='new_testrail_suite_mappings.json'):
    """Load the mapping file created by the suite creator"""
    if not os.path.exists(mapping_file):
        print(f"❌ Mapping file not found: {mapping_file}")
        print("Please run create_comprehensive_testrail_suite.py first")
        return None
    
    with open(mapping_file, 'r') as f:
        return json.load(f)

def update_conftest_file(mapping_data):
    """Update the conftest.py file with new TestRail case mappings"""
    conftest_path = '../tests/conftest.py'
    
    if not os.path.exists(conftest_path):
        print(f"❌ conftest.py not found at: {conftest_path}")
        return False
    
    # Read current conftest.py
    with open(conftest_path, 'r') as f:
        content = f.read()
    
    # Extract the new mappings
    framework_mappings = mapping_data.get('framework_mappings', {}).get('test_function_to_case_id', {})
    suite_id = mapping_data.get('suite_info', {}).get('suite_id')
    
    if not framework_mappings:
        print("❌ No framework mappings found in mapping file")
        return False
    
    # Create the new case mapping section
    new_mapping_lines = []
    new_mapping_lines.append("        # ===== NEW COMPREHENSIVE SUITE MAPPINGS =====")
    new_mapping_lines.append(f"        # Suite ID: {suite_id}")
    new_mapping_lines.append(f"        # Total Cases: {len(framework_mappings)}")
    new_mapping_lines.append("")
    
    # Group mappings by category
    categories = {
        'API Tests': [],
        'Login Tests': [],
        'Navigation Tests': [],
        'Logout Tests': [],
        'Bank Tests': [],
        'Payables Tests': [],
        'Ledger Tests': [],
        'Security Tests': [],
        'Performance Tests': [],
        'Compatibility Tests': []
    }
    
    for test_name, case_id in framework_mappings.items():
        if case_id is None:
            continue
            
        if 'api' in test_name.lower() or 'date_format' in test_name:
            categories['API Tests'].append((test_name, case_id))
        elif 'login' in test_name.lower():
            categories['Login Tests'].append((test_name, case_id))
        elif 'navigation' in test_name.lower() or 'tab_' in test_name:
            categories['Navigation Tests'].append((test_name, case_id))
        elif 'logout' in test_name.lower():
            categories['Logout Tests'].append((test_name, case_id))
        elif 'bank' in test_name.lower():
            categories['Bank Tests'].append((test_name, case_id))
        elif 'payables' in test_name.lower():
            categories['Payables Tests'].append((test_name, case_id))
        elif 'ledger' in test_name.lower():
            categories['Ledger Tests'].append((test_name, case_id))
        elif 'security' in test_name.lower():
            categories['Security Tests'].append((test_name, case_id))
        elif 'performance' in test_name.lower():
            categories['Performance Tests'].append((test_name, case_id))
        elif 'compatibility' in test_name.lower():
            categories['Compatibility Tests'].append((test_name, case_id))
    
    # Add categorized mappings
    for category, mappings in categories.items():
        if mappings:
            new_mapping_lines.append(f"        # {category}")
            for test_name, case_id in sorted(mappings):
                new_mapping_lines.append(f"        '{test_name}': {case_id},  # C{case_id}")
            new_mapping_lines.append("")
    
    new_mapping_section = "\n".join(new_mapping_lines)
    
    # Find the case_mapping dictionary in conftest.py
    pattern = r'(case_mapping\s*=\s*\{)(.*?)(\s*\})'
    match = re.search(pattern, content, re.DOTALL)
    
    if not match:
        print("❌ Could not find case_mapping dictionary in conftest.py")
        return False
    
    # Replace the existing mapping
    new_content = content[:match.start()] + f"case_mapping = {{\n{new_mapping_section}        " + content[match.end():]
    
    # Create backup
    backup_path = conftest_path + '.backup'
    with open(backup_path, 'w') as f:
        f.write(content)
    print(f"✅ Created backup: {backup_path}")
    
    # Write updated conftest.py
    with open(conftest_path, 'w') as f:
        f.write(new_content)
    
    print(f"✅ Updated conftest.py with {len(framework_mappings)} new test case mappings")
    return True

def update_suite_id(mapping_data):
    """Update the suite ID in testrail_config.py"""
    config_path = '../configs/testrail_config.py'
    suite_id = mapping_data.get('suite_info', {}).get('suite_id')
    
    if not os.path.exists(config_path) or not suite_id:
        print("⚠️ Could not update suite ID in testrail_config.py")
        return False
    
    with open(config_path, 'r') as f:
        content = f.read()
    
    # Update the default suite ID
    updated_content = re.sub(
        r"self\.suite_id = int\(os\.getenv\('TESTRAIL_SUITE_ID', '\d+'\)\)",
        f"self.suite_id = int(os.getenv('TESTRAIL_SUITE_ID', '{suite_id}'))",
        content
    )
    
    if updated_content != content:
        with open(config_path, 'w') as f:
            f.write(updated_content)
        print(f"✅ Updated default suite ID to {suite_id} in testrail_config.py")
        return True
    else:
        print("⚠️ Could not find suite ID pattern to update in testrail_config.py")
        return False

def main():
    """Main execution function"""
    print("🔄 Updating conftest.py with new TestRail mappings...")
    
    # Load mapping data
    mapping_data = load_mapping_file()
    if not mapping_data:
        return
    
    # Update conftest.py
    if update_conftest_file(mapping_data):
        print("✅ conftest.py updated successfully")
    else:
        print("❌ Failed to update conftest.py")
        return
    
    # Update suite ID in config
    update_suite_id(mapping_data)
    
    print("\n🎉 Update complete!")
    print("You can now run tests with the new TestRail suite:")
    print("TESTRAIL_ENABLED=true python -m pytest tests/ -v --headless")

if __name__ == "__main__":
    main() 