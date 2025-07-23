#!/usr/bin/env python3
"""
Create Complete conftest.py TestRail Mappings
Maps ALL test function names to the corresponding TestRail case IDs from the new suite
"""

import json
import re
import os

def load_mapping_file():
    """Load the mapping file with all TestRail cases"""
    mapping_file = 'new_testrail_suite_mappings.json'
    with open(mapping_file, 'r') as f:
        return json.load(f)

def create_comprehensive_mappings():
    """Create comprehensive test function to TestRail case mappings"""
    mapping_data = load_mapping_file()
    case_mappings = mapping_data['case_mappings']
    
    # Comprehensive mapping of test function names to TestRail case titles
    test_mappings = {
        # API Tests (C7936-C7946)
        'test_get_journal_entries_valid_date_format_request': 'GET Journal Entries - Valid Date Format',
        'test_get_journal_entries_invalid_date_format_request': 'GET Journal Entries - Invalid Date Format',
        'test_create_journal_entry_valid_date_format': 'POST Create Journal Entry - Valid Date Format',
        'test_create_journal_entry_invalid_date_format': 'POST Create Journal Entry - Invalid Date Format',
        'test_get_bank_uploaded_files_date_format': 'GET Bank Uploaded Files - Date Format',
        'test_get_bank_transactions_data_date_format': 'GET Bank Transactions Data - Date Format',
        'test_get_entity_documents_date_format': 'GET Entity Documents - Date Format',
        'test_get_accounting_uploaded_files_date_format': 'GET Accounting Uploaded Files - Date Format',
        'test_all_endpoints_reject_invalid_date_formats': 'All Endpoints Reject Invalid Date Formats',
        'test_date_format_consistency_across_endpoints': 'Date Format Consistency Across Endpoints',
        'test_date_format_validation_demo': 'Date Format Validation Demo',
        
        # Authentication & Login Tests (C7947-C7949)
        'test_login': 'Basic Login Functionality',
        'test_scenario_1_valid_login': 'Valid Login Scenario with 2FA',
        'test_scenario_2_logout_user': 'Login then Logout Workflow',
        
        # Navigation Tests (C7950-C7960)
        'test_tab_navigation[text=Home-HomePage]': 'Navigate to Home Page',
        'test_tab_navigation[text=Vizion AI-VizionAIPage]': 'Navigate to Vizion AI Page',
        'test_tab_navigation[text=Reconciliation-ReconciliationPage]': 'Navigate to Reconciliation Page',
        'test_tab_navigation[text=Ledger-LedgerPage]': 'Navigate to Ledger Page',
        'test_tab_navigation[text=BI Analysis-BIAnalysisPage]': 'Navigate to BI Analysis Page',
        'test_tab_navigation[text=Connections-ConnectionPage]': 'Navigate to Connections Page',
        'test_tabs_navigation_single_login': 'All Tabs Navigation in Single Session',
        'test_tab_navigation_with_entity[text=Home-HomePage]': 'Navigation with Entity Context',
        'test_tab_navigation_with_entity[text=Vizion AI-VizionAIPage]': 'Navigation with Entity Context',
        'test_tab_navigation_with_entity[text=Reconciliation-ReconciliationPage]': 'Navigation with Entity Context',
        'test_tab_navigation_with_entity[text=Ledger-LedgerPage]': 'Navigation with Entity Context',
        'test_tab_navigation_with_entity[text=BI Analysis-BIAnalysisPage]': 'Navigation with Entity Context',
        'test_tab_navigation_with_entity[text=Connections-ConnectionPage]': 'Navigation with Entity Context',
        'test_entity_selection_validation': 'Entity Selection Validation',
        'test_tabs_navigation_single_login_with_entity': 'Single Login with Entity Selection',
        
        # Logout Tests (C7961-C7965)
        'test_logout_after_2fa_login': 'Logout After 2FA Authentication',
        'test_logout_direct_method': 'Direct Logout Button Method',
        'test_logout_via_menu': 'Logout via User Menu',
        'test_logout_keyboard_method': 'Logout via Keyboard Shortcuts',
        'test_logout_comprehensive_workflow': 'Comprehensive Logout Workflow',
        
        # Bank Operations Tests (C7966-C7986)
        'test_verify_bank_page_loads': 'Bank Page Loading Verification',
        'test_verify_transactions_display': 'Bank Transactions Display',
        'test_bank_page_responsiveness': 'Bank Page Performance',
        'test_empty_state_handling': 'Empty State Handling',
        'test_bank_account_selection': 'Bank Account Selection',
        'test_check_bank_account_list_display': 'Bank Account List Display',
        'test_view_account_balances': 'Account Balance Viewing',
        'test_account_settings_configuration': 'Account Settings Configuration',
        'test_transaction_filtering_by_date': 'Transaction Date Range Filtering',
        'test_transaction_search': 'Transaction Search Functionality',
        'test_view_bank_transactions_list': 'Transaction List Viewing',
        'test_sort_transactions_by_columns': 'Transaction Column Sorting',
        'test_transaction_action_buttons': 'Transaction Action Buttons',
        'test_verify_upload_area': 'Bank Statement Upload Area',
        'test_upload_statement_file_validation': 'Statement File Format Validation',
        'test_handle_duplicate_uploads': 'Duplicate Upload Handling',
        'test_process_uploaded_statements': 'Uploaded Statement Processing',
        'test_reconciliation_status_display': 'Reconciliation Status Display',
        'test_transaction_reconciliation': 'Transaction Reconciliation Process',
        'test_handle_unmatched_transactions': 'Unmatched Transaction Handling',
        'test_complete_bank_workflow': 'Complete Bank Reconciliation Workflow',
        
        # Payables Operations Tests (C7987-C8010)
        'test_verify_invoice_list_is_displayed': 'Invoice List Display Verification',
        'test_upload_invoice_file': 'Valid Invoice File Upload',
        'test_upload_invalid_file_type': 'Invalid File Type Upload Handling',
        'test_upload_duplicate_invoice': 'Duplicate Invoice Upload Prevention',
        'test_view_invoice_in_new_view': 'Invoice Viewing in New Tab',
        'test_payables_menu_operations': 'Menu Operations Testing',
        'test_payables_form_validation': 'Form Validation Testing',
        'test_menu_options_for_new_status': 'New Status Menu Options',
        'test_menu_options_for_matched_status': 'Matched Status Menu Options',
        'test_menu_options_for_reconciled_status': 'Reconciled Status Menu Options',
        'test_open_edit_popup_layout': 'Edit Popup Layout Verification',
        'test_mandatory_validation': 'Mandatory Field Validation',
        'test_line_totals_equal_before_validation': 'Line Totals Validation',
        'test_verify_je_amount_and_description': 'Journal Entry Fields Verification',
        'test_gl_account_dropdown': 'GL Account Dropdown Search',
        'test_recognition_timing_single_date': 'Single Date Recognition Timing',
        'test_recognition_timing_default': 'Default Period Recognition Timing',
        'test_record_invoice_and_status': 'Invoice Recording and Status Change',
        'test_show_journal_entry_for_record': 'Journal Entry Display for Recorded Invoice',
        'test_payables_edit_delete_buttons': 'Edit and Delete Button Functionality',
        'test_payables_status_dropdowns': 'Status Dropdown Operations',
        'test_payables_search_filter_options': 'Search and Filter Options',
        'test_delete_invoice_dialog': 'Delete Confirmation Dialog',
        'test_attempt_to_delete_invoice': 'Delete Attempt Validation',
        
        # Ledger Operations Tests (C8011-C8048)
        # Traditional GL Tests
        'test_verify_ledger_page_loads': 'Ledger Page Loading Verification',
        'test_verify_general_ledger_entries_display': 'General Ledger Entries Display',
        'test_verify_account_hierarchy_display': 'Chart of Accounts Display',
        'test_ledger_page_responsiveness': 'Ledger Page Performance',
        'test_chart_of_accounts_navigation': 'Chart of Accounts Navigation',
        'test_account_selection_functionality': 'Account Selection Functionality',
        'test_account_balance_display': 'Account Balance Display',
        'test_account_details_popup': 'Account Details Popup',
        'test_journal_entries_filtering_by_date': 'Journal Entries Date Filtering',
        'test_journal_entries_filtering_by_account': 'Journal Entries Account Filtering',
        'test_journal_entries_search': 'Journal Entries Search',
        'test_transaction_drill_down': 'Transaction Drill Down',
        'test_trial_balance_display': 'Trial Balance Report Display',
        'test_account_activity_report': 'Account Activity Report',
        'test_export_functionality': 'Data Export Functionality',
        'test_period_selection': 'Accounting Period Selection',
        'test_manual_journal_entry_creation': 'Manual Journal Entry Creation',
        'test_journal_entry_validation': 'Journal Entry Validation Rules',
        'test_journal_entry_posting': 'Journal Entry Posting',
        'test_journal_entry_reversal': 'Journal Entry Reversal',
        'test_bank_reconciliation_integration': 'Bank Reconciliation Integration',
        'test_payables_integration': 'Payables Module Integration',
        'test_complete_ledger_workflow': 'Complete Ledger Workflow',
        
        # Dashboard Tests
        'test_verify_ledger_dashboard_loads': 'Financial Dashboard Loading',
        'test_verify_financial_kpis_display': 'Financial KPIs Display',
        'test_verify_filter_controls_display': 'Dashboard Filter Controls',
        'test_get_total_income_value': 'Total Income Value Retrieval',
        'test_get_gross_profit_value': 'Gross Profit Value Retrieval',
        'test_get_all_kpi_values': 'All KPI Values Retrieval',
        'test_kpi_data_consistency': 'KPI Data Consistency',
        'test_period_selection_functionality': 'Period Selection Functionality',
        'test_date_preset_functionality': 'Date Preset Functionality',
        'test_period_filter_impact': 'Period Filter Impact Testing',
        'test_no_data_states_handling': 'No Data States Handling',
        'test_dashboard_url_parameters': 'Dashboard URL Parameters',
        'test_complete_dashboard_workflow': 'Complete Dashboard Workflow',
        'test_dashboard_responsiveness': 'Dashboard Performance Testing',
        'test_dashboard_edge_cases': 'Dashboard Edge Cases',
        
        # Security Regression Tests (C8049-C8055)
        'test_invalid_login_attempts': 'Invalid Login Attempts Protection',
        'test_session_timeout_handling': 'Session Timeout Management',
        'test_sql_injection_prevention': 'SQL Injection Prevention',
        'test_xss_prevention': 'Cross-Site Scripting (XSS) Prevention',
        'test_password_requirements': 'Password Requirements Validation',
        'test_csrf_protection': 'CSRF Token Validation',
        'test_secure_headers': 'HTTP Security Headers Verification',
        
        # Performance Regression Tests (C8056-C8061)
        'test_page_load_performance': 'Page Load Performance Testing',
        'test_memory_usage_monitoring': 'Memory Usage Monitoring',
        'test_concurrent_user_simulation': 'Concurrent User Simulation',
        'test_api_response_times': 'API Response Time Monitoring',
        'test_large_dataset_handling': 'Large Dataset Handling Performance',
        
        # Browser Compatibility Tests (C8062-C8065)
        'test_mobile_viewport_compatibility': 'Mobile Viewport Compatibility',
        'test_responsive_design_elements': 'Responsive Design Elements',
        'test_touch_interface_compatibility': 'Touch Interface Compatibility',
        'test_print_stylesheet_compatibility': 'Print Stylesheet Compatibility',
    }
    
    # Convert to case IDs
    final_mappings = {}
    unmapped_tests = []
    
    for test_name, case_title in test_mappings.items():
        if case_title in case_mappings:
            final_mappings[test_name] = case_mappings[case_title]
        else:
            unmapped_tests.append(f"{test_name} -> {case_title}")
    
    if unmapped_tests:
        print(f"⚠️ {len(unmapped_tests)} tests could not be mapped:")
        for unmapped in unmapped_tests[:5]:  # Show first 5
            print(f"   {unmapped}")
        if len(unmapped_tests) > 5:
            print(f"   ... and {len(unmapped_tests)-5} more")
    
    print(f"✅ Successfully mapped {len(final_mappings)} test functions to TestRail cases")
    return final_mappings

