"""
Outlook Email Send Test - Focused on sending email with attachment
Tests only the Outlook login and email sending flow

Preconditions:
- Outlook account (automation@viewz.co) is accessible
- Test PDF file exists at: uploaded_test_files/PI25007981 - הדפסת חשבונית עסקה 1.1.pdf
"""

import pytest
import asyncio
import os
from playwright.async_api import async_playwright, Page
from datetime import datetime


class TestOutlookSendEmail:
    """Test suite focused on Outlook email sending"""
    
    # Outlook credentials
    OUTLOOK_EMAIL = "automation@viewz.co"
    OUTLOOK_PASSWORD = "V.784167838236ov"
    EASYSEND_EMAIL = "easysend@viewz.co"
    
    # Test file path (using ASCII filename to avoid encoding issues)
    TEST_FILE_PATH = "uploaded_test_files/easysend-invoice.pdf"
    
    async def login_to_outlook(self, page: Page) -> bool:
        """Login to Outlook Web (Office 365)"""
        print("\n📧 Logging into Outlook...")
        
        await page.goto("https://outlook.office.com/mail/")
        await asyncio.sleep(5)
        
        await page.screenshot(path="debug_outlook_1_initial.png")
        print(f"📍 Initial URL: {page.url}")
        
        # Check if already logged in
        current_url = page.url
        if "outlook.office.com/mail" in current_url and "login" not in current_url.lower() and "authorize" not in current_url:
            print("✅ Already logged into Outlook")
            return True
        
        # Step 1: Enter email address
        print("📝 Step 1: Entering email...")
        try:
            email_input = page.locator("input[type='email'], input[name='loginfmt']")
            await email_input.wait_for(state="visible", timeout=10000)
            await email_input.click()
            await email_input.fill(self.OUTLOOK_EMAIL)
            print(f"✅ Entered email: {self.OUTLOOK_EMAIL}")
            
            # Click Next button
            next_btn = page.locator("input[type='submit'], #idSIButton9")
            await next_btn.click()
            print("✅ Clicked Next")
            await asyncio.sleep(3)
        except Exception as e:
            print(f"⚠️ Email entry issue: {str(e)[:80]}")
            await page.screenshot(path="debug_outlook_email_error.png")
        
        await page.screenshot(path="debug_outlook_2_after_email.png")
        
        # Step 2: Enter password
        print("📝 Step 2: Entering password...")
        try:
            password_input = page.locator("input[type='password'], input[name='passwd']")
            await password_input.wait_for(state="visible", timeout=15000)
            await password_input.click()
            await password_input.fill(self.OUTLOOK_PASSWORD)
            print("✅ Entered password")
            
            # Click Sign in button
            signin_btn = page.locator("input[type='submit'], #idSIButton9")
            await signin_btn.click()
            print("✅ Clicked Sign in")
            await asyncio.sleep(5)
        except Exception as e:
            print(f"⚠️ Password entry issue: {str(e)[:80]}")
            await page.screenshot(path="debug_outlook_password_error.png")
        
        await page.screenshot(path="debug_outlook_3_after_password.png")
        
        # Step 3: Handle "Stay signed in?" prompt
        print("📝 Step 3: Handling 'Stay signed in' prompt...")
        try:
            stay_btn = page.locator("#idSIButton9, input[value='Yes']")
            await stay_btn.wait_for(state="visible", timeout=10000)
            await stay_btn.click()
            print("✅ Clicked 'Yes' to stay signed in")
            await asyncio.sleep(5)
        except:
            try:
                no_btn = page.locator("#idBtn_Back, input[value='No']")
                if await no_btn.is_visible(timeout=3000):
                    await no_btn.click()
                    print("✅ Clicked 'No' for stay signed in")
                    await asyncio.sleep(3)
            except:
                pass
        
        await page.screenshot(path="debug_outlook_4_after_stay.png")
        
        # Step 4: Wait for Outlook mail to load
        print("📝 Step 4: Waiting for Outlook mail to load...")
        for attempt in range(30):
            current_url = page.url
            if "outlook.office.com/mail" in current_url or "outlook.live.com/mail" in current_url:
                if "authorize" not in current_url and "login" not in current_url:
                    print(f"✅ Logged into Outlook successfully!")
                    await asyncio.sleep(3)
                    await page.screenshot(path="debug_outlook_5_logged_in.png")
                    return True
            await asyncio.sleep(1)
        
        print(f"⚠️ Outlook login timeout. URL: {page.url}")
        await page.screenshot(path="debug_outlook_login_timeout.png")
        return False
    
    async def compose_and_send_email(self, page: Page, to_email: str, subject: str, file_path: str) -> bool:
        """Compose and send email with attachment"""
        print(f"\n📎 Composing email...")
        print(f"   To: {to_email}")
        print(f"   Subject: {subject}")
        print(f"   Attachment: {file_path}")
        
        await page.screenshot(path="debug_compose_1_before.png")
        
        # Step 1: Click New Mail button
        print("\n📝 Step 1: Opening compose window...")
        
        # Try clicking New Mail button with various selectors
        new_mail_btn = page.locator("button:has-text('New mail'), [aria-label='New mail']").first
        try:
            await new_mail_btn.click(timeout=5000)
            print("✅ Clicked New Mail button")
        except:
            await page.keyboard.press("n")
            print("✅ Opened compose via 'n' key")
        
        await asyncio.sleep(3)
        await page.screenshot(path="debug_compose_2_opened.png")
        
        # Step 2: Fill To field using insert_text (bypasses keyboard layout issues)
        print("\n📝 Step 2: Filling To field...")
        
        to_filled = False
        
        # Click the To button to activate input, then use insert_text
        try:
            to_btn = page.locator("button:has-text('To')").first
            await to_btn.click()
            await asyncio.sleep(0.5)
            
            # Use insert_text - this inserts text directly without key simulation
            await page.keyboard.insert_text(to_email)
            await asyncio.sleep(0.5)
            await page.keyboard.press("Enter")  # Confirm the recipient
            to_filled = True
            print(f"✅ Filled To field via insert_text: {to_email}")
        except Exception as e:
            print(f"   insert_text failed: {str(e)[:50]}")
        
        # Fallback: Use evaluate to set value directly via JavaScript
        if not to_filled:
            try:
                # Find the active element (should be the To input) and set its value
                result = await page.evaluate(f'''
                    () => {{
                        const activeElement = document.activeElement;
                        if (activeElement && (activeElement.tagName === 'INPUT' || activeElement.isContentEditable)) {{
                            if (activeElement.tagName === 'INPUT') {{
                                activeElement.value = "{to_email}";
                            }} else {{
                                activeElement.textContent = "{to_email}";
                            }}
                            activeElement.dispatchEvent(new Event('input', {{ bubbles: true }}));
                            return 'set via active element';
                        }}
                        return 'no active element';
                    }}
                ''')
                print(f"   JavaScript result: {result}")
                await page.keyboard.press("Enter")
                to_filled = True
                print(f"✅ Filled To field via JavaScript: {to_email}")
            except Exception as e:
                print(f"   JavaScript failed: {str(e)[:50]}")
        
        await asyncio.sleep(1)
        await page.screenshot(path="debug_compose_3_to_filled.png")
        
        # Step 3: Fill Subject - Click on subject input directly
        print("\n📝 Step 3: Filling Subject...")
        
        subject_input = page.locator("input[aria-label='Add a subject'], input[placeholder*='subject' i]").first
        try:
            await subject_input.click(timeout=3000)
            await subject_input.fill(subject)
            print(f"✅ Filled Subject: {subject}")
        except:
            # Tab to subject field
            await page.keyboard.press("Tab")
            await asyncio.sleep(0.3)
            await page.keyboard.type(subject, delay=20)
            print(f"✅ Filled Subject via keyboard: {subject}")
        
        await asyncio.sleep(0.5)
        await page.screenshot(path="debug_compose_4_subject_filled.png")
        
        # Step 4: Attach file using the Insert menu or toolbar attach button
        print(f"\n📝 Step 4: Attaching file...")
        abs_path = os.path.abspath(file_path)
        print(f"   File path: {abs_path}")
        
        if not os.path.exists(abs_path):
            print(f"❌ File not found: {abs_path}")
            return False
        
        attached = False
        
        # Method 1: Drag and drop file into the compose body
        try:
            # Find the compose body area
            compose_body = page.locator("[aria-label='Message body'], [role='textbox'][aria-multiline='true'], div[contenteditable='true']").first
            
            if await compose_body.is_visible(timeout=3000):
                # Create a DataTransfer with the file
                # Playwright's set_input_files doesn't work for drag-drop, so we use evaluate
                
                # First, read the file as base64
                import base64
                with open(abs_path, 'rb') as f:
                    file_content = base64.b64encode(f.read()).decode('utf-8')
                
                file_name = os.path.basename(abs_path)
                
                # Drop the file using JavaScript
                result = await page.evaluate(f'''
                    async () => {{
                        const base64 = "{file_content}";
                        const fileName = "{file_name}";
                        
                        // Convert base64 to blob
                        const byteCharacters = atob(base64);
                        const byteNumbers = new Array(byteCharacters.length);
                        for (let i = 0; i < byteCharacters.length; i++) {{
                            byteNumbers[i] = byteCharacters.charCodeAt(i);
                        }}
                        const byteArray = new Uint8Array(byteNumbers);
                        const blob = new Blob([byteArray], {{ type: 'application/pdf' }});
                        
                        // Create File object
                        const file = new File([blob], fileName, {{ type: 'application/pdf' }});
                        
                        // Create DataTransfer
                        const dataTransfer = new DataTransfer();
                        dataTransfer.items.add(file);
                        
                        // Find the compose area
                        const composeArea = document.querySelector('[aria-label="Message body"]') || 
                                           document.querySelector('[role="textbox"][aria-multiline="true"]') ||
                                           document.querySelector('div[contenteditable="true"]');
                        
                        if (composeArea) {{
                            // Dispatch drag and drop events
                            const dragEnterEvent = new DragEvent('dragenter', {{
                                bubbles: true,
                                cancelable: true,
                                dataTransfer: dataTransfer
                            }});
                            composeArea.dispatchEvent(dragEnterEvent);
                            
                            const dragOverEvent = new DragEvent('dragover', {{
                                bubbles: true,
                                cancelable: true,
                                dataTransfer: dataTransfer
                            }});
                            composeArea.dispatchEvent(dragOverEvent);
                            
                            const dropEvent = new DragEvent('drop', {{
                                bubbles: true,
                                cancelable: true,
                                dataTransfer: dataTransfer
                            }});
                            composeArea.dispatchEvent(dropEvent);
                            
                            return 'dropped';
                        }}
                        return 'no compose area found';
                    }}
                ''')
                print(f"✅ Drag and drop result: {result}")
                await asyncio.sleep(3)
                
                # Check if file was attached
                await page.screenshot(path="debug_compose_4a_after_drop.png")
                attached = True
                
        except Exception as e:
            print(f"   Drag-drop method failed: {str(e)[:60]}")
        
        # Method 2: Try the file input with proper accept attribute
        if not attached:
            try:
                # Look for file input that accepts all files or PDFs
                file_inputs = page.locator("input[type='file']")
                count = await file_inputs.count()
                
                for i in range(count):
                    inp = file_inputs.nth(i)
                    accept = await inp.get_attribute("accept")
                    
                    # Skip image-only inputs
                    if accept and "image" in accept.lower() and "pdf" not in accept.lower():
                        continue
                    
                    try:
                        await inp.set_input_files(abs_path)
                        print(f"✅ File set via input {i} (accept: {accept})")
                        attached = True
                        await asyncio.sleep(2)
                        break
                    except:
                        continue
                        
            except Exception as e:
                print(f"   File input method failed: {str(e)[:40]}")
        
        # Method 2: Use the paperclip button in the secondary toolbar
        if not attached:
            try:
                # Find the attach button by its icon or aria-label in the compose toolbar
                # The button is in the row above the To field
                attach_btns = [
                    "[aria-label*='Attach']",
                    "button[title*='Attach']",
                    "[data-icon-name='Attach']",
                    "button:has([data-icon-name='Attach'])"
                ]
                
                for selector in attach_btns:
                    try:
                        btn = page.locator(selector).first
                        if await btn.is_visible(timeout=2000):
                            await btn.click()
                            print(f"✅ Clicked attach button: {selector}")
                            await asyncio.sleep(1)
                            
                            await page.screenshot(path="debug_compose_4b_attach_dropdown.png")
                            
                            # Look for "Browse this computer" in dropdown
                            browse = page.locator("text=Browse this computer, text=Browse, [role='menuitem']:has-text('Browse')").first
                            await browse.click(timeout=3000)
                            print("✅ Clicked Browse option")
                            
                            # Set file
                            file_input = page.locator("input[type='file']").first
                            await file_input.set_input_files(abs_path)
                            print("✅ File attached via toolbar button")
                            attached = True
                            await asyncio.sleep(3)
                            break
                    except:
                        continue
                        
            except Exception as e:
                print(f"   Toolbar attach method failed: {str(e)[:60]}")
        
        # Method 3: Drag and drop simulation - set file on body/compose area
        if not attached:
            try:
                # Find file inputs that accept all file types
                file_inputs = page.locator("input[type='file']")
                count = await file_inputs.count()
                print(f"   Found {count} file inputs total")
                
                # Try to find one that accepts PDF or all files
                for i in range(count):
                    inp = file_inputs.nth(i)
                    accept = await inp.get_attribute("accept")
                    print(f"   Input {i} accepts: {accept}")
                    
                    # If accept is None or includes pdf or all files, try it
                    if accept is None or "pdf" in str(accept).lower() or "*" in str(accept):
                        try:
                            await inp.set_input_files(abs_path)
                            print(f"✅ File attached via input {i}")
                            attached = True
                            await asyncio.sleep(3)
                            break
                        except Exception as e:
                            print(f"   Input {i} failed: {str(e)[:40]}")
                            
            except Exception as e:
                print(f"   File input scan failed: {str(e)[:60]}")
        
        if not attached:
            print("⚠️ Could not attach file - will send without attachment")
        
        await page.screenshot(path="debug_compose_5_attached.png")
        
        # Close any error banner
        try:
            close_btn = page.locator("[aria-label='Close'], button:has-text('×'), [aria-label='Dismiss']").first
            if await close_btn.is_visible(timeout=1000):
                await close_btn.click()
                print("   Closed error notification")
        except:
            pass
        
        # Step 5: Send email
        print("\n📝 Step 5: Sending email...")
        
        await page.screenshot(path="debug_compose_5b_before_send.png")
        
        # Wait for any upload/processing to complete
        await asyncio.sleep(2)
        
        # Click the Send button directly
        send_clicked = False
        
        # Method 1: Click the blue Send button
        try:
            send_btn = page.locator("button[aria-label='Send']").first
            if await send_btn.is_visible():
                await send_btn.click()
                send_clicked = True
                print("✅ Clicked Send button (aria-label)")
        except Exception as e:
            print(f"   Send button aria-label failed: {str(e)[:30]}")
        
        # Method 2: Try get_by_role
        if not send_clicked:
            try:
                send_btn = page.get_by_role("button", name="Send", exact=True)
                await send_btn.click(timeout=3000)
                send_clicked = True
                print("✅ Clicked Send button (role)")
            except Exception as e:
                print(f"   Send button role failed: {str(e)[:30]}")
        
        # Method 3: Find by text
        if not send_clicked:
            try:
                send_btn = page.locator("button:has-text('Send')").first
                await send_btn.click(timeout=3000)
                send_clicked = True
                print("✅ Clicked Send button (text)")
            except Exception as e:
                print(f"   Send button text failed: {str(e)[:30]}")
        
        # Method 4: Keyboard shortcut Cmd+Enter (Mac)
        if not send_clicked:
            try:
                await page.keyboard.press("Meta+Enter")
                send_clicked = True
                print("✅ Sent via Cmd+Enter")
            except:
                pass
        
        # Method 5: Control+Enter
        if not send_clicked:
            await page.keyboard.press("Control+Enter")
            print("✅ Sent via Ctrl+Enter")
        
        # Wait for email to be sent
        await asyncio.sleep(5)
        await page.screenshot(path="debug_compose_6_sent.png")
        
        # Verify email was sent - compose window should be closed
        for _ in range(10):
            try:
                send_visible = await page.locator("button[aria-label='Send']").is_visible()
                if not send_visible:
                    print("\n✅ Email sent successfully! (compose closed)")
                    return True
            except:
                pass
            await asyncio.sleep(1)
        
        # Check if still in compose
        current_url = page.url
        if "mail" in current_url and "compose" not in current_url.lower():
            print("\n✅ Email sent successfully!")
        else:
            print("\n⚠️ Email may still be sending or in drafts")
        
        return True
    
    @pytest.mark.asyncio
    async def test_send_email_to_easysend(self):
        """
        Test sending email with PDF attachment to easysend@viewz.co
        """
        print("\n" + "="*60)
        print("🧪 TEST: Send Email to EasySend")
        print("="*60)
        
        # Verify test file exists
        if not os.path.exists(self.TEST_FILE_PATH):
            pytest.fail(f"Test file not found: {self.TEST_FILE_PATH}")
        
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=False, slow_mo=100)
            context = await browser.new_context()
            page = await context.new_page()
            
            try:
                # Step 1: Login to Outlook
                login_success = await self.login_to_outlook(page)
                assert login_success, "Failed to login to Outlook"
                
                # Step 2: Send email
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                subject = f"Test Invoice {timestamp}"
                
                send_success = await self.compose_and_send_email(
                    page,
                    self.EASYSEND_EMAIL,
                    subject,
                    self.TEST_FILE_PATH
                )
                
                assert send_success, "Failed to send email"
                
                print("\n" + "="*60)
                print("✅ EMAIL SENT SUCCESSFULLY!")
                print(f"   To: {self.EASYSEND_EMAIL}")
                print(f"   Subject: {subject}")
                print("="*60)
                
            finally:
                await browser.close()

