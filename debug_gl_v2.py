"""
Debug GL Account creation with visible browser - step by step
"""
import asyncio
import pyotp
import json
from playwright.async_api import async_playwright

async def debug_gl():
    with open('configs/stage_env_config.json', 'r') as f:
        config = json.load(f)
    
    base_url = config['base_url']
    username = config['username']
    password = config['password']
    otp_secret = config['otp_secret']
    basic_auth = config.get('basic_auth', {})
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, slow_mo=300)
        context = await browser.new_context(
            http_credentials={"username": basic_auth.get("username", ""), "password": basic_auth.get("password", "")}
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
            
            # Navigate to Chart of Accounts
            print("📊 Navigating to Chart of Accounts...")
            await page.goto(f"{base_url}/ledger/chart-of-accounts")
            await asyncio.sleep(3)
            
            # Click Add GL Account
            print("➕ Clicking Add GL Account...")
            await page.click("button:has-text('Add GL Account')")
            await asyncio.sleep(2)
            
            # Find the new row
            row = page.locator("tr:has-text('Auto')").first
            cells = row.locator("td")
            cell_count = await cells.count()
            print(f"📋 Row has {cell_count} cells")
            
            # Step 1: Fill Name
            print("\n1️⃣ FILLING NAME...")
            name_input = cells.nth(1).locator("input")
            await name_input.click()
            await name_input.fill("AR Test DEBUG Account")
            await asyncio.sleep(1)
            value = await name_input.input_value()
            print(f"   Name value: '{value}'")
            await page.screenshot(path="debug_step1_name.png")
            
            # Step 2: Currency - Click cell 2
            print("\n2️⃣ CURRENCY DROPDOWN...")
            currency_cell = cells.nth(2)
            
            # Check what's in the cell
            cell_html = await currency_cell.inner_html()
            print(f"   Cell HTML: {cell_html[:200]}...")
            
            # Try clicking the cell
            await currency_cell.click()
            await asyncio.sleep(1.5)
            
            # Check if dropdown opened
            options = page.locator("[role='option']")
            opt_count = await options.count()
            print(f"   Found {opt_count} options after clicking cell")
            
            if opt_count > 0:
                # Show first few options
                for i in range(min(opt_count, 5)):
                    txt = await options.nth(i).text_content()
                    print(f"      Option {i}: {txt}")
                
                # Select USD
                usd = page.locator("[role='option']:has-text('US Dollar'), [role='option']:has-text('USD')")
                if await usd.count() > 0:
                    await usd.first.click()
                    print("   ✅ Selected USD")
                    await asyncio.sleep(1)
            
            await page.screenshot(path="debug_step2_currency.png")
            
            # Step 3: Report Type - Cell 3
            print("\n3️⃣ REPORT TYPE DROPDOWN...")
            
            # Re-get row reference
            row = page.locator("tr:has-text('Auto')").first
            cells = row.locator("td")
            
            report_cell = cells.nth(3)
            cell_html = await report_cell.inner_html()
            print(f"   Cell HTML: {cell_html[:200]}...")
            
            await report_cell.click()
            await asyncio.sleep(1.5)
            
            options = page.locator("[role='option']")
            opt_count = await options.count()
            print(f"   Found {opt_count} options")
            
            if opt_count > 0:
                for i in range(min(opt_count, 5)):
                    txt = await options.nth(i).text_content()
                    print(f"      Option {i}: {txt}")
                
                # Select Balance Sheet
                bs = page.locator("[role='option']:has-text('Balance')")
                if await bs.count() > 0:
                    await bs.first.click()
                    print("   ✅ Selected Balance Sheet")
                    await asyncio.sleep(1)
            
            await page.screenshot(path="debug_step3_report_type.png")
            
            # Step 4: Type - Cell 4
            print("\n4️⃣ TYPE DROPDOWN...")
            
            row = page.locator("tr:has-text('Auto')").first
            cells = row.locator("td")
            
            type_cell = cells.nth(4)
            await type_cell.click()
            await asyncio.sleep(1.5)
            
            options = page.locator("[role='option']")
            opt_count = await options.count()
            print(f"   Found {opt_count} options")
            
            if opt_count > 0:
                for i in range(min(opt_count, 5)):
                    txt = await options.nth(i).text_content()
                    print(f"      Option {i}: {txt}")
                
                # Select Current Assets
                ca = page.locator("[role='option']:has-text('Current Assets')")
                if await ca.count() > 0:
                    await ca.first.click()
                    print("   ✅ Selected Current Assets")
                    await asyncio.sleep(1)
            
            await page.screenshot(path="debug_step4_type.png")
            
            # Step 5: Group - Cell 5
            print("\n5️⃣ GROUP DROPDOWN...")
            
            row = page.locator("tr:has-text('Auto')").first
            cells = row.locator("td")
            
            group_cell = cells.nth(5)
            await group_cell.click()
            await asyncio.sleep(1.5)
            
            options = page.locator("[role='option']")
            opt_count = await options.count()
            print(f"   Found {opt_count} options")
            
            if opt_count > 0:
                for i in range(min(opt_count, 8)):
                    txt = await options.nth(i).text_content()
                    print(f"      Option {i}: {txt}")
                
                # Select Trade Receivables
                tr = page.locator("[role='option']:has-text('Trade Receivables'), [role='option']:has-text('Trade receivables')")
                if await tr.count() > 0:
                    await tr.first.click()
                    print("   ✅ Selected Trade Receivables")
                    await asyncio.sleep(1)
            
            await page.screenshot(path="debug_step5_group.png")
            
            # Step 6: EBITDA - Cell 6
            print("\n6️⃣ EBITDA DROPDOWN...")
            
            row = page.locator("tr:has-text('Auto')").first
            cells = row.locator("td")
            
            ebitda_cell = cells.nth(6)
            await ebitda_cell.click()
            await asyncio.sleep(1.5)
            
            options = page.locator("[role='option']")
            opt_count = await options.count()
            print(f"   Found {opt_count} options")
            
            if opt_count > 0:
                for i in range(min(opt_count, 8)):
                    txt = await options.nth(i).text_content()
                    print(f"      Option {i}: {txt}")
                
                # Try to find Non-EBITDA or similar
                for pattern in ['Non-EBITDA', 'Non EBITDA', 'non-ebitda', 'None']:
                    ne = page.locator(f"[role='option']:has-text('{pattern}')")
                    if await ne.count() > 0:
                        await ne.first.click()
                        print(f"   ✅ Selected: {pattern}")
                        break
                await asyncio.sleep(1)
            
            await page.screenshot(path="debug_step6_ebitda.png")
            
            # Step 7: Cashflow - Cell 7
            print("\n7️⃣ CASHFLOW DROPDOWN...")
            
            row = page.locator("tr:has-text('Auto')").first
            cells = row.locator("td")
            
            cashflow_cell = cells.nth(7)
            await cashflow_cell.click()
            await asyncio.sleep(1.5)
            
            options = page.locator("[role='option']")
            opt_count = await options.count()
            print(f"   Found {opt_count} options")
            
            if opt_count > 0:
                for i in range(min(opt_count, 8)):
                    txt = await options.nth(i).text_content()
                    print(f"      Option {i}: {txt}")
                
                # Try to find Operating or similar
                for pattern in ['Operating', 'Intra', 'CFO']:
                    op = page.locator(f"[role='option']:has-text('{pattern}')")
                    if await op.count() > 0:
                        await op.first.click()
                        print(f"   ✅ Selected: {pattern}")
                        break
                await asyncio.sleep(1)
            
            await page.screenshot(path="debug_step7_cashflow.png")
            
            # Step 8: Save
            print("\n8️⃣ SAVING...")
            
            row = page.locator("tr:has-text('Auto')").first
            save_btn = row.locator("button:has(svg)").first
            
            if await save_btn.is_visible():
                await save_btn.click()
                print("   Clicked save button")
            
            await asyncio.sleep(3)
            await page.screenshot(path="debug_step8_after_save.png")
            
            # Check for validation error
            error = page.locator("text=Missing Required")
            if await error.is_visible():
                print("\n❌ VALIDATION ERROR - Missing Required Fields")
                error_content = await page.locator(".text-red-500, .text-destructive").all_text_contents()
                print(f"   Errors: {error_content}")
            else:
                print("\n✅ No validation error popup!")
                
                # Check if row still shows Auto-generated
                auto_row = page.locator("tr:has-text('Auto-generated')")
                if await auto_row.count() == 0:
                    print("   ✅ Account saved - edit row is gone!")
                else:
                    print("   ⚠️ Edit row still present")
            
            print("\n🔍 Keeping browser open for 30 seconds...")
            await asyncio.sleep(30)
            
        except Exception as e:
            print(f"❌ Error: {e}")
            await page.screenshot(path="debug_error.png")
        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(debug_gl())


