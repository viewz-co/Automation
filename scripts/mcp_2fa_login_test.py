#!/usr/bin/env python3
"""
MCP-Powered 2FA Login & Logout Test
Uses the Playwright MCP server to execute login with 2FA and logout scenarios

Based on the existing test_login.py with TOTP authentication
"""

import asyncio
import json
import sys
import time
from typing import Dict, Any
import httpx
from datetime import datetime
import pyotp


class PlaywrightMCPClient:
    """Python client for Playwright MCP Server"""
    
    def __init__(self, server_url: str = "http://127.0.0.1:8931"):
        self.server_url = server_url
        
    async def send_command(self, tool: str, parameters: Dict[str, Any] = None) -> Dict[str, Any]:
        """Send a command to the MCP server"""
        if parameters is None:
            parameters = {}
            
        payload = {
            "method": "tools/call",
            "params": {
                "name": tool,
                "arguments": parameters
            }
        }
        
        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(
                    f"{self.server_url}/call",
                    json=payload,
                    headers={"Content-Type": "application/json"}
                )
                
                if response.status_code == 200:
                    return response.json()
                else:
                    return {
                        "error": f"HTTP {response.status_code}: {response.text}"
                    }
                    
        except Exception as e:
            return {"error": f"Request failed: {str(e)}"}
    
    async def browser_navigate(self, url: str) -> Dict[str, Any]:
        """Navigate to a URL"""
        return await self.send_command("browser_navigate", {"url": url})
    
    async def browser_snapshot(self) -> Dict[str, Any]:
        """Take a page snapshot"""
        return await self.send_command("browser_snapshot")
    
    async def browser_take_screenshot(self, filename: str = None) -> Dict[str, Any]:
        """Take a screenshot"""
        params = {}
        if filename:
            params["filename"] = filename
        return await self.send_command("browser_take_screenshot", params)
    
    async def browser_click(self, element: str, ref: str) -> Dict[str, Any]:
        """Click an element"""
        return await self.send_command("browser_click", {
            "element": element,
            "ref": ref
        })
    
    async def browser_type(self, element: str, ref: str, text: str) -> Dict[str, Any]:
        """Type text into an element"""
        return await self.send_command("browser_type", {
            "element": element,
            "ref": ref,
            "text": text
        })
    
    async def browser_wait_for(self, time: float = None, text: str = None) -> Dict[str, Any]:
        """Wait for time or text"""
        params = {}
        if time:
            params["time"] = time
        if text:
            params["text"] = text
        return await self.send_command("browser_wait_for", params)
    
    async def browser_get_url(self) -> Dict[str, Any]:
        """Get current page URL"""
        return await self.send_command("browser_get_url")


