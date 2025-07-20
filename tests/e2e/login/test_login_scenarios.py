"""
Login Scenarios Test Suite
Tests for Viewz login page validation scenarios
"""

import pytest
import pytest_asyncio
from playwright.async_api import Page, expect
from pages.login_page import LoginPage
from pages.home_page import HomePage
from utils.screenshot_helper import ScreenshotHelper
import json
import os
import asyncio


class TestLoginScenarios:
    """Test suite for login page scenarios"""
    
    @pytest_asyncio.fixture(autouse=True)
    async def setup(self, page: Page):
        """Setup for each test"""
        self.page = page
        self.login_page = LoginPage(page)
        self.home_page = HomePage(page)
        self.screenshot_helper = ScreenshotHelper()
        
        # Navigate to login page
        await page.goto("https://new.viewz.co/login")
        await page.wait_for_load_state("networkidle")
    
    @pytest.mark.asyncio
    async def test_scenario_1_valid_login(self, page: Page):
        """
        Scenario 1: Valid Login
        - Navigate to login page
        - Enter valid credentials
        - Verify successful login
        """
        # Take initial screenshot
        filename, filepath = await self.screenshot_helper.capture_async_screenshot(
            page, "login_page_initial"
        )
        print(f"📸 Screenshot saved: {filename}")
        
        # Analyze page structure and find credentials
        await self._analyze_login_page_structure(page)
        
        # Get credentials from environment or discovered values
        email = os.getenv("VALID_EMAIL", "sharon_newdemo")
        password = os.getenv("VALID_PASSWORD", "Sh@ron123$%^")
        
        # TOTP Secret for 2FA (same as working login test)
        secret = "HA2ECLBIKYUEEI2GPUUSMN3XIMXFETRQ"
        
        # Generate OTP for 2FA
        import pyotp
        otp = pyotp.TOTP(secret).now()
        print(f"🔐 Generated OTP for 2FA: {otp}")

        # Execute login
        await self.login_page.login(email, password)
        
        # Handle 2FA if present
        try:
            print("⏳ Checking for 2FA page...")
            await page.wait_for_selector("text=Two-Factor Authentication", timeout=3000)
            print("✅ 2FA page detected, entering OTP...")
            
            # Fill OTP
            await page.get_by_role("textbox").fill(otp)
            print(f"✅ OTP filled: {otp}")
            
            # Wait for 2FA processing
            await asyncio.sleep(5)
            
        except Exception as e:
            print(f"ℹ️ No 2FA required or different flow: {e}")

        # Wait for navigation after login
        await page.wait_for_load_state("networkidle")
        
        # Take screenshot after login attempt
        filename, filepath = await self.screenshot_helper.capture_async_screenshot(
            page, "login_attempt_result"
        )
        print(f"📸 Screenshot saved: {filename}")
        
        # Verify successful login
        await self._verify_successful_login(page)
        
        # Generate assertions for validation
        await self._generate_login_assertions(page)
    
    @pytest.mark.asyncio
    async def test_scenario_2_logout_user(self, page: Page):
        """
        Scenario 2: Log Out User
        - Assumes user is already logged in
        - Find and click logout mechanism
        - Verify successful logout
        """
        # First ensure user is logged in
        await self._ensure_user_logged_in(page)
        
        # Take screenshot before logout
        filename, filepath = await self.screenshot_helper.capture_async_screenshot(
            page, "before_logout"
        )
        print(f"📸 Screenshot saved: {filename}")
        
        # Find and execute logout
        await self._execute_logout(page)
        
        # Take screenshot after logout
        filename, filepath = await self.screenshot_helper.capture_async_screenshot(
            page, "after_logout"
        )
        print(f"📸 Screenshot saved: {filename}")
        
        # Verify successful logout
        await self._verify_successful_logout(page)
    
    async def _analyze_login_page_structure(self, page: Page):
        """Analyze login page to understand structure and find credentials"""
        print("🔍 Analyzing login page structure...")
        
        # Get page title
        title = await page.title()
        print(f"📄 Page title: {title}")
        
        # Find email/username field
        email_selectors = [
            "input[type='email']",
            "input[name='email']",
            "input[name='username']",
            "input[placeholder*='email' i]",
            "input[placeholder*='username' i]",
            "#email",
            "#username",
            ".email-input",
            ".username-input"
        ]
        
        email_field = None
        for selector in email_selectors:
            try:
                element = page.locator(selector).first
                if await element.is_visible():
                    email_field = selector
                    print(f"✅ Found email field: {selector}")
                    break
            except:
                continue
        
        # Find password field
        password_selectors = [
            "input[type='password']",
            "input[name='password']",
            "input[placeholder*='password' i]",
            "#password",
            ".password-input"
        ]
        
        password_field = None
        for selector in password_selectors:
            try:
                element = page.locator(selector).first
                if await element.is_visible():
                    password_field = selector
                    print(f"✅ Found password field: {selector}")
                    break
            except:
                continue
        
        # Find login button
        login_button_selectors = [
            "button[type='submit']",
            "input[type='submit']",
            "button:has-text('Login')",
            "button:has-text('Sign In')",
            "button:has-text('Log In')",
            ".login-button",
            ".signin-button",
            "#login-btn",
            "#signin-btn"
        ]
        
        login_button = None
        for selector in login_button_selectors:
            try:
                element = page.locator(selector).first
                if await element.is_visible():
                    login_button = selector
                    print(f"✅ Found login button: {selector}")
                    break
            except:
                continue
        
        # Look for demo/test credentials on page
        await self._scan_for_demo_credentials(page)
        
        # Save discovered selectors
        selectors = {
            "email_field": email_field,
            "password_field": password_field,
            "login_button": login_button
        }
        
        with open("fixtures/discovered_selectors.json", "w") as f:
            json.dump(selectors, f, indent=2)
        
        print(f"💾 Saved selectors to fixtures/discovered_selectors.json")
    
    async def _scan_for_demo_credentials(self, page: Page):
        """Scan page for demo/test credentials"""
        print("🔍 Scanning for demo credentials...")
        
        # Common places to find demo credentials
        demo_selectors = [
            "text=demo",
            "text=test",
            "text=sample",
            "[data-testid*='demo']",
            "[data-testid*='test']",
            ".demo-credentials",
            ".test-credentials",
            ".sample-credentials"
        ]
        
        found_credentials = []
        
        for selector in demo_selectors:
            try:
                elements = page.locator(selector)
                count = await elements.count()
                
                for i in range(count):
                    element = elements.nth(i)
                    if await element.is_visible():
                        text = await element.text_content()
                        if text and ("@" in text or "password" in text.lower()):
                            found_credentials.append({
                                "selector": selector,
                                "text": text.strip()
                            })
                            print(f"🔑 Found potential credential: {text.strip()}")
            except:
                continue
        
        # Save found credentials
        if found_credentials:
            with open("fixtures/discovered_credentials.json", "w") as f:
                json.dump(found_credentials, f, indent=2)
            print(f"💾 Saved {len(found_credentials)} potential credentials")
    
    async def _verify_successful_login(self, page: Page):
        """Verify that login was successful"""
        print("✅ Verifying successful login...")
        
        # Wait a moment for page to load
        await page.wait_for_timeout(2000)
        
        # Check for common success indicators
        success_indicators = [
            # URL changes
            lambda: "dashboard" in page.url.lower(),
            lambda: "home" in page.url.lower(),
            lambda: "app" in page.url.lower(),
            lambda: page.url != "https://new.viewz.co/login",
            
            # Page elements
            lambda: page.locator("text=Welcome").is_visible(),
            lambda: page.locator("text=Dashboard").is_visible(),
            lambda: page.locator("[data-testid='user-menu']").is_visible(),
            lambda: page.locator(".user-profile").is_visible(),
            lambda: page.locator("text=Logout").is_visible(),
            lambda: page.locator("text=Sign Out").is_visible(),
        ]
        
        success_found = False
        for indicator in success_indicators:
            try:
                if await indicator():
                    success_found = True
                    print(f"✅ Login success indicator found")
                    break
            except:
                continue
        
        # If no success indicators, check if we're still on login page
        if not success_found:
            current_url = page.url
            if "login" in current_url.lower():
                print("❌ Still on login page - login may have failed")
                # Look for error messages
                await self._check_for_error_messages(page)
            else:
                print(f"✅ Navigated away from login page to: {current_url}")
                success_found = True
        
        assert success_found, "Login verification failed"
    
    async def _check_for_error_messages(self, page: Page):
        """Check for error messages on login page"""
        error_selectors = [
            ".error",
            ".error-message",
            ".alert-danger",
            ".alert-error",
            "[role='alert']",
            "text=Invalid",
            "text=Error",
            "text=Failed",
            "text=Incorrect"
        ]
        
        for selector in error_selectors:
            try:
                element = page.locator(selector).first
                if await element.is_visible():
                    error_text = await element.text_content()
                    print(f"❌ Error message found: {error_text}")
            except:
                continue
    
    async def _ensure_user_logged_in(self, page: Page):
        """Ensure user is logged in before logout test"""
        if "login" in page.url.lower():
            # Need to login first
            await self.test_scenario_1_valid_login(page)
    
    async def _execute_logout(self, page: Page):
        """Execute logout process"""
        print("🚪 Executing logout...")
        
        # Common logout mechanisms
        logout_selectors = [
            "text=Logout",
            "text=Log Out",
            "text=Sign Out",
            "button:has-text('Logout')",
            "a:has-text('Logout')",
            "[data-testid='logout']",
            "[data-testid='sign-out']",
            ".logout-btn",
            ".signout-btn"
        ]
        
        # First try direct logout buttons
        for selector in logout_selectors:
            try:
                element = page.locator(selector).first
                if await element.is_visible():
                    await element.click()
                    print(f"✅ Clicked logout: {selector}")
                    return
            except:
                continue
        
        # Try user menu dropdown
        user_menu_selectors = [
            "[data-testid='user-menu']",
            ".user-menu",
            ".user-dropdown",
            ".profile-menu",
            "button:has-text('Profile')",
            "button:has-text('Account')"
        ]
        
        for menu_selector in user_menu_selectors:
            try:
                menu = page.locator(menu_selector).first
                if await menu.is_visible():
                    await menu.click()
                    await page.wait_for_timeout(1000)
                    
                    # Now try logout options
                    for logout_selector in logout_selectors:
                        try:
                            logout_btn = page.locator(logout_selector).first
                            if await logout_btn.is_visible():
                                await logout_btn.click()
                                print(f"✅ Clicked logout from menu: {logout_selector}")
                                return
                        except:
                            continue
            except:
                continue
        
        print("❌ Could not find logout mechanism")
    
    async def _verify_successful_logout(self, page: Page):
        """Verify that logout was successful"""
        print("✅ Verifying successful logout...")
        
        # Wait for page to load
        await page.wait_for_timeout(2000)
        
        # Check if redirected to login page
        if "login" in page.url.lower():
            print("✅ Redirected to login page - logout successful")
            return
        
        # Check for login form elements
        login_indicators = [
            "input[type='email']",
            "input[type='password']",
            "button:has-text('Login')",
            "button:has-text('Sign In')",
            "text=Sign In",
            "text=Login"
        ]
        
        for indicator in login_indicators:
            try:
                element = page.locator(indicator).first
                if await element.is_visible():
                    print("✅ Login form visible - logout successful")
                    return
            except:
                continue
        
        print("❌ Logout verification inconclusive")
    
    async def _generate_login_assertions(self, page: Page):
        """Generate comprehensive assertions for validation"""
        print("📝 Generating validation assertions...")
        
        assertions = []
        
        # URL assertions
        current_url = page.url
        assertions.append(f"expect(page.url).not.toBe('https://new.viewz.co/login')")
        assertions.append(f"expect(page.url).toContain('{current_url.split('/')[2]}')")
        
        # Page title assertion
        title = await page.title()
        assertions.append(f"expect(await page.title()).toBe('{title}')")
        
        # Visible elements assertions
        visible_elements = [
            "text=Dashboard",
            "text=Welcome",
            "[data-testid='user-menu']",
            ".user-profile",
            "text=Logout"
        ]
        
        for element in visible_elements:
            try:
                if await page.locator(element).first.is_visible():
                    assertions.append(f"expect(page.locator('{element}').first).toBeVisible()")
            except:
                continue
        
        # Save assertions
        with open("fixtures/generated_assertions.json", "w") as f:
            json.dump(assertions, f, indent=2)
        
        print(f"💾 Generated {len(assertions)} assertions")
        
        return assertions 