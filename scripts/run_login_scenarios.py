#!/usr/bin/env python3
"""
Viewz Login Scenarios - Python Script
Executes login scenarios for https://new.viewz.co/login using Playwright Python

This script can be run directly:
    python scripts/run_login_scenarios.py

Or with pytest:
    pytest scripts/run_login_scenarios.py -v -s
"""

import asyncio
import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from playwright.async_api import async_playwright, Page, Browser, BrowserContext
from utils.screenshot_helper import ScreenshotHelper


class ViewzLoginScenarios:
    """Execute Viewz login scenarios with comprehensive analysis"""
    
    def __init__(self):
        self.screenshot_helper = ScreenshotHelper()
        self.discovered_selectors = {}
        self.discovered_credentials = []
        self.test_results = {
            "navigation": False,
            "page_analysis": False,
            "valid_login": False,
            "logout": False
        }
        
    async def run_all_scenarios(self) -> Dict:
        """Run all login scenarios and return results"""
        print("🚀 Starting Viewz Login Scenarios")
        print("=" * 50)
        
        async with async_playwright() as p:
            # Launch browser
            browser = await p.chromium.launch(
                headless=False,  # Set to True for headless mode
                args=["--start-maximized"]
            )
            
            context = await browser.new_context(
                viewport=None,  # Use full screen
                record_video_dir="mcp-output/videos" if os.path.exists("mcp-output") else None
            )
            
            page = await context.new_page()
            
            try:
                # Execute scenarios
                await self.scenario_setup(page)
                await self.analyze_page_structure(page)
                await self.scenario_1_valid_login(page)
                await self.scenario_2_logout_user(page)
                
                # Generate final report
                await self.generate_final_report(page)
                
            except Exception as e:
                print(f"❌ Error during execution: {str(e)}")
                await self.screenshot_helper.capture_async_screenshot(page, "error_state")
                
            finally:
                await browser.close()
        
        return self.test_results
    
    async def scenario_setup(self, page: Page):
        """Setup and navigate to login page"""
        print("📍 Scenario Setup: Navigate to login page")
        
        try:
            # Navigate to login page
            await page.goto("https://new.viewz.co/login", wait_until="networkidle")
            
            # Take initial screenshot
            filename, filepath = await self.screenshot_helper.capture_async_screenshot(
                page, "login_page_initial"
            )
            print(f"📸 Initial screenshot: {filename}")
            
            # Verify we're on the right page
            current_url = page.url
            if "login" in current_url.lower():
                print(f"✅ Successfully navigated to: {current_url}")
                self.test_results["navigation"] = True
            else:
                print(f"❌ Unexpected URL: {current_url}")
                
        except Exception as e:
            print(f"❌ Navigation failed: {str(e)}")
    
    async def analyze_page_structure(self, page: Page):
        """Analyze page structure and find credentials"""
        print("\n🔍 Analyzing page structure...")
        
        try:
            # Get page title
            title = await page.title()
            print(f"📄 Page title: {title}")
            
            # Find form elements
            await self._find_form_elements(page)
            
            # Scan for demo credentials
            await self._scan_for_demo_credentials(page)
            
            # Save discovered information
            await self._save_discovered_data()
            
            self.test_results["page_analysis"] = True
            print("✅ Page analysis completed")
            
        except Exception as e:
            print(f"❌ Page analysis failed: {str(e)}")
    
    async def _find_form_elements(self, page: Page):
        """Find email, password, and login button elements"""
        print("🔍 Finding form elements...")
        
        # Email field selectors
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
        
        # Find email field
        for selector in email_selectors:
            try:
                element = page.locator(selector).first
                if await element.is_visible():
                    self.discovered_selectors["email_field"] = selector
                    print(f"✅ Found email field: {selector}")
                    break
            except:
                continue
        
        # Password field selectors
        password_selectors = [
            "input[type='password']",
            "input[name='password']",
            "input[placeholder*='password' i]",
            "#password",
            ".password-input"
        ]
        
        # Find password field
        for selector in password_selectors:
            try:
                element = page.locator(selector).first
                if await element.is_visible():
                    self.discovered_selectors["password_field"] = selector
                    print(f"✅ Found password field: {selector}")
                    break
            except:
                continue
        
        # Login button selectors
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
        
        # Find login button
        for selector in login_button_selectors:
            try:
                element = page.locator(selector).first
                if await element.is_visible():
                    self.discovered_selectors["login_button"] = selector
                    print(f"✅ Found login button: {selector}")
                    break
            except:
                continue
    
    async def _scan_for_demo_credentials(self, page: Page):
        """Scan page for demo/test credentials"""
        print("🔑 Scanning for demo credentials...")
        
        # Demo credential selectors
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
        
        for selector in demo_selectors:
            try:
                elements = page.locator(selector)
                count = await elements.count()
                
                for i in range(count):
                    element = elements.nth(i)
                    if await element.is_visible():
                        text = await element.text_content()
                        if text and ("@" in text or "password" in text.lower()):
                            credential = {
                                "selector": selector,
                                "text": text.strip(),
                                "index": i
                            }
                            self.discovered_credentials.append(credential)
                            print(f"🔑 Found potential credential: {text.strip()}")
            except:
                continue
        
        # Also check page content for credentials
        await self._check_page_content_for_credentials(page)
    
    async def _check_page_content_for_credentials(self, page: Page):
        """Check page content for visible credentials"""
        try:
            page_content = await page.content()
            
            # Look for email patterns
            import re
            email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
            emails = re.findall(email_pattern, page_content)
            
            for email in emails:
                if any(keyword in email.lower() for keyword in ['demo', 'test', 'sample', 'admin']):
                    credential = {
                        "type": "email",
                        "value": email,
                        "source": "page_content"
                    }
                    self.discovered_credentials.append(credential)
                    print(f"📧 Found email in content: {email}")
                    
        except Exception as e:
            print(f"❌ Error checking page content: {str(e)}")
    
    async def _save_discovered_data(self):
        """Save discovered selectors and credentials"""
        # Save selectors
        with open("fixtures/discovered_selectors.json", "w") as f:
            json.dump(self.discovered_selectors, f, indent=2)
        
        # Save credentials
        if self.discovered_credentials:
            with open("fixtures/discovered_credentials.json", "w") as f:
                json.dump(self.discovered_credentials, f, indent=2)
            print(f"💾 Saved {len(self.discovered_credentials)} potential credentials")
        
        print(f"💾 Saved selectors to fixtures/discovered_selectors.json")
    
    async def scenario_1_valid_login(self, page: Page):
        """Execute Scenario 1: Valid Login"""
        print("\n🎯 Scenario 1: Valid Login")
        
        try:
            # Get credentials
            email, password = self._get_test_credentials()
            
            # Fill email field
            if "email_field" in self.discovered_selectors:
                email_selector = self.discovered_selectors["email_field"]
                await page.fill(email_selector, email)
                print(f"✅ Filled email: {email}")
            else:
                print("❌ Email field not found")
                return
            
            # Fill password field
            if "password_field" in self.discovered_selectors:
                password_selector = self.discovered_selectors["password_field"]
                await page.fill(password_selector, password)
                print(f"✅ Filled password: {'*' * len(password)}")
            else:
                print("❌ Password field not found")
                return
            
            # Click login button
            if "login_button" in self.discovered_selectors:
                login_selector = self.discovered_selectors["login_button"]
                await page.click(login_selector)
                print(f"✅ Clicked login button")
            else:
                print("❌ Login button not found")
                return
            
            # Wait for navigation
            await page.wait_for_timeout(3000)
            
            # Take screenshot after login attempt
            filename, filepath = await self.screenshot_helper.capture_async_screenshot(
                page, "login_attempt_result"
            )
            print(f"📸 Login attempt screenshot: {filename}")
            
            # Verify login success
            login_successful = await self._verify_login_success(page)
            self.test_results["valid_login"] = login_successful
            
            if login_successful:
                print("✅ Login successful!")
            else:
                print("❌ Login failed")
                await self._check_for_error_messages(page)
                
        except Exception as e:
            print(f"❌ Login scenario failed: {str(e)}")
    
    def _get_test_credentials(self) -> Tuple[str, str]:
        """Get test credentials from environment or discovered credentials"""
        # Try environment variables first
        email = os.getenv("VALID_EMAIL")
        password = os.getenv("VALID_PASSWORD")
        
        if email and password:
            return email, password
        
        # Try discovered credentials
        for cred in self.discovered_credentials:
            if cred.get("type") == "email":
                email = cred["value"]
                break
        
        # Default test credentials
        if not email:
            email = "demo@viewz.co"
        if not password:
            password = "demo123"
        
        return email, password
    
    async def _verify_login_success(self, page: Page) -> bool:
        """Verify that login was successful"""
        print("✅ Verifying login success...")
        
        # Wait for page to load
        await page.wait_for_timeout(2000)
        
        current_url = page.url
        
        # Check if URL changed from login page
        if "login" not in current_url.lower():
            print(f"✅ Navigated away from login page to: {current_url}")
            return True
        
        # Check for success indicators
        success_selectors = [
            "text=Dashboard",
            "text=Welcome",
            "[data-testid='user-menu']",
            ".user-profile",
            "text=Logout",
            "text=Sign Out"
        ]
        
        for selector in success_selectors:
            try:
                element = page.locator(selector).first
                if await element.is_visible():
                    print(f"✅ Found success indicator: {selector}")
                    return True
            except:
                continue
        
        return False
    
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
                    print(f"❌ Error message: {error_text}")
            except:
                continue
    
    async def scenario_2_logout_user(self, page: Page):
        """Execute Scenario 2: Logout User"""
        print("\n🚪 Scenario 2: Logout User")
        
        try:
            # Ensure we're logged in
            if not self.test_results["valid_login"]:
                print("❌ Cannot logout - user not logged in")
                return
            
            # Take screenshot before logout
            filename, filepath = await self.screenshot_helper.capture_async_screenshot(
                page, "before_logout"
            )
            print(f"📸 Before logout screenshot: {filename}")
            
            # Find and execute logout
            logout_successful = await self._execute_logout(page)
            
            # Take screenshot after logout
            filename, filepath = await self.screenshot_helper.capture_async_screenshot(
                page, "after_logout"
            )
            print(f"📸 After logout screenshot: {filename}")
            
            # Verify logout
            if logout_successful:
                logout_verified = await self._verify_logout_success(page)
                self.test_results["logout"] = logout_verified
                
                if logout_verified:
                    print("✅ Logout successful!")
                else:
                    print("❌ Logout verification failed")
            else:
                print("❌ Logout execution failed")
                
        except Exception as e:
            print(f"❌ Logout scenario failed: {str(e)}")
    
    async def _execute_logout(self, page: Page) -> bool:
        """Execute logout process"""
        print("🔍 Looking for logout mechanism...")
        
        # Direct logout selectors
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
        
        # Try direct logout first
        for selector in logout_selectors:
            try:
                element = page.locator(selector).first
                if await element.is_visible():
                    await element.click()
                    print(f"✅ Clicked logout: {selector}")
                    return True
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
                    print(f"✅ Opened user menu: {menu_selector}")
                    await page.wait_for_timeout(1000)
                    
                    # Try logout from menu
                    for logout_selector in logout_selectors:
                        try:
                            logout_btn = page.locator(logout_selector).first
                            if await logout_btn.is_visible():
                                await logout_btn.click()
                                print(f"✅ Clicked logout from menu: {logout_selector}")
                                return True
                        except:
                            continue
            except:
                continue
        
        print("❌ Could not find logout mechanism")
        return False
    
    async def _verify_logout_success(self, page: Page) -> bool:
        """Verify that logout was successful"""
        print("✅ Verifying logout success...")
        
        # Wait for redirect
        await page.wait_for_timeout(3000)
        
        current_url = page.url
        
        # Check if redirected to login page
        if "login" in current_url.lower():
            print("✅ Redirected to login page")
            return True
        
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
                    print(f"✅ Login form visible: {indicator}")
                    return True
            except:
                continue
        
        return False
    
    async def generate_final_report(self, page: Page):
        """Generate final test report"""
        print("\n📊 Test Results Summary")
        print("=" * 30)
        
        results = self.test_results
        
        print(f"✅ Navigation to login page: {'SUCCESS' if results['navigation'] else 'FAILED'}")
        print(f"✅ Page structure analysis: {'SUCCESS' if results['page_analysis'] else 'FAILED'}")
        print(f"{'✅' if results['valid_login'] else '❌'} Scenario 1 (Valid Login): {'SUCCESS' if results['valid_login'] else 'FAILED'}")
        print(f"{'✅' if results['logout'] else '❌'} Scenario 2 (Logout): {'SUCCESS' if results['logout'] else 'FAILED'}")
        
        # Generate assertions
        await self._generate_assertions()
        
        # Take final screenshot
        filename, filepath = await self.screenshot_helper.capture_async_screenshot(
            page, "test_complete"
        )
        print(f"\n📸 Final screenshot: {filename}")
        
        # Save final report
        report = {
            "timestamp": datetime.now().isoformat(),
            "test_results": self.test_results,
            "discovered_selectors": self.discovered_selectors,
            "discovered_credentials": len(self.discovered_credentials),
            "url": page.url,
            "title": await page.title()
        }
        
        with open("fixtures/test_report.json", "w") as f:
            json.dump(report, f, indent=2)
        
        print(f"💾 Test report saved to fixtures/test_report.json")
        
        # Success rate
        success_count = sum(1 for result in results.values() if result)
        total_count = len(results)
        success_rate = (success_count / total_count) * 100
        
        print(f"\n🎯 Overall Success Rate: {success_rate:.1f}% ({success_count}/{total_count})")
    
    async def _generate_assertions(self):
        """Generate test assertions"""
        print("\n📝 Generated Assertions:")
        
        assertions = []
        
        # URL assertions
        assertions.append("# URL Assertions")
        assertions.append("expect(page.url).not.toBe('https://new.viewz.co/login')")
        assertions.append("expect(page.url).toContain('viewz.co')")
        assertions.append("")
        
        # Element assertions
        assertions.append("# Element Assertions")
        if "email_field" in self.discovered_selectors:
            assertions.append(f"expect(page.locator('{self.discovered_selectors['email_field']}').first).toBeVisible()")
        if "password_field" in self.discovered_selectors:
            assertions.append(f"expect(page.locator('{self.discovered_selectors['password_field']}').first).toBeVisible()")
        if "login_button" in self.discovered_selectors:
            assertions.append(f"expect(page.locator('{self.discovered_selectors['login_button']}').first).toBeVisible()")
        
        assertions.append("")
        assertions.append("# Success Assertions")
        assertions.append("expect(page.locator('text=Dashboard').first).toBeVisible()")
        assertions.append("expect(page.locator('[data-testid=\"user-menu\"]').first).toBeVisible()")
        assertions.append("expect(page.locator('text=Logout').first).toBeVisible()")
        
        # Save assertions
        with open("fixtures/generated_assertions.txt", "w") as f:
            f.write("\n".join(assertions))
        
        # Print assertions
        for assertion in assertions:
            print(f"  {assertion}")
        
        print(f"\n💾 Assertions saved to fixtures/generated_assertions.txt")


async def main():
    """Main execution function"""
    # Create fixtures directory
    os.makedirs("fixtures", exist_ok=True)
    os.makedirs("mcp-output", exist_ok=True)
    
    # Run scenarios
    scenarios = ViewzLoginScenarios()
    results = await scenarios.run_all_scenarios()
    
    # Print final status
    print("\n" + "=" * 50)
    print("🎉 Viewz Login Scenarios Completed!")
    print("=" * 50)
    
    return results


if __name__ == "__main__":
    # Run the scenarios
    results = asyncio.run(main())
    
    # Exit with appropriate code
    success_count = sum(1 for result in results.values() if result)
    if success_count == len(results):
        print("✅ All scenarios passed!")
        sys.exit(0)
    else:
        print(f"❌ {len(results) - success_count} scenarios failed")
        sys.exit(1) 