class TwoFactorLoginTest:
    """Execute 2FA login and logout test via MCP server"""
    
    def __init__(self):
        self.client = PlaywrightMCPClient()
        self.totp_secret = os.getenv('TEST_TOTP_SECRET')  # From original test
        self.test_results = {
            "navigation": False,
            "login_form_filled": False,
            "two_factor_auth": False,
            "login_success": False,
            "logout_success": False
        }
        
        # Load test data
        self.login_data = self._load_login_data()
    
    def _load_login_data(self) -> Dict[str, str]:
        """Load login data from fixtures"""
        try:
            with open("fixtures/test_data.json", "r") as f:
                data = json.load(f)
                return data.get("login_data", {
                    "username": "demo@viewz.co",
                    "password": "demo123"
                })
        except:
            return {
                "username": "demo@viewz.co", 
                "password": "demo123"
            }
    
    def generate_totp(self) -> str:
        """Generate TOTP code"""
        totp = pyotp.TOTP(self.totp_secret)
        current_otp = totp.now()
        print(f"🔐 Generated TOTP: {current_otp}")
        return current_otp
    
    async def run_full_test(self):
        """Run complete login and logout test"""
        print("🚀 Starting 2FA Login & Logout Test via MCP")
        print("=" * 50)
        
        try:
            # Step 1: Navigate to login page
            await self.step_1_navigate_to_login()
            
            # Step 2: Fill login form
            await self.step_2_fill_login_form()
            
            # Step 3: Handle 2FA
            await self.step_3_handle_two_factor_auth()
            
            # Step 4: Verify login success
            await self.step_4_verify_login_success()
            
            # Step 5: Execute logout
            await self.step_5_execute_logout()
            
            # Step 6: Generate report
            await self.step_6_generate_report()
            
        except Exception as e:
            print(f"❌ Test execution failed: {str(e)}")
            await self.client.browser_take_screenshot("test_error.png")
        
        return self.test_results
    
    async def step_1_navigate_to_login(self):
        """Navigate to login page"""
        print("\n📍 Step 1: Navigate to login page")
        
        # Navigate to login page (using the URL from your existing test)
        result = await self.client.browser_navigate("https://app.viewz.co/login")
        
        if "error" in result:
            print(f"❌ Navigation failed: {result['error']}")
            return
        
        print("✅ Navigated to login page")
        
        # Wait for page to load
        await self.client.browser_wait_for(time=3)
        
        # Take screenshot
        await self.client.browser_take_screenshot("01_login_page.png")
        print("📸 Login page screenshot captured")
        
        self.test_results["navigation"] = True
    
    async def step_2_fill_login_form(self):
        """Fill login form with credentials"""
        print("\n📝 Step 2: Fill login form")
        
        # Fill username/email
        email_result = await self.client.browser_type(
            "Email field",
            "input[type='email'], input[name='username'], input[name='email']",
            self.login_data["username"]
        )
        
        if "error" in email_result:
            print(f"❌ Email fill failed: {email_result['error']}")
            return
        
        print(f"✅ Email filled: {self.login_data['username']}")
        
        # Fill password
        password_result = await self.client.browser_type(
            "Password field",
            "input[type='password'], input[name='password']",
            self.login_data["password"]
        )
        
        if "error" in password_result:
            print(f"❌ Password fill failed: {password_result['error']}")
            return
        
        print("✅ Password filled")
        
        # Click login button
        login_result = await self.client.browser_click(
            "Login button",
            "button[type='submit'], button:has-text('Login'), button:has-text('Sign In')"
        )
        
        if "error" in login_result:
            print(f"❌ Login click failed: {login_result['error']}")
            return
        
        print("✅ Login button clicked")
        
        # Wait for response
        await self.client.browser_wait_for(time=3)
        
        # Take screenshot
        await self.client.browser_take_screenshot("02_after_login_click.png")
        print("📸 After login click screenshot captured")
        
        self.test_results["login_form_filled"] = True
    
    async def step_3_handle_two_factor_auth(self):
        """Handle Two-Factor Authentication"""
        print("\n🔐 Step 3: Handle Two-Factor Authentication")
        
        # Wait for 2FA page to appear
        print("⏳ Waiting for 2FA page...")
        await self.client.browser_wait_for(text="Two-Factor Authentication")
        
        # Take screenshot of 2FA page
        await self.client.browser_take_screenshot("03_2fa_page.png")
        print("📸 2FA page screenshot captured")
        
        # Generate TOTP code
        otp_code = self.generate_totp()
        
        # Fill OTP field
        otp_result = await self.client.browser_type(
            "OTP field",
            "input[type='text'], input[name='otp'], input[name='code'], [role='textbox']",
            otp_code
        )
        
        if "error" in otp_result:
            print(f"❌ OTP fill failed: {otp_result['error']}")
            return
        
        print(f"✅ OTP filled: {otp_code}")
        
        # Wait a moment (as in original test)
        await self.client.browser_wait_for(time=5)
        
        # Try to click verify button if it exists
        verify_result = await self.client.browser_click(
            "Verify button",
            "button[type='verify'], button:has-text('Verify'), button:has-text('Submit')"
        )
        
        if "error" not in verify_result:
            print("✅ Verify button clicked")
        else:
            print("ℹ️ No verify button found, form may auto-submit")
        
        # Wait for 2FA processing
        await self.client.browser_wait_for(time=5)
        
        # Take screenshot after 2FA
        await self.client.browser_take_screenshot("04_after_2fa.png")
        print("📸 After 2FA screenshot captured")
        
        self.test_results["two_factor_auth"] = True
    
    async def step_4_verify_login_success(self):
        """Verify login was successful"""
        print("\n✅ Step 4: Verify login success")
        
        # Get current URL
        url_result = await self.client.browser_get_url()
        
        if "error" not in url_result:
            current_url = url_result.get("url", "")
            print(f"📍 Current URL: {current_url}")
            
            # Check if we're no longer on login page
            if "login" not in current_url.lower():
                print("✅ Successfully navigated away from login page")
                self.test_results["login_success"] = True
            else:
                print("❌ Still on login page - login may have failed")
        
        # Take screenshot of logged-in state
        await self.client.browser_take_screenshot("05_logged_in_state.png")
        print("📸 Logged-in state screenshot captured")
        
        # Check for success indicators
        snapshot_result = await self.client.browser_snapshot()
        if "error" not in snapshot_result:
            print("✅ Page snapshot captured for analysis")
    
    async def step_5_execute_logout(self):
        """Execute logout process"""
        print("\n🚪 Step 5: Execute logout")
        
        if not self.test_results["login_success"]:
            print("❌ Cannot logout - login was not successful")
            return
        
        # Take screenshot before logout
        await self.client.browser_take_screenshot("06_before_logout.png")
        print("📸 Before logout screenshot captured")
        
        # Try different logout mechanisms
        logout_selectors = [
            "text=Logout",
            "text=Log Out", 
            "text=Sign Out",
            "button:has-text('Logout')",
            "a:has-text('Logout')",
            "[data-testid='logout']",
            "[data-testid='sign-out']"
        ]
        
        logout_successful = False
        
        for selector in logout_selectors:
            print(f"🔍 Trying logout selector: {selector}")
            
            logout_result = await self.client.browser_click("Logout", selector)
            
            if "error" not in logout_result:
                print(f"✅ Logout clicked: {selector}")
                logout_successful = True
                break
            else:
                print(f"❌ Logout failed with {selector}")
        
        if not logout_successful:
            # Try user menu dropdown approach
            print("🔍 Trying user menu dropdown approach...")
            
            user_menu_selectors = [
                "[data-testid='user-menu']",
                ".user-menu",
                ".profile-menu",
                "button:has-text('Profile')",
                "button:has-text('Account')"
            ]
            
            for menu_selector in user_menu_selectors:
                menu_result = await self.client.browser_click("User menu", menu_selector)
                
                if "error" not in menu_result:
                    print(f"✅ User menu clicked: {menu_selector}")
                    await self.client.browser_wait_for(time=2)
                    
                    # Now try logout from dropdown
                    for logout_selector in logout_selectors:
                        dropdown_logout = await self.client.browser_click("Logout from menu", logout_selector)
                        
                        if "error" not in dropdown_logout:
                            print(f"✅ Logout from dropdown: {logout_selector}")
                            logout_successful = True
                            break
                    
                    if logout_successful:
                        break
        
        if logout_successful:
            # Wait for logout to complete
            await self.client.browser_wait_for(time=5)
            
            # Take screenshot after logout
            await self.client.browser_take_screenshot("07_after_logout.png")
            print("📸 After logout screenshot captured")
            
            # Verify logout success
            url_result = await self.client.browser_get_url()
            if "error" not in url_result:
                current_url = url_result.get("url", "")
                print(f"📍 URL after logout: {current_url}")
                
                if "login" in current_url.lower():
                    print("✅ Successfully returned to login page")
                    self.test_results["logout_success"] = True
                else:
                    print("❌ Not on login page - logout may have failed")
        else:
            print("❌ Could not find logout mechanism")
    
    async def step_6_generate_report(self):
        """Generate final test report"""
        print("\n📊 Step 6: Generate test report")
        
        # Take final screenshot
        await self.client.browser_take_screenshot("08_final_state.png")
        print("📸 Final state screenshot captured")
        
        # Generate report
        report = {
            "timestamp": datetime.now().isoformat(),
            "test_name": "2FA Login & Logout Test",
            "test_results": self.test_results,
            "totp_secret_used": self.totp_secret,
            "login_data": {
                "username": self.login_data["username"],
                "password": "***REDACTED***"
            },
            "method": "MCP_Server_Automation"
        }
        
        # Save report
        with open("fixtures/2fa_test_report.json", "w") as f:
            json.dump(report, f, indent=2)
        
        print("💾 Test report saved to fixtures/2fa_test_report.json")
        
        # Print summary
        print("\n📋 Test Results Summary:")
        print("=" * 30)
        
        results = self.test_results
        success_count = sum(1 for result in results.values() if result)
        total_count = len(results)
        
        print(f"✅ Navigation: {'SUCCESS' if results['navigation'] else 'FAILED'}")
        print(f"✅ Login Form: {'SUCCESS' if results['login_form_filled'] else 'FAILED'}")
        print(f"✅ Two-Factor Auth: {'SUCCESS' if results['two_factor_auth'] else 'FAILED'}")
        print(f"✅ Login Success: {'SUCCESS' if results['login_success'] else 'FAILED'}")
        print(f"✅ Logout Success: {'SUCCESS' if results['logout_success'] else 'FAILED'}")
        
        success_rate = (success_count / total_count) * 100
        print(f"\n🎯 Overall Success Rate: {success_rate:.1f}% ({success_count}/{total_count})")


