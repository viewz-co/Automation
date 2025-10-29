# 📋 Create Receivables TestRail Cases

## Overview

This guide provides step-by-step instructions to create the 13 TestRail cases needed for Receivables testing.

**TestRail Case Range**: C8066 - C8078

---

## Quick Summary

- **Total Cases to Create**: 13
- **Case ID Range**: C8066-C8078
- **Section**: Reconciliation > Receivables
- **Test Framework**: 26 automated test functions mapping to 13 cases

---

## TestRail Cases to Create

### C8066: Verify Receivable List is Displayed

**Title**: Verify Receivable List is Displayed

**Section**: Reconciliation > Receivables

**Priority**: High

**Type**: Functional

**Automated**: Yes (2 test functions)

**Description**:
Verify that the receivables list/table is displayed correctly when navigating to the receivables section.

**Preconditions**:
- User is logged in
- User has access to Reconciliation module
- Entity is selected

**Steps**:
1. Navigate to Reconciliation section
2. Click on Receivables tab
3. Wait for page to load
4. Verify receivables list/table is visible

**Expected Result**:
- Receivables list table is displayed
- Table shows receivables with proper columns (Date, Customer, Amount, Status, etc.)
- Data loads without errors

**Automated Test Functions**:
- `test_verify_receivable_list_is_displayed` (test_receivables_operations.py)
- `test_verify_receivable_list_is_displayed` (test_complete_receivables_operations.py)

---

### C8067: Upload Valid Receivable File

**Title**: Upload Valid Receivable File

**Section**: Reconciliation > Receivables

**Priority**: High

**Type**: Functional

**Automated**: Yes (2 test functions)

**Description**:
Test the ability to upload a valid receivable file (PDF format).

**Preconditions**:
- User is on the Receivables page
- Upload functionality is available
- Test receivable PDF file exists

**Steps**:
1. Navigate to Receivables page
2. Click Upload button
3. Select valid PDF file
4. Confirm upload

**Expected Result**:
- File uploads successfully
- Receivable appears in the list
- Success message is displayed

**Automated Test Functions**:
- `test_upload_receivable_file` (test_receivables_operations.py)
- `test_upload_receivable_file` (test_complete_receivables_operations.py)

---

### C8068: Upload Invalid File Type

**Title**: Upload Invalid File Type

**Section**: Reconciliation > Receivables

**Priority**: Medium

**Type**: Negative

**Automated**: Yes (1 test function)

**Description**:
Verify that the system rejects invalid file types (non-PDF files).

**Preconditions**:
- User is on the Receivables page
- Upload functionality is available

**Steps**:
1. Navigate to Receivables page
2. Click Upload button
3. Attempt to select .txt or other non-PDF file
4. Observe system response

**Expected Result**:
- System rejects invalid file type
- Error message displayed
- File is not uploaded

**Automated Test Functions**:
- `test_upload_invalid_file_type`

---

### C8069: Upload Duplicate Receivable

**Title**: Upload Duplicate Receivable

**Section**: Reconciliation > Receivables

**Priority**: Medium

**Type**: Negative

**Automated**: Yes (1 test function)

**Description**:
Verify that the system prevents duplicate receivable uploads.

**Preconditions**:
- User is on the Receivables page
- Receivable file already exists in system

**Steps**:
1. Upload a receivable file
2. Attempt to upload the same file again
3. Observe system response

**Expected Result**:
- System detects duplicate
- Warning/error message displayed
- Duplicate is not created

**Automated Test Functions**:
- `test_upload_duplicate_receivable`

---

### C8070: Edit/Delete Buttons Functionality

**Title**: Edit/Delete Buttons Functionality

**Section**: Reconciliation > Receivables

**Priority**: High

**Type**: Functional

**Automated**: Yes (1 test function)

**Description**:
Verify that Edit and Delete buttons are present and accessible in the receivables list.

**Preconditions**:
- User is on the Receivables page
- Receivables exist in the list

**Steps**:
1. Navigate to Receivables page
2. Locate receivable row
3. Verify Edit button exists
4. Verify Delete button exists
5. Check button accessibility

**Expected Result**:
- Edit button is visible
- Delete button is visible
- Buttons are clickable and functional

**Automated Test Functions**:
- `test_receivables_edit_delete_buttons`

---

### C8071: Status Dropdowns

**Title**: Status Dropdowns

**Section**: Reconciliation > Receivables

**Priority**: Medium

**Type**: Functional

**Automated**: Yes (1 test function)

**Description**:
Verify that status dropdown controls function correctly for filtering receivables.

**Preconditions**:
- User is on the Receivables page
- Receivables with various statuses exist

**Steps**:
1. Navigate to Receivables page
2. Locate status dropdown
3. Open dropdown
4. Select different status options
5. Verify filtering works

**Expected Result**:
- Status dropdown is visible
- Dropdown opens correctly
- Status options are available (New, Matched, Recorded, etc.)
- Filtering by status works

**Automated Test Functions**:
- `test_receivables_status_dropdowns`

---

### C8072: Search/Filter and Menu Operations

**Title**: Search/Filter and Menu Operations

