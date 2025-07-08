# Updated TestRail Case Mapping
# Copy this to your tests/conftest.py file

        case_mapping = {
            'test_login': 371,  # C345: Login with 2FA Authentication
            'test_tab_navigation[text=Home-HomePage]': 372,  # C346: Tab Navigation Functionality
            'test_tab_navigation[text=Vizion AI-VizionAIPage]': 372,  # C346: Tab Navigation Functionality
            'test_tab_navigation[text=Reconciliation-ReconciliationPage]': 372,  # C346: Tab Navigation Functionality
            'test_tab_navigation[text=Ledger-LedgerPage]': 372,  # C346: Tab Navigation Functionality
            'test_tab_navigation[text=BI Analysis-BIAnalysisPage]': 372,  # C346: Tab Navigation Functionality
            'test_tab_navigation[text=Connections-ConnectionPage]': 372,  # C346: Tab Navigation Functionality
            'test_tabs_navigation_single_login': 373,  # C347: Single Login Tab Navigation
            'test_logout_after_2fa_login': 374,  # C348: Complete Login and Logout Flow with 2FA
            'test_logout_direct_method': 375,  # C349: Direct Logout Method
            'test_logout_via_menu': 376,  # C350: Menu-based Logout
            'test_logout_comprehensive_fallback': 377,  # C351: Comprehensive Logout with Fallback Methods
            'test_logout_session_validation': 378,  # C352: Session Validation after Logout
            'test_scenario_1_valid_login': 379,  # C353: Valid Login Scenario Test
            'test_scenario_2_logout_user': 380,  # C354: Logout User Scenario Test
        }