"""
BO Login Page Object
Extends the base login page functionality for BO environment access
"""

from playwright.async_api import Page
from pages.login_page import LoginPage
import asyncio


class BOLoginPage(LoginPage):
    """BO-specific login page extending the base LoginPage functionality"""
    
    def __init__(self, page: Page, bo_base_url: str = "https://bo.viewz.co"):
        super().__init__(page)
        self.bo_base_url = bo_base_url
        
        # BO-specific selectors (based on actual BO page structure)
        self.bo_username_input = 'input[name="userName"], input[name="username"], input[type="email"], input[placeholder*="username" i], input[placeholder*="email" i]'
        self.bo_password_input = 'input[name="password"], input[type="password"], input[placeholder*="password" i]'
        self.bo_login_button = 'button[type="submit"], button:has-text("Login"), button.login-btn, button:has-text("Sign In"), input[type="submit"]'
        
        # OTP/2FA selectors for BO
        self.otp_input = 'input[name="otp"], input[name="code"], input[placeholder*="code" i], input[type="text"]'
        self.otp_submit_button = 'button:has-text("Verify"), button:has-text("Submit"), button[type="submit"]'
        
        # BO success indicators
        self.bo_logged_in_selectors = [
            'main',
            'div[role="main"]',
            '.dashboard',
            '.admin-panel',
            'text=Accounts',
            'text=Dashboard',
            'svg.viewz-logo',
            '.navigation',
            '.menu'
        ]

    async def goto_bo(self):
        """Navigate to BO login page"""
        await self.page.goto(f"{self.bo_base_url}/login")
        await self.page.wait_for_load_state("networkidle")

    async def bo_login(self, username: str, password: str):
        """Perform BO login with flexible selector matching"""
        print(f"🔐 Attempting BO login for user: {username}")
        
        # Fill username with flexible selector matching
        username_filled = False
        for selector in self.bo_username_input.split(', '):
            try:
                username_element = self.page.locator(selector)
                if await username_element.is_visible():
                    await username_element.fill(username)
                    print(f"✅ Username filled using selector: {selector}")
                    username_filled = True
                    break
            except Exception:
                continue
        
        if not username_filled:
            raise Exception("❌ Could not find username input field")
        
        # Fill password with flexible selector matching
        password_filled = False
        for selector in self.bo_password_input.split(', '):
            try:
                password_element = self.page.locator(selector)
                if await password_element.is_visible():
                    await password_element.fill(password)
                    print(f"✅ Password filled using selector: {selector}")
                    password_filled = True
                    break
            except Exception:
                continue
        
        if not password_filled:
            raise Exception("❌ Could not find password input field")
        
        # Click login button with flexible selector matching
        login_clicked = False
        for selector in self.bo_login_button.split(', '):
            try:
                login_element = self.page.locator(selector)
                if await login_element.is_visible():
                    await login_element.click()
                    print(f"✅ Login button clicked using selector: {selector}")
                    login_clicked = True
                    break
            except Exception:
                continue
        
        if not login_clicked:
            raise Exception("❌ Could not find login button")
        
        await asyncio.sleep(2)

    async def handle_bo_otp(self, otp_secret: str):
        """Handle OTP input for BO environment with multiple attempts"""
        import pyotp
        
        print(f"🔐 Handling BO OTP verification...")
        
        # Wait for OTP page to appear
        otp_page_detected = False
        otp_indicators = [
            "text=Two-Factor Authentication",
            "text=Authentication",
            "text=verification",
            "text=code",
            "text=OTP",
            "text=Authenticator"
        ]
        
        for indicator in otp_indicators:
            try:
                await self.page.wait_for_selector(indicator, timeout=3000)
                print(f"✅ OTP page detected with indicator: {indicator}")
                otp_page_detected = True
                break
            except Exception:
                continue
        
        if not otp_page_detected:
            print("⚠️ OTP page not detected, but continuing with OTP entry attempt...")
        
        # Try multiple OTP generation strategies
        max_attempts = 3
        import time
        totp = pyotp.TOTP(otp_secret)
        
        for attempt in range(max_attempts):
            print(f"🔄 OTP Attempt {attempt + 1}/{max_attempts}")
            
            # Wait for fresh OTP window if needed
            seconds_remaining = 30 - (int(time.time()) % 30)
            if seconds_remaining < 10:
                print(f"⏳ Only {seconds_remaining}s left, waiting for fresh OTP...")
                await asyncio.sleep(seconds_remaining + 1)
            
            # Generate fresh OTP
            otp_code = totp.now()
            seconds_valid = 30 - (int(time.time()) % 30)
            print(f"🕐 Using fresh OTP: {otp_code} (valid for {seconds_valid}s)")
            
            # Fill OTP - try split input boxes first (6 individual inputs)
            otp_filled = False
            
            # Method 1: Handle split OTP boxes
            try:
                otp_inputs = self.page.locator('input[data-input-otp="true"], input[maxlength="1"]')
                input_count = await otp_inputs.count()
                
                if input_count == 6:
                    print(f"📦 Found 6 split OTP input boxes")
                    await otp_inputs.first.click()
                    await asyncio.sleep(0.2)
                    
                    for digit in otp_code:
                        await self.page.keyboard.press(digit)
                        await asyncio.sleep(0.12)
                    
                    otp_filled = True
                    print(f"✅ OTP entered digit by digit: {otp_code}")
            except Exception as e:
                print(f"⚠️ Split box method failed: {str(e)[:40]}")
            
            # Method 2: Click and type with keyboard
            if not otp_filled:
                try:
                    first_input = self.page.locator('input[type="text"]:visible').first
                    await first_input.click()
                    await asyncio.sleep(0.2)
                    
                    # Clear and type
                    await self.page.keyboard.press("Control+a")
                    await self.page.keyboard.press("Backspace")
                    await asyncio.sleep(0.1)
                    
                    for digit in otp_code:
                        await self.page.keyboard.press(digit)
                        await asyncio.sleep(0.1)
                    
                    otp_filled = True
                    print(f"✅ OTP typed via keyboard: {otp_code}")
                except Exception as e:
                    print(f"⚠️ Keyboard type failed: {str(e)[:40]}")
            
            # Method 3: Traditional fill() as fallback
            if not otp_filled:
                for selector in self.otp_input.split(', '):
                    try:
                        otp_element = self.page.locator(selector)
                        if await otp_element.is_visible():
                            await otp_element.clear()
                            await otp_element.fill(otp_code)
                            print(f"✅ OTP filled using selector: {selector}")
                            otp_filled = True
                            break
                    except Exception:
                        continue
            
            if not otp_filled:
                print("❌ Could not find OTP input field")
                continue
            
            if otp_filled:
                # Try to submit OTP
                submit_clicked = False
                for selector in self.otp_submit_button.split(', '):
                    try:
                        submit_element = self.page.locator(selector)
                        if await submit_element.is_visible():
                            await submit_element.click()
                            print(f"✅ OTP submitted using selector: {selector}")
                            submit_clicked = True
                            break
                    except Exception:
                        continue
                
                if not submit_clicked:
                    print("⚠️ OTP submit button not found, but OTP may auto-submit")
                
                # Wait for processing
                await asyncio.sleep(5)
                
                # Check if we're still on login page
                current_url = self.page.url
                if 'login' not in current_url:
                    print(f"✅ OTP verification successful! Redirected to: {current_url}")
                    return True
                else:
                    print(f"⚠️ Still on login page after attempt {attempt + 1}")
                    
                    # Check for error messages
                    try:
                        page_text = await self.page.text_content('body')
                        if 'invalid' in page_text.lower() or 'failed' in page_text.lower():
                            print("❌ OTP verification failed, trying different time window...")
                            continue
                    except:
                        pass
        
        print("❌ All OTP attempts failed")
        return False

    async def is_bo_logged_in(self):
        """Check if BO login was successful"""
        await asyncio.sleep(2)  # Wait for page to settle
        
        current_url = self.page.url
        print(f"🔍 Checking login status at URL: {current_url}")
        
        # If we're still on login page, definitely not logged in
        if 'login' in current_url:
            print("❌ Still on login page - login failed")
            return False
        
        # Try multiple selectors to check if logged in
        for selector in self.bo_logged_in_selectors:
            try:
                locator = self.page.locator(selector)
                await locator.wait_for(timeout=3000)
                if await locator.is_visible():
                    print(f"✅ BO login verified with selector: {selector}")
                    return True
            except Exception:
                continue
        
        # Additional URL-based check
        if any(indicator in current_url.lower() for indicator in ['dashboard', 'home', 'accounts', 'admin', 'settings']):
            print(f"✅ BO login verified by URL: {current_url}")
            return True
        
        # Take screenshot for debugging
        try:
            await self.page.screenshot(path="debug_bo_login_verification.png")
            print("📸 Debug screenshot saved: debug_bo_login_verification.png")
        except:
            pass
        
        print("❌ BO login verification failed")
        return False

    async def full_bo_login(self, username: str, password: str, otp_secret: str):
        """Complete BO login flow including OTP"""        
        # Navigate to BO login
        await self.goto_bo()
        
        # Perform login
        await self.bo_login(username, password)
        
        # Handle OTP with multiple attempts
        otp_success = await self.handle_bo_otp(otp_secret)
        
        if not otp_success:
            print("❌ OTP verification failed")
            return False
        
        # Verify login success
        return await self.is_bo_logged_in()
