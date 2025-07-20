import os
# API Date Format Testing Guide

## Overview

This guide covers the comprehensive API date format validation tests that ensure all specified endpoints use the required **YYYY-MM-DD** date format for all request and response payloads.

## 📋 **Requirements**

All request and response payloads for the following APIs must use the date format: **YYYY-MM-DD**

### Applicable Endpoints:

1. **GET** `/api/v2/accounting/getJournalEntries`
2. **POST** `/api/v2/accounting/createJournalEntry`
3. **GET** `/api/v2/banks/getBankUploadedFiles`
4. **GET** `/api/v2/banks/getBankTransactionsData`
5. **GET** `/api/v2/docs/getEntityDocuments`
6. **GET** `/api/v2/accounting/getAccountingUploadedFiles`

## 🏗️ **Test Architecture**

### Components Created:

1. **API Client** (`api/api_client.py`)
   - HTTP client with authentication support
   - Endpoint-specific methods for all APIs
   - Request/response handling with logging

2. **Date Validator** (`utils/date_validator.py`)
   - YYYY-MM-DD format validation
   - Deep JSON payload traversal
   - Automatic date field detection
   - Comprehensive validation reporting

3. **Test Suite** (`tests/api/test_date_format_validation.py`)
   - Comprehensive test coverage for all endpoints
   - Valid and invalid date format testing
   - Cross-endpoint consistency validation
   - TestRail integration with case mapping

## 🧪 **Test Coverage**

### Individual Endpoint Tests:

| Endpoint | Valid Format Test | Invalid Format Test | TestRail Cases |
|----------|------------------|---------------------|----------------|
| **GET Journal Entries** | ✅ | ✅ | C600, C601 |
| **POST Journal Entry** | ✅ | ✅ | C602, C603 |
| **GET Bank Uploaded Files** | ✅ | ✅ | C604 |
| **GET Bank Transactions** | ✅ | ✅ | C605 |
| **GET Entity Documents** | ✅ | ✅ | C606 |
| **GET Accounting Files** | ✅ | ✅ | C607 |

### Comprehensive Tests:

| Test Type | Description | TestRail Case |
|-----------|-------------|---------------|
| **Cross-endpoint Rejection** | All endpoints reject invalid dates | C608 |
| **Format Consistency** | All endpoints use consistent YYYY-MM-DD | C609 |

## 🚀 **Setup and Execution**

### Prerequisites

1. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Environment Configuration:**
   ```bash
   # API Testing Configuration
   export API_BASE_URL=https://new.viewz.co
   export TEST_USERNAME=sharon_newdemo
   export TEST_PASSWORD=Sh@ron123$%^
   
   # TestRail Integration (optional)
   export TESTRAIL_ENABLED=true
   export TESTRAIL_URL=https://viewz.testrail.io
   export TESTRAIL_USERNAME=automation@viewz.co
   export TESTRAIL_PASSWORD=your-api-key
   export TESTRAIL_PROJECT_ID=1
   export TESTRAIL_SUITE_ID=4
   ```

### Running the Tests

#### **Run All API Date Format Tests:**
```bash
pytest tests/api/test_date_format_validation.py -v
```

#### **Run with TestRail Integration:**
```bash
TESTRAIL_ENABLED=true pytest tests/api/test_date_format_validation.py -v
```

#### **Run Specific Test Categories:**

**Journal Entries Tests:**
```bash
pytest tests/api/test_date_format_validation.py::TestAPIDateFormatValidation::test_get_journal_entries_valid_date_format_request -v
pytest tests/api/test_date_format_validation.py::TestAPIDateFormatValidation::test_create_journal_entry_valid_date_format -v
```

**Bank API Tests:**
```bash
pytest tests/api/test_date_format_validation.py -k "bank" -v
```

**Comprehensive Validation Tests:**
```bash
pytest tests/api/test_date_format_validation.py::TestAPIDateFormatValidation::test_all_endpoints_reject_invalid_date_formats -v
pytest tests/api/test_date_format_validation.py::TestAPIDateFormatValidation::test_date_format_consistency_across_endpoints -v
```

## 📊 **Test Validation Logic**

### Valid Date Formats:
- ✅ `2024-01-01` (Standard format)
- ✅ `2024-12-31` (End of year)
- ✅ `2023-06-15` (Mid-year)
- ✅ `2020-02-29` (Leap year)

### Invalid Date Formats:
- ❌ `01/01/2024` (MM/DD/YYYY)
- ❌ `01-01-2024` (MM-DD-YYYY)
- ❌ `2024/01/01` (YYYY/MM/DD)
- ❌ `2024.01.01` (YYYY.MM.DD)
- ❌ `Jan 1, 2024` (Month name)
- ❌ `2024-1-1` (No zero padding)
- ❌ `2024-13-01` (Invalid month)
- ❌ `2024-12-32` (Invalid day)

### Validation Process:

1. **Request Validation:**
   - Validates date parameters before sending to API
   - Tests both valid and invalid date formats
   - Verifies API rejection of invalid formats

2. **Response Validation:**
   - Deep traversal of JSON response structures
   - Automatic detection of date fields using patterns
   - Validates all date fields use YYYY-MM-DD format

3. **Cross-endpoint Consistency:**
   - Tests all endpoints with same invalid formats
   - Ensures consistent rejection behavior
   - Validates uniform date format usage

## 🔍 **Test Scenarios**

