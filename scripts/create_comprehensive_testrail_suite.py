#!/usr/bin/env python3
"""
Create Comprehensive TestRail Test Suite
Creates a complete test suite in TestRail with all 137+ tests from the Playwright framework
Organizes tests into logical sections and creates proper case mappings
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

class TestRailSuiteCreator:
    def __init__(self):
        self.config = TestRailConfig()
        self.project_id = self.config.project_id
        
        # Suite configuration
        self.suite_name = "Playwright Python Framework - Complete Test Suite"
        self.suite_description = """
        Comprehensive test suite for the Playwright Python automation framework.
        
        This suite includes:
        - API Tests (11 tests): Date format validation and endpoint testing
        - E2E Login/Authentication (3 tests): Login workflows and 2FA
        - E2E Navigation (11 tests): Tab navigation and entity selection
        - E2E Logout (5 tests): Multiple logout methods and workflows
        - E2E Bank Operations (21 tests): Complete bank reconciliation
        - E2E Payables Operations (25 tests): Invoice processing workflows
        - E2E Ledger Operations (44 tests): GL functionality and dashboard
        - Security Regression (7 tests): Security vulnerability testing
        - Performance Regression (6 tests): Performance monitoring
        - Browser Compatibility (4 tests): Cross-browser and device testing
        
        Total: 137+ comprehensive test cases
        Framework: Playwright + pytest + TestRail Integration
        Updated: """ + datetime.now().strftime("%Y-%m-%d")
        
        self.created_suite_id = None
        self.section_mappings = {}
        self.case_mappings = {}
        
    def create_test_suite(self):
        """Create the main test suite"""
        print("🚀 Creating comprehensive TestRail test suite...")
        
        data = {
            'name': self.suite_name,
            'description': self.suite_description
        }
        
        result = self.config._send_request('POST', f'add_suite/{self.project_id}', data)
        if result:
            self.created_suite_id = result['id']
            print(f"✅ Created test suite: {self.suite_name} (ID: {self.created_suite_id})")
            return True
        else:
            print("❌ Failed to create test suite")
            return False
    
    def create_sections(self):
        """Create organized sections within the test suite"""
        print("\n📂 Creating test suite sections...")
        
        sections = [
            {
                'name': '🌐 API Tests',
                'description': 'API endpoint testing including date format validation across all endpoints'
            },
            {
                'name': '🔐 Authentication & Login',
                'description': 'Login workflows, 2FA authentication, and session management'
            },
            {
                'name': '🧭 Navigation',
                'description': 'Tab navigation, entity selection, and page routing tests'
            },
            {
                'name': '🚪 Logout',
                'description': 'Logout functionality testing including multiple logout methods'
            },
            {
                'name': '🏦 Bank Operations',
                'description': 'Bank reconciliation, transaction management, file uploads, and account operations'
            },
            {
                'name': '💰 Payables Operations',
                'description': 'Invoice processing, payables workflows, form validation, and status management'
            },
            {
                'name': '📊 Ledger Operations',
                'description': 'General Ledger functionality, financial dashboard, KPI management, and reporting'
            },
            {
                'name': '🔐 Security Regression',
                'description': 'Security vulnerability testing including SQL injection, XSS, CSRF, and authentication security'
            },
            {
                'name': '⚡ Performance Regression',
                'description': 'Performance monitoring, load testing, memory usage, and response time validation'
            },
            {
                'name': '📱 Browser Compatibility',
                'description': 'Cross-browser testing, mobile compatibility, responsive design, and device testing'
            }
        ]
        
        for section in sections:
            data = {
                'suite_id': self.created_suite_id,
                'name': section['name'],
                'description': section['description']
            }
            
            result = self.config._send_request('POST', f'add_section/{self.project_id}', data)
            if result:
                section_id = result['id']
                self.section_mappings[section['name']] = section_id
                print(f"✅ Created section: {section['name']} (ID: {section_id})")
                time.sleep(0.5)  # Prevent rate limiting
            else:
                print(f"❌ Failed to create section: {section['name']}")
        
        return len(self.section_mappings) == len(sections)
    
    def create_test_cases(self):
        """Create all test cases organized by category"""
        print("\n📝 Creating test cases...")
        
        # Define all test cases organized by category
        test_cases = {
            '🌐 API Tests': [
                {'title': 'GET Journal Entries - Valid Date Format', 'description': 'Verify date format in GET /api/v2/accounting/getJournalEntries response', 'priority': 3},
                {'title': 'GET Journal Entries - Invalid Date Format', 'description': 'Test invalid date format rejection in journal entries endpoint', 'priority': 2},
                {'title': 'POST Create Journal Entry - Valid Date Format', 'description': 'Verify date format in POST /api/v2/accounting/createJournalEntry request', 'priority': 3},
                {'title': 'POST Create Journal Entry - Invalid Date Format', 'description': 'Test invalid date format in create journal entry request', 'priority': 2},
                {'title': 'GET Bank Uploaded Files - Date Format', 'description': 'Verify date format in GET /api/v2/banks/getBankUploadedFiles', 'priority': 2},
                {'title': 'GET Bank Transactions Data - Date Format', 'description': 'Verify date format in GET /api/v2/banks/getBankTransactionsData', 'priority': 2},
                {'title': 'GET Entity Documents - Date Format', 'description': 'Verify date format in GET /api/v2/docs/getEntityDocuments', 'priority': 2},
                {'title': 'GET Accounting Uploaded Files - Date Format', 'description': 'Verify date format in GET /api/v2/accounting/getAccountingUploadedFiles', 'priority': 2},
                {'title': 'All Endpoints Reject Invalid Date Formats', 'description': 'Cross-endpoint date format validation testing', 'priority': 2},
                {'title': 'Date Format Consistency Across Endpoints', 'description': 'Verify consistent YYYY-MM-DD format across all API endpoints', 'priority': 2},
                {'title': 'Date Format Validation Demo', 'description': 'Demonstration of date validation capabilities', 'priority': 1}
            ],
            
            '🔐 Authentication & Login': [
                {'title': 'Basic Login Functionality', 'description': 'Test basic login with username and password', 'priority': 4},
                {'title': 'Valid Login Scenario with 2FA', 'description': 'Complete login workflow including 2FA authentication', 'priority': 4},
                {'title': 'Login then Logout Workflow', 'description': 'End-to-end authentication workflow from login to logout', 'priority': 3}
            ],
            
            '🧭 Navigation': [
                {'title': 'Navigate to Home Page', 'description': 'Test navigation to Home page and verify loading', 'priority': 3},
                {'title': 'Navigate to Vizion AI Page', 'description': 'Test navigation to Vizion AI page and verify loading', 'priority': 2},
                {'title': 'Navigate to Reconciliation Page', 'description': 'Test navigation to Reconciliation page and verify loading', 'priority': 3},
                {'title': 'Navigate to Ledger Page', 'description': 'Test navigation to Ledger page and verify loading', 'priority': 3},
                {'title': 'Navigate to BI Analysis Page', 'description': 'Test navigation to BI Analysis page and verify loading', 'priority': 2},
                {'title': 'Navigate to Connections Page', 'description': 'Test navigation to Connections page and verify loading', 'priority': 2},
                {'title': 'All Tabs Navigation in Single Session', 'description': 'Test all tab navigation in a single login session', 'priority': 3},
                {'title': 'Navigation with Entity Context', 'description': 'Test navigation functionality with entity selection context', 'priority': 2},
                {'title': 'Entity Selection Validation', 'description': 'Validate entity selection functionality and persistence', 'priority': 2},
                {'title': 'Single Login with Entity Selection', 'description': 'Complete workflow: login, entity selection, navigation', 'priority': 3},
                {'title': 'Menu Pinning and Navigation', 'description': 'Test menu pinning functionality and navigation persistence', 'priority': 1}
            ],
            
            '🚪 Logout': [
                {'title': 'Logout After 2FA Authentication', 'description': 'Test logout functionality after 2FA login process', 'priority': 3},
                {'title': 'Direct Logout Button Method', 'description': 'Test logout using direct logout button', 'priority': 3},
                {'title': 'Logout via User Menu', 'description': 'Test logout functionality through user menu', 'priority': 3},
                {'title': 'Logout via Keyboard Shortcuts', 'description': 'Test logout using keyboard shortcuts and hotkeys', 'priority': 1},
                {'title': 'Comprehensive Logout Workflow', 'description': 'Test complete logout workflow with all available methods', 'priority': 2}
            ],
            
            '🏦 Bank Operations': [
                {'title': 'Bank Page Loading Verification', 'description': 'Verify bank page loads correctly with all elements', 'priority': 3},
                {'title': 'Bank Transactions Display', 'description': 'Verify transaction table structure and data display', 'priority': 3},
                {'title': 'Bank Page Performance', 'description': 'Test bank page responsiveness and loading times', 'priority': 2},
                {'title': 'Empty State Handling', 'description': 'Test bank page behavior with no data or empty states', 'priority': 2},
                {'title': 'Bank Account Selection', 'description': 'Test selection of different bank accounts', 'priority': 3},
                {'title': 'Bank Account List Display', 'description': 'Verify bank account list is properly displayed', 'priority': 2},
                {'title': 'Account Balance Viewing', 'description': 'Test viewing of account balances and totals', 'priority': 3},
                {'title': 'Account Settings Configuration', 'description': 'Test bank account settings and configuration options', 'priority': 2},
                {'title': 'Transaction Date Range Filtering', 'description': 'Test filtering transactions by date range', 'priority': 3},
                {'title': 'Transaction Search Functionality', 'description': 'Test searching transactions by description/amount', 'priority': 3},
                {'title': 'Transaction List Viewing', 'description': 'Test viewing and scrolling through transaction lists', 'priority': 2},
                {'title': 'Transaction Column Sorting', 'description': 'Test sorting transactions by different columns', 'priority': 2},
                {'title': 'Transaction Action Buttons', 'description': 'Test transaction-specific action buttons and menus', 'priority': 2},
                {'title': 'Bank Statement Upload Area', 'description': 'Verify bank statement upload area and functionality', 'priority': 3},
                {'title': 'Statement File Format Validation', 'description': 'Test validation of uploaded file formats (CSV, Excel, OFX)', 'priority': 3},
                {'title': 'Duplicate Upload Handling', 'description': 'Test handling of duplicate file uploads', 'priority': 2},
                {'title': 'Uploaded Statement Processing', 'description': 'Test processing and parsing of uploaded statements', 'priority': 3},
                {'title': 'Reconciliation Status Display', 'description': 'Test display of transaction reconciliation status', 'priority': 3},
                {'title': 'Transaction Reconciliation Process', 'description': 'Test matching transactions with journal entries', 'priority': 4},
                {'title': 'Unmatched Transaction Handling', 'description': 'Test handling of unmatched transactions', 'priority': 3},
                {'title': 'Complete Bank Reconciliation Workflow', 'description': 'End-to-end bank reconciliation workflow testing', 'priority': 4}
            ],
            
            '💰 Payables Operations': [
                {'title': 'Invoice List Display Verification', 'description': 'Verify invoice list is properly displayed with all columns', 'priority': 3},
                {'title': 'Valid Invoice File Upload', 'description': 'Test uploading valid invoice files (PDF, images)', 'priority': 3},
                {'title': 'Invalid File Type Upload Handling', 'description': 'Test handling of invalid file types during upload', 'priority': 3},
                {'title': 'Duplicate Invoice Upload Prevention', 'description': 'Test prevention and handling of duplicate invoice uploads', 'priority': 2},
                {'title': 'Invoice Viewing in New Tab', 'description': 'Test opening and viewing invoices in new browser tabs', 'priority': 2},
                {'title': 'Menu Operations Testing', 'description': 'Test all menu operations and context menus', 'priority': 2},
                {'title': 'Form Validation Testing', 'description': 'Test form validation rules and error handling', 'priority': 3},
                {'title': 'New Status Menu Options', 'description': 'Test available menu options for invoices in New status', 'priority': 2},
                {'title': 'Matched Status Menu Options', 'description': 'Test available menu options for invoices in Matched status', 'priority': 2},
                {'title': 'Reconciled Status Menu Options', 'description': 'Test available menu options for invoices in Reconciled status', 'priority': 2},
                {'title': 'Edit Popup Layout Verification', 'description': 'Verify edit popup layout and all form elements', 'priority': 2},
                {'title': 'Mandatory Field Validation', 'description': 'Test validation of mandatory fields in edit forms', 'priority': 3},
                {'title': 'Line Totals Validation', 'description': 'Test validation that line totals equal before VAT amounts', 'priority': 3},
                {'title': 'Journal Entry Fields Verification', 'description': 'Verify journal entry amount and description fields are read-only', 'priority': 2},
                {'title': 'GL Account Dropdown Search', 'description': 'Test GL Account dropdown search and selection', 'priority': 2},
                {'title': 'Single Date Recognition Timing', 'description': 'Test recognition timing with single date option', 'priority': 2},
                {'title': 'Default Period Recognition Timing', 'description': 'Test recognition timing with deferred period option', 'priority': 2},
                {'title': 'Invoice Recording and Status Change', 'description': 'Test recording invoices and automatic status changes', 'priority': 4},
                {'title': 'Journal Entry Display for Recorded Invoice', 'description': 'Test showing journal entries for recorded invoices', 'priority': 3},
                {'title': 'Edit and Delete Button Functionality', 'description': 'Test edit and delete button functionality across statuses', 'priority': 2},
                {'title': 'Status Dropdown Operations', 'description': 'Test status dropdown changes and validations', 'priority': 2},
                {'title': 'Search and Filter Options', 'description': 'Test search and filtering options for invoice lists', 'priority': 2},
                {'title': 'Delete Confirmation Dialog', 'description': 'Test delete confirmation dialog actions and validation', 'priority': 2},
                {'title': 'Delete Attempt Validation', 'description': 'Test validation when attempting to delete recorded invoices', 'priority': 3}
            ],
            
            '📊 Ledger Operations': [
                # Traditional General Ledger Tests
                {'title': 'Ledger Page Loading Verification', 'description': 'Test that ledger page loads correctly with proper headings', 'priority': 4},
                {'title': 'General Ledger Entries Display', 'description': 'Test that GL entries/transactions are properly displayed', 'priority': 4},
                {'title': 'Chart of Accounts Display', 'description': 'Test chart of accounts hierarchy display', 'priority': 3},
                {'title': 'Ledger Page Performance', 'description': 'Test ledger page performance and loading times', 'priority': 2},
                {'title': 'Chart of Accounts Navigation', 'description': 'Test navigation through chart of accounts hierarchy', 'priority': 3},
                {'title': 'Account Selection Functionality', 'description': 'Test selecting specific GL accounts', 'priority': 3},
                {'title': 'Account Balance Display', 'description': 'Test account balance viewing and calculations', 'priority': 3},
                {'title': 'Account Details Popup', 'description': 'Test account detail views and information display', 'priority': 2},
                {'title': 'Journal Entries Date Filtering', 'description': 'Test date range filtering for journal entries', 'priority': 3},
                {'title': 'Journal Entries Account Filtering', 'description': 'Test filtering journal entries by specific accounts', 'priority': 3},
                {'title': 'Journal Entries Search', 'description': 'Test searching entries by description/reference', 'priority': 2},
                {'title': 'Transaction Drill Down', 'description': 'Test drilling down to transaction details', 'priority': 2},
                {'title': 'Trial Balance Report Display', 'description': 'Test trial balance report generation and display', 'priority': 3},
                {'title': 'Account Activity Report', 'description': 'Test account activity/history reporting', 'priority': 2},
                {'title': 'Data Export Functionality', 'description': 'Test exporting ledger data (CSV, Excel, PDF)', 'priority': 2},
                {'title': 'Accounting Period Selection', 'description': 'Test accounting period selection and filtering', 'priority': 3},
                {'title': 'Manual Journal Entry Creation', 'description': 'Test creating manual journal entries', 'priority': 4},
                {'title': 'Journal Entry Validation Rules', 'description': 'Test validation rules (debit = credit)', 'priority': 4},
                {'title': 'Journal Entry Posting', 'description': 'Test posting journal entries to ledger', 'priority': 4},
                {'title': 'Journal Entry Reversal', 'description': 'Test reversing posted journal entries', 'priority': 3},
                {'title': 'Bank Reconciliation Integration', 'description': 'Test connection between ledger and bank reconciliation', 'priority': 3},
                {'title': 'Payables Module Integration', 'description': 'Test connection between ledger and payables module', 'priority': 3},
                {'title': 'Complete Ledger Workflow', 'description': 'Test end-to-end ledger operations workflow', 'priority': 4},
                
                # Financial Dashboard Tests
                {'title': 'Financial Dashboard Loading', 'description': 'Test financial dashboard loads with all KPIs', 'priority': 3},
                {'title': 'Financial KPIs Display', 'description': 'Test display of key performance indicators', 'priority': 3},
                {'title': 'Dashboard Filter Controls', 'description': 'Test filter controls and period selection', 'priority': 2},
                {'title': 'Total Income Value Retrieval', 'description': 'Test retrieval and display of total income values', 'priority': 2},
                {'title': 'Gross Profit Value Retrieval', 'description': 'Test retrieval and display of gross profit values', 'priority': 2},
                {'title': 'All KPI Values Retrieval', 'description': 'Test retrieval of all KPI values and calculations', 'priority': 2},
                {'title': 'KPI Data Consistency', 'description': 'Test consistency of KPI data across dashboard', 'priority': 2},
                {'title': 'Period Selection Functionality', 'description': 'Test period selection (Y/Q/M) functionality', 'priority': 2},
                {'title': 'Date Preset Functionality', 'description': 'Test date preset changes (Last Year, etc.)', 'priority': 2},
                {'title': 'Period Filter Impact Testing', 'description': 'Test impact of period filters on data display', 'priority': 2},
                {'title': 'No Data States Handling', 'description': 'Test handling of no data states and empty dashboards', 'priority': 1},
                {'title': 'Dashboard URL Parameters', 'description': 'Test URL parameter extraction and handling', 'priority': 1},
                {'title': 'Complete Dashboard Workflow', 'description': 'Test complete dashboard workflow from load to analysis', 'priority': 3},
                {'title': 'Dashboard Performance Testing', 'description': 'Test dashboard responsiveness and performance', 'priority': 2},
                {'title': 'Dashboard Edge Cases', 'description': 'Test dashboard behavior in edge cases and error conditions', 'priority': 1}
            ],
            
            '🔐 Security Regression': [
                {'title': 'Invalid Login Attempts Protection', 'description': 'Test brute force protection and account lockout mechanisms', 'priority': 4},
                {'title': 'Session Timeout Management', 'description': 'Test session timeout and automatic logout functionality', 'priority': 4},
                {'title': 'SQL Injection Prevention', 'description': 'Test SQL injection blocking in login and form fields', 'priority': 4},
                {'title': 'Cross-Site Scripting (XSS) Prevention', 'description': 'Test XSS protection and script injection blocking', 'priority': 4},
                {'title': 'Password Requirements Validation', 'description': 'Test password strength requirements and validation', 'priority': 3},
                {'title': 'CSRF Token Validation', 'description': 'Test Cross-Site Request Forgery protection mechanisms', 'priority': 3},
                {'title': 'HTTP Security Headers Verification', 'description': 'Test presence of security headers in HTTP responses', 'priority': 2}
            ],
            
            '⚡ Performance Regression': [
                {'title': 'Page Load Performance Testing', 'description': 'Test page load times across all major modules', 'priority': 3},
                {'title': 'Memory Usage Monitoring', 'description': 'Test memory usage patterns and leak detection', 'priority': 2},
                {'title': 'Concurrent User Simulation', 'description': 'Test performance with multiple concurrent operations', 'priority': 3},
                {'title': 'API Response Time Monitoring', 'description': 'Test API performance and response times', 'priority': 3},
                {'title': 'Large Dataset Handling Performance', 'description': 'Test performance when handling large datasets', 'priority': 2},
                {'title': 'Resource Usage Optimization', 'description': 'Test CPU and network resource usage optimization', 'priority': 1}
            ],
            
            '📱 Browser Compatibility': [
                {'title': 'Mobile Viewport Compatibility', 'description': 'Test application functionality on mobile device viewports', 'priority': 2},
                {'title': 'Responsive Design Elements', 'description': 'Test responsive design across different screen sizes', 'priority': 2},
                {'title': 'Touch Interface Compatibility', 'description': 'Test touch interface elements and gestures', 'priority': 1},
                {'title': 'Print Stylesheet Compatibility', 'description': 'Test print formatting and print-friendly layouts', 'priority': 1}
            ]
        }
        
        # Create test cases for each section
        total_cases = 0
        for section_name, cases in test_cases.items():
            if section_name not in self.section_mappings:
                print(f"⚠️ Section '{section_name}' not found in mappings")
                continue
                
            section_id = self.section_mappings[section_name]
            print(f"\n📝 Creating {len(cases)} test cases for {section_name}...")
            
            for case in cases:
                data = {
                    'title': case['title'],
                    'section_id': section_id,
                    'template_id': 1,  # Test Case (Steps)
                    'type_id': 1,      # Automated
                    'priority_id': case['priority'],
                    'custom_steps_separated': [
                        {
                            'content': case['description'],
                            'expected': 'Test should pass successfully'
                        }
                    ]
                }
                
                result = self.config._send_request('POST', f'add_case/{section_id}', data)
                if result:
                    case_id = result['id']
                    self.case_mappings[case['title']] = case_id
                    total_cases += 1
                    print(f"✅ Created: {case['title']} (C{case_id})")
                    time.sleep(0.3)  # Prevent rate limiting
                else:
                    print(f"❌ Failed to create: {case['title']}")
        
        print(f"\n🎉 Successfully created {total_cases} test cases!")
        return total_cases > 0
    
    def generate_mapping_file(self):
        """Generate a mapping file for the new test cases"""
        print("\n📄 Generating test case mapping file...")
        
        mapping_data = {
            'suite_info': {
                'suite_id': self.created_suite_id,
                'suite_name': self.suite_name,
                'project_id': self.project_id,
                'created_date': datetime.now().isoformat(),
                'total_cases': len(self.case_mappings)
            },
            'section_mappings': self.section_mappings,
            'case_mappings': self.case_mappings,
            'framework_mappings': {
                'test_function_to_case_id': {
                    # API Tests
                    'test_get_journal_entries_valid_date_format_request': self.case_mappings.get('GET Journal Entries - Valid Date Format'),
                    'test_get_journal_entries_invalid_date_format_request': self.case_mappings.get('GET Journal Entries - Invalid Date Format'),
                    'test_create_journal_entry_valid_date_format': self.case_mappings.get('POST Create Journal Entry - Valid Date Format'),
                    'test_create_journal_entry_invalid_date_format': self.case_mappings.get('POST Create Journal Entry - Invalid Date Format'),
                    'test_get_bank_uploaded_files_date_format': self.case_mappings.get('GET Bank Uploaded Files - Date Format'),
                    'test_get_bank_transactions_data_date_format': self.case_mappings.get('GET Bank Transactions Data - Date Format'),
                    'test_get_entity_documents_date_format': self.case_mappings.get('GET Entity Documents - Date Format'),
                    'test_get_accounting_uploaded_files_date_format': self.case_mappings.get('GET Accounting Uploaded Files - Date Format'),
                    'test_all_endpoints_reject_invalid_date_formats': self.case_mappings.get('All Endpoints Reject Invalid Date Formats'),
                    'test_date_format_consistency_across_endpoints': self.case_mappings.get('Date Format Consistency Across Endpoints'),
                    'test_date_format_validation_demo': self.case_mappings.get('Date Format Validation Demo'),
                    
                    # Login Tests
                    'test_login': self.case_mappings.get('Basic Login Functionality'),
                    'test_scenario_1_valid_login': self.case_mappings.get('Valid Login Scenario with 2FA'),
                    'test_scenario_2_logout_user': self.case_mappings.get('Login then Logout Workflow'),
                    
                    # Navigation Tests
                    'test_tab_navigation[text=Home-HomePage]': self.case_mappings.get('Navigate to Home Page'),
                    'test_tab_navigation[text=Vizion AI-VizionAIPage]': self.case_mappings.get('Navigate to Vizion AI Page'),
                    'test_tab_navigation[text=Reconciliation-ReconciliationPage]': self.case_mappings.get('Navigate to Reconciliation Page'),
                    'test_tab_navigation[text=Ledger-LedgerPage]': self.case_mappings.get('Navigate to Ledger Page'),
                    'test_tab_navigation[text=BI Analysis-BIAnalysisPage]': self.case_mappings.get('Navigate to BI Analysis Page'),
                    'test_tab_navigation[text=Connections-ConnectionPage]': self.case_mappings.get('Navigate to Connections Page'),
                    'test_tabs_navigation_single_login': self.case_mappings.get('All Tabs Navigation in Single Session'),
                    
                    # Logout Tests
                    'test_logout_after_2fa_login': self.case_mappings.get('Logout After 2FA Authentication'),
                    'test_logout_direct_method': self.case_mappings.get('Direct Logout Button Method'),
                    'test_logout_via_menu': self.case_mappings.get('Logout via User Menu'),
                    'test_logout_keyboard_method': self.case_mappings.get('Logout via Keyboard Shortcuts'),
                    'test_logout_comprehensive_workflow': self.case_mappings.get('Comprehensive Logout Workflow'),
                    
                    # Note: Add more mappings as needed for Bank, Payables, Ledger, Security, Performance, and Compatibility tests
                }
            }
        }
        
        # Save mapping file
        mapping_file = 'new_testrail_suite_mappings.json'
        with open(mapping_file, 'w') as f:
            json.dump(mapping_data, f, indent=2)
        
        print(f"✅ Created mapping file: {mapping_file}")
        return mapping_file
    
    def print_summary(self):
        """Print a summary of the created test suite"""
        print("\n" + "="*80)
        print("🎉 TESTRAIL SUITE CREATION COMPLETE!")
        print("="*80)
        print(f"📊 Suite Name: {self.suite_name}")
        print(f"🆔 Suite ID: {self.created_suite_id}")
        print(f"📂 Sections Created: {len(self.section_mappings)}")
        print(f"📝 Test Cases Created: {len(self.case_mappings)}")
        print(f"🏗️ Project ID: {self.project_id}")
        
        print("\n📂 Section Summary:")
        for section_name, section_id in self.section_mappings.items():
            print(f"   {section_name}: Section ID {section_id}")
        
        print(f"\n🔗 TestRail URL: {self.config.url}/index.php?/suites/view/{self.created_suite_id}")
        print("\n✅ You can now update your conftest.py to use the new suite ID and case mappings!")


def main():
    """Main execution function"""
    print("🚀 Starting TestRail Suite Creation...")
    print("This will create a comprehensive test suite with all 137+ tests from your framework")
    
    # Ask for confirmation
    confirm = input("\nDo you want to proceed? (y/N): ").strip().lower()
    if confirm != 'y':
        print("❌ Operation cancelled")
        return
    
    creator = TestRailSuiteCreator()
    
    try:
        # Step 1: Create the main test suite
        if not creator.create_test_suite():
            print("❌ Failed to create test suite. Exiting.")
            return
        
        # Step 2: Create organized sections
        if not creator.create_sections():
            print("❌ Failed to create all sections. Exiting.")
            return
        
        # Step 3: Create all test cases
        if not creator.create_test_cases():
            print("❌ Failed to create test cases. Exiting.")
            return
        
        # Step 4: Generate mapping file
        creator.generate_mapping_file()
        
        # Step 5: Print summary
        creator.print_summary()
        
    except KeyboardInterrupt:
        print("\n❌ Operation cancelled by user")
    except Exception as e:
        print(f"❌ Error occurred: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main() 