"""
Test BO Relogin Only - for debugging the relogin flow
"""

import pytest
import asyncio
import json
from playwright.async_api import async_playwright
from pages.bo_login_page import BOLoginPage
from pages.bo_accounts_page import BOAccountsPage


class TestBOReloginOnly:
    """Test only the BO relogin part"""
    
    BO_ACCOUNT_ID = "71"
    
    @pytest.mark.asyncio
    async def test_bo_relogin_flow(self):
        """Test BO login and relogin to account 71"""
        
        print("\n" + "="*60)
        print("🧪 TEST: BO Relogin Flow Only")
        print("="*60)
        
        # Load BO config
        bo_config = None
        try:
            with open('configs/bo_stage_env_config.json', 'r') as f:
                bo_config = json.load(f)
        except Exception as e:
            print(f"⚠️ Could not load BO config: {e}")
            pytest.fail("BO config required")
        
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=False, slow_mo=100)
            
            bo_url = bo_config.get("base_url", "https://bo.stage.viewz.co")
            bo_creds = bo_config.get("basic_auth", {})
            
            # Create context WITHOUT http_credentials - use route interception for domain-specific auth
            bo_context = await browser.new_context()
            
            # Set up route interception for domain-specific Basic Auth
            import base64
            
            # BO credentials
            bo_auth = base64.b64encode(f"{bo_creds.get('username', 'admin')}:{bo_creds.get('password', '')}".encode()).decode()
            
            # App credentials (different!)
            app_auth = base64.b64encode("admin:38Uo0tuxA3pj*b0F".encode()).decode()
            
            async def handle_auth(route):
                url = route.request.url
                headers = dict(route.request.headers)
                
                if "bo.stage.viewz.co" in url or "bo.viewz.co" in url:
                    headers["Authorization"] = f"Basic {bo_auth}"
                elif "app.stage.viewz.co" in url or "app.viewz.co" in url:
                    headers["Authorization"] = f"Basic {app_auth}"
                
                await route.continue_(headers=headers)
            
            await bo_context.route("**/*", handle_auth)
            print(f"✅ Created context with domain-specific auth (BO + App)")
            
            bo_page = await bo_context.new_page()
            
            try:
                # ==========================================
                # STEP 1: Login to BO
                # ==========================================
                print("\n🏢 STEP 1: Logging into BO...")
                
                bo_login_page = BOLoginPage(bo_page, bo_url)
                await bo_login_page.goto_bo()
                await asyncio.sleep(2)
                
                await bo_page.screenshot(path="debug_bo_only_login_page.png")
                
                # Perform BO login
                await bo_login_page.bo_login(
                    bo_config.get("username", ""),
                    bo_config.get("password", "")
                )
                await asyncio.sleep(3)
                
                # Handle 2FA/OTP automatically
                page_content = await bo_page.content()
                if "Two-Factor" in page_content or "Authentication" in page_content or "code" in page_content.lower():
                    print("🔐 2FA required, entering OTP...")
                    await bo_login_page.handle_bo_otp(bo_config.get("otp_secret", ""))
                    await asyncio.sleep(3)
                
                print(f"✅ BO Login complete. URL: {bo_page.url}")
                
                # Save storage state
                await bo_context.storage_state(path="bo_auth_state.json")
                print("💾 Saved BO auth state to bo_auth_state.json")
                
                # ==========================================
                # STEP 2: Navigate to accounts and search
                # ==========================================
                print(f"\n🔍 STEP 2: Searching for account {self.BO_ACCOUNT_ID}...")
                
                await bo_page.goto(f"{bo_url}/settings/accounts")
                await asyncio.sleep(3)
                
                print(f"📍 On accounts page: {bo_page.url}")
                
                # Search for account 71
                search_input = bo_page.locator("input[placeholder*='Search'], input[type='search'], input[type='text']").first
                if await search_input.is_visible():
                    await search_input.fill(self.BO_ACCOUNT_ID)
                    await bo_page.keyboard.press("Enter")
                    await asyncio.sleep(2)
                    print(f"✅ Searched for account {self.BO_ACCOUNT_ID}")
                
                await bo_page.screenshot(path="debug_bo_only_accounts.png")
                
                # ==========================================
                # STEP 3: Automated Relogin
                # ==========================================
                print("\n🔄 STEP 3: Relogin to account...")
                
                # Find the exact row for account 71
                all_rows = bo_page.locator("table tbody tr")
                row_count = await all_rows.count()
                print(f"📋 Found {row_count} rows in accounts table")
                
                account_row = None
                for i in range(row_count):
                    row = all_rows.nth(i)
                    first_cell = row.locator("td").first
                    cell_text = await first_cell.text_content()
                    cell_text = cell_text.strip() if cell_text else ""
                    if cell_text == self.BO_ACCOUNT_ID:
                        account_row = row
                        print(f"✅ Found account {self.BO_ACCOUNT_ID} at row {i}")
                        break
                
                if account_row:
                    # Hover to reveal action icons
                    await account_row.hover()
                    await asyncio.sleep(1)
                    
                    # Click relogin button
                    relogin_btn = account_row.locator("button[value='relogin']").first
                    if await relogin_btn.is_visible():
                        await relogin_btn.click()
                        print("✅ Clicked relogin button")
                        await asyncio.sleep(3)
                        
                        # Generate fresh OTP right before relogin
                        import pyotp
                        import time
                        relogin_otp_secret = bo_config.get("relogin_otp_secret", bo_config.get("otp_secret", ""))
                        totp = pyotp.TOTP(relogin_otp_secret)
                        
                        # Wait for fresh OTP window if near boundary
                        seconds_remaining = 30 - (int(time.time()) % 30)
                        if seconds_remaining < 5:
                            print(f"⏳ Waiting {seconds_remaining + 1}s for fresh OTP window...")
                            await asyncio.sleep(seconds_remaining + 1)
                        
                        fresh_otp = totp.now()
                        print(f"🔐 Generated fresh relogin OTP: {fresh_otp}")
                        
                        # Handle relogin OTP in new window
                        bo_accounts_page = BOAccountsPage(bo_page)
                        await bo_accounts_page.handle_relogin_otp(relogin_otp_secret)
                    else:
                        print("⚠️ Relogin button not visible, trying fallback...")
                        # Try clicking the arrow icon directly
                        arrow = account_row.locator("i.fa-arrow-right").first
                        if await arrow.is_visible():
                            await arrow.click()
                            print("✅ Clicked arrow icon")
                            await asyncio.sleep(3)
                            
                            bo_accounts_page = BOAccountsPage(bo_page)
                            relogin_otp = bo_config.get("relogin_otp_secret", bo_config.get("otp_secret", ""))
                            await bo_accounts_page.handle_relogin_otp(relogin_otp)
                else:
                    print(f"❌ Account {self.BO_ACCOUNT_ID} not found!")
                
                # ==========================================
                # STEP 4: Check result
                # ==========================================
                print("\n📄 STEP 4: Checking pages...")
                
                all_pages = bo_context.pages
                print(f"📄 Total pages open: {len(all_pages)}")
                
                app_page = None
                for i, pg in enumerate(all_pages):
                    print(f"   Page {i}: {pg.url}")
                    if "app.stage.viewz.co" in pg.url or "app.viewz.co" in pg.url:
                        app_page = pg
                        print(f"✅ Found app page!")
                
                if app_page:
                    await app_page.bring_to_front()
                    await asyncio.sleep(2)
                    await app_page.screenshot(path="debug_bo_only_app_page.png")
                    print(f"📍 App page URL: {app_page.url}")
                    
                    # Try navigating to payables
                    await app_page.goto("https://app.stage.viewz.co/reconciliation/payables")
                    await asyncio.sleep(3)
                    
                    await app_page.screenshot(path="debug_bo_only_payables.png")
                    print(f"📍 After payables navigation: {app_page.url}")
                    
                    if "/login" in app_page.url:
                        print("❌ Redirected to login - auth failed!")
                    elif "/reconciliation/payables" in app_page.url:
                        print("✅ SUCCESS! On payables page!")
                    else:
                        print(f"⚠️ Unexpected URL: {app_page.url}")
                else:
                    print("❌ No app page found after relogin")
                
                print("\n" + "="*60)
                print("✅ BO RELOGIN TEST COMPLETE!")
                print("="*60)
                
            except Exception as e:
                print(f"\n❌ Test failed with error: {str(e)}")
                await bo_page.screenshot(path="debug_bo_only_failure.png")
                raise
            
            finally:
                await browser.close()

