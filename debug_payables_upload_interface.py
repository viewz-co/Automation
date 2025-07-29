#!/usr/bin/env python3
"""
Debug script to investigate Payables upload interface
"""

import asyncio
import os
from playwright.async_api import async_playwright
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

async def debug_payables_interface():
    """Debug the actual Payables page to find upload interface"""
    
    # Setup (using same env vars as tests)
    base_url = os.getenv('BASE_URL', 'https://app.viewz.co')
    username = os.getenv('TEST_USERNAME')
    password = os.getenv('TEST_PASSWORD')
    totp_secret = os.getenv('TEST_TOTP_SECRET')
    
    if not username or not password:
        print("❌ Missing credentials. Set TEST_USERNAME, TEST_PASSWORD environment variables")
        return
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, slow_mo=1000)
        context = await browser.new_context(base_url=base_url)
        page = await context.new_page()
        
        try:
            print("🔍 Starting Payables interface investigation...")
            
            # Login
            print("📝 Logging in...")
            await page.goto("/login")
            await page.fill('input[name="username"]', username)
            await page.fill('input[name="password"]', password)
            await page.click('button[type="submit"]')
            
            # Handle 2FA (using same logic as working tests)
            print("🔐 Handling 2FA...")
            import pyotp
            secret = "HA2ECLBIKYUEEI2GPUUSMN3XIMXFETRQ"  # Same as working tests
            otp = pyotp.TOTP(secret).now()
            
            try:
                await page.wait_for_selector("text=Two-Factor Authentication", timeout=5000)
                await page.get_by_role("textbox").fill(otp)
                await asyncio.sleep(3)
                
                # Try to wait for success indicators
                try:
                    await page.wait_for_selector("text=SuccessOTP verified successfully", timeout=5000)
                    print("✅ 2FA success message detected")
                except:
                    try:
                        await page.wait_for_selector("text=Success", timeout=2000)
                        print("✅ 2FA generic success detected")
                    except:
                        try:
                            await page.wait_for_url("**/home**", timeout=3000)
                            print("✅ 2FA success - redirected to home")
                        except:
                            print("⚠️ 2FA may have completed without clear indicator")
                            await asyncio.sleep(2)
            except Exception as e:
                print(f"⚠️ 2FA handling failed: {str(e)}")
            
            # Entity selection
            print("🏢 Selecting entity...")
            try:
                await page.click("button:has-text('Demo')")
                await page.click("text=Viewz Demo INC")
                await asyncio.sleep(2)
            except:
                print("⚠️ Entity selection may have been skipped")
            
            # Navigate with menu reveal
            print("🧭 Navigating to Payables...")
            
            # Menu reveal
            logo = page.locator("svg.viewz-logo")
            if await logo.count() > 0:
                box = await logo.bounding_box()
                if box:
                    await page.mouse.move(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)
                    await asyncio.sleep(0.5)
            
            # Pin menu
            pin_button = page.locator("button:has(svg.lucide-pin)")
            if await pin_button.count() > 0 and await pin_button.is_visible():
                await pin_button.click()
                await asyncio.sleep(0.5)
            
            # Navigate to Reconciliation
            await page.click("text=Reconciliation")
            await asyncio.sleep(1)
            
            # Navigate to Payables
            await page.click("text=Payables")
            await asyncio.sleep(3)
            
            print("🔍 Analyzing Payables page structure...")
            
            # Take screenshot
            await page.screenshot(path="debug_payables_page.png", full_page=True)
            print("📸 Screenshot saved: debug_payables_page.png")
            
            # Analyze page content
            page_title = await page.title()
            current_url = page.url
            print(f"📄 Page title: {page_title}")
            print(f"🔗 Current URL: {current_url}")
            
            # Look for common upload-related elements
            upload_candidates = [
                "input[type='file']",
                "button:has-text('Upload')", 
                "button:has-text('Browse')",
                "button:has-text('Add')",
                "button:has-text('Import')",
                "button:has-text('New')",
                "button:has-text('Create')",
                ".upload-area",
                ".dropzone",
                "[data-testid*='upload']",
                "[data-testid*='file']",
                "button[data-action*='upload']",
                ".file-upload",
                ".upload-btn",
                ".add-btn"
            ]
            
            print("\n🔍 Searching for upload interface elements...")
            found_elements = []
            
            for selector in upload_candidates:
                try:
                    elements = page.locator(selector)
                    count = await elements.count()
                    if count > 0:
                        print(f"✅ Found {count} element(s): {selector}")
                        for i in range(min(count, 3)):  # Check first 3 elements
                            try:
                                element = elements.nth(i)
                                text = await element.text_content()
                                is_visible = await element.is_visible()
                                tag_name = await element.evaluate("el => el.tagName.toLowerCase()")
                                classes = await element.get_attribute("class") or ""
                                print(f"   [{i}] {tag_name} - Text: '{text}' - Visible: {is_visible} - Classes: '{classes}'")
                                found_elements.append({
                                    'selector': selector,
                                    'index': i,
                                    'text': text,
                                    'visible': is_visible,
                                    'tag': tag_name,
                                    'classes': classes
                                })
                            except Exception as e:
                                print(f"   [{i}] Error getting details: {str(e)}")
                except Exception as e:
                    print(f"❌ Error with selector {selector}: {str(e)}")
            
            # Check for any buttons on the page
            print("\n🔍 All buttons on the page:")
            all_buttons = page.locator("button")
            button_count = await all_buttons.count()
            print(f"📊 Total buttons found: {button_count}")
            
            for i in range(min(button_count, 10)):  # Show first 10 buttons
                try:
                    button = all_buttons.nth(i)
                    text = await button.text_content()
                    is_visible = await button.is_visible()
                    classes = await button.get_attribute("class") or ""
                    print(f"   Button[{i}]: '{text}' - Visible: {is_visible} - Classes: '{classes}'")
                except:
                    print(f"   Button[{i}]: Error getting details")
            
            # Check for file input elements specifically
            print("\n🔍 File input elements:")
            file_inputs = page.locator("input[type='file']")
            file_count = await file_inputs.count()
            print(f"📊 File inputs found: {file_count}")
            
            if file_count > 0:
                for i in range(file_count):
                    try:
                        file_input = file_inputs.nth(i)
                        is_visible = await file_input.is_visible()
                        name = await file_input.get_attribute("name") or ""
                        id_attr = await file_input.get_attribute("id") or ""
                        accept = await file_input.get_attribute("accept") or ""
                        print(f"   FileInput[{i}]: Visible: {is_visible} - Name: '{name}' - ID: '{id_attr}' - Accept: '{accept}'")
                    except:
                        print(f"   FileInput[{i}]: Error getting details")
            
            print("\n📊 Summary of potential upload elements:")
            if found_elements:
                for elem in found_elements:
                    print(f"✅ {elem['selector']} - '{elem['text']}' (Visible: {elem['visible']})")
            else:
                print("❌ No obvious upload interface elements found")
                print("💡 The upload functionality might be:")
                print("   - Hidden behind another action (like clicking a specific button)")
                print("   - Part of a modal/popup that opens")
                print("   - Using drag-and-drop instead of buttons")
                print("   - Located in a different section")
            
            # Wait for manual inspection
            print("\n⏱️ Page will stay open for 30 seconds for manual inspection...")
            print("🔍 Check the browser window to see the actual Payables page")
            await asyncio.sleep(30)
            
        except Exception as e:
            print(f"❌ Debug failed: {str(e)}")
            await page.screenshot(path="debug_error.png")
        
        finally:
            await browser.close()
            print("🏁 Debug session completed")

if __name__ == "__main__":
    asyncio.run(debug_payables_interface()) 