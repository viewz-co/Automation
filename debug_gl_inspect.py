"""
Debug GL - inspect cell structure
"""
import asyncio
import pyotp
import json
from playwright.async_api import async_playwright

async def debug():
    with open('configs/stage_env_config.json', 'r') as f:
        config = json.load(f)
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, slow_mo=100)
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
        await page.click("button:has-text('Add GL Account')")
        await asyncio.sleep(2)
        
        # Get row
        row = page.locator("tr:has-text('Auto')").first
        
        # Get HTML of the row
        row_html = await row.inner_html()
        print("=" * 60)
        print("ROW HTML (first 3000 chars):")
        print("=" * 60)
        print(row_html[:3000])
        print("=" * 60)
        
        # Check for comboboxes
        comboboxes = row.locator("[role='combobox']")
        cb_count = await comboboxes.count()
        print(f"\n[role='combobox'] count: {cb_count}")
        
        # Check for data-state elements
        data_state = row.locator("[data-state]")
        ds_count = await data_state.count()
        print(f"[data-state] count: {ds_count}")
        
        # Try clicking the first combobox
        if cb_count > 0:
            print("\nFirst combobox:")
            cb = comboboxes.first
            cb_html = await cb.evaluate("el => el.outerHTML")
            print(cb_html[:300])
        
        # Or find any clickable things in cells
        cells = row.locator("td")
        print(f"\nInspecting cells for clickable elements...")
        
        for i in range(8):
            cell = cells.nth(i)
            cell_html = await cell.inner_html()
            print(f"\n--- Cell {i} HTML ---")
            print(cell_html[:400] if len(cell_html) > 400 else cell_html)
        
        print("\n🔍 Browser stays open 20 seconds...")
        await asyncio.sleep(20)
        
        await browser.close()

if __name__ == "__main__":
    asyncio.run(debug())