**Section**: Reconciliation > Receivables

**Priority**: Medium

**Type**: Functional

**Automated**: Yes (2 test functions)

**Description**:
Verify search/filter functionality and context menu operations in receivables.

**Preconditions**:
- User is on the Receivables page
- Multiple receivables exist

**Steps**:
1. Test search functionality
   - Enter search term
   - Verify results filter correctly
2. Test context menu
   - Right-click receivable
   - Verify menu appears
   - Check menu options

**Expected Result**:
- Search filters results correctly
- Context menu appears on right-click
- Menu options are appropriate

**Automated Test Functions**:
- `test_receivables_search_filter_options`
- `test_receivables_menu_operations`

---

### C8073: Form Validation

**Title**: Form Validation

**Section**: Reconciliation > Receivables

**Priority**: High

**Type**: Functional

**Automated**: Yes (3 test functions)

**Description**:
Verify that form validation works correctly for receivable edit forms.

**Preconditions**:
- User can open edit receivable form

**Steps**:
1. Open edit form for a receivable
2. Test mandatory field validation
   - Leave required fields empty
   - Attempt to submit
   - Verify validation messages
3. Test field format validation
4. Test form popup layout

**Expected Result**:
- Mandatory fields are validated
- Validation messages are clear
- Form layout is correct
- Invalid data is rejected

**Automated Test Functions**:
- `test_open_edit_popup_layout`
- `test_mandatory_validation`
- `test_receivables_form_validation`

---

### C8074: Form Calculations and Recognition Timing

**Title**: Form Calculations and Recognition Timing

**Section**: Reconciliation > Receivables

**Priority**: Medium

**Type**: Functional

**Automated**: Yes (4 test functions)

**Description**:
Verify form calculations, GL account dropdown, and recognition timing options.

**Preconditions**:
- User can edit receivables
- GL accounts are configured

**Steps**:
1. Test line totals calculation
   - Enter line items
   - Verify totals calculate correctly
2. Test GL Account dropdown
   - Open GL account dropdown
   - Search for accounts
   - Select account
3. Test recognition timing
   - Select "Single Date" option
   - Select "Deferred Period" option
   - Verify timing options work

**Expected Result**:
- Line totals calculate correctly
- GL account dropdown works
- Recognition timing options function properly
- Calculations are accurate

**Automated Test Functions**:
- `test_line_totals_equal_before_validation`
- `test_gl_account_dropdown`
- `test_recognition_timing_single_date`
- `test_recognition_timing_default`

---

### C8075: Recording and Journal Entries

**Title**: Recording and Journal Entries

**Section**: Reconciliation > Receivables

**Priority**: High

**Type**: Functional

**Automated**: Yes (3 test functions)

**Description**:
Verify receivable recording functionality and journal entry display.

**Preconditions**:
- Receivable exists in "New" or "Matched" status
- User has permission to record receivables

**Steps**:
1. Select a receivable
2. Click Record button
3. Verify status changes to "Recorded"
4. View journal entry
   - Click "Show Journal Entry"
   - Verify JE details display
   - Confirm JE amounts are read-only
5. Verify JE description fields

**Expected Result**:
- Receivable is recorded successfully
- Status updates to "Recorded"
- Journal entry is created
- JE display shows correct information
- JE amount and description fields are read-only

**Automated Test Functions**:
- `test_record_receivable_and_status`
- `test_show_journal_entry_for_record`
- `test_verify_je_amount_and_description`

---

### C8076: Delete Operations

**Title**: Delete Operations

**Section**: Reconciliation > Receivables

**Priority**: Medium

**Type**: Functional

**Automated**: Yes (2 test functions)

**Description**:
Verify delete operations including confirmation dialog and delete prevention for recorded receivables.

**Preconditions**:
- Receivables exist with different statuses

**Steps**:
1. Test delete confirmation
   - Click delete on a "New" receivable
   - Verify confirmation dialog appears
   - Test Cancel and Confirm options
2. Test delete prevention
   - Attempt to delete "Recorded" receivable
   - Verify system prevents deletion
   - Check for appropriate message

**Expected Result**:
- Delete confirmation dialog appears
- Dialog has Cancel and Confirm buttons
- Recorded receivables cannot be deleted
- System shows appropriate message

**Automated Test Functions**:
- `test_delete_receivable_dialog`
- `test_attempt_to_delete_receivable`

---

### C8077: View Operations

**Title**: View Operations

**Section**: Reconciliation > Receivables

**Priority**: Low

**Type**: Functional

**Automated**: Yes (1 test function)

**Description**:
Verify that receivables can be opened in a new tab/view for detailed viewing.

**Preconditions**:
- Receivables exist in the list

**Steps**:
1. Locate a receivable in the list
2. Right-click or use action menu
3. Select "View in New Tab" option
4. Verify new tab opens
5. Verify receivable details display correctly

**Expected Result**:
- Option to view in new tab is available
- New tab/window opens
- Receivable details are displayed correctly
- All information is readable

**Automated Test Functions**:
- `test_view_receivable_in_new_view`

---

