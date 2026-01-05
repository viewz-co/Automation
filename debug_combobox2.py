"""Debug - click cell first, then find combobox"""
import asyncio
import pyotp
import json
from playwright.async_api import async_playwright

async def select_from_dropdown(page, cell, option_text, field_name):
    """Click cell, wait for combobox, click combobox, select option"""
    print(f"   {field_name}...")
    
    # Step 1: Click the cell to activate it
    await cell.click()
    await asyncio.sleep(0.8)
    
    # Step 2: Now find the combobox button that appeared
    combo = cell.locator("button[role='combobox']")
    if await combo.count() > 0:
        print(f"      Found combobox button")
        await combo.first.click()
        await asyncio.sleep(0.8)
        
        # Step 3: Find and click the option
        opts = page.locator("[role='option']")
        opt_count = await opts.count()
        print(f"      {opt_count} options available")
        
        if opt_count > 0:
            target = page.locator(f"[role='option']:has-text('{option_text}')")
            if await target.count() > 0:
                await target.first.click()
                print(f"      ✅ Selected: {option_text}")
                await asyncio.sleep(0.5)
                return True
            else:
                # Just click first option
                await opts.first.click()
                first_text = await opts.first.text_content()
                print(f"      ⚠️ '{option_text}' not found, selected: {first_text}")
                await asyncio.sleep(0.5)
                return True
    else:
        # Check if options are already visible
        opts = page.locator("[role='option']")
        opt_count = await opts.count()
        if opt_count > 0:
            print(f"      Options already visible: {opt_count}")
            target = page.locator(f"[role='option']:has-text('{option_text}')")
            if await target.count() > 0:
                await target.first.click()
                print(f"      ✅ Selected: {option_text}")
                await asyncio.sleep(0.5)
                return True
        print(f"      ⚠️ No combobox found")
    return False

async def debug():
    with open('configs/stage_env_config.json', 'r') as f:
        config = json.load(f)
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, slow_mo=200)
        context = await browser.new_context(
            http_credentials={"username": config['basic_auth']['username'], 
                            "password": config['basic_auth']['password']}
        )
        page = await context.new_page()
        
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
        
        # Go to Chart of Accounts
        print("📊 Navigating to Chart of Accounts...")
        await page.goto(f"{config['base_url']}/ledger/chart-of-accounts")
        await asyncio.sleep(2)
        
        # Click Add GL Account
        print("➕ Adding GL Account...")
        await page.click("button:has-text('Add GL Account')")
        await asyncio.sleep(2)
        
        row = page.locator("tr:has-text('Auto')").first
        cells = row.locator("td")
        
        # 1. Name
        print("1️⃣ Filling Name...")
        name_input = cells.nth(1).locator("input")
        await name_input.click()
        await name_input.fill("Test GL Account Final")
        await asyncio.sleep(0.5)
        
        # 2. Currency
        print("2️⃣", end="")
        row = page.locator("tr:has-text('Auto')").first
        cells = row.locator("td")
        await select_from_dropdown(page, cells.nth(2), "US Dollar", "Currency")
        
        # 3. Report Type (might auto-open)
        print("3️⃣", end="")
        row = page.locator("tr:has-text('Auto')").first
        cells = row.locator("td")
        await select_from_dropdown(page, cells.nth(3), "Balance", "Report Type")
        
        # 4. Type
        print("4️⃣", end="")
        row = page.locator("tr:has-text('Auto')").first
        cells = row.locator("td")
        await select_from_dropdown(page, cells.nth(4), "Current Assets", "Type")
        
        # 5. Group
        print("5️⃣", end="")
        row = page.locator("tr:has-text('Auto')").first
        cells = row.locator("td")
        await select_from_dropdown(page, cells.nth(5), "Trade", "Group")
        
        # Close any overlay
        await page.keyboard.press("Escape")
        await asyncio.sleep(0.5)
        
        # 6. EBITDA
        print("6️⃣", end="")
        row = page.locator("tr:has-text('Auto')").first
        cells = row.locator("td")
        await select_from_dropdown(page, cells.nth(6), "Non", "EBITDA")
        
        # 7. Cashflow
        print("7️⃣", end="")
        row = page.locator("tr:has-text('Auto')").first
        cells = row.locator("td")
        await select_from_dropdown(page, cells.nth(7), "Operating", "Cashflow")
        
        # 8. Intercompany
        print("8️⃣", end="")
        row = page.locator("tr:has-text('Auto')").first
        cells = row.locator("td")
        await select_from_dropdown(page, cells.nth(8), "Non", "Intercompany")
        
        await page.keyboard.press("Escape")
        await asyncio.sleep(1)
        
        # Check cell values
        print("\n📋 Cell values before save:")
        row = page.locator("tr:has-text('Auto')").first
        cells = row.locator("td")
        for i in range(9):
            txt = await cells.nth(i).text_content()
            print(f"   {i}: '{txt.strip()[:40] if txt else 'empty'}'")
        
        await page.screenshot(path="debug_combo2_before_save.png")
        
        # Save
        print("\n💾 Saving...")
        row = page.locator("tr:has-text('Auto')").first
        btns = row.locator("button")
        await btns.first.click()
        await asyncio.sleep(3)
        
        await page.screenshot(path="debug_combo2_after_save.png")
        
        # Check result
        auto_rows = await page.locator("tr:has-text('Auto-generated')").count()
        print(f"\nAuto-generated rows: {auto_rows}")
        
        if auto_rows == 0:
            print("✅ SUCCESS!")
        else:
            print("❌ Not saved")
        
        print("\n⏳ Browser open for 20 seconds...")
        await asyncio.sleep(20)
        await browser.close()

asyncio.run(debug())


