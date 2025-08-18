#!/usr/bin/env python3
"""
Debug BO After Login
Script to see what's available after successful BO login
"""

import asyncio
from playwright.async_api import async_playwright
import json
import pyotp

async def debug_bo_after_login():
    """Debug what's available after BO login"""
    
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
            
            # Handle OTP
            await asyncio.sleep(2)
            totp = pyotp.TOTP(bo_config['otp_secret'])
            otp_code = totp.now()
            print(f"🔐 Generated OTP: {otp_code}")
            
            await page.wait_for_selector("text=code", timeout=10000)
            await page.fill('input[type="text"]', otp_code)
            await page.click('button:has-text("Verify")')
            
            await asyncio.sleep(5)
            print("✅ Login completed")
            
            # Check where we are after login
            url = page.url
            title = await page.title()
            print(f"📄 Current page after login:")
            print(f"   URL: {url}")
            print(f"   Title: {title}")
            
            # Take screenshot
            await page.screenshot(path="debug_bo_after_login.png")
            print("📸 Screenshot saved: debug_bo_after_login.png")
            
            # Look for navigation elements
            print("\n🔍 Looking for navigation elements:")
            nav_elements = await page.locator('nav, .nav, .navigation, .menu, a').all()
            print(f"Found {len(nav_elements)} potential navigation elements")
            
            unique_links = set()
            for i, nav_elem in enumerate(nav_elements):
                try:
                    text = await nav_elem.text_content()
                    href = await nav_elem.get_attribute('href')
                    if text and text.strip():
                        text = text.strip()
                        if href:
                            unique_links.add(f"{text} -> {href}")
                        else:
                            unique_links.add(f"{text}")
                except:
                    continue
            
            print("\n📋 Found navigation/link options:")
            for link in sorted(unique_links):
                if any(keyword in link.lower() for keyword in ['account', 'user', 'admin', 'dashboard', 'home', 'manage']):
                    print(f"   ⭐ {link}")
                else:
                    print(f"   - {link}")
            
            # Look for any text containing "account"
            print("\n🔍 Looking for text containing 'account':")
            account_elements = await page.locator('text=account, text=Account, text=ACCOUNT').all()
            print(f"Found {len(account_elements)} elements with 'account' text")
            
            for i, elem in enumerate(account_elements):
                try:
                    text = await elem.text_content()
                    print(f"   Account element {i+1}: {text}")
                except:
                    print(f"   Account element {i+1}: Could not get text")
            
            # Look for buttons that might lead to account management
            print("\n🔍 Looking for management/admin buttons:")
            mgmt_buttons = await page.locator('button, a').all()
            
            for btn in mgmt_buttons:
                try:
                    text = await btn.text_content()
                    if text and any(keyword in text.lower() for keyword in ['account', 'user', 'manage', 'admin', 'relogin']):
                        href = await btn.get_attribute('href')
                        print(f"   🎯 Management button: {text} {f'-> {href}' if href else ''}")
                except:
                    continue
            
            # Try common BO admin paths
            print("\n🔍 Testing common BO admin paths:")
            common_paths = [
                '/dashboard',
                '/admin',
                '/users',
                '/accounts',
                '/manage',
                '/user-management',
                '/account-management'
            ]
            
            for path in common_paths:
                try:
                    test_url = f"{bo_config['base_url']}{path}"
                    print(f"   Testing: {test_url}")
                    
                    # Try to navigate
                    response = await page.goto(test_url, wait_until="networkidle", timeout=5000)
                    if response and response.status == 200:
                        await asyncio.sleep(1)
                        page_title = await page.title()
                        page_text = await page.text_content('body')
                        
                        if 'account' in page_text.lower() or 'user' in page_text.lower():
                            print(f"   ✅ {path} -> Found account/user related content!")
                            print(f"      Title: {page_title}")
                            await page.screenshot(path=f"debug_bo_path_{path.replace('/', '_')}.png")
                        else:
                            print(f"   ℹ️  {path} -> Accessible but no account content detected")
                    else:
                        print(f"   ❌ {path} -> Not accessible")
                        
                except Exception as e:
                    print(f"   ❌ {path} -> Error: {str(e)[:100]}")
            
            # Go back to the main page after login
            await page.goto(url)
            await asyncio.sleep(2)
            
            # Save page content for analysis
            content = await page.content()
            with open('debug_bo_after_login_content.html', 'w') as f:
                f.write(content)
            print(f"\n💾 Page content saved: debug_bo_after_login_content.html")
            
            # Wait to keep browser open for inspection
            print("\n⏸️  Browser will stay open for 60 seconds for manual inspection...")
            await asyncio.sleep(60)
            
        except Exception as e:
            print(f"❌ Error during debug: {str(e)}")
            await page.screenshot(path="debug_bo_after_login_error.png")
            
        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(debug_bo_after_login())
