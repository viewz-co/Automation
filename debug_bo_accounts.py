#!/usr/bin/env python3
"""
Debug BO Accounts Page
Script to inspect the accounts page structure after successful login
"""

import asyncio
from playwright.async_api import async_playwright
import json
import pyotp

async def debug_bo_accounts_page():
    """Debug the BO accounts page to understand its structure"""
    
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
            
            await asyncio.sleep(3)
            print("✅ Login completed")
            
            # Navigate to accounts page
            print("🏠 Navigating to accounts page...")
            await page.goto(f"{bo_config['base_url']}/accounts")
            await page.wait_for_load_state("networkidle")
            
            # Take screenshot
            await page.screenshot(path="debug_bo_accounts_page.png")
            print("📸 Screenshot saved: debug_bo_accounts_page.png")
            
            # Check page title and URL
            title = await page.title()
            url = page.url
            print(f"📄 Page title: {title}")
            print(f"🔗 Current URL: {url}")
            
            # Check for any text content
            print("\n📄 Page text content:")
            text_content = await page.text_content('body')
            print(text_content[:500] + "..." if len(text_content) > 500 else text_content)
            
            # Look for table elements
            print("\n🔍 Looking for table elements:")
            tables = await page.locator('table').all()
            print(f"Found {len(tables)} table(s)")
            
            for i, table in enumerate(tables):
                try:
                    table_text = await table.text_content()
                    print(f"Table {i+1} content: {table_text[:200]}...")
                except:
                    print(f"Table {i+1}: Could not get content")
            
            # Look for list elements
            print("\n🔍 Looking for list elements:")
            lists = await page.locator('ul, ol').all()
            print(f"Found {len(lists)} list(s)")
            
            # Look for divs that might contain accounts
            print("\n🔍 Looking for potential account containers:")
            divs_with_account = await page.locator('div:has-text("account"), div:has-text("Account")').all()
            print(f"Found {len(divs_with_account)} div(s) with 'account' text")
            
            # Look for any buttons with relogin text
            print("\n🔍 Looking for relogin buttons:")
            relogin_buttons = await page.locator('button:has-text("login"), button:has-text("Login"), a:has-text("login"), a:has-text("Login")').all()
            print(f"Found {len(relogin_buttons)} potential relogin button(s)")
            
            for i, btn in enumerate(relogin_buttons):
                try:
                    btn_text = await btn.text_content()
                    print(f"Button {i+1}: {btn_text}")
                except:
                    print(f"Button {i+1}: Could not get text")
            
            # Look for any rows in tables
            print("\n🔍 Looking for table rows:")
            rows = await page.locator('tr').all()
            print(f"Found {len(rows)} row(s)")
            
            for i, row in enumerate(rows[:5]):  # Show first 5 rows
                try:
                    row_text = await row.text_content()
                    print(f"Row {i+1}: {row_text}")
                except:
                    print(f"Row {i+1}: Could not get text")
            
            # Save page content
            content = await page.content()
            with open('debug_bo_accounts_content.html', 'w') as f:
                f.write(content)
            print("\n💾 Page content saved: debug_bo_accounts_content.html")
            
            # Wait to keep browser open for inspection
            print("\n⏸️  Browser will stay open for 30 seconds for manual inspection...")
            await asyncio.sleep(30)
            
        except Exception as e:
            print(f"❌ Error during debug: {str(e)}")
            await page.screenshot(path="debug_bo_accounts_error.png")
            
        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(debug_bo_accounts_page())
