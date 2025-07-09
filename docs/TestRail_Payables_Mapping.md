# TestRail Payables Test Cases Mapping (T451-T470)

This document shows the complete mapping of all 20 TestRail payables test cases (T451-T470) to the automated Playwright tests.

## Overview
- **Total TestRail Cases**: 20 (T451-T470)
- **Automated Tests**: 20 test methods
- **Test File**: `tests/e2e/reconciliation/payables/test_complete_payables_operations.py`
- **Page Object**: `pages/payables_page.py`

## Complete TestRail Mapping

### T451: Verify invoices list is displayed
- **Test Method**: `test_verify_invoice_list_is_displayed`
- **Description**: Verify that the invoice list is displayed in payables section
- **Priority**: High
- **Status**: ✅ Implemented

### T452: Upload a valid invoice file
- **Test Method**: `test_upload_invoice_file`
- **Description**: Test uploading a valid invoice file
- **Priority**: High
- **Status**: ✅ Implemented

### T453: Upload invalid file type
- **Test Method**: `test_upload_invalid_file_type`
- **Description**: Test uploading invalid file type and verify error handling
- **Priority**: Medium
- **Status**: ✅ Implemented

### T454: Upload duplicate invoice
- **Test Method**: `test_upload_duplicate_invoice`
- **Description**: Test duplicate invoice upload prevention
- **Priority**: Medium
- **Status**: ✅ Implemented

### T455: Delete invoice in New status
- **Test Method**: `test_delete_invoice_in_new_status`
- **Description**: Test deleting invoice in New status
- **Priority**: Medium
- **Status**: ✅ Implemented

### T456: Attempt to delete invoice in Recorded status
- **Test Method**: `test_attempt_to_delete_invoice`
- **Description**: Test attempting to delete invoice in Recorded status (should be prevented)
- **Priority**: Medium
- **Status**: ✅ Implemented

### T457: Menu options for New status
- **Test Method**: `test_menu_options_for_new_status`
- **Description**: Test context menu options for invoices in New status
- **Priority**: Medium
- **Status**: ✅ Implemented

### T458: Menu options for Matched status
- **Test Method**: `test_menu_options_for_matched_status`
- **Description**: Test context menu options for invoices in Matched status
- **Priority**: Medium
- **Status**: ✅ Implemented

### T459: Menu options for Recorded status
- **Test Method**: `test_menu_options_for_reconciled_status`
- **Description**: Test context menu options for invoices in Recorded status
- **Priority**: Medium
- **Status**: ✅ Implemented

### T460: Open Edit popup layout
- **Test Method**: `test_open_edit_popup_layout`
- **Description**: Test Edit popup layout and functionality
- **Priority**: Medium
- **Status**: ✅ Implemented

### T461: Mandatory fields validation in Edit popup
- **Test Method**: `test_mandatory_validation`
- **Description**: Test mandatory field validation in Edit popup
- **Priority**: High
- **Status**: ✅ Implemented

### T462: Line totals equal Before VAT validation
- **Test Method**: `test_line_totals_equal_before_validation`
- **Description**: Test line totals validation in Edit popup
- **Priority**: Medium
- **Status**: ✅ Implemented

### T463: GL Account dropdown search
- **Test Method**: `test_gl_account_dropdown`
- **Description**: Test GL Account dropdown search functionality
- **Priority**: Medium
- **Status**: ✅ Implemented

### T464: Recognition timing Single Date
- **Test Method**: `test_recognition_timing_single_date`
- **Description**: Test single date recognition timing option
- **Priority**: Medium
- **Status**: ✅ Implemented

### T465: Recognition timing Deferred Period
- **Test Method**: `test_recognition_timing_default`
- **Description**: Test deferred period recognition timing option
- **Priority**: Medium
- **Status**: ✅ Implemented

### T466: Record invoice and status change
- **Test Method**: `test_record_invoice_and_status`
- **Description**: Test invoice recording and status update
- **Priority**: High
- **Status**: ✅ Implemented

