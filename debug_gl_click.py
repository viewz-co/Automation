"""
Debug GL - test clicking cells to activate comboboxes
"""
import asyncio
import pyotp
import json
from playwright.async_api import async_playwright

async def debug():
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
        
        # Login
        await page.goto(f"{config['base_url']}/login")
        await page.fill('input[name="username"]', config['username'])
        await page.fill('input[name="password"]', config['password'])
        await page.click('button[type="submit"]')
        
        await page.wait_for_selector("text=Two-Factor Authentication", timeout=10000)
        otp = pyotp.TOTP(config['otp_secret']).now()
        await page.get_by_role("textbox").fill(otp)
        await asyncio.sleep(3)
        
        # Navigate
        await page.goto(f"{config['base_url']}/ledger/chart-of-accounts")
        await asyncio.sleep(3)
        
        # Click Add
        print("➕ Click Add GL Account...")
        await page.click("button:has-text('Add GL Account')")
        await asyncio.sleep(2)
        
        # Get row
        row = page.locator("tr:has-text('Auto')").first
        cells = row.locator("td")
        
        # 1. Fill Name
        print("\n1️⃣ FILL NAME...")
        name_input = cells.nth(1).locator("input")
        await name_input.fill("Debug GL Test")
        await asyncio.sleep(0.5)
        print("   ✅ Name filled")
        
        # 2. Click Cell 2 (Currency) to activate combobox
        print("\n2️⃣ CLICK CELL 2 (Currency)...")
        await cells.nth(2).click()
        await asyncio.sleep(1)
        
        # Check what appeared
        cell2_html = await cells.nth(2).inner_html()
        print(f"   Cell 2 HTML after click: {cell2_html[:300]}")
        
        # Look for combobox that just appeared
        combobox = cells.nth(2).locator("[role='combobox']")
        cb_count = await combobox.count()
        print(f"   Combobox count: {cb_count}")
        
        # Check if options are already visible
        options = page.locator("[role='option']")
        opt_count = await options.count()
        print(f"   Options visible: {opt_count}")
        
        if opt_count > 0:
            # Already open - just select
            print("   Dropdown already open!")
            for i in range(min(3, opt_count)):
                opt = await options.nth(i).text_content()
                print(f"      {opt}")
            
            # Select USD
            usd = page.locator("[role='option']:has-text('US Dollar')").first
            if await usd.count() > 0:
                await usd.click()
                print("   ✅ USD selected")
        elif cb_count > 0:
            # Need to click combobox to open
            print("   Clicking combobox to open dropdown...")
            await combobox.first.click()
            await asyncio.sleep(1)
            
            opt_count = await options.count()
            print(f"   Options after combobox click: {opt_count}")
            if opt_count > 0:
                usd = page.locator("[role='option']:has-text('US Dollar')").first
                if await usd.count() > 0:
                    await usd.click()
                    print("   ✅ USD selected")
        
        await asyncio.sleep(1)
        
        # Check cell 2 state now
        cell2_text = await cells.nth(2).inner_text()
        print(f"   Cell 2 text now: '{cell2_text}'")
        
        # 3. Click Cell 3 (Report Type)
        print("\n3️⃣ CLICK CELL 3 (Report Type)...")
        await cells.nth(3).click()
        await asyncio.sleep(1)
        
        cell3_html = await cells.nth(3).inner_html()
        print(f"   Cell 3 HTML after click: {cell3_html[:300]}")
        
        options = page.locator("[role='option']")
        opt_count = await options.count()
        print(f"   Options visible: {opt_count}")
        
        if opt_count > 0:
            for i in range(min(5, opt_count)):
                opt = await options.nth(i).text_content()
                print(f"      {opt}")
            
            balance = page.locator("[role='option']:has-text('Balance')").first
            if await balance.count() > 0:
                await balance.click()
                print("   ✅ Balance Sheet selected")
        
        await asyncio.sleep(1)
        
        # 4. Type
        print("\n4️⃣ CLICK CELL 4 (Type)...")
        await cells.nth(4).click()
        await asyncio.sleep(1)
        
        options = page.locator("[role='option']")
        opt_count = await options.count()
        print(f"   Options visible: {opt_count}")
        
        if opt_count > 0:
            for i in range(min(5, opt_count)):
                opt = await options.nth(i).text_content()
                print(f"      {opt}")
            
            current = page.locator("[role='option']:has-text('Current')").first
            if await current.count() > 0:
                await current.click()
                print("   ✅ Current Assets selected")
        
        await asyncio.sleep(1)
        
        # 5. Group
        print("\n5️⃣ CLICK CELL 5 (Group)...")
        await cells.nth(5).click()
        await asyncio.sleep(1)
        
        options = page.locator("[role='option']")
        opt_count = await options.count()
        print(f"   Options visible: {opt_count}")
        
        if opt_count > 0:
            for i in range(min(5, opt_count)):
                opt = await options.nth(i).text_content()
                print(f"      {opt}")
            
            trade = page.locator("[role='option']:has-text('Trade')").first
            if await trade.count() > 0:
                await trade.click()
                print("   ✅ Trade selected")
        
        await asyncio.sleep(1)
        
        # 6. EBITDA
        print("\n6️⃣ CLICK CELL 6 (EBITDA)...")
        await cells.nth(6).click()
        await asyncio.sleep(1)
        
        options = page.locator("[role='option']")
        opt_count = await options.count()
        print(f"   Options visible: {opt_count}")
        
        if opt_count > 0:
            for i in range(min(5, opt_count)):
                opt = await options.nth(i).text_content()
                print(f"      {opt}")
            
            non = page.locator("[role='option']:has-text('Non')").first
            if await non.count() > 0:
                await non.click()
                print("   ✅ Non-EBITDA selected")
        
        await asyncio.sleep(1)
        
        # 7. Cashflow
        print("\n7️⃣ CLICK CELL 7 (Cashflow)...")
        await cells.nth(7).click()
        await asyncio.sleep(1)
        
        options = page.locator("[role='option']")
        opt_count = await options.count()
        print(f"   Options visible: {opt_count}")
        
        if opt_count > 0:
            for i in range(min(5, opt_count)):
                opt = await options.nth(i).text_content()
                print(f"      {opt}")
            
            op = page.locator("[role='option']:has-text('Operating')").first
            if await op.count() > 0:
                await op.click()
                print("   ✅ Operating selected")
        
        await asyncio.sleep(1)
        await page.screenshot(path="debug_before_save.png")
        
        # Show final row state
        print("\n📊 FINAL ROW STATE:")
        for i in range(8):
            cell = cells.nth(i)
            text = await cell.inner_text()
            print(f"   Cell {i}: '{text[:30]}'")
        
        # 8. Save
        print("\n💾 SAVING...")
        # Escape first to close any dropdown
        await page.keyboard.press("Escape")
        await asyncio.sleep(0.5)
        
        save_btn = row.locator("button svg").first.locator("..")  # Parent of svg
        if await save_btn.is_visible():
            await save_btn.click(force=True)
            print("   Clicked save button")
        
        await asyncio.sleep(5)
        await page.screenshot(path="debug_after_save.png")
        
        # Check errors
        if await page.locator("text=Missing Required").is_visible():
            print("   ❌ Validation errors!")
        else:
            print("   ✅ No validation errors!")
        
        print("\n🔍 Browser stays open 20 seconds...")
        await asyncio.sleep(20)
        
        await browser.close()

if __name__ == "__main__":
    asyncio.run(debug())