def update_conftest_with_complete_mappings():
    """Update conftest.py with ALL test mappings"""
    mappings = create_comprehensive_mappings()
    
    conftest_path = '../tests/conftest.py'
    
    # Read current conftest.py
    with open(conftest_path, 'r') as f:
        content = f.read()
    
    # Create the new mapping section
    mapping_lines = []
    mapping_lines.append("        # ===== COMPLETE COMPREHENSIVE SUITE MAPPINGS =====")
    mapping_lines.append("        # Suite ID: 139")
    mapping_lines.append(f"        # Total Cases Mapped: {len(mappings)}")
    mapping_lines.append("")
    
    # Group by category and add mappings
    categories = {
        'API Tests': [],
        'Authentication Tests': [],
        'Navigation Tests': [],
        'Logout Tests': [],
        'Bank Tests': [],
        'Payables Tests': [],
        'Ledger Tests': [],
        'Security Tests': [],
        'Performance Tests': [],
        'Compatibility Tests': []
    }
    
    for test_name, case_id in sorted(mappings.items()):
        if any(x in test_name.lower() for x in ['api', 'date_format', 'journal_entries', 'endpoint']):
            categories['API Tests'].append((test_name, case_id))
        elif any(x in test_name.lower() for x in ['login', 'scenario']):
            categories['Authentication Tests'].append((test_name, case_id))
        elif any(x in test_name.lower() for x in ['navigation', 'tab_', 'entity']):
            categories['Navigation Tests'].append((test_name, case_id))
        elif 'logout' in test_name.lower():
            categories['Logout Tests'].append((test_name, case_id))
        elif 'bank' in test_name.lower():
            categories['Bank Tests'].append((test_name, case_id))
        elif 'payables' in test_name.lower() or 'invoice' in test_name.lower():
            categories['Payables Tests'].append((test_name, case_id))
        elif any(x in test_name.lower() for x in ['ledger', 'dashboard', 'kpi', 'chart_of_accounts']):
            categories['Ledger Tests'].append((test_name, case_id))
        elif any(x in test_name.lower() for x in ['security', 'sql', 'xss', 'csrf']):
            categories['Security Tests'].append((test_name, case_id))
        elif any(x in test_name.lower() for x in ['performance', 'memory', 'load']):
            categories['Performance Tests'].append((test_name, case_id))
        elif any(x in test_name.lower() for x in ['mobile', 'responsive', 'compatibility']):
            categories['Compatibility Tests'].append((test_name, case_id))
        else:
            categories['API Tests'].append((test_name, case_id))  # Default fallback
    
    for category, tests in categories.items():
        if tests:
            mapping_lines.append(f"        # {category}")
            for test_name, case_id in tests:
                mapping_lines.append(f"        '{test_name}': {case_id},  # C{case_id}")
            mapping_lines.append("")
    
    new_mapping_section = "\n".join(mapping_lines)
    
    # Find and replace the case_mapping dictionary
    pattern = r'(case_mapping\s*=\s*\{)(.*?)(\s*\})'
    match = re.search(pattern, content, re.DOTALL)
    
    if match:
        # Create backup
        backup_path = conftest_path + '.backup_complete'
        with open(backup_path, 'w') as f:
            f.write(content)
        print(f"✅ Created backup: {backup_path}")
        
        # Replace mapping
        new_content = content[:match.start()] + f"case_mapping = {{\n{new_mapping_section}        " + content[match.end():]
        
        with open(conftest_path, 'w') as f:
            f.write(new_content)
        
        print(f"✅ Updated conftest.py with {len(mappings)} complete test case mappings")
        return True
    else:
        print("❌ Could not find case_mapping dictionary in conftest.py")
        return False

def main():
    """Main execution"""
    print("🔄 Creating complete TestRail mappings for ALL tests...")
    
    if update_conftest_with_complete_mappings():
        print("\n🎉 Complete mappings created successfully!")
        print("Now ALL your tests will be mapped to TestRail cases when you run:")
        print("TESTRAIL_ENABLED=true python -m pytest tests/ -v --headless")
    else:
        print("\n❌ Failed to create complete mappings")

if __name__ == "__main__":
    main() 