### T467: Show Journal Entry for Recorded invoice
- **Test Method**: `test_show_journal_entry_for_record`
- **Description**: Test journal entry display for recorded invoices
- **Priority**: Medium
- **Status**: ✅ Implemented

### T468: View invoice in new tab
- **Test Method**: `test_view_invoice_in_new_view`
- **Description**: Test viewing invoice in new tab/window
- **Priority**: Low
- **Status**: ✅ Implemented

### T469: Verify JE amount and description fields are read-only
- **Test Method**: `test_verify_je_amount_and_description`
- **Description**: Test that JE amount and description fields are read-only
- **Priority**: Medium
- **Status**: ✅ Implemented

### T470: Delete confirmation dialog actions
- **Test Method**: `test_delete_invoice_dialog`
- **Description**: Test delete confirmation dialog functionality
- **Priority**: Medium
- **Status**: ✅ Implemented

## Additional Tests (Using Core Page Object Methods)

### Core Navigation Tests
- **Test Method**: `test_payables_edit_delete_buttons`
- **TestRail Case**: T455 (Delete invoice in New status)
- **Description**: Test edit/delete buttons functionality

### Core Dropdown Tests
- **Test Method**: `test_payables_status_dropdowns`
- **TestRail Case**: T457 (Menu options for New status)
- **Description**: Test status dropdowns functionality

### Core Search Tests
- **Test Method**: `test_payables_search_filter_options`
- **TestRail Case**: T463 (GL Account dropdown search)
- **Description**: Test search/filter options functionality

## Test Execution Commands

### Run All Payables Tests
```bash
python -m pytest tests/e2e/reconciliation/payables/test_complete_payables_operations.py -v
```

### Run Specific TestRail Case
```bash
# Example: Run T451 test
python -m pytest tests/e2e/reconciliation/payables/test_complete_payables_operations.py::TestPayablesOperations::test_verify_invoice_list_is_displayed -v

# Example: Run T460 test
python -m pytest tests/e2e/reconciliation/payables/test_complete_payables_operations.py::TestPayablesOperations::test_open_edit_popup_layout -v
```

### Run Tests by Priority
```bash
# High priority tests (T451, T452, T461, T466)
python -m pytest tests/e2e/reconciliation/payables/test_complete_payables_operations.py -k "verify_invoice_list_is_displayed or upload_invoice_file or mandatory_validation or record_invoice_and_status" -v
```

## TestRail Integration

All tests are configured to report results to TestRail:
- **TestRail URL**: https://viewz.testrail.io
- **Project ID**: 1
- **Suite ID**: 4
- **Test Run**: Auto-created during execution

### TestRail Results Location
1. Go to https://viewz.testrail.io
2. Navigate to Project 1
3. Go to Test Runs section
4. Look for "Automated Test Run - Playwright Framework"
5. Each test reports to its specific TestRail case (T451-T470)

## Page Object Methods

The `PayablesPage` class provides these core methods:
- `navigate_to_payables()` - Navigate to payables section
- `verify_invoice_list_displayed()` - Check if invoice list is visible
- `verify_upload_area_visible()` - Check if upload area is present
- `verify_edit_delete_buttons()` - Check if edit/delete buttons exist
- `verify_status_dropdowns()` - Check if status dropdowns are present
- `verify_search_filter_options()` - Check if search/filter options exist
- `click_first_edit_button()` - Click first edit button
- `click_first_delete_button()` - Click first delete button
- `search_invoices(query)` - Search invoices with query

## Test Coverage Summary

✅ **All 20 TestRail cases (T451-T470) are mapped and implemented**
✅ **Navigation pattern follows established framework**
✅ **TestRail integration configured for all tests**
✅ **Page object pattern implemented**
✅ **Test evidence capture included**

## Next Steps

1. **Run tests to verify functionality**
2. **Check TestRail results reporting**
3. **Enhance specific test implementations as needed**
4. **Add more detailed assertions based on actual UI elements** 