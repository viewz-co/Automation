#!/usr/bin/env python3
"""
Script to create API Security OTP Validation test cases in TestRail Suite 139
Playwright Python Framework - Complete Test Suite

Creates test cases for:
- Unauthenticated access rejection tests
- Invalid token rejection tests  
- OTP flow validation tests
- Token manipulation attack tests
- Comprehensive security endpoint scanning
"""

import os
import requests
import json
from base64 import b64encode

# TestRail configuration
TESTRAIL_URL = os.getenv('TESTRAIL_URL', 'https://viewz.testrail.io')
TESTRAIL_USERNAME = os.getenv('TESTRAIL_USERNAME', 'automation@viewz.co')
TESTRAIL_PASSWORD = os.getenv('TESTRAIL_PASSWORD', 'e.fJg:z5q5mnAdL')

PROJECT_ID = 1
SUITE_ID = 139  # Suite 139: Main automation suite

# Authentication
auth = b64encode(f"{TESTRAIL_USERNAME}:{TESTRAIL_PASSWORD}".encode()).decode()
headers = {
    'Authorization': f'Basic {auth}',
    'Content-Type': 'application/json'
}

def send_request(method, uri, data=None):
    """Send request to TestRail API"""
    url = f"{TESTRAIL_URL}/index.php?/api/v2/{uri}"
    
    print(f"🔗 {method} {url}")
    
    try:
        if method == 'GET':
            response = requests.get(url, headers=headers, timeout=30)
        elif method == 'POST':
            response = requests.post(url, headers=headers, json=data, timeout=30)
        
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 400:
            print(f"   Response: {response.text[:500]}")
        
        response.raise_for_status()
        return response.json() if response.content else None
    except requests.exceptions.RequestException as e:
        print(f"❌ API error: {e}")
        if hasattr(e, 'response') and e.response:
            print(f"   Response: {e.response.text[:500]}")
        return None

def get_sections(suite_id):
    """Get all sections in a suite"""
    result = send_request('GET', f'get_sections/{PROJECT_ID}&suite_id={suite_id}')
    if result:
        if isinstance(result, dict) and 'sections' in result:
            return result['sections']
        return result
    return []

def create_section(suite_id, name, description="", parent_id=None):
    """Create a new section in the suite"""
    data = {
        'suite_id': suite_id,
        'name': name,
        'description': description
    }
    if parent_id:
        data['parent_id'] = parent_id
    
    result = send_request('POST', f'add_section/{PROJECT_ID}', data)
    if result:
        print(f"✅ Created section: {name} (ID: {result.get('id')})")
        return result
    return None

def create_case(section_id, title, **kwargs):
    """Create a new test case"""
    data = {
        'title': title,
        **kwargs
    }
    
    result = send_request('POST', f'add_case/{section_id}', data)
    if result:
        print(f"✅ Created case C{result.get('id')}: {title}")
        return result
    else:
        print(f"❌ Failed to create case: {title}")
    return None

