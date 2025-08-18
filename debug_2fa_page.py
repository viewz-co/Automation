#!/usr/bin/env python3
"""
Debug script to capture what's actually on the 2FA page
"""
import asyncio
import pyotp
import os
from playwright.async_api import async_playwright
from pages.login_page import LoginPage

async def debug_2fa_page():
    """Debug the 2FA page to see actual content"""
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        try:
            # Login credentials
            username = os.getenv('TEST_USERNAME', 'sharon@viewz.co')
            password = os.getenv('TEST_PASSWORD', 'Sh@ron123$%^')
            secret = os.getenv('TEST_TOTP_SECRET', 'HA2ECLBIKYUEEI2GPUUSMN3XIMXFETRQ')
            
            print(f"🔐 Using credentials: {username}")
            
            # Perform login
            base_url = os.getenv('BASE_URL', 'https://app.viewz.co')
            await page.goto(f"{base_url}/login")
            
            # Use the login page methods
            await page.fill('input[name="username"]', username)
            await page.fill('input[name="password"]', password)
            await page.click('button[type="submit"]')
            
            print("✅ Login submitted, waiting for 2FA page...")
            
            # Wait a bit for page to load
            await asyncio.sleep(3)
            
            # Capture page content
            print("📄 Current page URL:", page.url)
            print("📄 Page title:", await page.title())
            
            # Get all text content
            body_text = await page.locator('body').inner_text()
            print("📄 Page content:")
            print("=" * 50)
            print(body_text)
            print("=" * 50)
            
            # Try to find any form or input elements
            forms = await page.query_selector_all('form')
            print(f"📝 Found {len(forms)} form(s)")
            
            inputs = await page.query_selector_all('input')
            print(f"📝 Found {len(inputs)} input(s)")
            for i, input_elem in enumerate(inputs):
                input_type = await input_elem.get_attribute('type')
                input_placeholder = await input_elem.get_attribute('placeholder')
                input_name = await input_elem.get_attribute('name')
                print(f"   Input {i+1}: type={input_type}, placeholder={input_placeholder}, name={input_name}")
            
            # Look for specific text patterns
            patterns_to_check = [
                "Two-Factor Authentication",
                "2FA",
                "Authentication Code",
                "Verification Code", 
                "Enter code",
                "OTP",
                "Security Code",
                "אימות דו-שלבי",  # Hebrew: Two-factor authentication
                "קוד אימות",      # Hebrew: Authentication code
                "הזן קוד"        # Hebrew: Enter code
            ]
            
            print("🔍 Checking for text patterns:")
            for pattern in patterns_to_check:
                try:
                    element = page.locator(f"text={pattern}")
                    count = await element.count()
                    if count > 0:
                        print(f"   ✅ Found: '{pattern}' ({count} matches)")
                    else:
                        print(f"   ❌ Not found: '{pattern}'")
                except:
                    print(f"   ❌ Error checking: '{pattern}'")
            
            # Take a screenshot for analysis
            await page.screenshot(path="/app/screenshots/2fa_page_debug.png")
            print("📸 Screenshot saved: 2fa_page_debug.png")
            
            # Try to generate and enter OTP
            otp = pyotp.TOTP(secret).now()
            print(f"🔑 Generated OTP: {otp}")
            
            # Try to find and fill the OTP field
            try:
                textbox = page.get_by_role("textbox")
                await textbox.fill(otp)
                print("✅ OTP filled successfully")
                
                # Wait to see what happens
                await asyncio.sleep(5)
                
                print("📄 After OTP entry:")
                print("📄 Current page URL:", page.url)
                print("📄 Page title:", await page.title())
                
            except Exception as e:
                print(f"❌ Error filling OTP: {e}")
            
        except Exception as e:
            print(f"❌ Error: {e}")
        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(debug_2fa_page())