import os
import time
import pytest
from configs.testrail_config import TestRailConfig, TestRailStatus

class TestRailIntegration:
    def __init__(self):
        self.config = TestRailConfig()
        self.run_id = None
        self.test_results = {}
        
    def setup_test_run(self, case_ids=None):
        """Setup TestRail test run"""
        if not self._is_enabled():
            return None
            
        self.run_id = self.config.create_test_run(case_ids)
        if self.run_id:
            print(f"Created TestRail run: {self.run_id}")
        return self.run_id
    
    def update_test_result(self, case_id, status, comment="", elapsed=None):
        """Update individual test result"""
        if not self._is_enabled() or not self.run_id:
            return
            
        self.config.update_test_result(self.run_id, case_id, status, comment, elapsed)
        
    def finalize_test_run(self):
        """Close TestRail test run"""
        if not self._is_enabled() or not self.run_id:
            return
            
        self.config.close_test_run(self.run_id)
        
    def _is_enabled(self):
        """Check if TestRail integration is enabled"""
        return os.getenv('TESTRAIL_ENABLED', 'false').lower() == 'true'

# Global instance
testrail = TestRailIntegration()

# Decorator for marking tests with TestRail case IDs
def testrail_case(case_id):
    """Decorator to mark test with TestRail case ID"""
    def decorator(func):
        func.testrail_case_id = case_id
        return func
    return decorator

# Pytest hooks for TestRail integration
def pytest_configure(config):
    """Setup TestRail integration at the start of test session"""
    if testrail._is_enabled():
        # Get all test case IDs from marked tests
        case_ids = []
        for item in config.session.items:
            if hasattr(item.function, 'testrail_case_id'):
                case_ids.append(item.function.testrail_case_id)
        
        if case_ids:
            testrail.setup_test_run(case_ids)

def pytest_runtest_makereport(item, call):
    """Create test report and update TestRail"""
    if call.when == 'call' and testrail._is_enabled():
        # Check if test has TestRail case ID
        if hasattr(item.function, 'testrail_case_id'):
            case_id = item.function.testrail_case_id
            
            # Determine test status
            if call.excinfo is None:
                status = TestRailStatus.PASSED
                comment = "Test passed successfully"
            else:
                status = TestRailStatus.FAILED
                comment = f"Test failed: {str(call.excinfo.value)}"
            
            # Calculate elapsed time
            elapsed = getattr(call, 'duration', None)
            if elapsed:
                elapsed = f"{elapsed:.2f}s"
            
            # Update TestRail
            testrail.update_test_result(case_id, status, comment, elapsed)

def pytest_sessionfinish(session, exitstatus):
    """Finalize TestRail integration at the end of test session"""
    if testrail._is_enabled():
        testrail.finalize_test_run()

# Helper function to get TestRail case mapping
def get_testrail_case_mapping():
    """Get mapping of test names to TestRail case IDs"""
    mapping = {
        'test_login': 'C1',  # Replace with actual TestRail case IDs
        'test_tab_navigation[text=Home-HomePage]': 'C2',
        'test_tab_navigation[text=Vizion AI-VizionAIPage]': 'C3',
        'test_tab_navigation[text=Reconciliation-ReconciliationPage]': 'C4',
        'test_tab_navigation[text=Ledger-LedgerPage]': 'C5',
        'test_tab_navigation[text=BI Analysis-BIAnalysisPage]': 'C6',
        'test_tab_navigation[text=Connections-ConnectionPage]': 'C7',
        'test_tabs_navigation_single_login': 'C8',
    }
    return mapping 