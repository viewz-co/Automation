"""
Debug GL Account creation - visible browser, step by step
"""
import asyncio
import pyotp
import json
from playwright.async_api import async_playwright

async def debug_gl():
    with open('configs/stage_env_config.json', 'r') as f:
        config = json.load(f)
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, slow_mo=200)
        context = await browser.new_context(
            http_credentials={
                "username": config['basic_auth']['username'],
                "password": config['basic_auth']['password']
            }
        )
        page = await context.new_page()
        
        try:
            # Login
            print("🔐 Logging in...")
            await page.goto(f"{config['base_url']}/login")
            await page.fill('input[name="username"]', config['username'])
            await page.fill('input[name="password"]', config['password'])
            await page.click('button[type="submit"]')
            
            await page.wait_for_selector("text=Two-Factor Authentication", timeout=10000)
            otp = pyotp.TOTP(config['otp_secret']).now()
            await page.get_by_role("textbox").fill(otp)
            await asyncio.sleep(3)
            print(f"✅ Logged in: {page.url}")
            
            # Navigate
            print("📊 Going to Chart of Accounts...")
            await page.goto(f"{config['base_url']}/ledger/chart-of-accounts")
            await asyncio.sleep(3)
            
            # Click Add
            print("➕ Click Add GL Account...")
            await page.click("button:has-text('Add GL Account')")
            await asyncio.sleep(2)
            
            # Get row
            row = page.locator("tr:has-text('Auto')").first
            cells = row.locator("td")
            
            # Log cell count and find all buttons/comboboxes in row
            cell_count = await cells.count()
            print(f"📋 Row has {cell_count} cells")
            
            # List what's in each cell
            for i in range(min(10, cell_count)):
                cell = cells.nth(i)
                btn = cell.locator("button, [role='combobox']")
                inp = cell.locator("input")
                btn_count = await btn.count()
                inp_count = await inp.count()
                text = await cell.inner_text()
                print(f"   Cell {i}: '{text[:20]}...' | buttons: {btn_count}, inputs: {inp_count}")
            
            # Fill Name
            print("\n1️⃣ FILL NAME...")
            name_input = cells.nth(1).locator("input")
            await name_input.click()
            await name_input.fill("Debug GL Account")
            print("   ✅ Name filled")
            
            # Close any dropdown
            await page.keyboard.press("Escape")
            await asyncio.sleep(0.5)
            
            # Click outside to ensure name is committed
            await cells.nth(0).click()
            await asyncio.sleep(0.5)
            
            # Currency
            print("\n2️⃣ CURRENCY...")
            currency_cell = cells.nth(2)
            currency_btn = currency_cell.locator("button").first
            print(f"   Found button in cell 2: {await currency_btn.count() > 0}")
            await currency_btn.click()
            await asyncio.sleep(1)
            
            # List options
            options = page.locator("[role='option']")
            opt_count = await options.count()
            print(f"   Options visible: {opt_count}")
            if opt_count > 0:
                print("   First 3 options:")
                for i in range(min(3, opt_count)):
                    print(f"      {await options.nth(i).text_content()}")
            
            # Select US Dollar
            usd = page.locator("[role='option']:has-text('US Dollar')").first
            if await usd.count() > 0:
                await usd.click()
                print("   ✅ USD selected")
            await asyncio.sleep(1)
            
            # Click outside
            await page.keyboard.press("Escape")
            await asyncio.sleep(0.5)
            
            # Report Type
            print("\n3️⃣ REPORT TYPE...")
            report_cell = cells.nth(3)
            report_btn = report_cell.locator("button").first
            print(f"   Found button in cell 3: {await report_btn.count() > 0}")
            
            # Try clicking button directly
            try:
                await report_btn.click(timeout=5000)
            except Exception as e:
                print(f"   ❌ Button click failed: {str(e)[:50]}")
                # Try clicking cell
                try:
                    await report_cell.click(force=True)
                except Exception as e2:
                    print(f"   ❌ Cell click failed: {str(e2)[:50]}")
            
            await asyncio.sleep(1)
            
            options = page.locator("[role='option']")
            opt_count = await options.count()
            print(f"   Options visible: {opt_count}")
            if opt_count > 0:
                print("   Options:")
                for i in range(min(5, opt_count)):
                    print(f"      {await options.nth(i).text_content()}")
                
                # Select Balance Sheet
                balance = page.locator("[role='option']:has-text('Balance')").first
                if await balance.count() > 0:
                    await balance.click()
                    print("   ✅ Balance Sheet selected")
            
            await asyncio.sleep(1)
            await page.screenshot(path="debug_after_report_type.png")
            
            # Show current row state
            print("\n📸 Current row state:")
            for i in range(min(8, cell_count)):
                cell = cells.nth(i)
                text = await cell.inner_text()
                print(f"   Cell {i}: '{text[:25]}'")
            
            print("\n🔍 Browser stays open 30 seconds...")
            await asyncio.sleep(30)
            
        except Exception as e:
            print(f"❌ Error: {e}")
            import traceback
            traceback.print_exc()
            await page.screenshot(path="debug_error.png")
        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(debug_gl())

