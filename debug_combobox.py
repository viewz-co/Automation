"""Debug by clicking the combobox button directly"""
import asyncio
import pyotp
import json
from playwright.async_api import async_playwright

async def debug():
    with open('configs/stage_env_config.json', 'r') as f:
        config = json.load(f)
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, slow_mo=300)
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
        print("1️⃣ Name...")
        name_input = cells.nth(1).locator("input")
        await name_input.click()
        await name_input.fill("Test GL Account")
        await asyncio.sleep(0.5)
        print(f"   Name filled: {await name_input.input_value()}")
        
        # 2. Currency - Find the combobox button in the cell
        print("\n2️⃣ Currency...")
        currency_cell = cells.nth(2)
        
        # Look at what's in the cell
        cell_html = await currency_cell.inner_html()
        print(f"   Cell HTML: {cell_html[:300]}")
        
        # Find combobox button
        combo = currency_cell.locator("button[role='combobox']")
        combo_count = await combo.count()
        print(f"   Combobox buttons found: {combo_count}")
        
        if combo_count > 0:
            await combo.first.click()
            print("   Clicked combobox button")
            await asyncio.sleep(1)
            
            # Check for listbox/options
            listbox = page.locator("[role='listbox']")
            listbox_count = await listbox.count()
            print(f"   Listboxes found: {listbox_count}")
            
            opts = page.locator("[role='option']")
            opt_count = await opts.count()
            print(f"   Options found: {opt_count}")
            
            if opt_count > 0:
                # Print first few options
                for i in range(min(5, opt_count)):
                    txt = await opts.nth(i).text_content()
                    print(f"      Option {i}: {txt}")
                
                # Click US Dollar option
                usd_opt = page.locator("[role='option']:has-text('US Dollar')")
                if await usd_opt.count() > 0:
                    print("   Clicking US Dollar option...")
                    await usd_opt.first.click()
                    await asyncio.sleep(1)
                    
                    # Check if it was selected
                    currency_text = await currency_cell.text_content()
                    print(f"   Currency cell now shows: '{currency_text}'")
        else:
            # No combobox, try clicking the cell directly
            print("   No combobox found, clicking cell...")
            await currency_cell.click()
            await asyncio.sleep(1)
        
        await page.screenshot(path="debug_combobox_currency.png")
        
        # Check all cells
        print("\n📋 Current cell values:")
        for i in range(8):
            txt = await cells.nth(i).text_content()
            print(f"   Cell {i}: '{txt.strip()[:30] if txt else 'empty'}'")
        
        print("\n⏳ Keeping browser open for 30 seconds...")
        await asyncio.sleep(30)
        await browser.close()

asyncio.run(debug())


