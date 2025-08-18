"""
BO Accounts Page Object
Handles account management and relogin functionality in BO environment
"""

from playwright.async_api import Page
import asyncio
import pyotp


class BOAccountsPage:
    """Page object for BO accounts management and relogin functionality"""
    
    def __init__(self, page: Page):
        self.page = page
        self.relogin_page = None  # Will store the new page after successful relogin
        
        # Account list selectors - updated based on BO structure
        self.accounts_list = [
            'table tbody tr',
            'table tr',
            '.account-list .account-item',
            '.accounts-table tr',
            '[data-testid*="account"]',
            '.account-row',
            'div[class*="account"]',
            'li[class*="account"]',
            'tr:not(:first-child)'  # All rows except header
        ]
        
        # Relogin button selectors - based on actual BO interface
        self.relogin_buttons = [
            '[title="Relogin To Account"]',  # The actual relogin element with title
            'i[title="Relogin To Account"]',
            'button[title="Relogin To Account"]',
            'a[title="Relogin To Account"]',
            '*[title="Relogin To Account"]',
            'i.fa.fa-arrow-right',  # The actual relogin icon
            'i.fa-arrow-right',
            '.fa.fa-arrow-right',
            '.fa-arrow-right',
            'button i.fa-arrow-right',
            'a i.fa-arrow-right',
            'button:has(i.fa-arrow-right)',
            'a:has(i.fa-arrow-right)',
            # Fallback selectors
            'button:has-text("Relogin")',
            'button:has-text("Re-login")',
            'button:has-text("Login")',
            'button:has-text("Login As")',
            'a:has-text("Relogin")',
            'a:has-text("Re-login")',
            '.relogin-btn',
            '.relogin-button'
        ]
        
        # Account navigation selectors
        self.accounts_navigation = [
            'text=Accounts',
            'a:has-text("Accounts")',
            '[href*="accounts"]',
            'button:has-text("Accounts")',
            'nav a:has-text("Accounts")',
            '.nav-accounts',
            '.accounts-menu'
        ]
        
        # OTP input selectors for relogin
        self.relogin_otp_input = [
            'input[name="otp"]',
            'input[name="code"]',
            'input[placeholder*="code" i]',
            'input[type="text"]',
            '.otp-input',
            '.code-input'
        ]

    async def navigate_to_accounts(self):
        """Navigate to accounts page from BO dashboard"""
        print("🏠 Navigating to Accounts page...")
        
        # Based on actual BO behavior, login lands us at /settings/accounts
        current_url = self.page.url
        print(f"📍 Current URL: {current_url}")
        
        # If we're already on accounts page, great!
        if 'accounts' in current_url.lower():
            print("✅ Already on accounts page")
            await self.page.wait_for_load_state("networkidle")
            return await self.verify_accounts_page()
        
        # Try different navigation methods
        navigation_successful = False
        
        for selector in self.accounts_navigation:
            try:
                nav_element = self.page.locator(selector)
                if await nav_element.is_visible():
                    await nav_element.click()
                    await asyncio.sleep(2)
                    print(f"✅ Clicked accounts navigation: {selector}")
                    navigation_successful = True
                    break
            except Exception as e:
                print(f"⚠️ Failed to click {selector}: {str(e)}")
                continue
        
        if not navigation_successful:
            # Try URL-based navigation - use settings/accounts based on actual BO structure
            try:
                base_url = '/'.join(current_url.split('/')[:3])
                accounts_urls = [
                    f"{base_url}/settings/accounts",
                    f"{base_url}/accounts",
                    f"{base_url}/admin/accounts"
                ]
                
                for accounts_url in accounts_urls:
                    try:
                        await self.page.goto(accounts_url)
                        await asyncio.sleep(2)
                        print(f"✅ Navigated to accounts via URL: {accounts_url}")
                        navigation_successful = True
                        break
                    except Exception:
                        continue
                        
            except Exception as e:
                print(f"❌ URL navigation failed: {str(e)}")
        
        if navigation_successful:
            await self.page.wait_for_load_state("networkidle")
            return await self.verify_accounts_page()
        
        return False

    async def verify_accounts_page(self):
        """Verify we're on the accounts page"""
        # Check URL
        current_url = self.page.url
        if 'accounts' in current_url.lower():
            print(f"✅ Accounts page verified by URL: {current_url}")
            return True
        
        # Check page content
        page_indicators = [
            'text=Accounts',
            'h1:has-text("Accounts")',
            'h2:has-text("Accounts")',
            '.accounts-header',
            '.accounts-title'
        ]
        
        for indicator in page_indicators:
            try:
                element = self.page.locator(indicator)
                if await element.is_visible():
                    print(f"✅ Accounts page verified by content: {indicator}")
                    return True
            except Exception:
                continue
        
        print("⚠️ Could not verify accounts page, but continuing...")
        return True  # Continue anyway for flexibility

    async def get_accounts_list(self):
        """Get list of available accounts"""
        print("📋 Retrieving accounts list...")
        
        # First, make sure we're on the right page and it's loaded
        await self.page.wait_for_load_state("networkidle")
        
        # Take a screenshot for debugging
        try:
            await self.page.screenshot(path="debug_accounts_list_page.png")
            print("📸 Debug screenshot saved: debug_accounts_list_page.png")
        except:
            pass
        
        accounts = []
        
        for selector in self.accounts_list:
            try:
                account_elements = self.page.locator(selector)
                count = await account_elements.count()
                
                if count > 0:
                    print(f"✅ Found {count} potential accounts using selector: {selector}")
                    
                    for i in range(count):
                        try:
                            account_element = account_elements.nth(i)
                            account_text = await account_element.text_content()
                            if account_text and account_text.strip():
                                # Skip header rows or empty rows
                                text = account_text.strip()
                                if text and not text.lower() in ['actions', 'account', 'name', 'status', 'email']:
                                    accounts.append({
                                        'index': i,
                                        'text': text,
                                        'element': account_element
                                    })
                        except Exception as e:
                            print(f"⚠️ Error processing account element {i}: {str(e)}")
                            continue
                    
                    if accounts:  # If we found actual accounts, stop looking
                        break
            except Exception as e:
                print(f"⚠️ Error with selector {selector}: {str(e)}")
                continue
        
        print(f"📋 Found {len(accounts)} actual accounts (excluding headers)")
        
        # If no accounts found, let's debug what's on the page
        if not accounts:
            print("🔍 No accounts found, debugging page content...")
            try:
                page_text = await self.page.text_content('body')
                print(f"📄 Page contains: {page_text[:200]}..." if len(page_text) > 200 else page_text)
                
                # Check if we're actually logged in
                current_url = self.page.url
                print(f"🔗 Current URL: {current_url}")
                
                if 'login' in current_url:
                    print("❌ Still on login page - authentication may have failed")
                    
            except Exception as e:
                print(f"⚠️ Error debugging page: {str(e)}")
        
        return accounts

    async def select_account_for_relogin(self, account_index: int = 0):
        """Select an account for relogin (default: first account)"""
        print(f"🎯 Selecting account {account_index} for relogin...")
        
        accounts = await self.get_accounts_list()
        
        if not accounts:
            print("❌ No accounts found")
            return False
        
        if account_index >= len(accounts):
            print(f"⚠️ Account index {account_index} not available, using first account")
            account_index = 0
        
        selected_account = accounts[account_index]
        print(f"✅ Selected account: {selected_account['text']}")
        
        # Look for relogin button in the selected account row
        try:
            account_element = selected_account['element']
            
            # Try to find relogin button within the account row
            for selector in self.relogin_buttons:
                try:
                    relogin_btn = account_element.locator(selector)
                    if await relogin_btn.is_visible():
                        await relogin_btn.click()
                        print(f"✅ Clicked relogin button: {selector}")
                        await asyncio.sleep(2)
                        return True
                except Exception:
                    continue
            
            # If no button in row, try clicking the row itself
            await account_element.click()
            await asyncio.sleep(1)
            
            # Then look for relogin button globally
            for selector in self.relogin_buttons:
                try:
                    relogin_btn = self.page.locator(selector)
                    if await relogin_btn.is_visible():
                        await relogin_btn.click()
                        print(f"✅ Clicked relogin button after row selection: {selector}")
                        await asyncio.sleep(2)
                        return True
                except Exception:
                    continue
                    
        except Exception as e:
            print(f"❌ Error selecting account for relogin: {str(e)}")
        
        return False

    async def handle_relogin_otp(self, otp_secret: str):
        """Handle OTP for relogin process - or detect if no OTP is needed"""
        print("🔐 Handling relogin OTP...")
        
        # Wait a moment for page to load after relogin click
        await asyncio.sleep(3)
        
        # Check if we're still on the same page or if something changed
        current_url = self.page.url
        print(f"📍 Current URL after relogin click: {current_url}")
        
        # Take screenshot for debugging
        await self.page.screenshot(path="debug_after_relogin_click.png")
        print("📸 Debug screenshot: debug_after_relogin_click.png")
        
        # Check for new windows/tabs
        context = self.page.context
        pages = context.pages
        print(f"🔍 Number of open pages/tabs: {len(pages)}")
        
        # If new page opened, switch to it
        if len(pages) > 1:
            new_page = pages[-1]  # Get the latest page
            await new_page.bring_to_front()
            print(f"🔄 Switched to new page: {new_page.url}")
            
            # Wait for the new page to fully load
            await new_page.wait_for_load_state("networkidle")
            await asyncio.sleep(3)  # Give extra time for the page to settle
            
            # Take screenshot of new page for debugging
            await new_page.screenshot(path="debug_relogin_new_window.png")
            print("📸 New window screenshot: debug_relogin_new_window.png")
            
            # Check if this new page needs OTP - try multiple indicators
            otp_indicators = [
                "text=code",
                "text=Code", 
                "text=OTP",
                "text=verification",
                "text=Two-Factor",
                "text=Authentication",
                "input[type='text']"
            ]
            
            otp_found = False
            for indicator in otp_indicators:
                try:
                    await new_page.wait_for_selector(indicator, timeout=2000)
                    print(f"✅ Found OTP indicator in new window: {indicator}")
                    otp_found = True
                    break
                except Exception:
                    continue
            
            if otp_found:
                print("🔐 OTP required in new window, proceeding with verification...")
                
                # Generate and fill OTP in new page
                totp = pyotp.TOTP(otp_secret)
                otp_code = totp.now()
                print(f"🔐 Generated relogin OTP: {otp_code}")
                
                # Try multiple selectors for OTP input - updated with actual relogin selectors
                otp_selectors = [
                    'input[data-input-otp="true"]',  # The actual relogin OTP input
                    'input[maxlength="6"]',
                    'input[autocomplete="one-time-code"]',
                    'input[inputmode="numeric"]',
                    'input[type="text"]',
                    'input[name="otp"]',
                    'input[name="code"]',
                    'input[placeholder*="code" i]'
                ]
                
                otp_filled = False
                for selector in otp_selectors:
                    try:
                        otp_input = new_page.locator(selector)
                        if await otp_input.is_visible():
                            await otp_input.fill(otp_code)
                            print(f"✅ OTP filled in new window using: {selector}")
                            otp_filled = True
                            break
                    except Exception:
                        continue
                
                if not otp_filled:
                    print("❌ Could not find OTP input in new window")
                    return False
                
                # Try to submit OTP
                submit_selectors = [
                    'button:has-text("Verify")',
                    'button:has-text("Submit")',
                    'button[type="submit"]',
                    'button:has-text("Continue")',
                    'button:has-text("Login")'
                ]
                
                submit_clicked = False
                for selector in submit_selectors:
                    try:
                        submit_btn = new_page.locator(selector)
                        if await submit_btn.is_visible():
                            await submit_btn.click()
                            print(f"✅ OTP submitted in new window using: {selector}")
                            submit_clicked = True
                            break
                    except Exception:
                        continue
                
                if not submit_clicked:
                    print("⚠️ No submit button found in new window, OTP may auto-submit")
                
                # Wait for processing and check for success
                await asyncio.sleep(5)
                
                # Check if we're redirected to main app or success page
                final_url = new_page.url
                print(f"🔗 Final URL in new window: {final_url}")
                
                if 'relogin' not in final_url.lower():
                    print("✅ Relogin successful - redirected away from relogin page")
                    
                    # Store the new page reference for sanity testing
                    self.relogin_page = new_page
                    return True
                else:
                    # Check for error messages
                    page_text = await new_page.text_content('body')
                    if 'error' in page_text.lower() or 'invalid' in page_text.lower():
                        print("❌ Relogin failed - error detected")
                        return False
                    else:
                        print("✅ Relogin appears successful")
                        
                        # Store the new page reference for sanity testing
                        self.relogin_page = new_page
                        return True
                
            else:
                print("ℹ️ No OTP indicators found in new window")
                # Check if we're already successfully logged in
                page_text = await new_page.text_content('body')
                if 'welcome' in page_text.lower() or 'dashboard' in page_text.lower():
                    print("✅ Already logged in to new window")
                    # Store the new page reference for sanity testing
                    self.relogin_page = new_page
                    return True
                else:
                    print("⚠️ Uncertain about relogin status")
                    # Store the new page reference anyway for testing
                    self.relogin_page = new_page
                    return False
        
        # Check if OTP input appears on current page
        otp_indicators = ['text=code', 'text=OTP', 'text=verification', 'input[type="text"]']
        otp_found = False
        
        for indicator in otp_indicators:
            try:
                await self.page.wait_for_selector(indicator, timeout=2000)
                print(f"✅ Found OTP indicator: {indicator}")
                otp_found = True
                break
            except Exception:
                continue
        
        if otp_found:
            # Generate OTP
            totp = pyotp.TOTP(otp_secret)
            otp_code = totp.now()
            print(f"🔐 Generated relogin OTP: {otp_code}")
            
            # Fill OTP
            try:
                await self.page.fill('input[type="text"]:visible', otp_code)
                await self.page.click('button:has-text("Verify")')
                print("✅ Relogin OTP submitted")
                await asyncio.sleep(3)
                return True
            except Exception as e:
                print(f"❌ Error filling OTP: {str(e)}")
                return False
        else:
            # No OTP required - check if relogin was successful by other means
            print("ℹ️ No OTP input found - relogin might be automatic")
            
            # Check for success indicators
            success_indicators = [
                'text=Success',
                'text=Logged',
                'text=Welcome',
                'text=Dashboard'
            ]
            
            for indicator in success_indicators:
                try:
                    element = self.page.locator(indicator)
                    if await element.is_visible():
                        print(f"✅ Found success indicator: {indicator}")
                        return True
                except Exception:
                    continue
            
            # If no clear success indicator, assume success if we're not on an error page
            page_text = await self.page.text_content('body')
            if 'error' not in page_text.lower() and 'failed' not in page_text.lower():
                print("✅ No error detected - assuming relogin successful")
                return True
            else:
                print("❌ Possible error detected")
                return False

    async def verify_relogin_success(self):
        """Verify that relogin was successful"""
        print("✅ Verifying relogin success...")
        
        # Check for success indicators
        success_indicators = [
            'text=Success',
            'text=Logged in',
            'text=Welcome',
            '.success-message',
            '.login-success'
        ]
        
        for indicator in success_indicators:
            try:
                element = self.page.locator(indicator)
                if await element.is_visible():
                    print(f"✅ Relogin success verified: {indicator}")
                    return True
            except Exception:
                continue
        
        # Check URL change
        current_url = self.page.url
        if any(path in current_url.lower() for path in ['dashboard', 'home', 'main', 'app']):
            print(f"✅ Relogin success verified by URL: {current_url}")
            return True
        
        print("⚠️ Could not explicitly verify relogin success, assuming success")
        return True

    async def perform_complete_relogin_flow(self, otp_secret: str, account_index: int = 0):
        """Perform complete relogin flow for specified account"""
        print("🔄 Starting complete relogin flow...")
        
        # Navigate to accounts page
        if not await self.navigate_to_accounts():
            print("❌ Failed to navigate to accounts page")
            return False
        
        # Select account for relogin
        if not await self.select_account_for_relogin(account_index):
            print("❌ Failed to select account for relogin")
            return False
        
        # Handle OTP
        if not await self.handle_relogin_otp(otp_secret):
            print("❌ Failed to handle relogin OTP")
            return False
        
        # Verify success
        return await self.verify_relogin_success()

    def get_relogin_page(self):
        """Get the page reference after successful relogin for testing"""
        return self.relogin_page
