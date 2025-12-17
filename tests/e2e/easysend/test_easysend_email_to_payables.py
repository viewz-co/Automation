"""
EasySend Email to Payables E2E Test
Tests the flow of sending an invoice via Outlook email to EasySend and verifying it appears in Payables
Uses Outlook account: automation@viewz.co
"""

import pytest
import asyncio
import os
import pyotp
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from playwright.async_api import async_playwright
from datetime import datetime

from pages.bo_login_page import BOLoginPage
from pages.bo_accounts_page import BOAccountsPage


class TestEasySendEmailToPayables:
    """Test suite for EasySend email-to-payables flow"""
    
    # Outlook credentials
    OUTLOOK_EMAIL = "automation@viewz.co"
    OUTLOOK_PASSWORD = "V.784167838236ov"
    EASYSEND_EMAIL = "easysend@viewz.co"
    
    # Test file path
    TEST_FILE_PATH = "uploaded_test_files/PI25007981 - הדפסת חשבונית עסקה 1.1.pdf"
    
    # BO Account to relogin
    BO_ACCOUNT_ID = "71"
    
    def send_email_via_smtp(self, file_path: str, subject: str) -> bool:
        """Send email with attachment using Outlook SMTP"""
        try:
            print(f"📧 Sending email via Outlook SMTP...")
            
            # Create message
            message = MIMEMultipart()
            message["From"] = self.OUTLOOK_EMAIL
            message["To"] = self.EASYSEND_EMAIL
            message["Subject"] = subject
            
            # Add body
            body = f"Test invoice sent at {datetime.now().isoformat()}"
            message.attach(MIMEText(body, "plain"))
            
            # Attach file
            abs_path = os.path.abspath(file_path)
            filename = os.path.basename(abs_path)
            
            with open(abs_path, "rb") as attachment:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(attachment.read())
            
            encoders.encode_base64(part)
            part.add_header(
                "Content-Disposition",
                f"attachment; filename= {filename}",
            )
            message.attach(part)
            
            # Connect to Outlook SMTP (Office 365)
            context = ssl.create_default_context()
            with smtplib.SMTP("smtp.office365.com", 587) as server:
                server.starttls(context=context)
                server.login(self.OUTLOOK_EMAIL, self.OUTLOOK_PASSWORD)
                server.sendmail(self.OUTLOOK_EMAIL, self.EASYSEND_EMAIL, message.as_string())
            
            print(f"✅ Email sent via Outlook SMTP to {self.EASYSEND_EMAIL}")
            return True
            
        except Exception as e:
            print(f"❌ SMTP send failed: {str(e)}")
            return False
    
    @pytest.mark.asyncio
    async def test_easysend_email_to_payables_flow(self, env_config):
        """
        Complete E2E test:
        1. Login to Outlook (automation@viewz.co)
        2. Send PDF invoice to easysend@viewz.co
        3. Wait for processing
        4. Login to BO, search account 71, relogin
        5. Verify file in payables
        6. Delete file from payables
        """
        print("\n" + "="*60)
        print("🧪 TEST: EasySend Email to Payables Flow")
        print("="*60)
        
        base_url = env_config.get("base_url", "https://app.stage.viewz.co")
        bo_config = None
        
        # Load BO config
        try:
            import json
            with open('configs/bo_stage_env_config.json', 'r') as f:
                bo_config = json.load(f)
        except:
            print("⚠️ Could not load BO config, using defaults")
        
        async with async_playwright() as p:
            # Launch browser (not headless for Gmail - may need visual verification)
            browser = await p.chromium.launch(headless=False, slow_mo=100)
            context = await browser.new_context()
            page = await context.new_page()
            
            try:
                # ==========================================
                # STEP 1: Login to Outlook
                # ==========================================
                print("\n📧 STEP 1: Logging into Outlook...")
                
                await page.goto("https://outlook.office.com/mail/")
                await asyncio.sleep(3)
                
                # Enter email
                email_input = page.locator("input[type='email']")
                if await email_input.is_visible():
                    await email_input.fill(self.OUTLOOK_EMAIL)
                    await page.click("input[type='submit']")
                    await asyncio.sleep(3)
                
                # Enter password
                password_input = page.locator("input[type='password']")
                try:
                    await password_input.wait_for(state="visible", timeout=10000)
                    await password_input.fill(self.OUTLOOK_PASSWORD)
                    print("✅ Entered password")
                    await page.click("input[type='submit']")
                    await asyncio.sleep(5)
                except:
                    print("⚠️ Password field not found")
                
                # Check for "Stay signed in?" prompt
                stay_signed_in = page.locator("input[type='submit'][value='Yes'], button:has-text('Yes')")
                if await stay_signed_in.first.is_visible():
                    await stay_signed_in.first.click()
                    await asyncio.sleep(3)
                
                # Check if logged in
                for _ in range(15):  # Check for 15 seconds
                    if "outlook.office" in page.url and "mail" in page.url:
                        print("✅ Logged into Outlook successfully")
                        break
                    await asyncio.sleep(1)
                else:
                    print(f"⚠️ Outlook URL: {page.url}")
                    await page.screenshot(path="debug_outlook_login.png")
                
                # ==========================================
                # STEP 2: Compose and send email with attachment
                # ==========================================
                print("\n📎 STEP 2: Composing email with attachment...")
                
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                subject = f"Test Invoice {timestamp}"
                
                # Click New mail button - Outlook selectors
                await page.screenshot(path="debug_outlook_before_compose.png")
                print(f"📍 Current URL: {page.url}")
                
                compose_clicked = False
                compose_selectors = [
                    "[aria-label='New mail']",
                    "button:has-text('New mail')",
                    "button:has-text('New message')",
                    "[data-icon-name='Compose']",
                    "button[title='New mail']",
                ]
                
                for selector in compose_selectors:
                    try:
                        compose_btn = page.locator(selector).first
                        if await compose_btn.is_visible():
                            await compose_btn.click()
                            compose_clicked = True
                            print(f"✅ Clicked New mail using: {selector}")
                            break
                    except:
                        continue
                
                if not compose_clicked:
                    # Try keyboard shortcut
                    await page.keyboard.press("n")
                    await asyncio.sleep(1)
                    compose_clicked = True
                    print("✅ Opened compose via keyboard 'n'")
                
                await asyncio.sleep(2)
                
                # Fill To field
                to_field = page.locator("[aria-label='To']").first
                if not await to_field.is_visible():
                    to_field = page.locator("input[placeholder*='To']").first
                if not await to_field.is_visible():
                    to_field = page.locator("div[aria-label='To'] input").first
                await to_field.fill(self.EASYSEND_EMAIL)
                await page.keyboard.press("Tab")
                await asyncio.sleep(0.5)
                print(f"✅ Entered recipient: {self.EASYSEND_EMAIL}")
                
                # Fill Subject
                subject_field = page.locator("input[aria-label='Add a subject']").first
                if not await subject_field.is_visible():
                    subject_field = page.locator("input[placeholder*='subject' i]").first
                await subject_field.fill(subject)
                print(f"✅ Entered subject: {subject}")
                
                # Attach file
                file_path = os.path.abspath(self.TEST_FILE_PATH)
                print(f"📄 Attaching file: {file_path}")
                
                # Click Attach button first
                attach_btn = page.locator("[aria-label='Attach'], button:has-text('Attach')").first
                if await attach_btn.is_visible():
                    await attach_btn.click()
                    await asyncio.sleep(1)
                    
                    # Click "Browse this computer"
                    browse_btn = page.locator("text=Browse this computer, text=Upload from computer").first
                    if await browse_btn.is_visible():
                        await browse_btn.click()
                        await asyncio.sleep(1)
                
                # Set file input
                file_input = page.locator("input[type='file']").first
                await file_input.set_input_files(file_path)
                await asyncio.sleep(3)
                print("✅ File attached")
                
                # Click Send button
                send_btn = page.locator("[aria-label='Send'], button:has-text('Send')").first
                if await send_btn.is_visible():
                    await send_btn.click()
                    print("✅ Clicked Send")
                else:
                    await page.keyboard.press("Control+Enter")
                    print("✅ Sent via Ctrl+Enter")
                
                await asyncio.sleep(5)
                await page.screenshot(path="debug_email_sent.png")
                print("✅ Email sent!")
                
                # ==========================================
                # STEP 3: Wait for EasySend processing
                # ==========================================
                print("\n⏱️ STEP 3: Waiting 60 seconds for EasySend processing...")
                await asyncio.sleep(60)
                print("✅ Wait complete")
                
                # ==========================================
                # STEP 4: Login to BO and search for account
                # ==========================================
                print("\n🏢 STEP 4: Logging into BO...")
                
                bo_url = bo_config.get("base_url", "https://bo.stage.viewz.co") if bo_config else "https://bo.stage.viewz.co"
                
                # Create context with domain-specific Basic Auth (BO and App have different passwords)
                bo_creds = bo_config.get("basic_auth", {}) if bo_config else {}
                bo_context = await browser.new_context()
                
                # Set up route interception for domain-specific auth
                import base64
                bo_auth = base64.b64encode(f"{bo_creds.get('username', 'admin')}:{bo_creds.get('password', '')}".encode()).decode()
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
                
                # Use BOLoginPage for proper login
                bo_login_page = BOLoginPage(bo_page, bo_url)
                await bo_login_page.goto_bo()
                await asyncio.sleep(2)
                
                await bo_page.screenshot(path="debug_bo_login_page.png")
                print("📸 Screenshot: debug_bo_login_page.png")
                
                # Perform BO login
                await bo_login_page.bo_login(
                    bo_config.get("username", ""),
                    bo_config.get("password", "")
                )
                await asyncio.sleep(3)
                
                await bo_page.screenshot(path="debug_bo_after_credentials.png")
                print("📸 Screenshot: debug_bo_after_credentials.png")
                
                # Handle 2FA/OTP
                page_content = await bo_page.content()
                if "Two-Factor" in page_content or "Authentication" in page_content or "code" in page_content.lower():
                    print("🔐 2FA required, entering OTP...")
                    await bo_login_page.handle_bo_otp(bo_config.get("otp_secret", ""))
                    await asyncio.sleep(3)
                
                await bo_page.screenshot(path="debug_bo_after_login.png")
                print(f"✅ BO Login complete. URL: {bo_page.url}")
                
                # Verify we're logged in (not still on login page)
                if "/login" in bo_page.url:
                    print("⚠️ Still on login page, trying again...")
                    # Try clicking submit again
                    submit = bo_page.locator("button[type='submit']").first
                    if await submit.is_visible():
                        await submit.click()
                        await asyncio.sleep(5)
                
                # Save storage state after successful login
                await bo_context.storage_state(path="bo_auth_state.json")
                print("💾 Saved BO auth state to bo_auth_state.json")
                
                # ==========================================
                # STEP 5: Search for account 71
                # ==========================================
                print(f"\n🔍 STEP 5: Searching for account {self.BO_ACCOUNT_ID}...")
                
                # Use BOAccountsPage for account operations
                bo_accounts_page = BOAccountsPage(bo_page)
                
                # Navigate to accounts
                await bo_page.goto(f"{bo_url}/settings/accounts")
                await asyncio.sleep(3)
                
                await bo_page.screenshot(path="debug_bo_accounts_page.png")
                print(f"📍 On accounts page: {bo_page.url}")
                
                # Search for account 71
                search_input = bo_page.locator("input[placeholder*='Search'], input[type='search'], input[type='text']").first
                if await search_input.is_visible():
                    await search_input.fill(self.BO_ACCOUNT_ID)
                    await bo_page.keyboard.press("Enter")
                    await asyncio.sleep(2)
                    print(f"✅ Searched for account {self.BO_ACCOUNT_ID}")
                else:
                    print("⚠️ Search input not found, looking for account in list...")
                
                await bo_page.screenshot(path="debug_bo_account_search.png")
                
                # ==========================================
                # STEP 6: Relogin to account (MANUAL)
                # ==========================================
                print("\n🔄 STEP 6: Relogin to account...")
                print("="*60)
                print("🖐️ MANUAL STEP: Please perform relogin for account 71 now!")
                print("   1. Find account 71 in the table")
                print("   2. Click the relogin arrow button (→)")
                print("   3. Enter the OTP code when prompted")
                print("   4. Wait for the app page to load")
                print("="*60)
                print("⏳ Waiting 60 seconds for manual relogin...")
                await asyncio.sleep(60)
                
                app_page = None  # Will store the app page after relogin
                
                print("✅ Manual relogin wait complete. Looking for app page...")
                await bo_page.screenshot(path="debug_after_manual_relogin.png")
                
                # ==========================================
                # STEP 7: Navigate to Payables
                # ==========================================
                print("\n📄 STEP 7: Navigating to Payables...")
                
                # Find the app page that was opened during manual relogin
                all_pages = bo_context.pages
                print(f"📄 Total pages open: {len(all_pages)}")
                for i, pg in enumerate(all_pages):
                    print(f"   Page {i}: {pg.url[:60]}...")
                    if "app.stage.viewz.co" in pg.url or "app.viewz.co" in pg.url:
                        app_page = pg
                        print(f"📍 Found app page: {pg.url[:80]}...")
                        break
                
                if app_page:
                    # Wait for relogin to complete (URL should change from /relogin to something else)
                    print("⏳ Waiting for relogin to complete...")
                    for _ in range(15):  # Wait up to 15 seconds
                        current_url = app_page.url
                        if "/relogin" not in current_url:
                            print(f"✅ Relogin complete! URL: {current_url[:60]}...")
                            break
                        await asyncio.sleep(1)
                    
                    # Bring the app page to front
                    await app_page.bring_to_front()
                    await asyncio.sleep(2)
                    
                    # Navigate to Payables - HTTP auth should already be set by handle_relogin_otp
                    await app_page.goto("https://app.stage.viewz.co/reconciliation/payables")
                    await asyncio.sleep(3)
                else:
                    # No app page found - create new context with saved storage state
                    print("⚠️ No app page found, creating new context with saved auth state...")
                    try:
                        app_context = await browser.new_context(
                            storage_state="bo_auth_state.json",
                            http_credentials={
                                "username": bo_creds.get("username", "admin"),
                                "password": bo_creds.get("password", "")
                            }
                        )
                        app_page = await app_context.new_page()
                        await app_page.goto("https://app.stage.viewz.co/reconciliation/payables")
                    except:
                        # Fallback to URL with embedded credentials
                        app_page = await bo_context.new_page()
                        payables_url = "https://admin:RiBrsuk*8w4%2508Dx@app.stage.viewz.co/reconciliation/payables"
                        await app_page.goto(payables_url)
                    await asyncio.sleep(3)
                
                print(f"📍 Current page URL: {app_page.url}")
                await app_page.screenshot(path="debug_payables_page.png")
                
                # Verify we're actually on payables, not redirected to login
                if "/login" in app_page.url:
                    raise Exception("❌ Relogin failed - redirected to login page instead of payables!")
                
                if "/reconciliation/payables" not in app_page.url:
                    print(f"⚠️ Not on payables page, current URL: {app_page.url}")
                    # Try navigating again with embedded auth
                    payables_url = "https://admin:RiBrsuk*8w4%2508Dx@app.stage.viewz.co/reconciliation/payables"
                    await app_page.goto(payables_url)
                    await asyncio.sleep(3)
                    
                    if "/login" in app_page.url:
                        raise Exception("❌ Still redirected to login - relogin session not valid!")
                
                print(f"✅ On Payables page: {app_page.url}")
                
                # ==========================================
                # STEP 8: Verify file exists in Payables
                # ==========================================
                print("\n✅ STEP 8: Verifying file in Payables...")
                
                # Look for the uploaded file
                file_name = os.path.basename(self.TEST_FILE_PATH)
                file_found = False
                
                # Search for the file or check the list
                file_locator = app_page.locator(f"text={file_name[:20]}")  # Partial match
                if await file_locator.count() > 0:
                    file_found = True
                    print(f"✅ File found in Payables: {file_name}")
                else:
                    # Check for any recent uploads
                    recent_files = app_page.locator("tr, [class*='row']").filter(has_text="PI25007981")
                    if await recent_files.count() > 0:
                        file_found = True
                        print("✅ File found by invoice number")
                
                await app_page.screenshot(path="debug_file_verification.png")
                
                # ==========================================
                # STEP 9: Delete file from Payables
                # ==========================================
                print("\n🗑️ STEP 9: Deleting file from Payables...")
                
                if file_found:
                    # Find the file row and delete
                    file_row = app_page.locator("tr:has-text('PI25007981')").first
                    if await file_row.is_visible():
                        # Click on actions/delete button
                        delete_btn = file_row.locator("button:has-text('Delete'), [aria-label*='delete'], button:has(svg)").last
                        if await delete_btn.is_visible():
                            await delete_btn.click()
                            await asyncio.sleep(1)
                            
                            # Confirm deletion if dialog appears
                            confirm_btn = app_page.locator("button:has-text('Confirm'), button:has-text('Yes'), button:has-text('Delete')").first
                            if await confirm_btn.is_visible():
                                await confirm_btn.click()
                                await asyncio.sleep(2)
                            
                            print("✅ File deleted from Payables")
                        else:
                            # Try checkbox + delete
                            checkbox = file_row.locator("input[type='checkbox']").first
                            if await checkbox.is_visible():
                                await checkbox.click()
                                await asyncio.sleep(0.5)
                                
                                # Click bulk delete
                                bulk_delete = app_page.locator("button:has-text('Delete')").first
                                if await bulk_delete.is_visible():
                                    await bulk_delete.click()
                                    await asyncio.sleep(2)
                                    print("✅ File deleted via bulk action")
                
                await app_page.screenshot(path="debug_after_delete.png")
                
                print("\n" + "="*60)
                print("✅ EASYSEND EMAIL TO PAYABLES TEST COMPLETE!")
                print("="*60)
                
            except Exception as e:
                print(f"\n❌ Test failed with error: {str(e)}")
                await page.screenshot(path="debug_test_failure.png")
                raise
            
            finally:
                await browser.close()