async def check_mcp_server():
    """Check if MCP server is running"""
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get("http://127.0.0.1:8931/health")
            return response.status_code == 200
    except:
        return False


async def main():
    """Main execution function"""
    print("🔍 Checking MCP server status...")
    
    # Check if MCP server is running
    server_running = await check_mcp_server()
    
    if not server_running:
        print("❌ MCP server is not running!")
        print("🚀 Please start the MCP server first:")
        print("   ./scripts/start_mcp_server.sh")
        sys.exit(1)
    
    print("✅ MCP server is running")
    
    # Create fixtures directory
    import os
    os.makedirs("fixtures", exist_ok=True)
    
    # Run the test
    test = TwoFactorLoginTest()
    results = await test.run_full_test()
    
    print("\n" + "=" * 50)
    print("🎉 2FA Login & Logout Test Completed!")
    print("=" * 50)
    
    return results


if __name__ == "__main__":
    try:
        results = asyncio.run(main())
        
        # Exit with appropriate code
        success_count = sum(1 for result in results.values() if result)
        if success_count == len(results):
            print("✅ All test steps passed!")
            sys.exit(0)
        else:
            print(f"❌ {len(results) - success_count} test steps failed")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n❌ Test interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Test execution failed: {str(e)}")
        sys.exit(1) 