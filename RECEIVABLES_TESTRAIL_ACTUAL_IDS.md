# Receivables TestRail Cases - ACTUAL IDs

## ✅ Successfully Created Cases

All 13 receivables test cases have been automatically created in TestRail:

| TestRail Case ID | Title | Test Functions |
|-----------------|-------|----------------|
| **C62988** | Verify Receivable List is Displayed | `test_verify_receivable_list_is_displayed` |
| **C62989** | Upload Valid Receivable File | `test_upload_receivable_file` |
| **C62990** | Upload Invalid File Type | `test_upload_invalid_file_type` |
| **C62991** | Upload Duplicate Receivable | `test_upload_duplicate_receivable` |
| **C62992** | Edit/Delete Buttons Functionality | `test_receivables_edit_delete_buttons` |
| **C62993** | Status Dropdowns | `test_receivables_status_dropdowns` |
| **C62994** | Search/Filter and Menu Operations | `test_receivables_search_filter_options`<br>`test_receivables_menu_operations` |
| **C62995** | Form Validation | `test_open_edit_popup_layout`<br>`test_mandatory_validation`<br>`test_receivables_form_validation` |
| **C62996** | Form Calculations and Recognition Timing | `test_line_totals_equal_before_validation`<br>`test_gl_account_dropdown`<br>`test_recognition_timing_single_date`<br>`test_recognition_timing_default` |
| **C62997** | Recording and Journal Entries | `test_record_receivable_and_status`<br>`test_show_journal_entry_for_record`<br>`test_verify_je_amount_and_description` |
| **C62998** | Delete Operations | `test_delete_receivable_dialog`<br>`test_attempt_to_delete_receivable` |
| **C62999** | View Operations | `test_view_receivable_in_new_view` |
| **C63000** | Context Menu by Status | `test_menu_options_for_new_status`<br>`test_menu_options_for_matched_status`<br>`test_menu_options_for_reconciled_status` |

## 📍 Location in TestRail

- **Project**: Viewz
- **Suite ID**: 4
- **Section**: Receivables (ID: 3784)
- **Parent Section**: New UI - Reconciliation - Banks screen

## ✅ What's Been Done

1. ✅ Created 13 TestRail cases automatically
2. ✅ Updated `conftest.py` with actual case IDs (62988-63000)
3. ✅ All test functions are mapped to their TestRail cases
4. ✅ Tests are ready to run with TestRail integration

## 🧪 Running Tests with TestRail

Now you can run the receivables tests and results will automatically report to TestRail:

```bash
# Activate virtual environment
source venv/bin/activate

# Run all receivables tests with TestRail reporting
TESTRAIL_ENABLED=true python -m pytest tests/e2e/reconciliation/receivables/ -v --headless

# Run specific test file
TESTRAIL_ENABLED=true python -m pytest tests/e2e/reconciliation/receivables/test_receivables_operations.py -v --headless

# Run full regression with receivables included
TESTRAIL_ENABLED=true python run_full_regression_prod.py
```

## 🎯 View in TestRail

You can now see these cases in your TestRail instance:

1. Go to: https://viewz.testrail.io
2. Navigate to: Project "Viewz" → Suite 4 → Receivables section
3. You'll see all 13 cases with full details, steps, and expected results

## 📊 Coverage Summary

- **Total Test Functions**: 26
- **TestRail Cases**: 13
- **Mapping**: Multiple related test functions are grouped under single TestRail cases
- **Integration**: ✅ Fully integrated with existing test framework
