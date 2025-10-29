# Receivables TestRail Mapping

## TestRail Cases for Receivables (13 Cases)

Based on the pattern from Payables, here's the proposed mapping for 13 TestRail cases covering 26 test functions:

| TestRail Case | Test Functions | Category |
|---------------|----------------|----------|
| **C8011** | `test_verify_receivable_list_is_displayed` (x2) | Display & Navigation |
| **C8012** | `test_upload_receivable_file` (x2) | File Upload - Valid |
| **C8013** | `test_upload_invalid_file_type` | File Upload - Invalid |
| **C8014** | `test_upload_duplicate_receivable` | File Upload - Duplicate |
| **C8015** | `test_receivables_edit_delete_buttons` | UI Elements - Buttons |
| **C8016** | `test_receivables_status_dropdowns` | UI Elements - Dropdowns |
| **C8017** | `test_receivables_search_filter_options`<br>`test_receivables_menu_operations` | Search & Menu Operations |
| **C8018** | `test_open_edit_popup_layout`<br>`test_mandatory_validation`<br>`test_receivables_form_validation` | Form Validation |
| **C8019** | `test_line_totals_equal_before_validation`<br>`test_gl_account_dropdown`<br>`test_recognition_timing_single_date`<br>`test_recognition_timing_default` | Form Calculations & Timing |
| **C8020** | `test_record_receivable_and_status`<br>`test_show_journal_entry_for_record`<br>`test_verify_je_amount_and_description` | Recording & Journal Entries |
| **C8021** | `test_delete_receivable_dialog`<br>`test_attempt_to_delete_receivable` | Delete Operations |
| **C8022** | `test_view_receivable_in_new_view` | View Operations |
| **C8023** | `test_menu_options_for_new_status`<br>`test_menu_options_for_matched_status`<br>`test_menu_options_for_reconciled_status` | Context Menu Options |

---

## Detailed Mapping

### C8011: Receivable List Display
- `test_verify_receivable_list_is_displayed` (test_receivables_operations.py)
- `test_verify_receivable_list_is_displayed` (test_complete_receivables_operations.py)

### C8012: Upload Valid Receivable File
- `test_upload_receivable_file` (test_receivables_operations.py)
- `test_upload_receivable_file` (test_complete_receivables_operations.py)

### C8013: Upload Invalid File Type
- `test_upload_invalid_file_type`

### C8014: Upload Duplicate Receivable
- `test_upload_duplicate_receivable`

### C8015: Edit/Delete Buttons
- `test_receivables_edit_delete_buttons`

### C8016: Status Dropdowns
- `test_receivables_status_dropdowns`

### C8017: Search/Filter and Menu Operations
- `test_receivables_search_filter_options`
- `test_receivables_menu_operations`

### C8018: Form Validation
- `test_open_edit_popup_layout`
- `test_mandatory_validation`
- `test_receivables_form_validation`

### C8019: Form Calculations and Recognition Timing
- `test_line_totals_equal_before_validation`
- `test_gl_account_dropdown`
- `test_recognition_timing_single_date`
- `test_recognition_timing_default`

### C8020: Recording and Journal Entries
- `test_record_receivable_and_status`
- `test_show_journal_entry_for_record`
- `test_verify_je_amount_and_description`

### C8021: Delete Operations
- `test_delete_receivable_dialog`
- `test_attempt_to_delete_receivable`

### C8022: View Operations
- `test_view_receivable_in_new_view`

### C8023: Context Menu by Status
- `test_menu_options_for_new_status`
- `test_menu_options_for_matched_status`
- `test_menu_options_for_reconciled_status`

---

## Summary

- **13 TestRail Cases** (C8011-C8023)
- **26 Test Functions** in pytest
- **Logical grouping** by functionality
- **Complete coverage** of receivables operations

## To Update:

1. Verify TestRail case IDs (C8011-C8023) match your TestRail instance
2. Update conftest.py with the mapping
3. Update test files with @testrail_case decorators
4. Create TestRail cases with proper descriptions if they don't exist

---

## TestRail Case Details Template

Use this template to create/update TestRail cases:

### C8011: Verify Receivable List is Displayed
- **Section**: Reconciliation > Receivables
- **Priority**: High
- **Type**: Functional
- **Steps**: Navigate to Receivables, Verify list displays
- **Expected**: Receivable list table is visible

### C8012: Upload Valid Receivable File
- **Section**: Reconciliation > Receivables  
- **Priority**: High
- **Type**: Functional
- **Steps**: Click Upload, Select valid PDF file
- **Expected**: File uploads successfully

### C8013: Upload Invalid File Type
- **Section**: Reconciliation > Receivables
- **Priority**: Medium
- **Type**: Negative
- **Steps**: Attempt to upload .txt file
- **Expected**: System rejects invalid file type

### C8014: Upload Duplicate Receivable
- **Section**: Reconciliation > Receivables
- **Priority**: Medium
- **Type**: Negative
- **Steps**: Upload same file twice
- **Expected**: System prevents duplicate upload

### C8015: Edit/Delete Buttons Functionality
- **Section**: Reconciliation > Receivables
- **Priority**: High
- **Type**: Functional
- **Steps**: Verify edit and delete buttons exist
- **Expected**: Buttons are visible and accessible

### C8016: Status Dropdowns
- **Section**: Reconciliation > Receivables
- **Priority**: Medium
- **Type**: Functional
- **Steps**: Check status dropdown controls
- **Expected**: Dropdowns function correctly

### C8017: Search/Filter and Menu Operations
- **Section**: Reconciliation > Receivables
- **Priority**: Medium
- **Type**: Functional
- **Steps**: Test search and context menu
- **Expected**: Search and menu work properly

### C8018: Form Validation
- **Section**: Reconciliation > Receivables
- **Priority**: High
- **Type**: Functional
- **Steps**: Test form validation rules
- **Expected**: Required fields validated

### C8019: Form Calculations and Timing
- **Section**: Reconciliation > Receivables
- **Priority**: Medium
- **Type**: Functional
- **Steps**: Test line totals, GL accounts, recognition timing
- **Expected**: Calculations correct, timing options work

### C8020: Recording and Journal Entries
- **Section**: Reconciliation > Receivables
- **Priority**: High
- **Type**: Functional
- **Steps**: Record receivable, view journal entry
- **Expected**: Recording works, JE displays correctly

### C8021: Delete Operations
- **Section**: Reconciliation > Receivables
- **Priority**: Medium
- **Type**: Functional
- **Steps**: Test delete confirmation and prevention
- **Expected**: Delete dialog works, recorded items protected

### C8022: View Operations
- **Section**: Reconciliation > Receivables
- **Priority**: Low
- **Type**: Functional
- **Steps**: Open receivable in new tab
- **Expected**: Receivable opens in new view

### C8023: Context Menu by Status
- **Section**: Reconciliation > Receivables
- **Priority**: Medium
- **Type**: Functional
- **Steps**: Right-click receivables with different statuses
- **Expected**: Correct menu options for each status

