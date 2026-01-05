"""Debug using keyboard with better filter text"""
import asyncio
import pyotp
import json
from playwright.async_api import async_playwright

async def select_dropdown(page, filter_text):
    """Type to filter and press Enter"""
    await page.keyboard.type(filter_text)
    await asyncio.sleep(0.5)
    await page.keyboard.press("Enter")
    await asyncio.sleep(0.8)

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
        await name_input.fill("Keyboard Test Account")
        await asyncio.sleep(0.3)
        
        # 2. Currency - use "US Doll" to be specific
        print("2️⃣ Currency...")
        await cells.nth(2).click()
        await asyncio.sleep(0.8)
        await select_dropdown(page, "US Doll")
        
        # 3. Report Type (auto-opened)
        print("3️⃣ Report Type...")
        await select_dropdown(page, "Balance")
        
        # 4. Type (auto-opened)
        print("4️⃣ Type...")
        await select_dropdown(page, "Current Assets")
        
        # 5. Group (auto-opened)
        print("5️⃣ Group...")
        await select_dropdown(page, "Trade")
        
        # Close overlay and click EBITDA
        await page.keyboard.press("Escape")
        await asyncio.sleep(0.5)
        
        # 6. EBITDA
        print("6️⃣ EBITDA...")
        row = page.locator("tr:has-text('Auto')").first
        cells = row.locator("td")
        await cells.nth(6).click(force=True)
        await asyncio.sleep(0.8)
        await select_dropdown(page, "Non")
        
        # 7. Cashflow
        print("7️⃣ Cashflow...")
        row = page.locator("tr:has-text('Auto')").first
        cells = row.locator("td")
        await cells.nth(7).click(force=True)
        await asyncio.sleep(0.8)
        await select_dropdown(page, "Oper")
        
        # 8. Intercompany
        print("8️⃣ Intercompany...")
        row = page.locator("tr:has-text('Auto')").first
        cells = row.locator("td")
        await cells.nth(8).click(force=True)
        await asyncio.sleep(0.8)
        await select_dropdown(page, "Non")
        
        await page.keyboard.press("Escape")
        await asyncio.sleep(1)
        
        # Show all cell values
        print("\n📋 Cell values before save:")
        row = page.locator("tr:has-text('Auto')").first
        cells = row.locator("td")
        for i in range(12):
            txt = await cells.nth(i).text_content()
            print(f"   Cell {i}: '{txt.strip()[:30] if txt else 'empty'}'")
        
        await page.screenshot(path="debug_kbd2_before_save.png")
        
        # Click save
        print("\n💾 Saving...")
        row = page.locator("tr:has-text('Auto')").first
        btns = row.locator("button")
        await btns.first.click()
        await asyncio.sleep(3)
        
        await page.screenshot(path="debug_kbd2_after_save.png")
        
        # Check result
        auto_rows = await page.locator("tr:has-text('Auto-generated')").count()
        error_visible = await page.locator("text=Missing Required").is_visible()
        
        print(f"\n❓ Validation error: {error_visible}")
        print(f"   Auto-generated rows: {auto_rows}")
        
        if auto_rows == 0 and not error_visible:
            print("\n✅ SUCCESS! Account was created!")
        else:
            print("\n❌ Account not created")
        
        print("\n⏳ Keeping browser open for 30 seconds...")
        await asyncio.sleep(30)
        await browser.close()

asyncio.run(debug())


