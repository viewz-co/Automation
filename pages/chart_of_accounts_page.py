"""
Chart of Accounts Page Object
UPDATED FLOW (Feb 2026 - Inline Edit with Tab Navigation):
Columns: Account ID, Name, Currency, Report Type, Type, Group, EBITDA, Cashflow, Budget, IC, Tag 1, Tag 2, Actions

New UI Flow:
1. Click "Add GL Account" → Creates inline row with "Auto-generated" in Account ID
2. Name input is focused - type account name
3. Press Tab to navigate through fields (dropdowns auto-open)
4. Press Enter OR click save button (green) to save
5. Press Escape to cancel

Instruction shown: "Press Tab or Enter to save • Escape to cancel"
"""

from playwright.async_api import Page
import asyncio
import random
import string
from datetime import datetime


class ChartOfAccountsPage:
    
    def __init__(self, page: Page):
        self.page = page
        self.base_url = None
        self.chart_of_accounts_path = "/ledger/chart-of-accounts"
        
        # Selectors for tests
        self.add_gl_button_selectors = [
            "button:has-text('Add GL Account')",
            "button:has-text('Add Account')",
            "[data-testid='add-gl-account']"
        ]
        self.new_row_selector = "tr:has-text('Auto-generated'), tr:has-text('Auto')"
        self.cancel_button_selector = "button:has-text('Cancel'), button[aria-label='Cancel'], button.cancel"
    
    async def is_loaded(self):
        """Check if Chart of Accounts page is loaded"""
        try:
            return self.chart_of_accounts_path in self.page.url
        except:
            return False

    async def navigate_to_chart_of_accounts(self, base_url: str = None):
        """Navigate to Chart of Accounts page"""
        try:
            if base_url:
                self.base_url = base_url
            url = f"{self.base_url}{self.chart_of_accounts_path}"
            print(f"📊 Navigating to: {url}")
            await self.page.goto(url)
            await asyncio.sleep(2)
            return self.chart_of_accounts_path in self.page.url
        except Exception as e:
            print(f"❌ Navigation error: {e}")
            return False

    async def is_loaded(self):
        """Check if Chart of Accounts page is loaded"""
        try:
            if self.chart_of_accounts_path in self.page.url:
                return True
            # Also check for page title/heading
            heading = self.page.locator("text=Chart of Accounts")
            return await heading.is_visible()
        except:
            return False

    async def click_add_gl_account(self):
        """Click Add GL Account button"""
        try:
            # Try multiple selectors
            for selector in self.add_gl_button_selectors:
                btn = self.page.locator(selector).first
                if await btn.is_visible():
                    await btn.click()
                    await asyncio.sleep(1.5)
                    print(f"✅ Clicked Add GL Account: {selector}")
                    return True
            
            # Fallback: try button with + icon
            btn = self.page.locator("button:has-text('+'), button[aria-label*='Add']").first
            if await btn.is_visible():
                await btn.click()
                await asyncio.sleep(1.5)
                print("✅ Clicked Add button (fallback)")
                return True
                
            print("❌ Could not find Add GL Account button")
            return False
        except Exception as e:
            print(f"❌ Error clicking Add: {e}")
            return False

    async def take_screenshot(self, name: str):
        """Take a screenshot"""
        try:
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            path = f"screenshots/gl_{name}_{ts}.png"
            await self.page.screenshot(path=path)
            print(f"📸 Screenshot: {path}")
        except Exception as e:
            print(f"⚠️ Screenshot error: {e}")

    async def _select_dropdown_option(self, option_text: str, field_name: str):
        """Select an option from an open dropdown (works with new inline edit UI)"""
        try:
            await asyncio.sleep(0.5)
            
            # Try multiple selectors for dropdown options
            selectors = [
                f"[role='option']:has-text('{option_text}')",
                f"[role='listbox'] [role='option']:has-text('{option_text}')",
                f"div[data-radix-popper-content-wrapper] >> text='{option_text}'",
                f"[cmdk-item]:has-text('{option_text}')",
                f"div[role='listbox'] >> text='{option_text}'",
            ]
            
            for selector in selectors:
                try:
                    option = self.page.locator(selector).first
                    if await option.count() > 0 and await option.is_visible():
                        await option.click()
                        print(f"      ✅ {field_name}: {option_text}")
                        await asyncio.sleep(0.3)
                        return True
                except:
                    continue
            
            # Fallback: try clicking text directly (but be more specific)
            try:
                option = self.page.locator(f"[role='option'] >> text='{option_text}'").first
                if await option.count() > 0 and await option.is_visible():
                    await option.click()
                    print(f"      ✅ {field_name}: {option_text} (role option)")
                    await asyncio.sleep(0.3)
                    return True
            except:
                pass
            
            # Try generic text match in any visible popup/dropdown
            try:
                popup_option = self.page.locator(f"[data-radix-popper-content-wrapper] >> text='{option_text}'").first
                if await popup_option.count() > 0 and await popup_option.is_visible():
                    await popup_option.click()
                    print(f"      ✅ {field_name}: {option_text} (popup)")
                    await asyncio.sleep(0.3)
                    return True
            except:
                pass
                
            print(f"      ⚠️ {field_name}: '{option_text}' not found in dropdown")
            return False
        except Exception as e:
            print(f"      ⚠️ {field_name}: {str(e)[:50]}")
            return False

    async def _find_inline_row(self):
        """Find the inline edit row (contains Auto-generated or has input)"""
        # Try multiple ways to find the new row
        selectors = [
            "tr:has-text('Auto-generated')",
            "tr:has-text('Auto')",
            "tr:has(input[placeholder*='Account'])",
            "tr:has(input[type='text'])",
        ]
        
        for selector in selectors:
            row = self.page.locator(selector).first
            if await row.count() > 0:
                return row
        return None

    async def create_gl_account(self, account_data: dict = None):
        """
        Create GL Account using new inline edit UI (Feb 2026):
        1. Click Add GL Account
        2. Fill Account Name in the input field
        3. Use Tab to navigate through dropdowns OR click save
        """
        try:
            if account_data is None:
                account_data = {}
            
            random_suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
            
            name = account_data.get('name', f"AR Account {random_suffix}")
            currency = account_data.get('currency', 'US Dollar')
            report_type = account_data.get('report_type', 'Balance Sheet')
            account_type = account_data.get('account_type', 'Current Assets')
            account_group = account_data.get('account_group', 'Trade receivables')
            cashflow = account_data.get('cashflow', 'AR')
            
            print(f"\n📝 Creating GL Account: {name}")
            await self.take_screenshot("before_add_gl")
            
            # Step 1: Click Add GL Account
            if not await self.click_add_gl_account():
                print("❌ Failed to click Add GL Account")
                return None
            
            await asyncio.sleep(1)
            await self.take_screenshot("after_add_click")
            
            # Step 2: Find the inline edit row
            row = await self._find_inline_row()
            if not row:
                print("❌ Could not find inline edit row")
                await self.take_screenshot("no_inline_row")
                return None
            
            print("   ✅ Found inline edit row")
            
            # Step 3: Fill Account Name
            print("   1️⃣ Account Name...")
            
            # Find the name input - try multiple approaches
            name_input = None
            
            # Method 1: Input with placeholder
            name_input = row.locator("input[placeholder*='Account'], input[placeholder*='Name']").first
            if not await name_input.count() > 0:
                # Method 2: First visible input in the row
                name_input = row.locator("input[type='text'], input:not([type='hidden'])").first
            if not await name_input.count() > 0:
                # Method 3: Any input in the row
                name_input = row.locator("input").first
            
            if await name_input.count() > 0:
                await name_input.click()
                await asyncio.sleep(0.2)
                await name_input.fill(name)
                print(f"      ✅ Name: {name}")
            else:
                # Try typing directly (input might be auto-focused)
                await self.page.keyboard.type(name)
                print(f"      ✅ Name (typed): {name}")
            
            await asyncio.sleep(0.5)
            
            # Step 4: Navigate through fields by clicking cells and selecting from dropdowns
            # Column order: Account ID(0), Name(1), Currency(2), Report Type(3), Type(4), Group(5), EBITDA(6), Cashflow(7), Budget(8)...
            
            row = await self._find_inline_row()
            if not row:
                print("   ❌ Lost reference to inline row")
                return None
            
            cells = row.locator("td")
            cell_count = await cells.count()
            print(f"   📊 Found {cell_count} cells in row")
            
            # Currency (cell 2)
            print("   2️⃣ Currency...")
            await cells.nth(2).click()
            await asyncio.sleep(0.8)
            if not await self._select_dropdown_option(currency, "Currency"):
                # Try Tab fallback
                await self.page.keyboard.press("Tab")
                await asyncio.sleep(0.3)
            
            # Report Type (cell 3) - usually auto-opens after currency selection
            print("   3️⃣ Report Type...")
            await asyncio.sleep(0.5)
            # Just try to select - dropdown should be open after currency
            if not await self._select_dropdown_option(report_type, "Report Type"):
                # If not found, click cell to open dropdown
                row = await self._find_inline_row()
                if row:
                    await row.locator("td").nth(3).click()
                    await asyncio.sleep(0.5)
                    await self._select_dropdown_option(report_type, "Report Type")
            
            # Type (cell 4) - usually auto-opens after report type
            print("   4️⃣ Type...")
            await asyncio.sleep(0.5)
            if not await self._select_dropdown_option(account_type, "Type"):
                row = await self._find_inline_row()
                if row:
                    await row.locator("td").nth(4).click()
                    await asyncio.sleep(0.5)
                    await self._select_dropdown_option(account_type, "Type")
            
            # Group (cell 5) - usually auto-opens after type
            print("   5️⃣ Group...")
            await asyncio.sleep(0.5)
            if not await self._select_dropdown_option(account_group, "Group"):
                row = await self._find_inline_row()
                if row:
                    await row.locator("td").nth(5).click()
                    await asyncio.sleep(0.5)
                    await self._select_dropdown_option(account_group, "Group")
            
            # EBITDA (cell 6) - usually auto-selected based on Type
            print("   6️⃣ EBITDA: auto ✅")
            await asyncio.sleep(0.3)
            
            # Close any open dropdown before proceeding
            await self.page.keyboard.press("Escape")
            await asyncio.sleep(0.3)
            
            # Cashflow (cell 7)
            print("   7️⃣ Cashflow...")
            row = await self._find_inline_row()
            if row:
                try:
                    # Use force to bypass any intercepting elements
                    await row.locator("td").nth(7).click(force=True, timeout=5000)
                    await asyncio.sleep(0.8)
                    await self._select_dropdown_option(cashflow, "Cashflow")
                except Exception as e:
                    print(f"      ⚠️ Could not click Cashflow cell: {str(e)[:30]}")
                    # Try pressing Tab to get to Cashflow
                    await self.page.keyboard.press("Tab")
                    await asyncio.sleep(0.5)
                    await self._select_dropdown_option(cashflow, "Cashflow")
            
            # Step 5: Save the account
            print("   8️⃣ Save...")
            await asyncio.sleep(0.5)
            
            # Close any open dropdown first
            await self.page.keyboard.press("Escape")
            await asyncio.sleep(0.3)
            
            await self.take_screenshot("before_save")
            
            save_success = False
            
            # Method 1: Find and click the green save button in the last cell
            row = await self._find_inline_row()
            if row:
                cells = row.locator("td")
                last_cell = cells.last
                
                # Look for buttons in the last cell (action column)
                action_buttons = last_cell.locator("button")
                btn_count = await action_buttons.count()
                print(f"      Found {btn_count} buttons in action column")
                
                if btn_count >= 1:
                    # First button is usually save (green checkmark)
                    try:
                        save_btn = action_buttons.first
                        await save_btn.click(timeout=5000, force=True)
                        save_success = True
                        print("      ✅ Clicked first action button (save)")
                    except Exception as e:
                        print(f"      ⚠️ Could not click save button: {str(e)[:30]}")
                
                # Also try looking for specific button styles
                if not save_success:
                    save_selectors = [
                        "button.bg-green-500, button.bg-emerald-500",
                        "button[class*='text-green'], button[class*='text-emerald']",
                        "button:has(svg[stroke='currentColor'])",
                    ]
                    for selector in save_selectors:
                        try:
                            btn = row.locator(selector).first
                            if await btn.count() > 0:
                                await btn.click(timeout=3000, force=True)
                                save_success = True
                                print(f"      ✅ Clicked save button: {selector}")
                                break
                        except:
                            continue
            
            # Method 2: Press Tab to submit (as per UI instruction "Press Tab or Enter to save")
            if not save_success:
                print("      Trying Tab key to save...")
                await self.page.keyboard.press("Tab")
                await asyncio.sleep(1)
                save_success = True
                print("      ✅ Pressed Tab to save")
            
            # Method 3: Press Enter to save (fallback)
            row_check = await self._find_inline_row()
            if row_check:
                print("      Row still in edit mode, trying Enter...")
                await self.page.keyboard.press("Enter")
                await asyncio.sleep(1)
            
            await asyncio.sleep(2)
            await self.take_screenshot("after_save")
            
            # Verify: Check if the inline row is gone (account saved)
            remaining_auto_rows = await self.page.locator("tr:has-text('Auto-generated')").count()
            
            if remaining_auto_rows == 0:
                print(f"✅ GL Account created successfully: {name}")
                return {
                    'name': name,
                    'currency': currency,
                    'report_type': report_type,
                    'account_type': account_type,
                    'account_group': account_group,
                    'cashflow': cashflow,
                    'created_at': datetime.now().isoformat()
                }
            else:
                # Check if there's an error message
                error_msg = self.page.locator("text=error, text=failed, text=invalid").first
                if await error_msg.is_visible():
                    print(f"   ❌ Error message visible")
                    await self.take_screenshot("save_error")
                else:
                    print("   ⚠️ Row still in edit mode - may need manual save")
                    
                    # Try one more time with Enter
                    await self.page.keyboard.press("Enter")
                    await asyncio.sleep(2)
                    
                    remaining = await self.page.locator("tr:has-text('Auto-generated')").count()
                    if remaining == 0:
                        print(f"✅ GL Account created (after retry): {name}")
                        return {
                            'name': name,
                            'currency': currency,
                            'report_type': report_type,
                            'account_type': account_type,
                            'account_group': account_group,
                            'cashflow': cashflow,
                            'created_at': datetime.now().isoformat()
                        }
                
                await self.take_screenshot("not_saved")
                return None
                
        except Exception as e:
            print(f"❌ Error creating GL Account: {e}")
            await self.take_screenshot("error")
            return None

    async def create_ar_account_for_invoicing(self, account_name: str = None):
        """Create AR account for Invoicing precondition"""
        random_suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        return await self.create_gl_account({
            'name': account_name or f"AR Invoicing {random_suffix}",
            'currency': 'US Dollar',
            'report_type': 'Balance Sheet',
            'account_type': 'Current Assets',
            'account_group': 'Trade receivables',
            'cashflow': 'AR'
        })

    async def verify_account_exists(self, account_name: str):
        """Verify an account exists by searching"""
        try:
            # Try multiple search input selectors
            search_selectors = [
                "input[placeholder*='Search']",
                "input[placeholder*='search']",
                "input[type='search']",
                "[data-testid='search-input']",
            ]
            
            for selector in search_selectors:
                search = self.page.locator(selector).first
                if await search.is_visible():
                    await search.clear()
                    await search.fill(account_name)
                    await asyncio.sleep(2)
                    
                    # Check if account appears in results
                    account_row = self.page.locator(f"tr:has-text('{account_name}')")
                    if await account_row.count() > 0:
                        print(f"✅ Account found: {account_name}")
                        return True
                    break
            
            # Fallback: just check if account name exists anywhere on page
            if await self.page.locator(f"text='{account_name}'").is_visible():
                print(f"✅ Account visible: {account_name}")
                return True
                
            print(f"⚠️ Account not found: {account_name}")
            return False
        except Exception as e:
            print(f"⚠️ Search error: {e}")
            return False
    
    async def create_gl_account_simple(self, name: str = None):
        """
        Simplified GL Account creation - just name and save
        For quick tests where we only need a basic account
        """
        try:
            if not name:
                random_suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
                name = f"Test Account {random_suffix}"
            
            print(f"\n📝 Creating GL Account (simple): {name}")
            
            # Click Add
            if not await self.click_add_gl_account():
                return None
            
            await asyncio.sleep(1)
            
            # Find and fill name input
            name_input = self.page.locator("tr:has-text('Auto') input, input[placeholder*='Account']").first
            if await name_input.count() > 0:
                await name_input.fill(name)
                print(f"   ✅ Name: {name}")
            else:
                await self.page.keyboard.type(name)
                print(f"   ✅ Name (typed): {name}")
            
            # Just press Enter to save with defaults
            await asyncio.sleep(0.5)
            await self.page.keyboard.press("Enter")
            await asyncio.sleep(2)
            
            # Verify saved
            if await self.page.locator("tr:has-text('Auto-generated')").count() == 0:
                print(f"✅ GL Account created: {name}")
                return {'name': name, 'created_at': datetime.now().isoformat()}
            
            return None
        except Exception as e:
            print(f"❌ Error: {e}")
            return None
