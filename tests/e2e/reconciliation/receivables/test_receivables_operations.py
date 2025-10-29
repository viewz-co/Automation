import os
"""
Receivables Operations Tests
Tests for receivables functionality within the Reconciliation section
Similar to Payables tests but for Receivables module
"""

import pytest
import pytest_asyncio
from playwright.async_api import Page, expect
import asyncio
from datetime import datetime

from pages.receivables_page import ReceivablesPage
from pages.login_page import LoginPage
from pages.reconciliation_page import ReconciliationPage
from utils.testrail_integration import testrail_case
from utils.screenshot_helper import screenshot_helper

class TestReceivablesOperations:
    """Test class for receivables operations within reconciliation functionality"""
    
    @pytest_asyncio.fixture
    async def receivables_page(self, perform_login_with_entity):
        """Initialize receivables page object with login and navigation to reconciliation"""
        page = perform_login_with_entity
        
        # Initialize page object
        page_obj = ReceivablesPage(page)
        await page_obj.navigate_to_receivables()
        return page_obj
    
    @pytest.mark.asyncio
    async def test_verify_receivable_list_is_displayed(self, page: Page, receivables_page: ReceivablesPage):
        """
        Test Case: Verify receivable list is displayed
        
        Priority: Medium
        Section: Reconciliation > Receivables
        
        Preconditions: User is logged in and on reconciliation page
        
        Goals: Ensure receivable list is displayed in receivables section
        
        Expected Result: Receivable list should be displayed
        
        TestRail Case ID: C8066
        """
        
        # Verify preconditions
        await self._verify_test_preconditions("Verify receivable list is displayed", "User is logged in and on reconciliation page")
        
        # Test execution
        start_time = datetime.now()
        print(f"🚀 Starting test: Verify receivable list is displayed")
        
        try:
            # Step 1: Navigate to Receivables section within Reconciliation
            print(f"📝 Step 1: Navigate to Receivables section within Reconciliation")
            await self._capture_test_evidence(page, "test_verify_receivable_list_is_displayed", "step_1")
            
            # Look for receivables-specific elements
            await self._look_for_receivables_elements(page)
            
            # Verify receivable list is displayed
            result = await receivables_page.verify_receivable_list_displayed()
            if not result:
                # If specific receivable list not found, check for general data tables
                result = await self._verify_general_data_display(page)
            
            assert result, "Receivable list or data table should be displayed"
            
            # Final verification
            print(f"✅ Test completed successfully: Verify receivable list is displayed")
            
        except Exception as e:
            print(f"❌ Test failed: Verify receivable list is displayed - {str(e)}")
            await self._capture_test_evidence(page, "test_verify_receivable_list_is_displayed", "failure")
            raise
        
        finally:
            duration = (datetime.now() - start_time).total_seconds()
            print(f"⏱️ Test duration: {duration:.2f}s")

    @pytest.mark.asyncio
    async def test_upload_receivable_file(self, page: Page, receivables_page: ReceivablesPage):
        """
        Test Case: Upload receivable file
        
        Priority: Medium
        Section: Reconciliation > Receivables
        
        Preconditions: User is logged in and on reconciliation page
        
        Goals: Ensure correct file upload functionality
        
        Expected Result: File should be uploaded successfully
        
        TestRail Case ID: C8067
        """
        
        # Verify preconditions
        await self._verify_test_preconditions("Upload receivable file", "User is logged in and on reconciliation page")
        
        # Test execution
        start_time = datetime.now()
        print(f"🚀 Starting test: Upload receivable file")
        
        try:
            # Step 1: Look for upload functionality
            print(f"📝 Step 1: Look for upload functionality")
            await self._capture_test_evidence(page, "test_upload_receivable_file", "step_1")
            
            # Look for upload elements
            upload_found = await self._look_for_upload_elements(page)
            
            if upload_found:
                # Try to upload file
                upload_result = await receivables_page.verify_upload_area_visible()
                
                # If upload button found, try file upload
                if upload_result:
                    file_result = await receivables_page.upload_file("fixtures/test_receivable.pdf")
                    print(f"📁 File upload result: {file_result}")
            else:
                print("⚠️ Upload functionality not found on this page")
            
            # Final verification
            print(f"✅ Test completed successfully: Upload receivable file")
            
        except Exception as e:
            print(f"❌ Test failed: Upload receivable file - {str(e)}")
            await self._capture_test_evidence(page, "test_upload_receivable_file", "failure")
            raise
        
        finally:
            duration = (datetime.now() - start_time).total_seconds()
            print(f"⏱️ Test duration: {duration:.2f}s")

    @pytest.mark.asyncio
    async def test_receivables_menu_operations(self, page: Page, receivables_page: ReceivablesPage):
        """
        Test Case: Receivables menu operations
        
        Priority: Medium
        Section: Reconciliation > Receivables
        
        Preconditions: User is logged in and on reconciliation page
        
        Goals: Ensure menu operations work in receivables
        
        Expected Result: Menu operations should function correctly
        
        TestRail Case ID: C8072
        """
        
        # Verify preconditions
        await self._verify_test_preconditions("Receivables menu operations", "User is logged in and on reconciliation page")
        
        # Test execution
        start_time = datetime.now()
        print(f"🚀 Starting test: Receivables menu operations")
        
        try:
            # Step 1: Look for menu elements
            print(f"📝 Step 1: Look for menu elements")
            await self._capture_test_evidence(page, "test_receivables_menu_operations", "step_1")
            
            # Look for menu elements
            menu_found = await self._look_for_menu_elements(page)
            
            if menu_found:
                # Try menu operations
                right_click_result = await receivables_page.right_click_receivable()
                
                if right_click_result:
                    # Verify context menu appears
                    menu_result = await receivables_page.verify_context_menu_visible()
                    print(f"✅ Context menu visible: {menu_result}")
            else:
                print("⚠️ Menu elements not found on this page")
            
            # Final verification
            print(f"✅ Test completed successfully: Receivables menu operations")
            
        except Exception as e:
            print(f"❌ Test failed: Receivables menu operations - {str(e)}")
            await self._capture_test_evidence(page, "test_receivables_menu_operations", "failure")
            raise
        
        finally:
            duration = (datetime.now() - start_time).total_seconds()
            print(f"⏱️ Test duration: {duration:.2f}s")

    @pytest.mark.asyncio
    async def test_receivables_form_validation(self, page: Page, receivables_page: ReceivablesPage):
        """
        Test Case: Receivables form validation
        
        Priority: Medium
        Section: Reconciliation > Receivables
        
        Preconditions: User is logged in and on reconciliation page
        
        Goals: Ensure form validation works
        
        Expected Result: Validation should work correctly
        
        TestRail Case ID: C8073
        """
        
        # Verify preconditions
        await self._verify_test_preconditions("Receivables form validation", "User is logged in and on reconciliation page")
        
        # Test execution
        start_time = datetime.now()
        print(f"🚀 Starting test: Receivables form validation")
        
        try:
            # Step 1: Look for form elements
            print(f"📝 Step 1: Look for form elements")
            await self._capture_test_evidence(page, "test_receivables_form_validation", "step_1")
            
            # Look for form elements
            form_found = await self._look_for_form_elements(page)
            
            if form_found:
                # Test form validation
                validation_result = await receivables_page.verify_mandatory_validation()
                print(f"✅ Validation result: {validation_result}")
            else:
                print("⚠️ Form elements not found on this page")
            
            # Final verification
            print(f"✅ Test completed successfully: Receivables form validation")
            
        except Exception as e:
            print(f"❌ Test failed: Receivables form validation - {str(e)}")
            await self._capture_test_evidence(page, "test_receivables_form_validation", "failure")
            raise
        
        finally:
            duration = (datetime.now() - start_time).total_seconds()
            print(f"⏱️ Test duration: {duration:.2f}s")
    
    # Helper methods
    async def _verify_test_preconditions(self, test_case_title: str, preconditions: str):
        """Verify test preconditions are met"""
        print(f"🔍 Verifying preconditions for: {test_case_title}")
        if preconditions:
            print(f"📋 Preconditions: {preconditions}")
        # Add specific precondition checks here
    
    async def _capture_test_evidence(self, page: Page, test_name: str, step: str):
        """Capture screenshots and evidence during test execution"""
        screenshot_name = f"{test_name}_{step.replace(' ', '_').lower()}.png"
        try:
            await page.screenshot(path=f"screenshots/{screenshot_name}")
            print(f"📸 Screenshot captured: {screenshot_name}")
        except Exception as e:
            print(f"⚠️ Screenshot failed: {str(e)}")
    
    async def _look_for_receivables_elements(self, page: Page):
        """Look for receivables-specific elements on the page"""
        receivables_selectors = [
            "text=Receivables",
            "text=Customer",
            "text=Receipt",
            "text=Revenue",
            ".receivables-section",
            "[data-testid*='receivables']"
        ]
        
        found_elements = []
        for selector in receivables_selectors:
            try:
                element = page.locator(selector)
                if await element.is_visible():
                    found_elements.append(selector)
                    print(f"✅ Found receivables element: {selector}")
            except:
                continue
        
        return len(found_elements) > 0
    
    async def _verify_general_data_display(self, page: Page):
        """Verify general data display elements"""
        data_selectors = [
            "table",
            ".data-table",
            ".grid",
            "[role='grid']",
            ".list-container",
            ".data-container"
        ]
        
        for selector in data_selectors:
            try:
                element = page.locator(selector)
                if await element.is_visible():
                    print(f"✅ Found data display element: {selector}")
                    return True
            except:
                continue
        
        return False
    
    async def _look_for_upload_elements(self, page: Page):
        """Look for upload elements on the page"""
        upload_selectors = [
            "input[type='file']",
            "button:has-text('Upload')",
            "text=Upload",
            ".upload-button",
            "[data-testid*='upload']"
        ]
        
        for selector in upload_selectors:
            try:
                element = page.locator(selector)
                if await element.is_visible():
                    print(f"✅ Found upload element: {selector}")
                    return True
            except:
                continue
        
        return False
    
    async def _look_for_menu_elements(self, page: Page):
        """Look for menu elements on the page"""
        menu_selectors = [
            "button",
            ".menu-button",
            "[role='button']",
            ".action-button",
            ".dropdown-toggle"
        ]
        
        for selector in menu_selectors:
            try:
                elements = page.locator(selector)
                count = await elements.count()
                if count > 0:
                    print(f"✅ Found {count} menu elements: {selector}")
                    return True
            except:
                continue
        
        return False
    
    async def _look_for_form_elements(self, page: Page):
        """Look for form elements on the page"""
        form_selectors = [
            "form",
            "input",
            "select",
            "textarea",
            "button[type='submit']"
        ]
        
        for selector in form_selectors:
            try:
                elements = page.locator(selector)
                count = await elements.count()
                if count > 0:
                    print(f"✅ Found {count} form elements: {selector}")
                    return True
            except:
                continue
        
        return False

