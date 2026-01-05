"""
Debug GL Account creation - visible browser with detailed logging
"""
import asyncio
import pyotp
import json
from playwright.async_api import async_playwright

async def debug_gl_creation():
    with open('configs/stage_env_config.json', 'r') as f:
        config = json.load(f)
    
    base_url = config['base_url']
    username = config['username']
    password = config['password']
    otp_secret = config['otp_secret']
    basic_auth = config.get('basic_auth', {})
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, slow_mo=100)
        context = await browser.new_context(
            http_credentials={
                "username": basic_auth.get("username", ""),
                "password": basic_auth.get("password", "")
            } if basic_auth else None
        )
        page = await context.new_page()
        
        try:
            # Login
            print("🔐 Logging in...")
            await page.goto(f"{base_url}/login")
            await page.fill('input[name="username"]', username)
            await page.fill('input[name="password"]', password)
            await page.click('button[type="submit"]')
            
            await page.wait_for_selector("text=Two-Factor Authentication", timeout=10000)
            otp = pyotp.TOTP(otp_secret).now()
            await page.get_by_role("textbox").fill(otp)
            await asyncio.sleep(3)
            print(f"✅ Logged in: {page.url}")
            
            # Navigate
            print("📊 Going to Chart of Accounts...")
            await page.goto(f"{base_url}/ledger/chart-of-accounts")
            await asyncio.sleep(3)
            
            # Click Add
            print("➕ Adding GL Account...")
            await page.click("button:has-text('Add GL Account')")
            await asyncio.sleep(2)
            
            # Get row
            row = page.locator("tr:has-text('Auto')").first
            cells = row.locator("td")
            cell_count = await cells.count()
            print(f"📋 Row has {cell_count} cells")
            
            # Fill Name
            print("\n1️⃣ FILLING NAME...")
            name_input = cells.nth(1).locator("input")
            await name_input.click()
            await asyncio.sleep(0.3)
            await name_input.fill("DEBUG GL Account 123")
            await asyncio.sleep(0.5)
            
            # Tab out of name field
            await page.keyboard.press("Tab")
            await asyncio.sleep(1)
            
            print("   Name filled and tabbed out")
            await page.screenshot(path="debug_1_name.png")
            
            # Currency dropdown
            print("\n2️⃣ CURRENCY DROPDOWN...")
            currency_cell = cells.nth(2)
            
            # What's in the cell?
            cell_html = await currency_cell.inner_html()
            print(f"   Cell HTML: {cell_html[:200]}...")
            
            # Click the cell
            await currency_cell.click()
            await asyncio.sleep(1)
            
            # Check if dropdown opened
            options = page.locator("[role='option']")
            opt_count = await options.count()
            print(f"   Found {opt_count} options after clicking cell")
            
            if opt_count > 0:
                # List first 5 options
                for i in range(min(5, opt_count)):
                    opt_text = await options.nth(i).text_content()
                    print(f"      Option {i}: {opt_text}")
                
                # Select USD
                usd = page.locator("[role='option']:has-text('US Dollar')")
                if await usd.count() > 0:
                    await usd.first.click()
                    print("   ✅ Selected US Dollar")
                else:
                    usd = page.locator("[role='option']:has-text('USD')")
                    if await usd.count() > 0:
                        await usd.first.click()
                        print("   ✅ Selected USD")
            else:
                print("   ⚠️ No dropdown options - trying to find button in cell")
                btn = currency_cell.locator("button")
                if await btn.count() > 0:
                    await btn.first.click()
                    await asyncio.sleep(1)
                    opt_count = await options.count()
                    print(f"   After clicking button: {opt_count} options")
            
            await asyncio.sleep(1)
            await page.screenshot(path="debug_2_currency.png")
            
            # Report Type
            print("\n3️⃣ REPORT TYPE...")
            report_cell = cells.nth(3)
            cell_html = await report_cell.inner_html()
            print(f"   Cell HTML: {cell_html[:150]}...")
            
            await report_cell.click()
            await asyncio.sleep(1)
            
            options = page.locator("[role='option']")
            opt_count = await options.count()
            print(f"   Found {opt_count} options")
            
            if opt_count > 0:
                for i in range(min(5, opt_count)):
                    opt_text = await options.nth(i).text_content()
                    print(f"      Option {i}: {opt_text}")
                
                balance = page.locator("[role='option']:has-text('Balance')")
                if await balance.count() > 0:
                    await balance.first.click()
                    print("   ✅ Selected Balance Sheet")
            
            await asyncio.sleep(1)
            await page.screenshot(path="debug_3_report_type.png")
            
            # Type
            print("\n4️⃣ TYPE...")
            type_cell = cells.nth(4)
            await type_cell.click()
            await asyncio.sleep(1)
            
            options = page.locator("[role='option']")
            opt_count = await options.count()
            print(f"   Found {opt_count} options")
            
            if opt_count > 0:
                for i in range(min(5, opt_count)):
                    opt_text = await options.nth(i).text_content()
                    print(f"      Option {i}: {opt_text}")
                
                current = page.locator("[role='option']:has-text('Current')")
                if await current.count() > 0:
                    await current.first.click()
                    print("   ✅ Selected Current Assets")
            
            await asyncio.sleep(1)
            await page.screenshot(path="debug_4_type.png")
            
            # Group
            print("\n5️⃣ GROUP...")
            group_cell = cells.nth(5)
            await group_cell.click()
            await asyncio.sleep(1)
            
            options = page.locator("[role='option']")
            opt_count = await options.count()
            print(f"   Found {opt_count} options")
            
            if opt_count > 0:
                for i in range(min(8, opt_count)):
                    opt_text = await options.nth(i).text_content()
                    print(f"      Option {i}: {opt_text}")
                
                trade = page.locator("[role='option']:has-text('Trade')")
                if await trade.count() > 0:
                    await trade.first.click()
                    print("   ✅ Selected Trade Receivables")
            
            await asyncio.sleep(1)
            await page.screenshot(path="debug_5_group.png")
            
            # EBITDA
            print("\n6️⃣ EBITDA...")
            ebitda_cell = cells.nth(6)
            await ebitda_cell.click()
            await asyncio.sleep(1)
            
            options = page.locator("[role='option']")
            opt_count = await options.count()
            print(f"   Found {opt_count} options")
            
            if opt_count > 0:
                for i in range(min(5, opt_count)):
                    opt_text = await options.nth(i).text_content()
                    print(f"      Option {i}: {opt_text}")
                
                non_ebitda = page.locator("[role='option']:has-text('Non')")
                if await non_ebitda.count() > 0:
                    await non_ebitda.first.click()
                    print("   ✅ Selected Non-EBITDA")
            
            await asyncio.sleep(1)
            await page.screenshot(path="debug_6_ebitda.png")
            
            # Cashflow
            print("\n7️⃣ CASHFLOW...")
            cashflow_cell = cells.nth(7)
            await cashflow_cell.click()
            await asyncio.sleep(1)
            
            options = page.locator("[role='option']")
            opt_count = await options.count()
            print(f"   Found {opt_count} options")
            
            if opt_count > 0:
                for i in range(min(5, opt_count)):
                    opt_text = await options.nth(i).text_content()
                    print(f"      Option {i}: {opt_text}")
                
                operating = page.locator("[role='option']:has-text('Operating')")
                if await operating.count() > 0:
                    await operating.first.click()
                    print("   ✅ Selected Operating")
            
            await asyncio.sleep(1)
            await page.screenshot(path="debug_7_cashflow.png")
            
            # Final state before save
            print("\n📸 Taking final screenshot before save...")
            await page.screenshot(path="debug_8_before_save.png")
            
            # Save
            print("\n💾 SAVING...")
            save_btn = row.locator("button:has(svg)").first
            if await save_btn.is_visible():
                await save_btn.click()
                print("   Clicked save button")
            
            await asyncio.sleep(5)
            await page.screenshot(path="debug_9_after_save.png")
            
            # Check for errors
            error = page.locator("text=Missing Required")
            if await error.is_visible():
                print("   ❌ Validation errors visible")
                error_content = await page.locator("[class*='error'], [role='alert']").first.inner_text()
                print(f"   Error: {error_content[:300]}")
            else:
                print("   ✅ No validation errors!")
                
                # Check if row is gone (saved)
                new_row = page.locator("tr:has-text('Auto-generated')")
                if await new_row.count() == 0:
                    print("   ✅ Account saved - row no longer in edit mode")
                else:
                    print("   ⚠️ Row still in edit mode")
            
            print("\n🔍 Browser stays open for 20 seconds...")
            await asyncio.sleep(20)
            
        except Exception as e:
            print(f"❌ Error: {e}")
            await page.screenshot(path="debug_error.png")
        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(debug_gl_creation())
