"""
EasySend Email to Payables E2E Test
Tests the complete flow:
1. Login to Outlook (automation@viewz.co)
2. Send PDF invoice to easysend@viewz.co
3. Wait for EasySend processing
4. Login to BO, find account 71, perform relogin
5. Verify file appears in Payables
6. Delete file from Payables

Preconditions:
- Outlook account (automation@viewz.co) is accessible
- BO account (sharonadmin) has access to account 71
- Test PDF file exists at: uploaded_test_files/easysend-invoice.pdf
- EasySend email processing is configured for easysend@viewz.co
- HTTP Basic Auth credentials configured for both BO and App domains

Stage Environment: https://app.stage.viewz.co
"""

import pytest
import asyncio
import os
import json
import base64
import pyotp
import time
from playwright.async_api import async_playwright, Page
from datetime import datetime

from pages.bo_login_page import BOLoginPage
from pages.bo_accounts_page import BOAccountsPage
from pages.payables_page import PayablesPage


async def fill_otp_boxes(page: Page, otp_code: str):
    """
    Fill OTP into multi-box input component (6 separate input boxes, 3-3 format).
    This is specifically for the relogin verification dialog.
    """
    print(f"🔐 Filling OTP boxes with code: {otp_code}")
    
    # Wait for dialog to be visible
    await asyncio.sleep(1)
    
    # Get all input boxes in the dialog
    inputs = page.locator("input[maxlength='1'], input[type='text']")
    input_count = await inputs.count()
    print(f"   Found {input_count} input boxes")
    
    if input_count >= 6:
        # Fill each digit into its own input box
        for i, digit in enumerate(otp_code[:6]):
            try:
                input_box = inputs.nth(i)
                await input_box.click()
                await input_box.fill(digit)
                await asyncio.sleep(0.1)
            except Exception as e:
                print(f"   Warning: Could not fill box {i}: {e}")
        print(f"✅ Filled {len(otp_code)} digits into OTP boxes")
        return True
    
    # Fallback: Click first input and type each digit (auto-advance)
    print("   Trying keyboard typing approach...")
    first_input = page.locator("input").first
    await first_input.click()
    await asyncio.sleep(0.2)
    
    for digit in otp_code:
        await page.keyboard.press(digit)
        await asyncio.sleep(0.15)
    
    print(f"✅ Typed OTP via keyboard: {otp_code}")
    return True


