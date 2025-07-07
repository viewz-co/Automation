import os
import requests
import json
from base64 import b64encode

class TestRailConfig:
    def __init__(self):
        # TestRail connection settings - use environment variables for security
        self.url = os.getenv('TESTRAIL_URL', 'https://viewz.testrail.io')
        self.username = os.getenv('TESTRAIL_USERNAME', 'automation@viewz.co')
        self.password = os.getenv('TESTRAIL_PASSWORD', 'e.fJg:z5q5mnAdL')  # Updated TestRail password
        
        # Project and suite configuration - Suite ID 4 from your URL
        self.project_id = int(os.getenv('TESTRAIL_PROJECT_ID', '1'))
        self.suite_id = int(os.getenv('TESTRAIL_SUITE_ID', '4'))
        
        # Test run configuration
        self.run_name = os.getenv('TESTRAIL_RUN_NAME', 'Automated Test Run - Playwright Framework')
        self.run_description = os.getenv('TESTRAIL_RUN_DESCRIPTION', 'Automated test execution from Playwright Python Framework')
        
        # Setup authentication
        self.auth = b64encode(f"{self.username}:{self.password}".encode()).decode()
        self.headers = {
            'Authorization': f'Basic {self.auth}',
            'Content-Type': 'application/json'
        }
    
    def _send_request(self, method, uri, data=None):
        """Send request to TestRail API"""
        url = f"{self.url}/index.php?/api/v2/{uri}"
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=self.headers)
            elif method == 'POST':
                response = requests.post(url, headers=self.headers, json=data)
            elif method == 'PUT':
                response = requests.put(url, headers=self.headers, json=data)
            
            # Better error handling
            if response.status_code == 403:
                print("❌ Authentication failed. Please check:")
                print("   1. Username is correct")
                print("   2. Password is an API KEY (not regular password)")
                print("   3. User has API access enabled")
                print("   4. User has permissions for this project")
                return None
            elif response.status_code == 401:
                print("❌ Invalid credentials. Please verify username and API key.")
                return None
            
            response.raise_for_status()
            return response.json() if response.content else None
        except requests.exceptions.RequestException as e:
            print(f"TestRail API error: {e}")
            return None
    
    def create_test_run(self, case_ids=None):
        """Create a new test run in TestRail"""
        data = {
            'suite_id': self.suite_id,
            'name': self.run_name,
            'description': self.run_description,
            'include_all': True if not case_ids else False,
            'case_ids': case_ids if case_ids else []
        }
        
        result = self._send_request('POST', f'add_run/{self.project_id}', data)
        return result['id'] if result else None
    
    def update_test_result(self, run_id, case_id, status, comment="", elapsed=None):
        """Update test result in TestRail
        
        Args:
            run_id: TestRail run ID
            case_id: TestRail case ID
            status: Test status (1=Passed, 5=Failed, 3=Untested, 4=Retest)
            comment: Optional comment
            elapsed: Optional elapsed time
        """
        data = {
            'status_id': status,
            'comment': comment
        }
        
        if elapsed:
            data['elapsed'] = elapsed
        
        result = self._send_request('POST', f'add_result_for_case/{run_id}/{case_id}', data)
        return result
    
    def close_test_run(self, run_id):
        """Close test run in TestRail"""
        result = self._send_request('POST', f'close_run/{run_id}')
        if result:
            print(f"Test run {run_id} closed successfully")
        return result
    
    def get_test_cases(self, suite_id=None):
        """Get test cases from TestRail"""
        suite_id = suite_id or self.suite_id
        result = self._send_request('GET', f'get_cases/{self.project_id}&suite_id={suite_id}')
        return result

# TestRail status constants
class TestRailStatus:
    PASSED = 1
    BLOCKED = 2
    UNTESTED = 3
    RETEST = 4
    FAILED = 5 