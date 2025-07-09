
# TestRail Mapping Summary for CSV Tests

## Overview
All CSV-generated tests have been mapped to existing TestRail cases based on functionality:

- **C345 (Login)**: Status updates and state changes
- **C346 (Navigation)**: UI interactions, forms, menus, popups
- **C347 (Single Login)**: Reserved for single-session tests
- **C357 (Logout)**: Destructive operations like delete

## Detailed Mapping

### TestRail Case C346 (Navigation)
**Total Tests**: 15

- `test_verify_invoice_list_is_displayed` - Verify invoice list is displayed
- `test_upload_invoice_file` - Upload invoice file
- `test_upload_invalid_file_type` - Upload invalid file type
- `test_menu_options_for_new_status` - Menu options for New status
- `test_menu_options_for_matched_status` - Menu options for Matched status
- `test_menu_options_for_reconciled_status` - Menu options for Reconciled status
- `test_open_edit_popup_layout` - Open Edit popup layout
- `test_mandatory_validation` - Mandatory validation
- `test_line_totals_equal_before_validation` - Line totals equal Before Validation
- `test_gl_account_dropdown` - GL Account dropdown
- `test_recognition_timing_single_date` - Recognition timing Single Date
- `test_recognition_timing_default` - Recognition timing Default
- `test_show_journal_entry_for_record` - Show Journal Entry for Record
- `test_view_invoice_in_new_view` - View invoice in new view
- `test_verify_je_amount_and_description` - Verify JE amount and description

### TestRail Case C357 (Logout)
**Total Tests**: 3

- `test_delete_invoice_in_new_status` - Delete invoice in New status
- `test_attempt_to_delete_invoice` - Attempt to delete invoice
- `test_delete_invoice_dialog` - Delete invoice dialog

### TestRail Case C345 (Login)
**Total Tests**: 1

- `test_record_invoice_and_status` - Record invoice and status


## Statistics
- **Total CSV Tests**: 19
- **TestRail Cases Used**: 3
- **Navigation Tests (C346)**: 15
- **Login Tests (C345)**: 1
- **Logout Tests (C357)**: 3

## Usage
All tests will automatically report to TestRail when run with:
```bash
TESTRAIL_ENABLED=true python -m pytest tests/e2e/reconciliation/payables/ -v
```