def main():
    print("=" * 70)
    print("🔐 Creating API Security OTP Validation Test Cases in TestRail Suite 139")
    print("=" * 70)
    
    # Get existing sections
    print("\n📁 Checking existing sections in Suite 139...")
    sections = get_sections(SUITE_ID)
    
    security_section_id = None
    api_section_id = None
    
    for section in sections:
        section_name = section.get('name', '').lower()
        print(f"   Section: {section.get('name')} (ID: {section.get('id')})")
        if 'security' in section_name and 'otp' in section_name:
            security_section_id = section.get('id')
            print(f"   ✅ Found existing Security section: {security_section_id}")
        elif 'api' in section_name and not section.get('parent_id'):
            api_section_id = section.get('id')
    
    # Create Security Tests section if it doesn't exist
    if not security_section_id:
        print("\n📁 Creating API Security - OTP Validation section...")
        section_result = create_section(
            SUITE_ID, 
            "API Security - OTP Validation",
            "Security tests verifying API endpoints require OTP authentication and reject unauthorized access.\n\n"
            "Test Categories:\n"
            "1. Unauthenticated Access - Endpoints reject requests without JWT tokens\n"
            "2. Invalid Token Rejection - Endpoints reject invalid/malformed tokens\n"
            "3. OTP Flow Validation - Login requires OTP, no tokens without OTP\n"
            "4. Token Manipulation - Protects against token tampering attacks\n"
            "5. Comprehensive Scan - All sensitive endpoints verified",
            parent_id=api_section_id  # Under API if exists
        )
        if section_result:
            security_section_id = section_result.get('id')
        else:
            print("❌ Failed to create Security section")
            return
    
    # Define the Security test cases (matching test_security_otp_validation.py)
    security_tests = [
        # =================================================================
        # CATEGORY 1: Unauthenticated Access Tests
        # =================================================================
        {
            'title': 'SEC-001: Verify Journal Entries API rejects unauthenticated requests',
            'custom_automation_id': 'test_journal_entries_rejects_unauthenticated_request',
            'custom_preconds': '''1. Stage environment is accessible (https://app.stage.viewz.co)
2. No JWT authentication token is set in request headers
3. Basic auth credentials available for stage environment access''',
            'custom_steps_separated': [
                {
                    'content': 'Send GET request to /api/v2/accounting/getJournalEntries without JWT token',
                    'expected': 'Request is sent with no Authorization header',
                },
                {
                    'content': 'Check response status code',
                    'expected': 'Status code is 401 (Unauthorized) or 403 (Forbidden), OR returns HTML (SPA redirect)',
                },
                {
                    'content': 'Verify no sensitive data is exposed in response',
                    'expected': 'Response does not contain journal entry data, transactions, or financial records',
                },
            ],
            'custom_expected': '''SECURITY ASSERTION: Endpoint must be protected
- Returns 401/403 status code, OR
- Returns HTML (SPA handles auth client-side), OR  
- Returns JSON error without sensitive data

PASS CRITERIA: No journal entries data exposed without authentication''',
            'custom_goals_tags': 'Security, OTP, Authentication, API',
            'type_id': 1,  # Automated
            'priority_id': 1,  # Critical - Security test
        },
        {
            'title': 'SEC-002: Verify Bank Files API rejects unauthenticated requests',
            'custom_automation_id': 'test_bank_files_rejects_unauthenticated_request',
            'custom_preconds': '''1. Stage environment is accessible
2. No JWT authentication token is set
3. Basic auth credentials available for stage access''',
            'custom_steps_separated': [
                {
                    'content': 'Send GET request to /api/v2/banks/getBankUploadedFiles without JWT token',
                    'expected': 'Request sent without Authorization header',
                },
                {
                    'content': 'Analyze response for data exposure',
                    'expected': 'No bank file data, filenames, or upload information exposed',
                },
            ],
            'custom_expected': '''SECURITY ASSERTION: Bank files must be protected
- No bank file metadata exposed
- No filename or upload date information returned
- Endpoint protected via 401/403 or SPA redirect''',
            'custom_goals_tags': 'Security, OTP, Banking, API',
            'type_id': 1,
            'priority_id': 1,
        },
        {
            'title': 'SEC-003: Verify Bank Transactions API rejects unauthenticated requests',
            'custom_automation_id': 'test_bank_transactions_rejects_unauthenticated_request',
            'custom_preconds': '''1. Stage environment is accessible
2. No JWT authentication token is set''',
            'custom_steps_separated': [
                {
                    'content': 'Send GET request to /api/v2/banks/getBankTransactionsData without JWT token',
                    'expected': 'Request sent without authentication',
                },
                {
                    'content': 'Verify transaction data protection',
                    'expected': 'No transaction amounts, dates, or descriptions exposed',
                },
            ],
            'custom_expected': '''SECURITY ASSERTION: Bank transactions must be protected
- No transaction data exposed without authentication
- Financial information remains confidential''',
            'custom_goals_tags': 'Security, OTP, Banking, Transactions',
            'type_id': 1,
            'priority_id': 1,
        },
        {
            'title': 'SEC-004: Verify Entity Documents API rejects unauthenticated requests',
            'custom_automation_id': 'test_entity_documents_rejects_unauthenticated_request',
            'custom_preconds': '''1. Stage environment is accessible
2. No JWT authentication token is set''',
            'custom_steps_separated': [
                {
                    'content': 'Send GET request to /api/v2/docs/getEntityDocuments without JWT token',
                    'expected': 'Request sent without authentication',
                },
                {
                    'content': 'Verify document data protection',
                    'expected': 'No document names, types, or metadata exposed',
                },
            ],
            'custom_expected': '''SECURITY ASSERTION: Entity documents must be protected
- No document information exposed
- File names and metadata remain confidential''',
            'custom_goals_tags': 'Security, OTP, Documents, API',
            'type_id': 1,
            'priority_id': 1,
        },
        {
            'title': 'SEC-005: Verify Accounting Files API rejects unauthenticated requests',
            'custom_automation_id': 'test_accounting_files_rejects_unauthenticated_request',
            'custom_preconds': '''1. Stage environment is accessible
2. No JWT authentication token is set''',
            'custom_steps_separated': [
                {
                    'content': 'Send GET request to /api/v2/accounting/getAccountingUploadedFiles without JWT',
                    'expected': 'Request sent without authentication',
                },
                {
                    'content': 'Verify accounting file data protection',
                    'expected': 'No accounting file information exposed',
                },
            ],
            'custom_expected': '''SECURITY ASSERTION: Accounting files must be protected
- No file data or metadata exposed without authentication''',
            'custom_goals_tags': 'Security, OTP, Accounting, API',
            'type_id': 1,
            'priority_id': 1,
        },
        {
            'title': 'SEC-006: Verify User Info API rejects unauthenticated requests',
            'custom_automation_id': 'test_user_info_rejects_unauthenticated_request',
            'custom_preconds': '''1. Stage environment is accessible
2. No JWT authentication token is set''',
            'custom_steps_separated': [
                {
                    'content': 'Send GET request to /api/v2/auth/getUserInfo without JWT token',
                    'expected': 'Request sent without authentication',
                },
                {
                    'content': 'Check for PII exposure',
                    'expected': 'No user email, name, phone, or personal data exposed',
                },
            ],
            'custom_expected': '''SECURITY ASSERTION: User PII must be protected
- No email addresses exposed
- No usernames or names exposed
- No phone numbers or addresses exposed
- No user_id or internal identifiers exposed''',
            'custom_goals_tags': 'Security, OTP, PII, User Data',
            'type_id': 1,
            'priority_id': 1,
        },
        
        # =================================================================
        # CATEGORY 2: Invalid Token Rejection Tests
        # =================================================================
        {
            'title': 'SEC-007: Verify Journal Entries API rejects invalid JWT tokens',
            'custom_automation_id': 'test_journal_entries_rejects_invalid_token',
            'custom_preconds': '''1. Stage environment is accessible
2. Test with multiple invalid token formats:
   - "invalid_token_string"
   - "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.invalid.payload"
   - "Bearer_only_no_token"
   - "null"
   - Empty string
   - "expired.jwt.token.simulation"''',
            'custom_steps_separated': [
                {
                    'content': 'Send GET request with invalid token "invalid_token_string"',
                    'expected': 'Request rejected, no data exposed',
                },
                {
                    'content': 'Send GET request with malformed JWT structure',
                    'expected': 'Request rejected, no data exposed',
                },
                {
                    'content': 'Send GET request with empty token',
                    'expected': 'Request rejected, no data exposed',
                },
                {
                    'content': 'Repeat for all invalid token formats in preconditions',
                    'expected': 'All invalid tokens are rejected consistently',
                },
            ],
            'custom_expected': '''SECURITY ASSERTION: All invalid tokens must be rejected
assert result['is_protected'] for each invalid token

PASS CRITERIA:
- No sensitive data exposed with any invalid token
- Consistent rejection behavior across all token formats''',
            'custom_goals_tags': 'Security, JWT, Token Validation',
            'type_id': 1,
            'priority_id': 1,
        },
        {
            'title': 'SEC-008: Verify Create Journal Entry API rejects invalid JWT tokens',
            'custom_automation_id': 'test_create_journal_entry_rejects_invalid_token',
            'custom_preconds': '''1. Stage environment is accessible
2. Test payload prepared:
   - entry_date: "2024-01-15"
   - reference: "SEC-TEST-001"
   - description: "Security test entry - should be rejected"
   - total_amount: 1000.00''',
            'custom_steps_separated': [
                {
                    'content': 'Send POST request to /api/v2/accounting/createJournalEntry with invalid token',
                    'expected': 'Request is rejected',
                },
                {
                    'content': 'Verify no journal entry is created',
                    'expected': 'POST operation blocked, no data modification',
                },
            ],
            'custom_expected': '''SECURITY ASSERTION: POST endpoints must reject invalid tokens
assert result['is_protected']

CRITICAL: Write operations must never succeed with invalid authentication''',
            'custom_goals_tags': 'Security, JWT, POST, Write Operations',
            'type_id': 1,
            'priority_id': 1,
        },
        
        # =================================================================
        # CATEGORY 3: OTP Flow Validation Tests
        # =================================================================
        {
            'title': 'SEC-009: CRITICAL - Verify login does NOT return JWT token without OTP',
            'custom_automation_id': 'test_login_does_not_return_token_without_otp',
            'custom_preconds': '''1. Stage environment is accessible
2. Valid stage credentials available:
   - Username: sharon_stage
   - Password: [configured]
3. OTP verification NOT completed''',
            'custom_steps_separated': [
                {
                    'content': 'Send POST request to /api/v2/auth/login with valid username and password only',
                    'expected': 'Login request is processed',
                },
                {
                    'content': 'Parse response and check for JWT token fields (jwToken, jwtToken, token, accessToken)',
                    'expected': 'No JWT token is present in response',
                },
                {
                    'content': 'Verify response indicates OTP is required (OTP_REQUIRED, otp_enabled: true)',
                    'expected': 'Response indicates 2FA/OTP verification is needed',
                },
            ],
            'custom_expected': '''CRITICAL SECURITY ASSERTION:
assert not result['has_jwt_token']
"JWT token returned WITHOUT OTP verification is a CRITICAL VULNERABILITY"

PASS CRITERIA:
- Login response does NOT contain JWT token without OTP
- Response indicates OTP verification required (or returns SPA HTML)
- Two-factor authentication flow cannot be bypassed''',
            'custom_goals_tags': 'Security, OTP, 2FA, Critical, Authentication',
            'type_id': 1,
            'priority_id': 1,  # Critical
        },
        {
            'title': 'SEC-010: Verify OTP validation rejects invalid OTP codes',
            'custom_automation_id': 'test_otp_validation_rejects_invalid_codes',
            'custom_preconds': '''1. Stage environment is accessible
2. Login initiated (session ready for OTP)
3. Invalid OTP codes to test:
   - "000000" (all zeros)
   - "123456" (sequential)
   - "999999" (all nines)
   - "abcdef" (letters)
   - "12345" (too short)
   - "1234567" (too long)
   - "" (empty)
   - "null" (null string)''',
            'custom_steps_separated': [
                {
                    'content': 'Initiate login with valid credentials',
                    'expected': 'Session is ready for OTP validation',
                },
                {
                    'content': 'Send OTP validation request with "000000"',
                    'expected': 'OTP rejected, no token issued',
                },
                {
                    'content': 'Send OTP validation request with "123456"',
                    'expected': 'OTP rejected, no token issued',
                },
                {
                    'content': 'Test all invalid OTP formats from preconditions',
                    'expected': 'All invalid OTPs rejected, no tokens issued',
                },
            ],
            'custom_expected': '''SECURITY ASSERTION: Invalid OTP codes must be rejected
assert result['status_code'] in [400, 401, 403] or not result['has_jwt_token']

PASS CRITERIA:
- All invalid OTP codes are rejected
- No JWT token is issued for invalid OTPs
- System prevents brute-force OTP attempts''',
            'custom_goals_tags': 'Security, OTP, Validation, Brute Force',
            'type_id': 1,
            'priority_id': 1,
        },
        {
            'title': 'SEC-011: Verify OTP validation rejects expired/past OTP codes',
            'custom_automation_id': 'test_otp_validation_rejects_expired_codes',
            'custom_preconds': '''1. Stage environment is accessible
2. Valid OTP secret available for generating codes
3. Test with OTP code from 5 minutes ago (10 time windows in past)''',
            'custom_steps_separated': [
                {
                    'content': 'Generate OTP code using TOTP with timestamp from 5 minutes ago',
                    'expected': 'Past OTP code is generated',
                },
                {
                    'content': 'Initiate login with valid credentials',
                    'expected': 'Session ready for OTP',
                },
                {
                    'content': 'Submit the expired OTP code',
                    'expected': 'Expired OTP is rejected',
                },
            ],
            'custom_expected': '''SECURITY ASSERTION: Expired OTP codes should be rejected
- Codes from 5+ minutes ago must not be accepted
- Time drift window should be reasonable (1-2 intervals max)

PASS CRITERIA:
- Past OTP code is rejected
- No token issued for expired OTP''',
            'custom_goals_tags': 'Security, OTP, Time-based, TOTP',
            'type_id': 1,
            'priority_id': 2,  # High
        },
        
        # =================================================================
        # CATEGORY 4: Comprehensive Security Scan
        # =================================================================
        {
            'title': 'SEC-012: Comprehensive security scan - All sensitive endpoints require auth',
            'custom_automation_id': 'test_all_sensitive_endpoints_require_auth',
            'custom_preconds': '''1. Stage environment is accessible
2. Endpoints to scan:
   - GET /v2/accounting/getJournalEntries
   - GET /v2/accounting/getAccountingUploadedFiles
   - POST /v2/accounting/createJournalEntry
   - GET /v2/banks/getBankUploadedFiles
   - GET /v2/banks/getBankTransactionsData
   - GET /v2/docs/getEntityDocuments
   - GET /v2/auth/getUserInfo
   - GET /v2/userGroups/getUserGroupDashboards
   - GET /entities/getUserGroupEntities''',
            'custom_steps_separated': [
                {
                    'content': 'Send unauthenticated request to each endpoint in the list',
                    'expected': 'Request sent for each endpoint',
                },
                {
                    'content': 'For each endpoint, check is_protected status',
                    'expected': 'All endpoints show is_protected = True',
                },
                {
                    'content': 'Verify no endpoint returns has_sensitive_data = True',
                    'expected': 'No sensitive data exposed on any endpoint',
                },
                {
                    'content': 'Log protection type for each endpoint (status_code, frontend_redirect, no_data_exposed)',
                    'expected': 'All endpoints have a valid protection mechanism',
                },
            ],
            'custom_expected': '''SECURITY ASSERTION: No vulnerable endpoints found
vulnerable_endpoints = []  # Must be empty after scan

PASS CRITERIA:
- All 9 endpoints are protected
- No sensitive data exposed
- Vulnerability report shows 0 issues

if vulnerable_endpoints:
    pytest.fail("SECURITY VULNERABILITIES FOUND")''',
            'custom_goals_tags': 'Security, Scan, Comprehensive, All Endpoints',
            'type_id': 1,
            'priority_id': 1,
        },
        
        # =================================================================
        # CATEGORY 5: Token Manipulation Attack Tests
        # =================================================================
        {
            'title': 'SEC-013: Verify endpoints reject manipulated/tampered JWT tokens',
            'custom_automation_id': 'test_endpoints_reject_manipulated_tokens',
            'custom_preconds': '''1. Stage environment is accessible
2. Manipulated tokens to test:
   - "" (empty)
   - "null"
   - "undefined"
   - "header.payload" (missing signature)
   - "header.payload.signature.extra" (extra parts)
   - "not.a.jwt"
   - "eyJhbGciOiJub25lIiwidHlwIjoiSldUIn0.eyJzdWIiOiJ0ZXN0In0." (alg:none attack)
   - "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbiIsImFkbWluIjp0cnVlfQ.fake_sig" (privilege escalation)
   - "' OR '1'='1" (SQL injection in token)
   - "'; DROP TABLE users;--" (SQL injection attack)''',
            'custom_steps_separated': [
                {
                    'content': 'Test alg:none JWT attack (algorithm set to "none")',
                    'expected': 'Token rejected, attack blocked',
                },
                {
                    'content': 'Test privilege escalation token (admin: true in payload)',
                    'expected': 'Token rejected, cannot escalate privileges',
                },
                {
                    'content': 'Test SQL injection in token value',
                    'expected': 'SQL injection blocked, no database queries executed',
                },
                {
                    'content': 'Test all malformed token structures',
                    'expected': 'All malformed tokens rejected',
                },
            ],
            'custom_expected': '''SECURITY ASSERTION: All manipulated tokens must be rejected
assert result['is_protected'] for each token

ATTACKS BLOCKED:
- alg:none JWT bypass attack
- Privilege escalation via token manipulation
- SQL injection in Authorization header
- Malformed JWT structure attacks

CRITICAL: No data exposure with any manipulated token''',
            'custom_goals_tags': 'Security, JWT, Attack, Manipulation, SQL Injection',
            'type_id': 1,
            'priority_id': 1,
        },
        {
            'title': 'SEC-014: Security Test Suite Summary and Documentation',
            'custom_automation_id': 'test_generate_security_summary',
            'custom_preconds': '''1. All other security tests have been executed
2. Test results collected''',
            'custom_steps_separated': [
                {
                    'content': 'Generate summary of all security test categories',
                    'expected': 'Summary includes all 6 categories',
                },
                {
                    'content': 'Document test coverage',
                    'expected': 'Coverage report generated',
                },
            ],
            'custom_expected': '''Security Test Suite Coverage:
1. Unauthenticated access rejection - 6 tests
2. Invalid token rejection - 2 tests
3. OTP flow validation (no token without OTP) - 3 tests
4. Comprehensive endpoint security scan - 1 test
5. Token manipulation attacks - 1 test
6. Documentation and summary - 1 test

TOTAL: 14 security tests''',
            'custom_goals_tags': 'Security, Documentation, Summary',
            'type_id': 1,
            'priority_id': 3,  # Low - Documentation
        },
    ]
    
    # Create test cases
    print(f"\n📝 Creating {len(security_tests)} security test cases in section {security_section_id}...")
    print("-" * 70)
    
    created_cases = []
    for test in security_tests:
        title = test.pop('title')
        case = create_case(security_section_id, title, **test)
        if case:
            created_cases.append({
                'id': case.get('id'),
                'title': title,
                'automation_id': test.get('custom_automation_id', '')
            })
    
    # Summary
    print("\n" + "=" * 70)
    print("📊 SUMMARY")
    print("=" * 70)
    print(f"✅ Created {len(created_cases)} security test cases in Suite 139")
    print(f"📁 Section: API Security - OTP Validation (ID: {security_section_id})")
    
    print("\n📋 Case IDs created:")
    for case in created_cases:
        print(f"   C{case['id']}: {case['title'][:60]}...")
    
    # Output mappings for conftest.py
    print("\n" + "=" * 70)
    print("📝 TESTRAIL MAPPINGS FOR conftest.py")
    print("=" * 70)
    print("\n# Add these mappings to tests/conftest.py case_mapping dict:")
    print("\n# ===== API SECURITY - OTP VALIDATION TESTS =====")
    print(f"# Security Section (ID: {security_section_id}) - OTP and Authentication validation")
    
    for case in created_cases:
        automation_id = case.get('automation_id', f"test_{case['id']}")
        print(f"'{automation_id}': {case['id']},  # C{case['id']}")
    
    # Also output as a dict that can be directly copied
    print("\n\n# Copy-paste ready mapping:")
    print("security_otp_mapping = {")
    for case in created_cases:
        automation_id = case.get('automation_id', f"test_{case['id']}")
        print(f"    '{automation_id}': {case['id']},  # C{case['id']}")
    print("}")
    
    # Save mapping to file
    mapping_file = 'security_otp_testrail_mapping.json'
    mapping_data = {
        'suite_id': SUITE_ID,
        'section_id': security_section_id,
        'section_name': 'API Security - OTP Validation',
        'cases': created_cases,
        'mapping': {case['automation_id']: case['id'] for case in created_cases}
    }
    
    with open(mapping_file, 'w') as f:
        json.dump(mapping_data, f, indent=2)
    print(f"\n💾 Mapping saved to: {mapping_file}")
    
    return created_cases

if __name__ == "__main__":
    main()

