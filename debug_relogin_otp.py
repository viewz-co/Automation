#!/usr/bin/env python3
"""
Debug Relogin OTP Page
Script to specifically debug the OTP page that appears after clicking relogin
"""

import asyncio
from playwright.async_api import async_playwright
import json
import pyotp

async def debug_relogin_otp():
    """Debug the relogin OTP page structure"""
    
    # Load BO config
    with open('configs/bo_env_config.json', 'r') as f:
        bo_config = json.load(f)
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()
        
        try:
            print("🎯 STEP 1: BO LOGIN")
            print("="*40)
            
            # Login to BO
            print(f"🌐 Navigating to BO login page: {bo_config['base_url']}/login")
            await page.goto(f"{bo_config['base_url']}/login")
            await page.wait_for_load_state("networkidle")
            
            # Perform login
            print("🔐 Performing BO login...")
            await page.fill('input[name="userName"]', bo_config['username'])
            await page.fill('input[name="password"]', bo_config['password'])
            await page.click('button[type="submit"]')
            
            # Handle initial OTP
            await asyncio.sleep(2)
            totp = pyotp.TOTP(bo_config['otp_secret'])
            otp_code = totp.now()
            print(f"🔐 Generated initial OTP: {otp_code}")
            
            await page.wait_for_selector("text=code", timeout=10000)
            await page.fill('input[type="text"]', otp_code)
            await page.click('button:has-text("Verify")')
            
            await asyncio.sleep(5)
            print("✅ Initial login completed")
            
            print("\n🎯 STEP 2: NAVIGATE TO RELOGIN")
            print("="*40)
            
            # Should be on accounts page now
            current_url = page.url
            print(f"📍 Current URL: {current_url}")
            
            # Find and click relogin button
            relogin_selector = '[title="Relogin To Account"]'
            relogin_buttons = page.locator(relogin_selector)
            count = await relogin_buttons.count()
            print(f"🔍 Found {count} relogin buttons")
            
            if count > 0:
                # Click the first relogin button
                await relogin_buttons.first.click()
                print("✅ Clicked relogin button")
                
                # Wait for page to change
                await asyncio.sleep(3)
                
                print("\n🎯 STEP 3: ANALYZE RELOGIN OTP PAGE")
                print("="*40)
                
                # Take screenshot
                await page.screenshot(path="debug_relogin_otp_page.png")
                print("📸 Screenshot saved: debug_relogin_otp_page.png")
                
                # Check URL after relogin click
                relogin_url = page.url
                print(f"📍 URL after relogin: {relogin_url}")
                
                # Check page title
                title = await page.title()
                print(f"📄 Page title: {title}")
                
                # Look for any text inputs
                print("\n🔍 Looking for input elements:")
                inputs = await page.locator('input').all()
                for i, input_elem in enumerate(inputs):
                    try:
                        input_type = await input_elem.get_attribute('type')
                        input_name = await input_elem.get_attribute('name')
                        input_placeholder = await input_elem.get_attribute('placeholder')
                        input_id = await input_elem.get_attribute('id')
                        input_class = await input_elem.get_attribute('class')
                        is_visible = await input_elem.is_visible()
                        
                        print(f"  Input {i+1}:")
                        print(f"    Type: {input_type}")
                        print(f"    Name: {input_name}")
                        print(f"    Placeholder: {input_placeholder}")
                        print(f"    ID: {input_id}")
                        print(f"    Class: {input_class}")
                        print(f"    Visible: {is_visible}")
                        print()
                    except Exception as e:
                        print(f"    Error getting attributes: {str(e)}")
                
                # Look for OTP-related text
                print("🔍 Looking for OTP-related text:")
                otp_keywords = ['otp', 'code', 'verification', 'authenticate', 'token']
                page_text = await page.text_content('body')
                
                for keyword in otp_keywords:
                    if keyword.lower() in page_text.lower():
                        print(f"  ✅ Found '{keyword}' in page text")
                
                # Look for forms
                print("\n🔍 Looking for forms:")
                forms = await page.locator('form').all()
                print(f"Found {len(forms)} form(s)")
                
                for i, form in enumerate(forms):
                    try:
                        form_text = await form.text_content()
                        print(f"  Form {i+1}: {form_text[:100]}...")
                    except:
                        print(f"  Form {i+1}: Could not get text")
                
                # Look for buttons
                print("\n🔍 Looking for buttons:")
                buttons = await page.locator('button').all()
                for i, button in enumerate(buttons):
                    try:
                        button_text = await button.text_content()
                        button_type = await button.get_attribute('type')
                        is_visible = await button.is_visible()
                        
                        if is_visible and button_text and button_text.strip():
                            print(f"  Button {i+1}: '{button_text}' (type: {button_type})")
                    except:
                        continue
                
                # Save page content
                content = await page.content()
                with open('debug_relogin_otp_content.html', 'w') as f:
                    f.write(content)
                print(f"\n💾 Page content saved: debug_relogin_otp_content.html")
                
                # Wait for manual inspection
                print("\n⏸️  Browser will stay open for 60 seconds for manual inspection...")
                print("Look for:")
                print("1. OTP input field")
                print("2. Submit/Verify button")
                print("3. Any error messages")
                await asyncio.sleep(60)
                
            else:
                print("❌ No relogin buttons found")
                
        except Exception as e:
            print(f"❌ Error during debug: {str(e)}")
            await page.screenshot(path="debug_relogin_error.png")
            
        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(debug_relogin_otp())
