#!/usr/bin/env python3
"""
Update Receivables TestRail Case IDs Script
Updates all TestRail case references in receivables tests to use correct C8066-C8078 range
"""

import re

# Mapping of test function names to TestRail case IDs
CASE_MAPPING = {
    'test_verify_receivable_list_is_displayed': '8066',
    'test_upload_receivable_file': '8067',
    'test_upload_invalid_file_type': '8068',
    'test_upload_duplicate_receivable': '8069',
    'test_receivables_edit_delete_buttons': '8070',
    'test_receivables_status_dropdowns': '8071',
    'test_receivables_search_filter_options': '8072',
    'test_receivables_menu_operations': '8072',
    'test_open_edit_popup_layout': '8073',
    'test_mandatory_validation': '8073',
    'test_receivables_form_validation': '8073',
    'test_line_totals_equal_before_validation': '8074',
    'test_gl_account_dropdown': '8074',
    'test_recognition_timing_single_date': '8074',
    'test_recognition_timing_default': '8074',
    'test_record_receivable_and_status': '8075',
    'test_show_journal_entry_for_record': '8075',
    'test_verify_je_amount_and_description': '8075',
    'test_delete_receivable_dialog': '8076',
    'test_attempt_to_delete_receivable': '8076',
    'test_view_receivable_in_new_view': '8077',
    'test_menu_options_for_new_status': '8078',
    'test_menu_options_for_matched_status': '8078',
    'test_menu_options_for_reconciled_status': '8078',
}

file_path = '/Users/sharonhoffman/Desktop/Automation/playwright_python_framework/tests/e2e/reconciliation/receivables/test_complete_receivables_operations.py'

# Read the file
with open(file_path, 'r') as f:
    content = f.read()

# Replace old case IDs with new ones in docstrings
replacements = [
    (r'TestRail Case 8015:', 'TestRail Case C8068:'),
    (r'TestRail Case 8016:', 'TestRail Case C8069:'),
    (r'TestRail Case 8017:', 'TestRail Case C8070:'),
    (r'TestRail Case 8018:', 'TestRail Case C8071:'),
    (r'TestRail Case 8019:', 'TestRail Case C8072:'),
    (r'TestRail Case 8020:', 'TestRail Case C8073:'),
    (r'TestRail Case 8021:', 'TestRail Case C8073:'),
    (r'TestRail Case 8022:', 'TestRail Case C8074:'),
    (r'TestRail Case 8023:', 'TestRail Case C8074:'),
    (r'TestRail Case 8024:', 'TestRail Case C8074:'),
    (r'TestRail Case 8025:', 'TestRail Case C8074:'),
    (r'TestRail Case 8026:', 'TestRail Case C8075:'),
    (r'TestRail Case 8027:', 'TestRail Case C8075:'),
    (r'TestRail Case 8028:', 'TestRail Case C8075:'),
    (r'TestRail Case 8029:', 'TestRail Case C8076:'),
    (r'TestRail Case 8030:', 'TestRail Case C8076:'),
    (r'TestRail Case 8031:', 'TestRail Case C8077:'),
    (r'TestRail Case 8032:', 'TestRail Case C8078:'),
    (r'TestRail Case 8033:', 'TestRail Case C8078:'),
    (r'TestRail Case 8034:', 'TestRail Case C8078:'),
]

for old, new in replacements:
    content = re.sub(old, new, content)

# Write the file back
with open(file_path, 'w') as f:
    f.write(content)

print("✅ Updated all TestRail case IDs in test_complete_receivables_operations.py")
print("   Old range: 8011-8034")
print("   New range: C8066-C8078")
print(f"   Total replacements: {len(replacements)}")