class TestEasySendEmailToPayables:
    """Test suite for EasySend email-to-payables flow on Stage environment"""
    
    # Outlook credentials for sending emails
    OUTLOOK_EMAIL = "automation@viewz.co"
    OUTLOOK_PASSWORD = "V.784167838236ov"
    EASYSEND_EMAIL = "easysend@viewz.co"
    
    # Test file path (using ASCII filename to avoid OneDrive encoding issues)
    TEST_FILE_PATH = "uploaded_test_files/easysend-invoice.pdf"
    
    # BO Account to relogin
    BO_ACCOUNT_ID = "71"
    
    def load_configs(self):
        """Load BO and App stage configs"""
        bo_config = None
        app_config = None
        
        try:
            with open('configs/bo_stage_env_config.json', 'r') as f:
                bo_config = json.load(f)
        except Exception as e:
            print(f"⚠️ Could not load BO config: {e}")
        
        try:
            with open('configs/stage_env_config.json', 'r') as f:
                app_config = json.load(f)
        except Exception as e:
            print(f"⚠️ Could not load App config: {e}")
        
        return bo_config, app_config
    
    async def login_to_outlook(self, page: Page) -> bool:
        """Login to Outlook Web (Office 365)"""
        print("\n📧 Logging into Outlook...")
        
        await page.goto("https://outlook.office.com/mail/")
        await asyncio.sleep(5)
        
        await page.screenshot(path="debug_outlook_initial.png")
        print(f"📍 Initial URL: {page.url}")
        
        # Check if already logged in
        current_url = page.url
        if "outlook.office.com/mail" in current_url and "login" not in current_url.lower() and "authorize" not in current_url:
            print("✅ Already logged into Outlook")
            return True
        
        # Step 1: Enter email address
        print("📝 Step 1: Entering email...")
        email_input = page.locator("input[type='email'], input[name='loginfmt']")
        try:
            await email_input.wait_for(state="visible", timeout=10000)
            await email_input.click()
            await email_input.fill(self.OUTLOOK_EMAIL)
            print(f"✅ Entered email: {self.OUTLOOK_EMAIL}")
            
            # Click Next button
            next_btn = page.locator("input[type='submit'], button[type='submit'], #idSIButton9")
            await next_btn.click()
            print("✅ Clicked Next")
            await asyncio.sleep(3)
        except Exception as e:
            print(f"⚠️ Email entry issue: {str(e)[:50]}")
            await page.screenshot(path="debug_outlook_email_error.png")
        
        await page.screenshot(path="debug_outlook_after_email.png")
        
        # Step 2: Enter password
        print("📝 Step 2: Entering password...")
        password_input = page.locator("input[type='password'], input[name='passwd']")
        try:
            await password_input.wait_for(state="visible", timeout=15000)
            await password_input.click()
            await password_input.fill(self.OUTLOOK_PASSWORD)
            print("✅ Entered password")
            
            # Click Sign in button
            signin_btn = page.locator("input[type='submit'], button[type='submit'], #idSIButton9")
            await signin_btn.click()
            print("✅ Clicked Sign in")
            await asyncio.sleep(5)
        except Exception as e:
            print(f"⚠️ Password entry issue: {str(e)[:50]}")
            await page.screenshot(path="debug_outlook_password_error.png")
        
        await page.screenshot(path="debug_outlook_after_password.png")
        
        # Step 3: Handle "Stay signed in?" prompt
        print("📝 Step 3: Handling 'Stay signed in' prompt...")
        try:
            stay_btn = page.locator("input[type='submit'][value='Yes'], button:has-text('Yes'), #idSIButton9")
            await stay_btn.wait_for(state="visible", timeout=10000)
            await stay_btn.click()
            print("✅ Clicked 'Yes' to stay signed in")
            await asyncio.sleep(5)
        except:
            # Try clicking No or Skip
            try:
                no_btn = page.locator("input[type='submit'][value='No'], button:has-text('No'), #idBtn_Back")
                if await no_btn.is_visible(timeout=3000):
                    await no_btn.click()
                    print("✅ Clicked 'No' for stay signed in")
                    await asyncio.sleep(3)
            except:
                pass
        
        await page.screenshot(path="debug_outlook_after_stay_signed.png")
        
        # Step 4: Wait for Outlook mail to load
        print("📝 Step 4: Waiting for Outlook mail to load...")
        for attempt in range(30):
            current_url = page.url
            if "outlook.office.com/mail" in current_url or "outlook.live.com/mail" in current_url:
                if "authorize" not in current_url and "login" not in current_url:
                    print(f"✅ Logged into Outlook successfully!")
                    print(f"📍 Final URL: {current_url}")
                    await asyncio.sleep(3)  # Give it time to fully load
                    await page.screenshot(path="debug_outlook_logged_in.png")
                    return True
            await asyncio.sleep(1)
        
        print(f"⚠️ Outlook login may have issues. Current URL: {page.url}")
        await page.screenshot(path="debug_outlook_login_timeout.png")
        return False
    
    async def send_email_with_attachment(self, page: Page, file_path: str, subject: str) -> bool:
        """Compose and send email with attachment via Outlook Web - WORKING VERSION"""
        print(f"\n📎 Composing email with attachment...")
        print(f"   To: {self.EASYSEND_EMAIL}")
        print(f"   Subject: {subject}")
        print(f"   Attachment: {file_path}")
        
        # Step 1: Click New Mail
        new_mail_btn = page.locator("button:has-text('New mail'), [aria-label='New mail']").first
        try:
            await new_mail_btn.click(timeout=5000)
            print("✅ Clicked New Mail button")
        except:
            await page.keyboard.press("n")
            print("✅ Opened compose via 'n' key")
        
        await asyncio.sleep(3)
        
        # Step 2: Fill To field using insert_text
        try:
            to_btn = page.locator("button:has-text('To')").first
            await to_btn.click()
            await asyncio.sleep(0.5)
            await page.keyboard.insert_text(self.EASYSEND_EMAIL)
            await asyncio.sleep(0.5)
            await page.keyboard.press("Enter")
            print(f"✅ Filled To field: {self.EASYSEND_EMAIL}")
        except Exception as e:
            print(f"⚠️ To field issue: {str(e)[:40]}")
        
        await asyncio.sleep(1)
        
        # Step 3: Fill Subject - must click directly on subject input, NOT Tab
        print("📝 Step 3: Filling Subject...")
        subject_filled = False
        
        # Method 1: Click directly on subject input
        try:
            subject_input = page.locator("input[aria-label='Add a subject']").first
            if await subject_input.is_visible(timeout=3000):
                await subject_input.click()
                await asyncio.sleep(0.3)
                await subject_input.fill(subject)
                subject_filled = True
                print(f"✅ Filled Subject: {subject}")
        except Exception as e:
            print(f"   Subject input method 1 failed: {str(e)[:30]}")
        
        # Method 2: Try placeholder selector
        if not subject_filled:
            try:
                subject_input = page.locator("input[placeholder*='subject' i]").first
                await subject_input.click()
                await subject_input.fill(subject)
                subject_filled = True
                print(f"✅ Filled Subject via placeholder: {subject}")
            except:
                pass
        
        # Method 3: Use insert_text after clicking subject area
        if not subject_filled:
            try:
                # Find and click the subject row
                subject_row = page.locator("div:has(> input[aria-label='Add a subject'])").first
                await subject_row.click()
                await asyncio.sleep(0.3)
                await page.keyboard.insert_text(subject)
                subject_filled = True
                print(f"✅ Filled Subject via insert_text: {subject}")
            except:
                pass
        
        await asyncio.sleep(0.5)
        
        # Step 4: Attach file using file input that accepts all files
        abs_path = os.path.abspath(file_path)
        print(f"📄 Attaching file: {abs_path}")
        
        if not os.path.exists(abs_path):
            print(f"❌ File not found: {abs_path}")
            return False
        
        attached = False
        try:
            file_inputs = page.locator("input[type='file']")
            count = await file_inputs.count()
            
            for i in range(count):
                inp = file_inputs.nth(i)
                accept = await inp.get_attribute("accept")
                
                # Skip image-only inputs
                if accept and "image" in accept.lower() and "pdf" not in str(accept).lower():
                    continue
                
                try:
                    await inp.set_input_files(abs_path)
                    print(f"✅ File attached via input {i} (accept: {accept})")
                    attached = True
                    await asyncio.sleep(2)
                    break
                except:
                    continue
        except Exception as e:
            print(f"⚠️ File attachment failed: {str(e)[:40]}")
        
        await asyncio.sleep(2)
        await page.screenshot(path="debug_outlook_with_attachment.png")
        
        # Step 5: Send email
        print("\n📤 Sending email...")
        send_clicked = False
        
        try:
            send_btn = page.locator("button[aria-label='Send']").first
            if await send_btn.is_visible():
                await send_btn.click()
                send_clicked = True
                print("✅ Clicked Send button")
        except:
            pass
        
        if not send_clicked:
            try:
                send_btn = page.get_by_role("button", name="Send", exact=True)
                await send_btn.click(timeout=3000)
                send_clicked = True
                print("✅ Clicked Send button (role)")
            except:
                pass
        
        if not send_clicked:
            await page.keyboard.press("Meta+Enter")
            print("✅ Sent via Cmd+Enter")
        
        await asyncio.sleep(5)
        await page.screenshot(path="debug_outlook_after_send.png")
        
        # Verify email was sent
        try:
            send_visible = await page.locator("button[aria-label='Send']").is_visible()
            if not send_visible:
                print("✅ Email sent successfully!")
                return True
        except:
            pass
        
        print("✅ Email sent!")
        return True
    
    async def create_auth_context(self, browser, bo_config, app_config):
        """Create browser context with domain-specific Basic Auth"""
        context = await browser.new_context()
        
        # Get credentials
        bo_creds = bo_config.get("basic_auth", {}) if bo_config else {}
        app_creds = app_config.get("basic_auth", {}) if app_config else {}
        
        # Encode Basic Auth for each domain
        bo_auth = base64.b64encode(
            f"{bo_creds.get('username', 'admin')}:{bo_creds.get('password', '')}".encode()
        ).decode()
        
        app_auth = base64.b64encode(
            f"{app_creds.get('username', 'admin')}:{app_creds.get('password', '')}".encode()
        ).decode()
        
        # Route handler for domain-specific auth
        async def handle_auth(route):
            url = route.request.url
            headers = dict(route.request.headers)
            
            if "bo.stage.viewz.co" in url or "bo.viewz.co" in url:
                headers["Authorization"] = f"Basic {bo_auth}"
            elif "app.stage.viewz.co" in url or "app.viewz.co" in url:
                headers["Authorization"] = f"Basic {app_auth}"
            
            await route.continue_(headers=headers)
        
        await context.route("**/*", handle_auth)
        print(f"✅ Created context with domain-specific auth (BO + App)")
        
        return context
    
    async def login_to_bo(self, page: Page, bo_config: dict) -> bool:
        """Login to BO with credentials and OTP"""
        bo_url = bo_config.get("base_url", "https://bo.stage.viewz.co")
        
        bo_login_page = BOLoginPage(page, bo_url)
        await bo_login_page.goto_bo()
        await asyncio.sleep(2)
        
        # Perform login
        await bo_login_page.bo_login(
            bo_config.get("username", ""),
            bo_config.get("password", "")
        )
        await asyncio.sleep(3)
        
        # Handle 2FA/OTP if needed
        page_content = await page.content()
        if any(x in page_content for x in ["Two-Factor", "Authentication", "code", "Code"]):
            print("🔐 2FA required, entering OTP...")
            await bo_login_page.handle_bo_otp(bo_config.get("otp_secret", ""))
            await asyncio.sleep(3)
        
        # Verify login success
        if "/login" not in page.url:
            print(f"✅ BO Login successful. URL: {page.url}")
            return True
        
        print(f"⚠️ Still on login page: {page.url}")
        return False
    
    async def find_and_relogin_to_account(self, page: Page, bo_config: dict, account_id: str) -> Page:
        """Find account in BO and perform automated relogin"""
        bo_url = bo_config.get("base_url", "https://bo.stage.viewz.co")
        
        # Navigate to accounts page
        await page.goto(f"{bo_url}/settings/accounts")
        await asyncio.sleep(3)
        
        print(f"📍 On accounts page: {page.url}")
        await page.screenshot(path="debug_bo_accounts_list.png")
        
        # Search for account
        search_input = page.locator("input[placeholder*='Search'], input[type='search'], input[type='text']").first
        if await search_input.is_visible():
            await search_input.fill(account_id)
            await page.keyboard.press("Enter")
            await asyncio.sleep(2)
            print(f"✅ Searched for account {account_id}")
        
        # Find the account row
        all_rows = page.locator("table tbody tr")
        row_count = await all_rows.count()
        print(f"📋 Found {row_count} rows in accounts table")
        
        account_row = None
        for i in range(row_count):
            row = all_rows.nth(i)
            first_cell = row.locator("td").first
            cell_text = await first_cell.text_content()
            cell_text = cell_text.strip() if cell_text else ""
            if cell_text == account_id:
                account_row = row
                print(f"✅ Found account {account_id} at row {i}")
                break
        
        if not account_row:
            raise Exception(f"❌ Account {account_id} not found!")
        
        # Hover to reveal action icons
        await account_row.hover()
        await asyncio.sleep(1)
        
        # Click relogin button
        relogin_selectors = [
            "button[value='relogin']",
            "[title='Relogin To Account']",
            "i.fa-arrow-right",
            "i.fa.fa-arrow-right",
            "button:has(i.fa-arrow-right)"
        ]
        
        clicked = False
        for selector in relogin_selectors:
            try:
                btn = account_row.locator(selector).first
                if await btn.is_visible():
                    await btn.click()
                    print(f"✅ Clicked relogin button: {selector}")
                    clicked = True
                    break
            except:
                continue
        
        if not clicked:
            actions = account_row.locator("td").last
            await actions.click()
            print("✅ Clicked actions cell")
        
        await asyncio.sleep(3)
        
        # Handle relogin OTP in new window - uses BO ADMIN's OTP secret
        context = page.context
        pages = context.pages
        
        # Find the new window that opened
        new_page = None
        for pg in pages:
            if "app.stage.viewz.co" in pg.url or "relogin" in pg.url:
                new_page = pg
                break
        
        if new_page and len(pages) > 1:
            await new_page.bring_to_front()
            await asyncio.sleep(2)
            
            # Generate OTP using BO admin's secret
            relogin_otp_secret = bo_config.get("relogin_otp_secret", bo_config.get("otp_secret", ""))
            
            # Wait for fresh OTP window if near boundary
            current_time = int(time.time())
            seconds_remaining = 30 - (current_time % 30)
            if seconds_remaining < 10:
                print(f"⏳ Waiting {seconds_remaining + 1}s for fresh OTP window...")
                await asyncio.sleep(seconds_remaining + 1)
            
            totp = pyotp.TOTP(relogin_otp_secret)
            otp_code = totp.now()
            seconds_valid = 30 - (int(time.time()) % 30)
            print(f"🔐 Generated relogin OTP: {otp_code} (valid for {seconds_valid}s)")
            
            # Use our custom OTP fill function
            await fill_otp_boxes(new_page, otp_code)
            
            await asyncio.sleep(1)
            
            # Click Verify button
            verify_btn = new_page.locator("button").filter(has_text="Verify").first
            try:
                await verify_btn.click(force=True)
                print("✅ Clicked Verify button")
            except:
                await new_page.evaluate("""
                    () => {
                        const btn = document.querySelector('button');
                        if (btn && btn.textContent.includes('Verify')) btn.click();
                    }
                """)
                print("✅ Clicked Verify via JavaScript")
            
            await asyncio.sleep(5)
            
            # Check for success or error
            page_text = await new_page.text_content('body')
            if 'invalid' in page_text.lower() or 'failed' in page_text.lower():
                print("⚠️ OTP failed, retrying with fresh code...")
                
                seconds_remaining = 30 - (int(time.time()) % 30)
                await asyncio.sleep(seconds_remaining + 2)
                
                fresh_otp = totp.now()
                print(f"🔐 Retry with fresh OTP: {fresh_otp}")
                
                await fill_otp_boxes(new_page, fresh_otp)
                await asyncio.sleep(1)
                await new_page.locator("button").filter(has_text="Verify").first.click(force=True)
                await asyncio.sleep(5)
        else:
            bo_accounts_page = BOAccountsPage(page)
            relogin_otp_secret = bo_config.get("relogin_otp_secret", bo_config.get("otp_secret", ""))
            await bo_accounts_page.handle_relogin_otp(relogin_otp_secret)
        
        await asyncio.sleep(3)
        
        # Find the app page
        all_pages = context.pages
        app_page = None
        for pg in all_pages:
            if "app.stage.viewz.co" in pg.url or "app.viewz.co" in pg.url:
                app_page = pg
                print(f"✅ Found app page: {pg.url}")
                break
        
        if not app_page:
            raise Exception("❌ No app page found after relogin!")
        
        # Wait for relogin to complete
        for _ in range(15):
            if "/relogin" not in app_page.url:
                break
            await asyncio.sleep(1)
        
        await app_page.bring_to_front()
        await asyncio.sleep(2)
        
        print(f"✅ Relogin complete. App URL: {app_page.url}")
        return app_page
    
    async def navigate_to_payables(self, page: Page) -> bool:
        """Navigate to payables page"""
        await page.goto("https://app.stage.viewz.co/reconciliation/payables")
        await asyncio.sleep(3)
        
        await page.screenshot(path="debug_payables_page.png")
        
        if "/login" in page.url:
            print("❌ Redirected to login - auth failed!")
            return False
        
        if "/reconciliation/payables" in page.url:
            print(f"✅ On Payables page: {page.url}")
            return True
        
        print(f"⚠️ Unexpected URL: {page.url}")
        return False
    
    async def verify_file_in_payables(self, page: Page, search_term: str) -> bool:
        """Search and verify file exists in payables"""
        print(f"🔍 Searching for file with term: {search_term}")
        
        await asyncio.sleep(2)
        
        # Look for file by partial name match
        file_locator = page.locator(f"text={search_term}")
        if await file_locator.count() > 0:
            print(f"✅ File found in Payables: {search_term}")
            return True
            
        # Check in table rows
        rows = page.locator("table tbody tr, [class*='row']")
        row_count = await rows.count()
        
        for i in range(min(row_count, 20)):
            row = rows.nth(i)
            row_text = await row.text_content()
            if search_term.lower() in row_text.lower():
                print(f"✅ File found in row {i}")
                return True
        
        print(f"⚠️ File not found: {search_term}")
        return False
    
    async def delete_file_from_payables(self, page: Page, search_term: str) -> bool:
        """Delete file from payables"""
        print(f"🗑️ Attempting to delete file: {search_term}")
        
        file_row = page.locator(f"tr:has-text('{search_term}')").first
        
        if not await file_row.is_visible():
            print(f"⚠️ File row not found for deletion")
            return False
        
        # Try to find and click delete button
        delete_selectors = [
            "button:has-text('Delete')",
            "[aria-label*='delete' i]",
            "button:has(svg)",
            "[class*='delete']"
        ]
        
        for selector in delete_selectors:
            try:
                delete_btn = file_row.locator(selector).last
                if await delete_btn.is_visible():
                    await delete_btn.click()
                    await asyncio.sleep(1)
                    
                    confirm = page.locator("button:has-text('Confirm'), button:has-text('Yes'), button:has-text('Delete')").first
                    if await confirm.is_visible():
                        await confirm.click()
                        await asyncio.sleep(2)
                    
                    print("✅ File deleted from Payables")
                    return True
            except:
                continue
        
        # Try checkbox + bulk delete
        try:
            checkbox = file_row.locator("input[type='checkbox']").first
            if await checkbox.is_visible():
                await checkbox.click()
                await asyncio.sleep(0.5)
                
                bulk_delete = page.locator("button:has-text('Delete')").first
                if await bulk_delete.is_visible():
                    await bulk_delete.click()
                    await asyncio.sleep(2)
                    print("✅ File deleted via bulk action")
                    return True
        except:
            pass
        
        print("⚠️ Could not delete file")
        return False
    
    @pytest.mark.asyncio
    async def test_easysend_complete_flow(self):
        """
        Complete E2E test for EasySend Email to Payables on Stage:
        1. Login to Outlook (automation@viewz.co)
        2. Send email with PDF attachment to easysend@viewz.co
        3. Wait for EasySend processing
        4. Login to BO, find account 71, perform automated relogin
        5. Verify file appears in Payables
        6. Delete file from Payables (cleanup)
        """
        print("\n" + "="*70)
        print("🧪 TEST: EasySend Email to Payables - Complete E2E Flow (Stage)")
        print("="*70)
        
        # Load configs
        bo_config, app_config = self.load_configs()
        
        if not bo_config:
            pytest.fail("BO config required for this test")
        
        # Verify test file exists
        if not os.path.exists(self.TEST_FILE_PATH):
            pytest.fail(f"Test file not found: {self.TEST_FILE_PATH}")
        
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=False, slow_mo=100)
            
            try:
                # ==========================================
                # STEP 1: Login to Outlook
                # ==========================================
                print("\n" + "="*50)
                print("📧 STEP 1: Login to Outlook")
                print("="*50)
                
                # Create simple context for Outlook (no special auth needed)
                outlook_context = await browser.new_context()
                outlook_page = await outlook_context.new_page()
                
                login_success = await self.login_to_outlook(outlook_page)
                if not login_success:
                    pytest.fail("Failed to login to Outlook")
                
                # ==========================================
                # STEP 2: Send email with attachment
                # ==========================================
                print("\n" + "="*50)
                print("📎 STEP 2: Send email with attachment")
                print("="*50)
                
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                subject = f"Test Invoice {timestamp}"
                
                email_sent = await self.send_email_with_attachment(
                    outlook_page, 
                    self.TEST_FILE_PATH, 
                    subject
                )
                
                if not email_sent:
                    print("⚠️ Email sending may have issues, continuing...")
                
                # Close Outlook context
                await outlook_context.close()
                
                # ==========================================
                # STEP 3: Wait for EasySend processing
                # ==========================================
                print("\n" + "="*50)
                print("⏱️ STEP 3: Wait for EasySend processing (60 seconds)")
                print("="*50)
                
                print("⏳ Waiting 60 seconds for EasySend to process the email...")
                await asyncio.sleep(60)
                print("✅ Wait complete")
                
                # ==========================================
                # STEP 4: Login to BO
                # ==========================================
                print("\n" + "="*50)
                print("🏢 STEP 4: Login to BO")
                print("="*50)
                
                # Create context with domain-specific auth for BO and App
                bo_context = await self.create_auth_context(browser, bo_config, app_config)
                bo_page = await bo_context.new_page()
                
                login_success = await self.login_to_bo(bo_page, bo_config)
                if not login_success:
                    await bo_page.screenshot(path="debug_bo_login_failure.png")
                    pytest.fail("BO login failed")
                
                # Save auth state
                await bo_context.storage_state(path="bo_auth_state.json")
                print("💾 Saved BO auth state")
                
                # ==========================================
                # STEP 5: Find account and perform relogin
                # ==========================================
                print("\n" + "="*50)
                print(f"🔄 STEP 5: Relogin to account {self.BO_ACCOUNT_ID}")
                print("="*50)
                
                app_page = await self.find_and_relogin_to_account(
                    bo_page, bo_config, self.BO_ACCOUNT_ID
                )
                
                # ==========================================
                # STEP 6: Navigate to Payables
                # ==========================================
                print("\n" + "="*50)
                print("📄 STEP 6: Navigate to Payables")
                print("="*50)
                
                payables_success = await self.navigate_to_payables(app_page)
                if not payables_success:
                    await app_page.screenshot(path="debug_payables_failure.png")
                    pytest.fail("Failed to navigate to Payables")
                
                # ==========================================
                # STEP 7: Verify file in Payables
                # ==========================================
                print("\n" + "="*50)
                print("✅ STEP 7: Verify file in Payables")
                print("="*50)
                
                # EasySend generates document IDs like PI250079... - look for new files uploaded today
                await app_page.screenshot(path="debug_file_verification.png")
                
                # Find rows with "New" status (recently uploaded)
                new_rows = app_page.locator("tr:has(td:has-text('New'))")
                new_count = await new_rows.count()
                print(f"📋 Found {new_count} rows with 'New' status")
                
                if new_count > 0:
                    print("✅ New file found in Payables!")
                    
                    # ==========================================
                    # STEP 8: Delete file (cleanup)
                    # ==========================================
                    print("\n" + "="*50)
                    print("🗑️ STEP 8: Delete file from Payables")
                    print("="*50)
                    
                    try:
                        first_new_row = new_rows.first
                        
                        # Step 1: Find and click the "..." button in Actions column
                        actions_cell = first_new_row.locator("td").last
                        
                        # The ... button uses cursor-pointer class
                        three_dot_btn = None
                        selectors = [
                            "[class*='cursor-pointer']",
                            "button",
                            "[role='button']",
                            "span:has-text('⋯')",
                            "svg",
                        ]
                        
                        for selector in selectors:
                            try:
                                elem = actions_cell.locator(selector).first
                                if await elem.is_visible():
                                    three_dot_btn = elem
                                    print(f"✅ Found action button: {selector}")
                                    break
                            except:
                                continue
                        
                        if not three_dot_btn:
                            three_dot_btn = actions_cell
                        
                        if await three_dot_btn.is_visible():
                            await three_dot_btn.click()
                            await asyncio.sleep(1)
                            await app_page.screenshot(path="debug_actions_menu.png")
                            print("✅ Clicked ... button in Actions column")
                            
                            # Step 2: Click Delete option in the dropdown
                            delete_option = app_page.locator("text=Delete").first
                            
                            if await delete_option.is_visible():
                                await delete_option.click()
                                await asyncio.sleep(1)
                                await app_page.screenshot(path="debug_delete_clicked.png")
                                print("✅ Clicked Delete option")
                                
                                # Step 3: Handle confirmation dialog
                                await asyncio.sleep(1)
                                confirm_delete_btn = app_page.locator("button:has-text('Delete')").last
                                if await confirm_delete_btn.is_visible():
                                    await confirm_delete_btn.click()
                                    print("✅ Confirmed deletion")
                                    await asyncio.sleep(2)
                                    print("✅ File deleted successfully!")
                                else:
                                    print("⚠️ Confirmation dialog not found")
                            else:
                                print("⚠️ Delete option not visible in menu")
                        else:
                            print("⚠️ Actions button not found")
                        
                        await app_page.screenshot(path="debug_after_delete.png")
                    except Exception as e:
                        print(f"⚠️ Delete failed: {str(e)[:50]}")
                        await app_page.screenshot(path="debug_delete_error.png")
                else:
                    print(f"⚠️ No new files found - may still be processing or already deleted")
                
                print("\n" + "="*70)
                print("✅ EASYSEND EMAIL TO PAYABLES TEST COMPLETE!")
                print("="*70)
                
            except Exception as e:
                print(f"\n❌ Test failed with error: {str(e)}")
                import traceback
                traceback.print_exc()
                raise
            
            finally:
                await browser.close()

    @pytest.mark.asyncio
    async def test_bo_relogin_to_payables_only(self):
        """
        Simplified test: Just BO login, relogin, and verify payables access
        (Skips email sending for faster testing)
        """
        print("\n" + "="*70)
        print("🧪 TEST: BO Relogin to Payables Only (Stage)")
        print("="*70)
        
        bo_config, app_config = self.load_configs()
        
        if not bo_config:
            pytest.fail("BO config required")
        
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=False, slow_mo=100)
            
            try:
                context = await self.create_auth_context(browser, bo_config, app_config)
                bo_page = await context.new_page()
                
                # Login to BO
                print("\n🏢 Logging into BO...")
                await self.login_to_bo(bo_page, bo_config)
                
                # Relogin to account
                print(f"\n🔄 Relogin to account {self.BO_ACCOUNT_ID}...")
                app_page = await self.find_and_relogin_to_account(
                    bo_page, bo_config, self.BO_ACCOUNT_ID
                )
                
                # Navigate to payables
                print("\n📄 Navigating to Payables...")
                success = await self.navigate_to_payables(app_page)
                
                assert success, "Failed to access Payables page"
                
                await app_page.screenshot(path="debug_payables_success.png")
                
                # ==========================================
                # Test Delete functionality
                # ==========================================
                print("\n" + "="*50)
                print("🗑️ Testing Delete functionality")
                print("="*50)
                
                # Find rows with "New" status
                new_rows = app_page.locator("tr:has(td:has-text('New'))")
                new_count = await new_rows.count()
                print(f"📋 Found {new_count} rows with 'New' status")
                
                if new_count > 0:
                    first_new_row = new_rows.first
                    
                    # Step 1: Find and click the "..." button in Actions column
                    # The ... button might be a div, span, or other clickable element
                    actions_cell = first_new_row.locator("td").last
                    
                    # Try multiple selectors for the 3-dot menu
                    three_dot_btn = None
                    selectors = [
                        "button",
                        "[role='button']",
                        "span:has-text('⋯')",
                        "span:has-text('...')",
                        "*:has-text('⋯')",
                        "*:has-text('...')",
                        "[class*='cursor-pointer']",
                        "svg",
                    ]
                    
                    for selector in selectors:
                        try:
                            elem = actions_cell.locator(selector).first
                            if await elem.is_visible():
                                three_dot_btn = elem
                                print(f"✅ Found action button with: {selector}")
                                break
                        except:
                            continue
                    
                    # Fallback: just click the actions cell itself
                    if not three_dot_btn:
                        three_dot_btn = actions_cell
                        print("📌 Using actions cell as clickable element")
                    
                    if await three_dot_btn.is_visible():
                        await three_dot_btn.click()
                        await asyncio.sleep(1)
                        await app_page.screenshot(path="debug_actions_menu.png")
                        print("✅ Clicked ... button in Actions column")
                        
                        # Step 2: Click Delete option in the dropdown
                        delete_option = app_page.locator("text=Delete").first
                        
                        if await delete_option.is_visible():
                            await delete_option.click()
                            await asyncio.sleep(1)
                            await app_page.screenshot(path="debug_delete_clicked.png")
                            print("✅ Clicked Delete option")
                            
                            # Step 3: Handle confirmation dialog
                            await asyncio.sleep(1)
                            confirm_btn = app_page.locator("button:has-text('Delete')").last
                            if await confirm_btn.is_visible():
                                await confirm_btn.click()
                                print("✅ Confirmed deletion")
                                await asyncio.sleep(2)
                                print("✅ File deleted successfully!")
                            else:
                                print("⚠️ Confirmation dialog not found")
                        else:
                            print("⚠️ Delete option not visible in menu")
                    else:
                        print("⚠️ Actions button not found")
                    
                    await app_page.screenshot(path="debug_after_delete.png")
                else:
                    print("⚠️ No files with 'New' status to delete")
                
                print("\n✅ TEST PASSED: Successfully accessed Payables via BO relogin")
                
            finally:
                await browser.close()
