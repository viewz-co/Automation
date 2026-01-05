"""
Budgeting Page Object Model
Handles Budget Group creation and Budget Builder operations
"""
import asyncio
import random
import string
from datetime import datetime
from playwright.async_api import Page


class BudgetingPage:
    def __init__(self, page: Page):
        self.page = page
        self.heading = 'Budgeting'
        self.base_url = "https://app.stage.viewz.co/budgeting"
    
    async def is_loaded(self) -> bool:
        """Check if the Budgeting page is loaded"""
        try:
            # Try heading first
            locator = self.page.get_by_role('heading', name=self.heading)
            await locator.wait_for(timeout=10000)
            return await locator.is_visible()
        except:
            # Fallback: check URL
            return 'budget' in self.page.url.lower()
    
    async def navigate_to_budgeting(self, entity_id: int = 1):
        """Navigate to the Budgeting page via sidebar menu"""
        try:
            # First try direct URL navigation
            url = f"{self.base_url}?entityId={entity_id}"
            await self.page.goto(url)
            await self.page.wait_for_load_state("networkidle")
            await asyncio.sleep(2)
            
            # Check if we're on budgeting page
            if 'budget' in self.page.url.lower():
                print(f"📍 Navigated to Budgeting via URL: {self.page.url}")
                return
            
            # If URL didn't work, use sidebar menu
            print("📍 Using sidebar menu to navigate to Budgeting...")
            
            # Hover over logo to expand menu
            logo = self.page.locator("svg.viewz-logo, [class*='logo']").first
            if await logo.count() > 0:
                box = await logo.bounding_box()
                if box:
                    await self.page.mouse.move(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)
                    await asyncio.sleep(1)
            
            # Pin menu if possible
            pin_button = self.page.locator("button:has(svg.lucide-pin)")
            if await pin_button.count() > 0 and await pin_button.is_visible():
                await pin_button.click()
                await asyncio.sleep(0.5)
            
            # Click Budgeting in sidebar
            budgeting_link = self.page.locator("text=Budgeting").first
            if await budgeting_link.count() > 0:
                await budgeting_link.click()
                await asyncio.sleep(2)
                print(f"📍 Navigated to Budgeting via sidebar: {self.page.url}")
            else:
                print("⚠️ Budgeting link not found in sidebar")
                
        except Exception as e:
            print(f"⚠️ Navigation error: {e}")
    
    async def take_screenshot(self, name: str):
        """Take a screenshot for debugging"""
        filename = f"debug_budgeting_{name}_{datetime.now().strftime('%H%M%S')}.png"
        await self.page.screenshot(path=filename)
        print(f"📸 Screenshot: {filename}")
        return filename
    
    # ==========================================
    # BUDGET GROUP OPERATIONS
    # ==========================================
    
    async def click_add_budget_group(self) -> bool:
        """Click the Add Budget Group button"""
        try:
            # Try different selectors for the add button
            add_selectors = [
                "button:has-text('Add Budget Group')",
                "button:has-text('Add Group')",
                "button:has-text('New Budget')",
                "button:has-text('Add')",
                "[data-testid='add-budget-group']",
            ]
            
            for selector in add_selectors:
                btn = self.page.locator(selector).first
                if await btn.count() > 0 and await btn.is_visible():
                    await btn.click()
                    print(f"✅ Clicked: {selector}")
                    await asyncio.sleep(1)
                    return True
            
            # Try clicking a + button
            plus_btn = self.page.locator("button:has(svg), button:has-text('+')").first
            if await plus_btn.count() > 0:
                await plus_btn.click()
                print("✅ Clicked + button")
                await asyncio.sleep(1)
                return True
                
            print("❌ Add Budget Group button not found")
            await self.take_screenshot("no_add_button")
            return False
            
        except Exception as e:
            print(f"❌ Error clicking Add Budget Group: {e}")
            return False
    
    async def fill_budget_group_form(self, budget_id: str = None, group_name: str = None) -> dict:
        """
        Fill the budget group creation form
        Form fields:
        - Budget ID (required): e.g., REV-001
        - Name (required): e.g., Revenue
        - Report Type (required): dropdown
        - Account Type (required): dropdown
        - Group (required): dropdown
        - Department, Tag 1, Cash Flow (optional): dropdowns
        """
        try:
            # Generate default values if not provided
            suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
            if not budget_id:
                budget_id = f"QA-{suffix}"
            if not group_name:
                group_name = f"QA Budget {suffix}"
            
            await asyncio.sleep(1)
            
            # 1. Fill Budget ID (first input with placeholder containing "REV" or first input)
            budget_id_input = self.page.locator("input[placeholder*='REV'], input[placeholder*='e.g']").first
            if await budget_id_input.count() > 0:
                await budget_id_input.fill(budget_id)
                print(f"✅ Budget ID: {budget_id}")
            
            # 2. Fill Name (second input or one with "Revenue" placeholder)
            name_input = self.page.locator("input[placeholder*='Revenue'], input[placeholder*='Name']").first
            if await name_input.count() > 0:
                await name_input.fill(group_name)
                print(f"✅ Name: {group_name}")
            else:
                # Try all inputs and fill the second one
                inputs = self.page.locator("input[type='text']")
                if await inputs.count() >= 2:
                    await inputs.nth(1).fill(group_name)
                    print(f"✅ Name (2nd input): {group_name}")
            
            # 3. Select Report Type (required dropdown)
            await self._select_dropdown("Report Type", "Balance Sheet")
            
            # 4. Select Account Type (required dropdown) 
            await self._select_dropdown("Account Type", "Current Assets")
            
            # 5. Select Group (required dropdown)
            await self._select_dropdown("Group", index=0)  # Select first available
            
            return {
                'budget_id': budget_id,
                'name': group_name
            }
            
        except Exception as e:
            print(f"❌ Error filling form: {e}")
            await self.take_screenshot("form_error")
            return None
    
    async def _select_dropdown(self, label: str, value: str = None, index: int = None):
        """Helper to select from a dropdown by label in a modal dialog"""
        try:
            await asyncio.sleep(0.3)
            
            # Find dropdown button by looking for "Select" text near the label
            # The modal has: Label text, then a button with "Select..." text
            dropdown_selectors = [
                f"button:has-text('Select'):near(:text('{label}'))",
                f"button:below(:text('{label}')):has-text('Select')",
                f"[role='combobox']:near(:text('{label}'))",
            ]
            
            dropdown = None
            for selector in dropdown_selectors:
                try:
                    d = self.page.locator(selector).first
                    if await d.count() > 0 and await d.is_visible():
                        dropdown = d
                        break
                except:
                    continue
            
            if not dropdown:
                # Try by position - find all Select buttons in the form
                select_buttons = self.page.locator("button:has-text('Select')")
                count = await select_buttons.count()
                
                # Map label to button index based on form layout
                label_map = {
                    "Report Type": 0,
                    "Account Type": 1, 
                    "Group": 2,
                    "Department": 3,
                    "Tag 1": 4,
                    "Cash Flow": 5,
                }
                
                idx = label_map.get(label, 0)
                if idx < count:
                    dropdown = select_buttons.nth(idx)
            
            if dropdown and await dropdown.count() > 0:
                await dropdown.click(force=True)
                await asyncio.sleep(0.5)
                
                # Find and click option
                if value:
                    option = self.page.locator(f"[role='option']:has-text('{value}'), [role='menuitem']:has-text('{value}')").first
                    if await option.count() > 0:
                        await option.click()
                        print(f"✅ {label}: {value}")
                        await asyncio.sleep(0.3)
                        return True
                
                # Select first available option
                options = self.page.locator("[role='option'], [role='menuitem']")
                option_count = await options.count()
                if option_count > 0:
                    target_idx = index if index is not None else 0
                    await options.nth(target_idx).click()
                    print(f"✅ {label}: selected option {target_idx}")
                    await asyncio.sleep(0.3)
                    return True
                else:
                    # Close dropdown by pressing Escape
                    await self.page.keyboard.press("Escape")
                    
            print(f"⚠️ {label}: dropdown not found")
            return False
            
        except Exception as e:
            print(f"⚠️ Dropdown {label}: {str(e)[:40]}")
            await self.page.keyboard.press("Escape")
            return False
    
    async def save_budget_group(self) -> bool:
        """Save the budget group by clicking Create Group button"""
        try:
            save_selectors = [
                "button:has-text('Create Group')",
                "button:has-text('Create')",
                "button:has-text('Save')",
                "button:has-text('Add')",
                "button[type='submit']",
            ]
            
            for selector in save_selectors:
                btn = self.page.locator(selector).first
                if await btn.count() > 0 and await btn.is_visible():
                    await btn.click(force=True)  # Force click to bypass overlay
                    print(f"✅ Clicked: {selector}")
                    await asyncio.sleep(2)
                    return True
            
            print("❌ Create Group button not found")
            await self.take_screenshot("no_create_button")
            return False
            
        except Exception as e:
            print(f"❌ Error saving: {e}")
            return False
    
    async def create_budget_group(self, group_name: str = None) -> dict:
        """Complete flow: Create a new budget group"""
        print("\n📝 Creating Budget Group...")
        
        # Click add button
        if not await self.click_add_budget_group():
            return None
        
        # Fill form
        group_data = await self.fill_budget_group_form(group_name)
        if not group_data:
            return None
        
        # Save
        if not await self.save_budget_group():
            return None
        
        print(f"✅ Budget Group created: {group_data['name']}")
        return group_data
    
    async def get_budget_groups(self) -> list:
        """Get list of existing budget groups"""
        try:
            groups = []
            
            # Try to find groups in table
            rows = self.page.locator("table tbody tr, [data-testid*='group'], .budget-group")
            count = await rows.count()
            
            for i in range(count):
                row = rows.nth(i)
                text = await row.text_content()
                groups.append(text.strip() if text else f"Group {i+1}")
            
            print(f"📋 Found {len(groups)} budget groups")
            return groups
            
        except Exception as e:
            print(f"⚠️ Error getting groups: {e}")
            return []
    
    async def select_budget_group(self, group_name: str) -> bool:
        """Select a budget group to open Budget Builder"""
        try:
            # Try to find and click the group
            group = self.page.locator(f"text={group_name}").first
            if await group.count() > 0:
                await group.click()
                print(f"✅ Selected budget group: {group_name}")
                await asyncio.sleep(2)
                return True
            
            # Try table row
            row = self.page.locator(f"tr:has-text('{group_name}')").first
            if await row.count() > 0:
                await row.click()
                print(f"✅ Clicked row for: {group_name}")
                await asyncio.sleep(2)
                return True
            
            print(f"❌ Budget group not found: {group_name}")
            return False
            
        except Exception as e:
            print(f"❌ Error selecting group: {e}")
            return False
    
    # ==========================================
    # BUDGET BUILDER OPERATIONS
    # ==========================================
    
    async def open_budget_builder(self, group_name: str = None) -> bool:
        """Open the Budget Builder for a group"""
        try:
            # If group name provided, select it first
            if group_name:
                await self.select_budget_group(group_name)
            
            # Look for Budget Builder button or link
            builder_selectors = [
                "button:has-text('Budget Builder')",
                "button:has-text('Builder')",
                "button:has-text('Edit Budget')",
                "a:has-text('Budget Builder')",
                "[data-testid='budget-builder']",
            ]
            
            for selector in builder_selectors:
                btn = self.page.locator(selector).first
                if await btn.count() > 0 and await btn.is_visible():
                    await btn.click()
                    print(f"✅ Opened Budget Builder: {selector}")
                    await asyncio.sleep(2)
                    return True
            
            # Check if already in builder (by looking for builder elements)
            if await self.is_builder_loaded():
                print("✅ Already in Budget Builder")
                return True
            
            print("❌ Budget Builder button not found")
            await self.take_screenshot("no_builder_button")
            return False
            
        except Exception as e:
            print(f"❌ Error opening builder: {e}")
            return False
    
    async def is_builder_loaded(self) -> bool:
        """Check if Budget Builder is loaded"""
        try:
            # Look for builder-specific elements
            builder_indicators = [
                "text=Budget Builder",
                "text=GL Account",
                "text=Amount",
                "table",
            ]
            
            for indicator in builder_indicators:
                el = self.page.locator(indicator).first
                if await el.count() > 0 and await el.is_visible():
                    return True
            
            return False
        except:
            return False
    
    async def add_budget_line(self, gl_account: str = None, amount: float = None, period: str = None) -> dict:
        """Add a budget line in the Budget Builder"""
        try:
            # Default values
            if not amount:
                amount = round(random.uniform(1000, 50000), 2)
            
            print(f"\n💰 Adding budget line: {gl_account or 'Auto'} = ${amount:,.2f}")
            
            # Click Add Line button
            add_btn = self.page.locator("button:has-text('Add'), button:has-text('New Line'), button:has-text('+')").first
            if await add_btn.count() > 0:
                await add_btn.click()
                await asyncio.sleep(1)
            
            # Fill GL Account (usually a dropdown)
            if gl_account:
                gl_input = self.page.locator("input[placeholder*='GL' i], input[placeholder*='Account' i], select").first
                if await gl_input.count() > 0:
                    await gl_input.click()
                    await asyncio.sleep(0.5)
                    # Select from dropdown
                    option = self.page.locator(f"text={gl_account}").first
                    if await option.count() > 0:
                        await option.click()
                        print(f"✅ Selected GL Account: {gl_account}")
            
            # Fill Amount
            amount_input = self.page.locator("input[type='number'], input[placeholder*='amount' i], input[placeholder*='Amount' i]").first
            if await amount_input.count() > 0:
                await amount_input.fill(str(amount))
                print(f"✅ Filled amount: ${amount:,.2f}")
            
            # Fill Period if applicable
            if period:
                period_input = self.page.locator("input[placeholder*='period' i], select[name*='period' i]").first
                if await period_input.count() > 0:
                    await period_input.fill(period)
            
            return {
                'gl_account': gl_account,
                'amount': amount,
                'period': period
            }
            
        except Exception as e:
            print(f"❌ Error adding budget line: {e}")
            await self.take_screenshot("budget_line_error")
            return None
    
    async def save_budget(self) -> bool:
        """Save the budget in Budget Builder"""
        try:
            save_btn = self.page.locator("button:has-text('Save'), button:has-text('Apply'), button[type='submit']").first
            if await save_btn.count() > 0:
                await save_btn.click()
                print("✅ Budget saved")
                await asyncio.sleep(2)
                return True
            
            print("❌ Save button not found")
            return False
            
        except Exception as e:
            print(f"❌ Error saving budget: {e}")
            return False
    
    async def build_budget_for_group(self, group_name: str, budget_lines: list = None) -> bool:
        """Complete flow: Build budget for a group"""
        print(f"\n🔨 Building budget for: {group_name}")
        
        # Open builder
        if not await self.open_budget_builder(group_name):
            return False
        
        # Add budget lines
        if budget_lines:
            for line in budget_lines:
                await self.add_budget_line(
                    gl_account=line.get('gl_account'),
                    amount=line.get('amount'),
                    period=line.get('period')
                )
        else:
            # Add a default line
            await self.add_budget_line(amount=10000)
        
        # Save
        return await self.save_budget()
    
    # ==========================================
    # VERIFICATION
    # ==========================================
    
    async def verify_budget_group_exists(self, group_name: str) -> bool:
        """Verify a budget group exists in the list"""
        try:
            group = self.page.locator(f"text={group_name}").first
            exists = await group.count() > 0
            print(f"{'✅' if exists else '❌'} Budget group '{group_name}' {'exists' if exists else 'not found'}")
            return exists
        except:
            return False
    
    async def delete_budget_group(self, group_name: str) -> bool:
        """Delete a budget group (cleanup)"""
        try:
            # Find the group row
            row = self.page.locator(f"tr:has-text('{group_name}')").first
            if await row.count() == 0:
                print(f"⚠️ Group not found: {group_name}")
                return False
            
            # Find delete button in the row
            delete_btn = row.locator("button:has-text('Delete'), button:has(svg[class*='trash']), [data-testid='delete']").first
            if await delete_btn.count() > 0:
                await delete_btn.click()
                await asyncio.sleep(1)
                
                # Confirm deletion
                confirm = self.page.locator("button:has-text('Confirm'), button:has-text('Delete'), button:has-text('Yes')").first
                if await confirm.count() > 0:
                    await confirm.click()
                    print(f"✅ Deleted budget group: {group_name}")
                    await asyncio.sleep(1)
                    return True
            
            print(f"❌ Delete button not found for: {group_name}")
            return False
            
        except Exception as e:
            print(f"❌ Error deleting group: {e}")
            return False
