import os
import time
import pytest
from configs.testrail_config import TestRailConfig, TestRailStatus

class TestRailIntegration:
    def __init__(self):
        self.config = TestRailConfig()
        self.run_id = None
        self.test_results = {}
        self.pending_results = set()  # Track pending test case IDs
        
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
            return None
        
        # Add to pending results
        self.pending_results.add(case_id)
        
        try:
            result = self.config.update_test_result(self.run_id, case_id, status, comment, elapsed)
            # Remove from pending if successful
            if result:
                self.pending_results.discard(case_id)
            return result
        except Exception as e:
            print(f"⚠️ Failed to update case {case_id}: {e}")
            # Keep in pending for retry
            return None
        
    def finalize_test_run(self):
        """Close TestRail test run"""
        if not self._is_enabled() or not self.run_id:
            return
        
        # Wait for any pending results with retries
        import time
        max_retries = 5
        retry_delay = 1
        
        for attempt in range(max_retries):
            if not self.pending_results:
                break
                
            print(f"⏳ Waiting for {len(self.pending_results)} pending results (attempt {attempt + 1}/{max_retries})")
            time.sleep(retry_delay)
            
            # Retry failed results
            pending_copy = self.pending_results.copy()
            for case_id in pending_copy:
                try:
                    # Retry with a simple passed status if we have no stored result
                    self.config.update_test_result(self.run_id, case_id, 1, "Retry update", None)
                    self.pending_results.discard(case_id)
                except Exception:
                    continue
                    
        # Always close the run, even if some results are pending
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