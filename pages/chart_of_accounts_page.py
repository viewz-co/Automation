"""
Chart of Accounts Page Object
UPDATED FLOW (Jan 2026 - new columns added):
Columns: Account ID, Name, Currency, Report Type, Type, Group, EBITDA, Cashflow, Budget, Interco., Tag 1, Tag 2, Actions

1. Name (input) - cell 1
2. Currency (click cell → dropdown auto-opens → click option) - cell 2
3. Report Type (dropdown auto-opens after currency → click option)
4. Type (dropdown auto-opens → click option)
5. Group (dropdown auto-opens → click option)
6. EBITDA (auto-selected - skip!)
7. Cashflow (click cell → dropdown auto-opens → click option) - cell 7
8. Budget (not required - skip, defaults to None)
9. Interco., Tag 1, Tag 2 (not required - skip)
10. Save
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
            btn = self.page.locator("button:has-text('Add GL Account')")
            await btn.click()
            await asyncio.sleep(1.5)
            print("✅ Clicked Add GL Account")
            return True
        except Exception as e:
            print(f"❌ Error: {e}")
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

    async def _click_option(self, option_text: str, field_name: str):
        """Click an option from the already-open dropdown"""
        try:
            await asyncio.sleep(0.5)
            
            # Try multiple selectors for options
            selectors = [
                f"[role='option']:has-text('{option_text}')",
                f"div[role='listbox'] >> text='{option_text}'",
                f"text='{option_text}'",
            ]
            
            for selector in selectors:
                option = self.page.locator(selector)
                if await option.count() > 0 and await option.first.is_visible():
                    await option.first.click()
                    print(f"      ✅ {field_name}: {option_text}")
                    await asyncio.sleep(0.5)
                    return True
            
            # If exact match not found, try partial match
            option = self.page.locator(f"text={option_text}").first
            if await option.is_visible():
                await option.click()
                print(f"      ✅ {field_name}: {option_text}")
                await asyncio.sleep(0.5)
                return True
                
            print(f"      ⚠️ {field_name}: '{option_text}' not found")
            return False
        except Exception as e:
            print(f"      ❌ {field_name}: {str(e)[:40]}")
            return False

    async def create_gl_account(self, account_data: dict = None):
        """
        Create GL Account:
        Click cell → dropdown opens → click option → repeat → save
        Note: Budget column added Jan 2026 - not required, skip it
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
            
            # Click Add GL Account
            if not await self.click_add_gl_account():
                return None
            
            row = self.page.locator("tr:has-text('Auto')").first
            cells = row.locator("td")
            
            # 1. Fill Name (cell index 1)
            print("   1️⃣ Name...")
            name_input = cells.nth(1).locator("input")
            await name_input.fill(name)
            await asyncio.sleep(0.3)
            print(f"      ✅ {name}")
            
            # 2. Currency - click cell, dropdown auto-opens, click option
            print("   2️⃣ Currency...")
            row = self.page.locator("tr:has-text('Auto')").first
            await row.locator("td").nth(2).click()
            await asyncio.sleep(1)
            # Dropdown is now open - click the option directly
            await self._click_option(currency, "Currency")
            
            # 3. Report Type - dropdown auto-opens after currency
            print("   3️⃣ Report Type...")
            await asyncio.sleep(0.5)
            await self._click_option(report_type, "Report Type")
            
            # 4. Type - dropdown auto-opens
            print("   4️⃣ Type...")
            await asyncio.sleep(0.5)
            await self._click_option(account_type, "Type")
            
            # 5. Group - dropdown auto-opens
            print("   5️⃣ Group...")
            await asyncio.sleep(0.5)
            await self._click_option(account_group, "Group")
            
            # 6. EBITDA - AUTO SELECTED
            print("   6️⃣ EBITDA: auto ✅")
            await asyncio.sleep(0.5)
            
            # 7. Cashflow - need to click the cell to open dropdown
            print("   7️⃣ Cashflow...")
            row = self.page.locator("tr:has-text('Auto')").first
            await row.locator("td").nth(7).click()
            await asyncio.sleep(1)
            await self._click_option(cashflow, "Cashflow")
            
            # 8. Budget - NOT REQUIRED, skip (added Jan 2026)
            # After Cashflow, go straight to Save - no need to skip Budget explicitly
            
            # 9. Save - click save button directly
            print("   8️⃣ Save...")
            await asyncio.sleep(0.5)
            
            save_clicked = False
            row = self.page.locator("tr:has-text('Auto')").first
            
            # Find the last cell which contains the action buttons
            cells = row.locator("td")
            last_cell = cells.last
            
            # Get buttons in the last cell - should be save (green) and delete (red)
            action_buttons = last_cell.locator("button")
            btn_count = await action_buttons.count()
            print(f"      Found {btn_count} action buttons in last cell")
            
            if btn_count >= 1:
                # First button in action cell should be save (green)
                save_btn = action_buttons.first
                await save_btn.click(timeout=5000)
                save_clicked = True
                print("      ✅ Clicked save button")
            
            if not save_clicked:
                print("      ❌ Could not find save button")
                await self.take_screenshot("no_save_button")
            
            await asyncio.sleep(3)
            
            # Verify
            auto_rows = await self.page.locator("tr:has-text('Auto-generated')").count()
            
            if auto_rows == 0:
                print(f"✅ GL Account created: {name}")
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
                print("   ⚠️ Row still in edit mode")
                await self.take_screenshot("not_saved")
                return None
                
        except Exception as e:
            print(f"❌ Error: {e}")
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
        """Verify an account exists"""
        try:
            search = self.page.locator("input[placeholder*='Search']").first
            if await search.is_visible():
                await search.fill(account_name)
                await asyncio.sleep(2)
                return await self.page.locator(f"tr:has-text('{account_name}')").is_visible()
            return False
        except:
            return False
