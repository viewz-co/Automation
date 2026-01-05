"""Quick debug to check save button"""
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
            http_credentials={"username": config['basic_auth']['username'], 
                            "password": config['basic_auth']['password']}
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
        
        # Go to Chart of Accounts
        await page.goto(f"{config['base_url']}/ledger/chart-of-accounts")
        await asyncio.sleep(2)
        
        # Click Add GL Account
        await page.click("button:has-text('Add GL Account')")
        await asyncio.sleep(2)
        
        row = page.locator("tr:has-text('Auto')").first
        cells = row.locator("td")
        
        # Fill name
        name_input = cells.nth(1).locator("input")
        await name_input.fill("Debug Account Test")
        await asyncio.sleep(0.5)
        
        # Currency
        await cells.nth(2).click()
        await asyncio.sleep(0.5)
        await page.locator("[role='option']:has-text('US Dollar')").first.click()
        await asyncio.sleep(0.5)
        
        # Report Type (auto-opened)
        await page.locator("[role='option']:has-text('Balance')").first.click()
        await asyncio.sleep(0.5)
        
        # Type (auto-opened)
        await page.locator("[role='option']:has-text('Current Assets')").first.click()
        await asyncio.sleep(0.5)
        
        # Group (auto-opened)  
        await page.locator("[role='option']:has-text('Trade Receivables')").first.click()
        await asyncio.sleep(0.5)
        
        # EBITDA (auto-opened)
        opts = await page.locator("[role='option']").all_text_contents()
        print(f"EBITDA options: {opts}")
        await page.locator("[role='option']").first.click()
        await asyncio.sleep(0.5)
        
        # Cashflow (auto-opened)
        opts = await page.locator("[role='option']").all_text_contents()
        print(f"Cashflow options: {opts}")
        await page.locator("[role='option']").first.click()
        await asyncio.sleep(0.5)
        
        await page.keyboard.press("Escape")
        await asyncio.sleep(1)
        
        # Find save button - inspect row
        row = page.locator("tr:has-text('Auto')").first
        row_html = await row.inner_html()
        print(f"\n📋 Row HTML (last 500 chars):\n{row_html[-500:]}")
        
        # Find all buttons in row
        btns = row.locator("button")
        btn_count = await btns.count()
        print(f"\n🔘 Found {btn_count} buttons in row")
        
        for i in range(btn_count):
            btn = btns.nth(i)
            classes = await btn.get_attribute("class") or ""
            inner = await btn.inner_html()
            print(f"   Button {i}: class={classes[:50]}... inner={inner[:100]}")
        
        await page.screenshot(path="debug_before_save.png")
        print("\n📸 Screenshot saved: debug_before_save.png")
        
        # Try clicking first button (usually save)
        if btn_count > 0:
            print("\n🖱️ Clicking first button (save)...")
            await btns.first.click()
            await asyncio.sleep(3)
            
            await page.screenshot(path="debug_after_save.png")
            print("📸 Screenshot saved: debug_after_save.png")
            
            # Check if row still exists
            auto_row = await page.locator("tr:has-text('Auto-generated')").count()
            print(f"Auto-generated rows: {auto_row}")
        
        print("\n⏳ Keeping browser open for 20 seconds...")
        await asyncio.sleep(20)
        await browser.close()

asyncio.run(debug())


