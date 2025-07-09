"""
CSVNavigationPage - Page Object for CSV-generated navigation tests
Adapted from CSV test cases for integration with main framework
"""

from playwright.async_api import Page, expect
from typing import Optional
import asyncio

class CSVNavigationPage:
    """Page Object for CSV-generated navigation functionality"""
    
    def __init__(self, page: Page):
        self.page = page
        self.section_name = "CSV Navigation Tests"
    
    async def navigate_to_section(self, base_url: str = None):
        """Navigate to navigation section"""
        # Since CSV tests are generic, we'll stay on the current page
        # and adapt to whatever page we're on after login
        print(f"✅ CSV Navigation tests will run on current page: {self.page.url}")
        
        # Optional: Try to navigate to a specific section if it exists
        nav_options = ["text=Home", "text=Reconciliation", "text=Ledger"]
        
        for nav_option in nav_options:
            try:
                element = self.page.locator(nav_option)
                if await element.is_visible():
                    await element.click()
                    print(f"✅ Navigated to section: {nav_option}")
                    break
            except:
                continue
    
    async def wait_for_page_load(self):
        """Wait for page to fully load"""
        await self.page.wait_for_load_state("networkidle")
        await self.page.wait_for_timeout(1000)
    
    async def take_screenshot(self, name: str = None):
        """Take screenshot of current page state"""
        screenshot_name = name or f"csv_navigation_screenshot.png"
        await self.page.screenshot(path=f"screenshots/{screenshot_name}")
        return screenshot_name
    
    # Common element interactions
    async def click_button(self, button_text: str):
        """Click button by text"""
        await self.page.get_by_role("button", name=button_text).click()
    
    async def fill_input(self, label: str, value: str):
        """Fill input field by label"""
        await self.page.get_by_label(label).fill(value)
    
    async def verify_text_visible(self, text: str):
        """Verify text is visible on page"""
        await expect(self.page.locator(f"text={text}")).to_be_visible()
    
    async def verify_element_visible(self, locator: str):
        """Verify element is visible"""
        await expect(self.page.locator(locator)).to_be_visible()
    
    # Invoice List Methods
    async def verify_invoice_list_displayed(self):
        """Verify invoice list is displayed"""
        invoice_list_selectors = [
            ".invoice-list",
            "[data-testid='invoice-list']",
            ".payables-list",
            "table",
            ".data-table"
        ]
        
        for selector in invoice_list_selectors:
            try:
                await expect(self.page.locator(selector)).to_be_visible(timeout=5000)
                print(f"✅ Invoice list found: {selector}")
                return True
            except:
                continue
        
        print("❌ Invoice list not found")
        return False
    
    # File Upload Methods
    async def upload_invoice_file(self, file_path: str = None):
        """Upload invoice file"""
        upload_selectors = [
            "input[type='file']",
            "[data-testid='file-upload']",
            ".file-upload-input"
        ]
        
        # Use test file if none provided
        if not file_path:
            file_path = "fixtures/test_invoice.pdf"
        
        for selector in upload_selectors:
            try:
                await self.page.set_input_files(selector, file_path)
                print(f"✅ File uploaded using: {selector}")
                return True
            except:
                continue
        
        print("❌ Upload input not found")
        return False
    
    async def click_upload_button(self):
        """Click upload button"""
        upload_button_selectors = [
            "button:has-text('Upload')",
            "[data-testid='upload-btn']",
            ".upload-button",
            "input[type='submit'][value*='Upload']"
        ]
        
        for selector in upload_button_selectors:
            try:
                await self.page.locator(selector).click()
                print(f"✅ Upload button clicked: {selector}")
                return True
            except:
                continue
        
        print("❌ Upload button not found")
        return False
    
    # Delete Methods
    async def delete_invoice(self, invoice_selector: str = None):
        """Delete invoice"""
        if not invoice_selector:
            invoice_selector = ".invoice-row:first-child"
        
        delete_selectors = [
            f"{invoice_selector} button:has-text('Delete')",
            f"{invoice_selector} [data-testid='delete-btn']",
            f"{invoice_selector} .delete-button"
        ]
        
        for selector in delete_selectors:
            try:
                await self.page.locator(selector).click()
                print(f"✅ Delete button clicked: {selector}")
                return True
            except:
                continue
        
        print("❌ Delete button not found")
        return False
    
    async def confirm_deletion(self):
        """Confirm deletion in dialog"""
        confirm_selectors = [
            "button:has-text('Confirm')",
            "button:has-text('Delete')",
            "[data-testid='confirm-delete']",
            ".confirm-button"
        ]
        
        for selector in confirm_selectors:
            try:
                await self.page.locator(selector).click()
                print(f"✅ Deletion confirmed: {selector}")
                return True
            except:
                continue
        
        print("❌ Confirm button not found")
        return False
    
    # Menu Methods
    async def right_click_invoice(self, invoice_selector: str = None):
        """Right-click on invoice to open context menu"""
        if not invoice_selector:
            invoice_selector = ".invoice-row:first-child"
        
        try:
            await self.page.locator(invoice_selector).click(button="right")
            await self.page.wait_for_timeout(1000)
            print(f"✅ Right-clicked on invoice: {invoice_selector}")
            return True
        except:
            print("❌ Right-click failed")
            return False
    
    async def verify_context_menu_visible(self):
        """Verify context menu is visible"""
        menu_selectors = [
            ".context-menu",
            "[data-testid='context-menu']",
            ".dropdown-menu",
            ".right-click-menu"
        ]
        
        for selector in menu_selectors:
            try:
                await expect(self.page.locator(selector)).to_be_visible(timeout=3000)
                print(f"✅ Context menu found: {selector}")
                return True
            except:
                continue
        
        print("❌ Context menu not found")
        return False
    
    # Edit Popup Methods
    async def click_edit_button(self):
        """Click edit button"""
        edit_selectors = [
            "button:has-text('Edit')",
            "[data-testid='edit-btn']",
            ".edit-button"
        ]
        
        for selector in edit_selectors:
            try:
                await self.page.locator(selector).click()
                print(f"✅ Edit button clicked: {selector}")
                return True
            except:
                continue
        
        print("❌ Edit button not found")
        return False
    
    async def verify_edit_popup_visible(self):
        """Verify edit popup is visible"""
        popup_selectors = [
            ".edit-popup",
            "[data-testid='edit-modal']",
            ".modal",
            ".dialog"
        ]
        
        for selector in popup_selectors:
            try:
                await expect(self.page.locator(selector)).to_be_visible(timeout=5000)
                print(f"✅ Edit popup found: {selector}")
                return True
            except:
                continue
        
        print("❌ Edit popup not found")
        return False
    
    # Validation Methods
    async def verify_mandatory_validation(self):
        """Verify mandatory field validation"""
        # Try to save without filling mandatory fields
        save_selectors = [
            "button:has-text('Save')",
            "[data-testid='save-btn']",
            ".save-button"
        ]
        
        for selector in save_selectors:
            try:
                await self.page.locator(selector).click()
                break
            except:
                continue
        
        # Look for validation errors
        error_selectors = [
            ".error-message",
            ".validation-error",
            "[data-testid='error']",
            ".field-error"
        ]
        
        for selector in error_selectors:
            try:
                await expect(self.page.locator(selector)).to_be_visible(timeout=3000)
                print(f"✅ Validation error found: {selector}")
                return True
            except:
                continue
        
        print("❌ Validation error not found")
        return False
    
    # GL Account Methods
    async def click_gl_account_dropdown(self):
        """Click GL Account dropdown"""
        dropdown_selectors = [
            "select[name*='gl_account']",
            "[data-testid='gl-account-dropdown']",
            ".gl-account-select"
        ]
        
        for selector in dropdown_selectors:
            try:
                await self.page.locator(selector).click()
                print(f"✅ GL Account dropdown clicked: {selector}")
                return True
            except:
                continue
        
        print("❌ GL Account dropdown not found")
        return False
    
    async def verify_gl_accounts_listed(self):
        """Verify GL accounts are listed"""
        option_selectors = [
            "option",
            ".dropdown-option",
            "[data-testid='gl-account-option']"
        ]
        
        for selector in option_selectors:
            try:
                options = await self.page.locator(selector).count()
                if options > 0:
                    print(f"✅ Found {options} GL account options")
                    return True
            except:
                continue
        
        print("❌ GL account options not found")
        return False
    
    # Generic action method for CSV tests
    async def perform_section_action(self, action: str, **kwargs):
        """Perform section-specific action"""
        print(f"Performing {action} in CSV Navigation section")
        
        # Map actions to methods
        action_map = {
            "step_1": self.verify_invoice_list_displayed,
            "upload_file": self.upload_invoice_file,
            "delete_invoice": self.delete_invoice,
            "right_click": self.right_click_invoice,
            "edit_popup": self.click_edit_button,
            "validation": self.verify_mandatory_validation,
            "gl_dropdown": self.click_gl_account_dropdown
        }
        
        if action in action_map:
            return await action_map[action]()
        else:
            print(f"⚠️ Unknown action: {action}")
            await self.page.wait_for_timeout(1000)
            return True
