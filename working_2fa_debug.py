#!/usr/bin/env python3
"""
Debug script using the same setup as working tests
"""
import asyncio
import pyotp
import os
from playwright.async_api import async_playwright
from pages.login_page import LoginPage

async def debug_2fa_properly():
    """Debug 2FA using the same setup as working tests"""
    
    # Load config like the tests do
    config = {
        "base_url": os.getenv("BASE_URL", "https://app.viewz.co"),
        "username": os.getenv("TEST_USERNAME", ""),
        "password": os.getenv("TEST_PASSWORD", ""),
        "otp_secret": os.getenv("TEST_TOTP_SECRET", ""),
    }
    
    login_data = {
        "username": config["username"],
        "password": config["password"]
    }
    
    print(f"🔐 Using credentials: {config['username']}")
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        # Use base_url like the working tests
        context = await browser.new_context(base_url=config["base_url"])
        page = await context.new_page()
        
        try:
            # Use the exact same login process as working tests
            login = LoginPage(page)
            await login.goto()  # This will now work with base_url
            await login.login(login_data["username"], login_data["password"])
            
            print("✅ Login submitted, waiting for response...")
            
            # Wait for navigation or 2FA page
            await asyncio.sleep(5)
            
            print("📄 Current page URL:", page.url)
            print("📄 Page title:", await page.title())
            
            # Get all text content
            body_text = await page.locator('body').inner_text()
            print("📄 Page content:")
            print("=" * 50)
            print(body_text[:1000])  # First 1000 chars
            print("=" * 50)
            
            # Look for 2FA patterns more comprehensively
            patterns_to_check = [
                "Two-Factor Authentication",
                "2FA", 
                "Two Factor",
                "Authentication Code",
                "Verification Code", 
                "Enter code",
                "verification code",
                "authentication code",
                "OTP",
                "Security Code",
                "אימות דו-שלבי",  # Hebrew: Two-factor authentication
                "קוד אימות",      # Hebrew: Authentication code
                "הזן קוד",        # Hebrew: Enter code
                "code",
                "Code",
                "verify",
                "Verify",
                "Authentication",
                "Factor"
            ]
            
            print("🔍 Checking for 2FA patterns:")
            found_patterns = []
            for pattern in patterns_to_check:
                try:
                    if pattern.lower() in body_text.lower():
                        found_patterns.append(pattern)
                        print(f"   ✅ Found in text: '{pattern}'")
                    
                    # Also check as locator
                    element = page.locator(f"text={pattern}")
                    count = await element.count()
                    if count > 0:
                        print(f"   ✅ Found as locator: '{pattern}' ({count} matches)")
                        found_patterns.append(f"{pattern} (locator)")
                except Exception as e:
                    continue
            
            if not found_patterns:
                print("   ❌ No 2FA patterns found")
            
            # Take screenshot
            await page.screenshot(path="/app/screenshots/working_2fa_debug.png")
            print("📸 Screenshot saved: working_2fa_debug.png")
            
            # Check what input fields exist
            inputs = await page.query_selector_all('input')
            print(f"📝 Found {len(inputs)} input field(s):")
            for i, input_elem in enumerate(inputs):
                input_type = await input_elem.get_attribute('type')
                input_placeholder = await input_elem.get_attribute('placeholder')
                input_name = await input_elem.get_attribute('name')
                input_value = await input_elem.get_attribute('value')
                is_visible = await input_elem.is_visible()
                print(f"   Input {i+1}: type={input_type}, name={input_name}, placeholder={input_placeholder}, visible={is_visible}")
                if input_value and len(input_value) > 10:
                    print(f"              value=[HIDDEN - {len(input_value)} chars]")
                else:
                    print(f"              value={input_value}")
            
            # Check if we need to wait longer or check for other elements
            print("\n🔍 Looking for common 2FA elements...")
            common_selectors = [
                'input[type="text"]',
                'input[type="number"]', 
                'input[placeholder*="code"]',
                'input[placeholder*="Code"]',
                'input[placeholder*="verification"]',
                'input[placeholder*="authentication"]',
                '[data-testid*="otp"]',
                '[data-testid*="2fa"]',
                '[class*="otp"]',
                '[class*="2fa"]',
                '[class*="verification"]'
            ]
            
            for selector in common_selectors:
                try:
                    elements = await page.query_selector_all(selector)
                    if elements:
                        print(f"   ✅ Found {len(elements)} elements for: {selector}")
                except:
                    continue
            
        except Exception as e:
            print(f"❌ Error: {e}")
            await page.screenshot(path="/app/screenshots/error_2fa_debug.png")
        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(debug_2fa_properly())