### C8078: Context Menu by Status

**Title**: Context Menu by Status

**Section**: Reconciliation > Receivables

**Priority**: Medium

**Type**: Functional

**Automated**: Yes (3 test functions)

**Description**:
Verify that context menu options are appropriate based on receivable status.

**Preconditions**:
- Receivables exist with different statuses (New, Matched, Recorded)

**Steps**:
1. Test context menu for "New" status
   - Right-click receivable with "New" status
   - Verify available menu options
   - Options should include: Edit, Delete, Match, Record
2. Test context menu for "Matched" status
   - Right-click receivable with "Matched" status
   - Verify available menu options
   - Options should include: Edit, Unmatch, Record
3. Test context menu for "Recorded" status
   - Right-click receivable with "Recorded" status
   - Verify available menu options
   - Options should include: View Journal Entry, View Only
   - Delete should NOT be available

**Expected Result**:
- Context menus display correctly for each status
- Menu options are appropriate for status
- Recorded receivables have limited options
- Menu actions function correctly

**Automated Test Functions**:
- `test_menu_options_for_new_status`
- `test_menu_options_for_matched_status`
- `test_menu_options_for_reconciled_status`

---

## TestRail Import Template

You can use this CSV template to bulk import the cases:

```csv
Section,Title,Type,Priority,Estimate,References,Description,Preconditions,Steps,Expected Result,Custom Automation Status
"Reconciliation > Receivables","Verify Receivable List is Displayed","Functional","High","5m","C8066","Verify receivables list displays correctly","User logged in, Entity selected","1. Navigate to Receivables\n2. Verify list displays","Receivables list is visible with data","Automated"
"Reconciliation > Receivables","Upload Valid Receivable File","Functional","High","5m","C8067","Upload valid PDF receivable file","User on Receivables page","1. Click Upload\n2. Select PDF\n3. Confirm","File uploads successfully","Automated"
"Reconciliation > Receivables","Upload Invalid File Type","Negative","Medium","3m","C8068","Reject invalid file types","User on Receivables page","1. Click Upload\n2. Select .txt file","System rejects file","Automated"
"Reconciliation > Receivables","Upload Duplicate Receivable","Negative","Medium","3m","C8069","Prevent duplicate uploads","Receivable exists","1. Upload duplicate file","System prevents duplicate","Automated"
"Reconciliation > Receivables","Edit/Delete Buttons Functionality","Functional","High","5m","C8070","Verify action buttons exist","Receivables visible","1. Check Edit button\n2. Check Delete button","Buttons are visible and functional","Automated"
"Reconciliation > Receivables","Status Dropdowns","Functional","Medium","3m","C8071","Test status filtering","Receivables exist","1. Open status dropdown\n2. Select status","Filtering works correctly","Automated"
"Reconciliation > Receivables","Search/Filter and Menu Operations","Functional","Medium","5m","C8072","Test search and context menu","Multiple receivables exist","1. Test search\n2. Test context menu","Search and menu work","Automated"
"Reconciliation > Receivables","Form Validation","Functional","High","10m","C8073","Test form validation rules","Can edit receivables","1. Open form\n2. Test validation","Validation works correctly","Automated"
"Reconciliation > Receivables","Form Calculations and Recognition Timing","Functional","Medium","10m","C8074","Test calculations and timing","Can edit receivables","1. Test line totals\n2. Test GL dropdown\n3. Test timing","All calculations correct","Automated"
"Reconciliation > Receivables","Recording and Journal Entries","Functional","High","10m","C8075","Test record function and JE","Receivable in New/Matched","1. Record receivable\n2. View JE","Receivable recorded, JE displays","Automated"
"Reconciliation > Receivables","Delete Operations","Functional","Medium","5m","C8076","Test delete with confirmation","Receivables exist","1. Test delete dialog\n2. Test delete prevention","Delete works, recorded protected","Automated"
"Reconciliation > Receivables","View Operations","Functional","Low","3m","C8077","View receivable in new tab","Receivables exist","1. View in new tab","Details display in new tab","Automated"
"Reconciliation > Receivables","Context Menu by Status","Functional","Medium","10m","C8078","Test menus for all statuses","Receivables with different statuses","1. Test New menu\n2. Test Matched menu\n3. Test Recorded menu","Menus show correct options","Automated"
```

---

## After Creating TestRail Cases

Once you've created the TestRail cases:

1. **Verify Case IDs Match**: Ensure your TestRail cases are C8066-C8078
2. **Run Tests**: Execute receivables tests with TestRail integration:
   ```bash
   TESTRAIL_ENABLED=true python -m pytest tests/e2e/reconciliation/receivables/ -v --headless
   ```
3. **Check Results**: Verify results appear in TestRail under the correct cases
4. **Update if Needed**: If your TestRail uses different IDs, update `conftest.py` mapping

---

## Summary

✅ **13 TestRail Cases** (C8066-C8078)  
✅ **26 Automated Test Functions**  
✅ **Complete Coverage** of receivables operations  
✅ **Ready for Regression** testing  

Your receivables test suite is now fully integrated and ready for use! 🚀

