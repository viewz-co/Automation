"""Visual debug with slow_mo so user can watch"""
import asyncio
import pyotp
import json
from playwright.async_api import async_playwright

async def debug():
    with open('configs/stage_env_config.json', 'r') as f:
        config = json.load(f)
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, slow_mo=500)
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
        print("📊 Going to Chart of Accounts...")
        await page.goto(f"{config['base_url']}/ledger/chart-of-accounts")
        await asyncio.sleep(2)
        
        # Click Add GL Account
        print("➕ Click Add GL Account...")
        await page.click("button:has-text('Add GL Account')")
        await asyncio.sleep(2)
        
        row = page.locator("tr:has-text('Auto')").first
        cells = row.locator("td")
        
        # 1. Name
        print("1️⃣ Fill Name...")
        name_input = cells.nth(1).locator("input")
        await name_input.fill("Visual Test Account")
        await asyncio.sleep(1)
        
        # 2. Currency - click the cell first
        print("2️⃣ Click Currency cell...")
        await cells.nth(2).click()
        await asyncio.sleep(1)
        
        # Now find and click the dropdown button
        print("   Looking for dropdown...")
        row = page.locator("tr:has-text('Auto')").first
        dropdown_btns = row.locator("button")
        btn_count = await dropdown_btns.count()
        print(f"   Found {btn_count} buttons")
        
        # Click the currency dropdown (should be visible now)
        currency_dropdown = row.locator("td").nth(2).locator("button")
        if await currency_dropdown.count() > 0:
            print("   Clicking currency dropdown button...")
            await currency_dropdown.first.click()
            await asyncio.sleep(1)
        
        # Now select US Dollar
        print("   Selecting US Dollar...")
        usd = page.get_by_text("US Dollar").first
        if await usd.is_visible():
            print("   Found US Dollar, clicking...")
            await usd.click()
            await asyncio.sleep(1)
        else:
            print("   US Dollar not visible!")
            # List what's visible
            visible_text = await page.locator("div, span").filter(has_text="Dollar").all_text_contents()
            print(f"   Text with 'Dollar': {visible_text[:5]}")
        
        # Check what's in the currency cell now
        row = page.locator("tr:has-text('Auto')").first
        currency_value = await row.locator("td").nth(2).text_content()
        print(f"   Currency cell value: '{currency_value}'")
        
        print("\n⏳ Watch the browser - keeping open for 60 seconds...")
        await asyncio.sleep(60)
        await browser.close()

asyncio.run(debug())

