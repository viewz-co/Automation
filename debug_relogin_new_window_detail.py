#!/usr/bin/env python3
"""
Debug Relogin New Window in Detail
Script to analyze the OTP input structure in the relogin new window
"""

import asyncio
from playwright.async_api import async_playwright
import json
import pyotp

async def debug_relogin_new_window_detail():
    """Debug the relogin new window OTP input structure"""
    
    # Load BO config
    with open('configs/bo_env_config.json', 'r') as f:
        bo_config = json.load(f)
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()
        
        try:
            print("🎯 GETTING TO RELOGIN NEW WINDOW")
            print("="*50)
            
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
            
            # Click relogin button
            relogin_selector = '[title="Relogin To Account"]'
            relogin_button = page.locator(relogin_selector).first
            await relogin_button.click()
            print("✅ Clicked relogin button")
            
            await asyncio.sleep(3)
            
            # Switch to new window
            pages = context.pages
            if len(pages) > 1:
                new_page = pages[-1]
                await new_page.bring_to_front()
                print(f"🔄 Switched to new window: {new_page.url}")
                
                # Wait for page to load
                await new_page.wait_for_load_state("networkidle")
                await asyncio.sleep(3)
                
                print("\n🔍 ANALYZING NEW WINDOW STRUCTURE")
                print("="*50)
                
                # Take screenshot
                await new_page.screenshot(path="debug_detailed_relogin_window.png")
                print("📸 Detailed screenshot: debug_detailed_relogin_window.png")
                
                # Get page title
                title = await new_page.title()
                print(f"📄 Page title: {title}")
                
                # Get all input elements
                print("\n🔍 ALL INPUT ELEMENTS:")
                inputs = await new_page.locator('input').all()
                for i, input_elem in enumerate(inputs):
                    try:
                        input_type = await input_elem.get_attribute('type')
                        input_name = await input_elem.get_attribute('name')
                        input_placeholder = await input_elem.get_attribute('placeholder')
                        input_id = await input_elem.get_attribute('id')
                        input_class = await input_elem.get_attribute('class')
                        is_visible = await input_elem.is_visible()
                        is_enabled = await input_elem.is_enabled()
                        
                        print(f"  Input {i+1}:")
                        print(f"    Type: {input_type}")
                        print(f"    Name: {input_name}")
                        print(f"    Placeholder: {input_placeholder}")
                        print(f"    ID: {input_id}")
                        print(f"    Class: {input_class}")
                        print(f"    Visible: {is_visible}")
                        print(f"    Enabled: {is_enabled}")
                        
                        # Try to get the element HTML
                        try:
                            html = await input_elem.evaluate('el => el.outerHTML')
                            print(f"    HTML: {html}")
                        except:
                            pass
                        print()
                    except Exception as e:
                        print(f"    Error: {str(e)}")
                
                # Get all form elements
                print("\n🔍 ALL FORM ELEMENTS:")
                forms = await new_page.locator('form').all()
                for i, form in enumerate(forms):
                    try:
                        form_html = await form.evaluate('el => el.outerHTML')
                        print(f"  Form {i+1}: {form_html[:200]}...")
                    except:
                        print(f"  Form {i+1}: Could not get HTML")
                
                # Look for any element with "otp" or "code" text
                print("\n🔍 ELEMENTS WITH OTP/CODE TEXT:")
                otp_elements = await new_page.locator('*:has-text("otp"), *:has-text("code"), *:has-text("OTP"), *:has-text("Code")').all()
                for i, elem in enumerate(otp_elements):
                    try:
                        tag_name = await elem.evaluate('el => el.tagName')
                        text_content = await elem.text_content()
                        html = await elem.evaluate('el => el.outerHTML')
                        print(f"  Element {i+1} ({tag_name}): {text_content}")
                        print(f"    HTML: {html[:150]}...")
                    except:
                        print(f"  Element {i+1}: Could not analyze")
                
                # Get page HTML content for analysis
                content = await new_page.content()
                with open('debug_relogin_window_html.html', 'w') as f:
                    f.write(content)
                print(f"\n💾 Full HTML saved: debug_relogin_window_html.html")
                
                # Try to find any text input that might be hidden or styled differently
                print("\n🔍 TRYING ALTERNATIVE INPUT SELECTORS:")
                alt_selectors = [
                    'input',
                    '[type="text"]',
                    '[type="number"]',
                    '[type="tel"]',
                    '[role="textbox"]',
                    '[contenteditable="true"]',
                    'input:not([type="hidden"])',
                    'input[maxlength="6"]',
                    'input[pattern*="\\d"]'
                ]
                
                for selector in alt_selectors:
                    try:
                        elements = new_page.locator(selector)
                        count = await elements.count()
                        if count > 0:
                            print(f"  {selector}: {count} elements found")
                            for j in range(count):
                                try:
                                    elem = elements.nth(j)
                                    is_visible = await elem.is_visible()
                                    is_enabled = await elem.is_enabled()
                                    html = await elem.evaluate('el => el.outerHTML')
                                    print(f"    Element {j}: Visible={is_visible}, Enabled={is_enabled}")
                                    print(f"    HTML: {html}")
                                except:
                                    pass
                    except Exception as e:
                        print(f"  {selector}: Error - {str(e)}")
                
                print("\n⏸️  Browser will stay open for 60 seconds for manual inspection...")
                print("Please look for the OTP input field and note its exact selector/structure")
                await asyncio.sleep(60)
                
            else:
                print("❌ No new window opened")
                
        except Exception as e:
            print(f"❌ Error during debug: {str(e)}")
            
        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(debug_relogin_new_window_detail())
