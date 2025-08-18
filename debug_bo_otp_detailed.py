#!/usr/bin/env python3
"""
Debug BO OTP Process in Detail
Script to step through OTP verification process to understand why login fails
"""

import asyncio
from playwright.async_api import async_playwright
import json
import pyotp

async def debug_bo_otp_detailed():
    """Debug the BO OTP process step by step"""
    
    # Load BO config
    with open('configs/bo_env_config.json', 'r') as f:
        bo_config = json.load(f)
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()
        
        try:
            print(f"🌐 Navigating to BO login page: {bo_config['base_url']}/login")
            await page.goto(f"{bo_config['base_url']}/login")
            await page.wait_for_load_state("networkidle")
            
            # Perform login
            print("🔐 Performing BO login...")
            await page.fill('input[name="userName"]', bo_config['username'])
            await page.fill('input[name="password"]', bo_config['password'])
            await page.click('button[type="submit"]')
            print("✅ Login form submitted")
            
            # Wait and check what happens
            await asyncio.sleep(3)
            url_after_submit = page.url
            print(f"📍 URL after login submit: {url_after_submit}")
            
            # Handle OTP
            totp = pyotp.TOTP(bo_config['otp_secret'])
            otp_code = totp.now()
            print(f"🔐 Generated OTP: {otp_code}")
            
            # Check for OTP page
            print("🔍 Looking for OTP page indicators...")
            
            # Wait for OTP page to appear
            otp_found = False
            otp_indicators = ["text=code", "text=Code", "text=OTP", "text=verification", "text=Two-Factor"]
            
            for indicator in otp_indicators:
                try:
                    await page.wait_for_selector(indicator, timeout=5000)
                    print(f"✅ OTP indicator found: {indicator}")
                    otp_found = True
                    break
                except:
                    print(f"⚠️ No {indicator} found")
                    continue
            
            if not otp_found:
                print("❌ No OTP page detected")
                await page.screenshot(path="debug_no_otp_page.png")
                print("📸 Screenshot saved: debug_no_otp_page.png")
                return
            
            # Take screenshot of OTP page
            await page.screenshot(path="debug_otp_page.png")
            print("📸 OTP page screenshot saved: debug_otp_page.png")
            
            # Find OTP input
            print("🔍 Looking for OTP input field...")
            otp_selectors = ['input[type="text"]', 'input[name="otp"]', 'input[name="code"]']
            otp_input_found = False
            
            for selector in otp_selectors:
                try:
                    otp_elements = page.locator(selector)
                    count = await otp_elements.count()
                    print(f"Found {count} elements for selector: {selector}")
                    
                    if count > 0:
                        # Try to fill the OTP
                        otp_element = otp_elements.last  # Use last visible element
                        await otp_element.fill(otp_code)
                        print(f"✅ OTP filled in {selector} with code: {otp_code}")
                        otp_input_found = True
                        break
                except Exception as e:
                    print(f"⚠️ Error with {selector}: {str(e)}")
                    continue
            
            if not otp_input_found:
                print("❌ Could not fill OTP")
                return
            
            # Wait a moment
            await asyncio.sleep(2)
            
            # Try to submit OTP
            print("🔍 Looking for OTP submit button...")
            submit_selectors = [
                'button:has-text("Verify")',
                'button:has-text("Submit")',
                'button[type="submit"]',
                'button:has-text("Continue")',
                'button:has-text("Login")'
            ]
            
            submit_found = False
            for selector in submit_selectors:
                try:
                    submit_button = page.locator(selector)
                    if await submit_button.is_visible():
                        await submit_button.click()
                        print(f"✅ Clicked submit button: {selector}")
                        submit_found = True
                        break
                except Exception as e:
                    print(f"⚠️ Error with submit {selector}: {str(e)}")
                    continue
            
            if not submit_found:
                print("⚠️ No submit button found, OTP might auto-submit")
            
            # Wait for processing
            print("⏳ Waiting for OTP verification...")
            await asyncio.sleep(8)  # Give more time
            
            # Check final URL
            final_url = page.url
            print(f"🏁 Final URL: {final_url}")
            
            # Take final screenshot
            await page.screenshot(path="debug_after_otp_submit.png")
            print("📸 Final screenshot saved: debug_after_otp_submit.png")
            
            # Check page content
            page_text = await page.text_content('body')
            print(f"📄 Page content length: {len(page_text)} characters")
            
            # Look for error messages
            error_indicators = ['error', 'invalid', 'incorrect', 'failed', 'expired']
            for indicator in error_indicators:
                if indicator.lower() in page_text.lower():
                    print(f"⚠️ Possible error detected: '{indicator}' found in page content")
            
            # Look for success indicators
            success_indicators = ['success', 'welcome', 'dashboard', 'accounts', 'settings']
            for indicator in success_indicators:
                if indicator.lower() in page_text.lower():
                    print(f"✅ Possible success indicator: '{indicator}' found in page content")
            
            # Check if we're still on login page
            if 'login' in final_url:
                print("❌ Still on login page - OTP verification likely failed")
                
                # Try to see what's on the page
                print("🔍 Checking for any error messages or hints...")
                try:
                    # Look for any visible text that might indicate the problem
                    visible_text = await page.locator('body').text_content()
                    lines = visible_text.split('\n')
                    relevant_lines = [line.strip() for line in lines if line.strip() and 
                                    any(word in line.lower() for word in ['error', 'invalid', 'code', 'try', 'again'])]
                    
                    if relevant_lines:
                        print("📋 Relevant text found:")
                        for line in relevant_lines[:10]:  # Show first 10 relevant lines
                            print(f"   {line}")
                    
                except Exception as e:
                    print(f"⚠️ Error extracting page text: {str(e)}")
            else:
                print("✅ Not on login page - likely successful!")
            
            # Keep browser open for inspection
            print("\n⏸️  Browser will stay open for 30 seconds for inspection...")
            await asyncio.sleep(30)
            
        except Exception as e:
            print(f"❌ Error during detailed debug: {str(e)}")
            await page.screenshot(path="debug_otp_detailed_error.png")
            
        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(debug_bo_otp_detailed())
