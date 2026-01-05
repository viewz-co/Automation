"""Final debug - see what happens after save"""
import asyncio
import pyotp
import json
from playwright.async_api import async_playwright

async def debug():
    with open('configs/stage_env_config.json', 'r') as f:
        config = json.load(f)
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, slow_mo=150)
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
        await asyncio.sleep(1.5)
        
        row = page.locator("tr:has-text('Auto')").first
        cells = row.locator("td")
        
        # 1. Name
        print("1️⃣ Name...")
        name_input = cells.nth(1).locator("input")
        await name_input.fill("Debug Final Test Account")
        await asyncio.sleep(0.3)
        
        # 2. Currency
        print("2️⃣ Currency...")
        await cells.nth(2).click()
        await asyncio.sleep(0.5)
        await page.locator("[role='option']:has-text('US Dollar')").first.click()
        await asyncio.sleep(0.5)
        
        # 3. Report Type (auto-opened)
        print("3️⃣ Report Type...")
        await page.locator("[role='option']:has-text('Balance')").first.click()
        await asyncio.sleep(0.5)
        
        # 4. Type (auto-opened)
        print("4️⃣ Type...")
        await page.locator("[role='option']:has-text('Current Assets')").first.click()
        await asyncio.sleep(0.5)
        
        # 5. Group (auto-opened)
        print("5️⃣ Group...")
        await page.locator("[role='option']:has-text('Trade')").first.click()
        await asyncio.sleep(0.5)
        
        # Close dropdown overlay
        await page.keyboard.press("Escape")
        await asyncio.sleep(0.5)
        
        # 6. EBITDA
        print("6️⃣ EBITDA...")
        row = page.locator("tr:has-text('Auto')").first
        cells = row.locator("td")
        await cells.nth(6).click(force=True)
        await asyncio.sleep(0.5)
        opts = page.locator("[role='option']")
        if await opts.count() > 0:
            await opts.first.click()
        await asyncio.sleep(0.5)
        
        # 7. Cashflow
        print("7️⃣ Cashflow...")
        opts = page.locator("[role='option']")
        if await opts.count() == 0:
            row = page.locator("tr:has-text('Auto')").first
            cells = row.locator("td")
            await cells.nth(7).click(force=True)
            await asyncio.sleep(0.5)
        opts = page.locator("[role='option']")
        if await opts.count() > 0:
            await opts.first.click()
        await asyncio.sleep(0.5)
        
        # 8. Intercompany
        print("8️⃣ Intercompany...")
        opts = page.locator("[role='option']")
        if await opts.count() == 0:
            row = page.locator("tr:has-text('Auto')").first
            cells = row.locator("td")
            await cells.nth(8).click(force=True)
            await asyncio.sleep(0.5)
        opts = page.locator("[role='option']")
        if await opts.count() > 0:
            await opts.first.click()
        await asyncio.sleep(0.5)
        
        await page.keyboard.press("Escape")
        await asyncio.sleep(1)
        
        # Take screenshot before save
        await page.screenshot(path="debug_before_save.png")
        print("📸 Screenshot: debug_before_save.png")
        
        # Show row state
        row = page.locator("tr:has-text('Auto')").first
        row_text = await row.text_content()
        print(f"\n📋 Row content before save: {row_text[:200]}")
        
        # Find and click save
        print("\n💾 Clicking save...")
        btns = row.locator("button")
        btn_count = await btns.count()
        print(f"   Found {btn_count} buttons")
        
        if btn_count > 0:
            await btns.first.click()
            print("   ✅ Clicked save button")
        
        await asyncio.sleep(3)
        
        # Check result
        await page.screenshot(path="debug_after_save.png")
        print("📸 Screenshot: debug_after_save.png")
        
        # Check for validation error
        error_visible = await page.locator("text=Missing Required").is_visible()
        print(f"\n❓ Validation error visible: {error_visible}")
        
        if error_visible:
            # Get error content
            errors = await page.locator(".text-red-500, [class*='error'], [class*='destructive']").all_text_contents()
            print(f"   Error content: {errors}")
        
        # Check if Auto-generated row is gone
        auto_row = await page.locator("tr:has-text('Auto-generated')").count()
        print(f"   Auto-generated rows remaining: {auto_row}")
        
        if auto_row == 0:
            print("\n✅ SUCCESS! Account was created!")
        else:
            print("\n❌ Account not created - row still in edit mode")
        
        print("\n⏳ Keeping browser open for 20 seconds...")
        await asyncio.sleep(20)
        await browser.close()

asyncio.run(debug())


