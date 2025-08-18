#!/usr/bin/env python3
"""
Capture the exact content of the 2FA page after successful login
"""
import asyncio
import pyotp
import os
from playwright.async_api import async_playwright
from pages.login_page import LoginPage

async def capture_2fa_content():
    """Capture exactly what's on the 2FA page"""
    
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
    
    print(f"🔐 Attempting login with: {config['username']}")
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(base_url=config["base_url"])
        page = await context.new_page()
        
        try:
            # Perform login exactly like the test does
            login = LoginPage(page)
            await login.goto()
            await login.login(login_data["username"], login_data["password"])
            
            print("✅ Login submitted, waiting for 2FA page...")
            
            # Wait longer to ensure page loads completely
            await asyncio.sleep(8)
            
            print(f"📄 Current URL: {page.url}")
            print(f"📄 Page title: {await page.title()}")
            
            # Capture EVERYTHING on the page
            full_html = await page.content()
            
            # Save HTML for analysis
            with open('/app/screenshots/2fa_page_full.html', 'w', encoding='utf-8') as f:
                f.write(full_html)
            print("💾 Full HTML saved: 2fa_page_full.html")
            
            # Get visible text
            body_text = await page.locator('body').inner_text()
            print("\n📄 === FULL PAGE TEXT CONTENT ===")
            print(body_text)
            print("=== END PAGE TEXT ===\n")
            
            # Save text content
            with open('/app/screenshots/2fa_page_text.txt', 'w', encoding='utf-8') as f:
                f.write(body_text)
            print("💾 Text content saved: 2fa_page_text.txt")
            
            # Check for any form elements
            forms = await page.query_selector_all('form')
            print(f"📝 Found {len(forms)} form(s)")
            
            # Get all input elements with details
            inputs = await page.query_selector_all('input')
            print(f"📝 Found {len(inputs)} input element(s):")
            for i, input_elem in enumerate(inputs):
                try:
                    input_type = await input_elem.get_attribute('type') or 'text'
                    input_placeholder = await input_elem.get_attribute('placeholder') or ''
                    input_name = await input_elem.get_attribute('name') or ''
                    input_id = await input_elem.get_attribute('id') or ''
                    input_class = await input_elem.get_attribute('class') or ''
                    is_visible = await input_elem.is_visible()
                    
                    print(f"   Input {i+1}:")
                    print(f"      type: {input_type}")
                    print(f"      name: {input_name}")
                    print(f"      id: {input_id}")
                    print(f"      placeholder: {input_placeholder}")
                    print(f"      class: {input_class}")
                    print(f"      visible: {is_visible}")
                    print()
                except Exception as e:
                    print(f"   Input {i+1}: Error getting details - {e}")
            
            # Take screenshot
            await page.screenshot(path="/app/screenshots/2fa_content_capture.png", full_page=True)
            print("📸 Full page screenshot saved: 2fa_content_capture.png")
            
            # Try to generate OTP and see what happens
            if config["otp_secret"]:
                otp = pyotp.TOTP(config["otp_secret"]).now()
                print(f"\n🔑 Generated OTP: {otp}")
                
                # Try different ways to fill OTP
                print("🔄 Attempting to fill OTP in various ways...")
                
                # Method 1: Try textbox role
                try:
                    textboxes = await page.query_selector_all('[role="textbox"]')
                    print(f"   Found {len(textboxes)} elements with role='textbox'")
                    
                    if textboxes:
                        # Try the last textbox (likely the OTP field)
                        await textboxes[-1].fill(otp)
                        print("   ✅ Filled OTP using textbox role")
                        await asyncio.sleep(3)
                        
                        # Check what happened
                        new_url = page.url
                        print(f"   📄 URL after OTP: {new_url}")
                        if new_url != page.url:
                            print("   🎉 URL changed - OTP might have worked!")
                        
                except Exception as e:
                    print(f"   ❌ Textbox method failed: {e}")
                
                # Method 2: Try input type="text"
                try:
                    text_inputs = await page.query_selector_all('input[type="text"]:visible')
                    print(f"   Found {len(text_inputs)} visible text inputs")
                    
                    if text_inputs:
                        await text_inputs[-1].fill(otp)
                        print("   ✅ Filled OTP using text input")
                        await asyncio.sleep(3)
                        
                except Exception as e:
                    print(f"   ❌ Text input method failed: {e}")
                
                # Method 3: Try any visible input that might accept numbers
                try:
                    number_inputs = await page.query_selector_all('input[type="number"]:visible, input:not([type]):visible')
                    print(f"   Found {len(number_inputs)} potential number inputs")
                    
                    if number_inputs:
                        await number_inputs[-1].fill(otp)
                        print("   ✅ Filled OTP using number input")
                        await asyncio.sleep(3)
                        
                except Exception as e:
                    print(f"   ❌ Number input method failed: {e}")
            
            # Final screenshot after OTP attempt
            await page.screenshot(path="/app/screenshots/after_otp_attempt.png", full_page=True)
            print("📸 Screenshot after OTP attempt saved: after_otp_attempt.png")
            
            # Final page state
            final_url = page.url
            final_title = await page.title()
            print(f"\n📄 Final URL: {final_url}")
            print(f"📄 Final title: {final_title}")
            
        except Exception as e:
            print(f"❌ Error: {e}")
            await page.screenshot(path="/app/screenshots/error_capture.png")
        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(capture_2fa_content())