### Scenario 1: Valid Date Format Request
```python
# Test sends valid YYYY-MM-DD dates
start_date = "2024-01-01"
end_date = "2024-12-31"

response = api_client.get_journal_entries(start_date=start_date, end_date=end_date)

# Validates:
# 1. API accepts the request (200/404 status)
# 2. Response dates follow YYYY-MM-DD format
# 3. All nested date fields are compliant
```

### Scenario 2: Invalid Date Format Request
```python
# Test sends invalid date format
invalid_date = "01/01/2024"  # MM/DD/YYYY format

response = api_client.get_journal_entries(start_date=invalid_date)

# Validates:
# 1. API rejects request (400/422 status)
# 2. Error response indicates format requirement
```

### Scenario 3: Response Date Validation
```python
# Deep validation of response payload
response_data = {
    "entries": [
        {
            "entry_date": "2024-01-15",
            "created_at": "2024-01-15",
            "metadata": {
                "transaction_date": "2024-01-15"
            }
        }
    ]
}

# Validates all date fields recursively
validator.validate_response_payload(response_data)
```

## 📈 **Expected Results**

### Success Criteria:

1. **All endpoints accept YYYY-MM-DD format** in request parameters
2. **All endpoints reject invalid date formats** with appropriate HTTP status codes (400/422)
3. **All response payloads use YYYY-MM-DD format** for date fields
4. **Date format consistency** across all endpoints
5. **No date format violations** in any API response

### Test Reporting:

```
✅ GET journal entries with valid dates: PASSED
✅ API correctly rejected invalid date format: '01/01/2024'
✅ POST journal entry with valid dates: PASSED
✅ All 6 tested endpoints use consistent YYYY-MM-DD format
📊 Date format consistency results:
  journal_entries: ✅ CONSISTENT
  bank_uploaded_files: ✅ CONSISTENT
  bank_transactions: ✅ CONSISTENT
  entity_documents: ✅ CONSISTENT
  accounting_files: ✅ CONSISTENT
```

## 🛠️ **Troubleshooting**

### Common Issues:

1. **Authentication Failures:**
   ```bash
   # Verify credentials
   export TEST_USERNAME=your_username
   export TEST_PASSWORD=your_password
   ```

2. **API Connection Issues:**
   ```bash
   # Check base URL
   export API_BASE_URL=https://new.viewz.co
   ```

3. **Date Validation Failures:**
   - Check if API responses contain unexpected date formats
   - Review validation logs for specific field paths
   - Verify date field detection patterns

### Debug Mode:

```bash
# Run with verbose logging
pytest tests/api/test_date_format_validation.py -v -s --log-cli-level=INFO
```

## 📋 **TestRail Integration**

### Test Case Mapping:

| TestRail Case | Test Function | Description |
|---------------|---------------|-------------|
| **C600** | `test_get_journal_entries_valid_date_format_request` | GET journal entries with valid dates |
| **C601** | `test_get_journal_entries_invalid_date_format_request` | GET journal entries with invalid dates |
| **C602** | `test_create_journal_entry_valid_date_format` | POST journal entry with valid dates |
| **C603** | `test_create_journal_entry_invalid_date_format` | POST journal entry with invalid dates |
| **C604** | `test_get_bank_uploaded_files_date_format` | GET bank uploaded files date format |
| **C605** | `test_get_bank_transactions_data_date_format` | GET bank transactions date format |
| **C606** | `test_get_entity_documents_date_format` | GET entity documents date format |
| **C607** | `test_get_accounting_uploaded_files_date_format` | GET accounting files date format |
| **C608** | `test_all_endpoints_reject_invalid_date_formats` | All endpoints reject invalid dates |
| **C609** | `test_date_format_consistency_across_endpoints` | Date format consistency validation |

### TestRail Execution:

```bash
# Run with TestRail reporting
TESTRAIL_ENABLED=true pytest tests/api/test_date_format_validation.py -v

# Check results in TestRail:
# https://viewz.testrail.io -> Test Runs -> Latest Automated Run
```

## 🔄 **Continuous Integration**

### CI/CD Integration:

```yaml
# GitHub Actions / CI Pipeline
- name: Run API Date Format Tests
  run: |
    export TESTRAIL_ENABLED=true
    export API_BASE_URL=${{ secrets.API_BASE_URL }}
    export TEST_USERNAME=${{ secrets.TEST_USERNAME }}
    export TEST_PASSWORD=${{ secrets.TEST_PASSWORD }}
    pytest tests/api/test_date_format_validation.py -v --tb=short
    
- name: Upload Test Results
  if: always()
  uses: actions/upload-artifact@v3
  with:
    name: api-date-format-test-results
    path: |
      reports/
      screenshots/
```

## 📚 **Additional Resources**

- **API Client Documentation:** `api/api_client.py`
- **Date Validator Documentation:** `utils/date_validator.py`
- **Test Implementation:** `tests/api/test_date_format_validation.py`
- **TestRail Configuration:** `tests/conftest.py`
- **Main Framework Documentation:** `README.md`

---

## 🎯 **Summary**

This comprehensive test suite ensures that all specified API endpoints strictly adhere to the **YYYY-MM-DD** date format requirement for both request parameters and response payloads. The tests provide:

- ✅ **Complete endpoint coverage** for all 6 specified APIs
- ✅ **Both positive and negative testing** scenarios
- ✅ **Deep payload validation** with automatic date field detection
- ✅ **Cross-endpoint consistency** verification
- ✅ **TestRail integration** with detailed case mapping
- ✅ **Comprehensive reporting** and troubleshooting support

The test suite can be executed standalone or integrated into CI/CD pipelines for continuous validation of API date format compliance. 