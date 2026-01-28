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
        # Dynamic base_url - extract from current page or use default
        current_url = page.url if hasattr(page, 'url') else ""
        if "stage.viewz.co" in current_url:
            self.base_url = "https://app.stage.viewz.co/budgeting"
        else:
            self.base_url = "https://app.viewz.co/budgeting"
    
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
            
            # If group_name is provided but budget_id is not, use group_name as budget_id too
            if group_name and not budget_id:
                budget_id = group_name
            elif not budget_id:
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
                    # Check if button is disabled
                    is_disabled = await btn.is_disabled()
                    if is_disabled:
                        print(f"⚠️ Button is disabled: {selector}")
                        await self.take_screenshot("button_disabled")
                        continue
                    
                    await btn.click(force=True)  # Force click to bypass overlay
                    print(f"✅ Clicked: {selector}")
                    
                    # Wait for modal to close or success message
                    await asyncio.sleep(3)
                    
                    # Check if there's an error message
                    error_msg = self.page.locator("text=Error, text=error, text=failed, [role='alert']")
                    if await error_msg.count() > 0:
                        error_text = await error_msg.first.text_content()
                        print(f"❌ Error message: {error_text}")
                        await self.take_screenshot("creation_error")
                        return False
                    
                    # Check if modal closed (success indicator)
                    modal = self.page.locator("[role='dialog'], .modal, [data-state='open']")
                    if await modal.count() == 0:
                        print("✅ Modal closed - creation likely succeeded")
                        return True
                    else:
                        # Modal still open - might need to click again or there's an error
                        await self.take_screenshot("modal_still_open")
                    
                    return True
            
            print("❌ Create Group button not found")
            await self.take_screenshot("no_create_button")
            return False
            
        except Exception as e:
            print(f"❌ Error saving: {e}")
            return False
    
    async def create_budget_group(self, group_name: str = None, budget_id: str = None) -> dict:
        """Complete flow: Create a new budget group"""
        print("\n📝 Creating Budget Group...")
        
        # Click add button
        if not await self.click_add_budget_group():
            return None
        
        # Fill form - pass group_name as keyword argument
        group_data = await self.fill_budget_group_form(budget_id=budget_id, group_name=group_name)
        if not group_data:
            return None
        
        # Save
        if not await self.save_budget_group():
            return None
        
        # Wait for modal to close
        await asyncio.sleep(2)
        
        # Verify modal closed - check if overlay is gone
        overlay = self.page.locator("[data-state='open'][class*='fixed inset-0']")
        if await overlay.count() > 0:
            # Try pressing Escape to close it
            await self.page.keyboard.press("Escape")
            await asyncio.sleep(1)
        
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
            # First, ensure no modal overlay is blocking
            overlay = self.page.locator("[data-state='open'][class*='fixed inset-0'], [class*='bg-black/80']")
            if await overlay.count() > 0:
                print("⏳ Waiting for modal overlay to close...")
                await self.page.keyboard.press("Escape")
                await asyncio.sleep(1)
                # Try again
                if await overlay.count() > 0:
                    # Click outside to close
                    await self.page.mouse.click(0, 0)
                    await asyncio.sleep(1)
            
            # If group name provided, select it first
            if group_name:
                await self.select_budget_group(group_name)
            
            # Look for Budget Builder button or tab link
            builder_selectors = [
                "a:has-text('Budget Builder')",  # Tab link
                "button:has-text('Budget Builder')",
                "button:has-text('Builder')",
                "button:has-text('Edit Budget')",
                "[data-testid='budget-builder']",
                "[value='budget_builder']",  # Tab value attribute
            ]
            
            for selector in builder_selectors:
                btn = self.page.locator(selector).first
                if await btn.count() > 0 and await btn.is_visible():
                    try:
                        await btn.click(timeout=5000)
                        print(f"✅ Opened Budget Builder: {selector}")
                        await asyncio.sleep(2)
                        return True
                    except Exception as click_err:
                        print(f"⚠️ Click failed for {selector}: {str(click_err)[:40]}")
                        continue
            
            # Check if already in builder (by looking for builder elements)
            if await self.is_builder_loaded():
                print("✅ Already in Budget Builder")
                return True
            
            print("❌ Budget Builder button not found")
            await self.take_screenshot("no_builder_button")
            return False
            
        except Exception as e:
            print(f"❌ Error opening builder: {e}")
            await self.take_screenshot("builder_error")
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
    
    async def add_budget_line(self, amount: float = None, gl_account_name: str = None) -> dict:
        """
        Add a budget amount in the Budget Builder.
        
        NOTE: Budget Builder shows GL Account categories (e.g., "Accrued Income", "Financing income")
        NOT the budget groups we create. Budget groups are containers/metadata.
        
        Flow:
        1. Find an existing row (by GL account name or use first expandable row)
        2. Click on Annual cell to edit
        3. Enter amount value, press Enter
        4. The monthly distribution happens automatically or via column actions
        """
        try:
            # Default values
            if not amount:
                amount = round(random.uniform(10000, 50000), 2)
            
            print(f"\n💰 Adding budget amount: ${amount:,.2f}")
            
            await asyncio.sleep(2)  # Wait for table to fully load
            
            # Table structure from screenshot:
            # [expand] | Budget Group | % | Annual | Jan | Feb | Mar | ... | Dec
            # Rows are GL account categories like "Accrued Income", "Financing income"
            
            target_row = None
            row_name = None
            
            # Find a row - either by name or just use first available row
            if gl_account_name:
                row = self.page.locator(f"tr:has-text('{gl_account_name}')").first
                if await row.count() > 0:
                    target_row = row
                    row_name = gl_account_name
                    print(f"   Found row for: {gl_account_name}")
            
            # If no specific row, find first expandable row with $0 values (editable)
            if not target_row:
                # Try to find a row that shows $0.0K (hasn't been budgeted yet)
                zero_rows = self.page.locator("tr:has-text('$0.0K')")
                if await zero_rows.count() > 0:
                    target_row = zero_rows.first
                    row_text = await target_row.text_content()
                    row_name = row_text.split()[0] if row_text else "First row"
                    print(f"   Using zero-budget row: {row_name[:30]}...")
                else:
                    # Just use first tbody row
                    target_row = self.page.locator("table tbody tr").first
                    if await target_row.count() > 0:
                        row_text = await target_row.text_content()
                        row_name = row_text.split()[0] if row_text else "First row"
                        print(f"   Using first table row: {row_name[:30]}...")
            
            if not target_row or await target_row.count() == 0:
                print("❌ No table row found")
                await self.take_screenshot("no_row_found")
                return None
            
            # Scroll row into view
            try:
                await target_row.scroll_into_view_if_needed()
            except:
                pass
            await asyncio.sleep(1)
            
            # Get all cells in this row
            cells = target_row.locator("td")
            cell_count = await cells.count()
            print(f"   Row has {cell_count} cells")
            
            # ========================================
            # STEP 1: Find and click the Annual column cell
            # ========================================
            # Based on screenshot: Budget Group | % | Annual | Jan | Feb | ...
            # Annual is at index 2 (0-indexed: 0=Budget Group, 1=%, 2=Annual)
            
            annual_cell_index = 2  # Annual column
            if cell_count > 3:
                annual_cell_index = 3  # If there's an expand button column first
            
            annual_cell = cells.nth(annual_cell_index)
            print(f"   📝 Step 1: Clicking on Annual cell (index {annual_cell_index})...")
            
            # Click to select, then double-click to edit
            await annual_cell.click()
            await asyncio.sleep(0.5)
            await annual_cell.dblclick()
            await asyncio.sleep(1)
            
            # Find any visible input (editing mode creates an input)
            input_el = self.page.locator("input:visible").first
            amount_filled = False
            
            if await input_el.count() > 0:
                amount_str = str(int(amount))
                
                # Clear and fill
                await input_el.fill("")
                await asyncio.sleep(0.2)
                await input_el.fill(amount_str)
                print(f"   Filled amount: {amount_str}")
                
                # Press Enter or Tab to commit
                await self.page.keyboard.press("Enter")
                print(f"   Pressed Enter to commit")
                
                await asyncio.sleep(2)
                amount_filled = True
                print(f"   ✅ Filled Annual Budget: ${amount:,.2f}")
            else:
                # Try typing directly
                print("   No input found, trying keyboard type...")
                await self.page.keyboard.type(str(int(amount)), delay=50)
                await self.page.keyboard.press("Enter")
                await asyncio.sleep(2)
                amount_filled = True
            
            if not amount_filled:
                print("⚠️ Could not fill Annual Budget")
                await self.take_screenshot("amount_fill_failed")
                return None
            
            # Screenshot after filling
            await self.take_screenshot("after_amount_fill")
            
            return {
                'gl_account': row_name,
                'amount': amount,
                'filled': amount_filled
            }
            
        except Exception as e:
            print(f"❌ Error adding budget: {e}")
            await self.take_screenshot("budget_error")
            return None
    
    async def save_budget(self) -> bool:
        """Save the budget in Budget Builder"""
        try:
            # Budget Builder has "Save Budget" button at the top
            save_selectors = [
                "button:has-text('Save Budget')",  # Main save button
                "button:has-text('Save')",
                "button:has-text('Apply')",
                "button[type='submit']",
            ]
            
            for selector in save_selectors:
                save_btns = self.page.locator(selector)
                btn_count = await save_btns.count()
                
                for i in range(btn_count):
                    save_btn = save_btns.nth(i)
                    if await save_btn.is_visible():
                        # Check if button is enabled
                        is_disabled = await save_btn.is_disabled()
                        if is_disabled:
                            print(f"⚠️ Save button {i} is disabled ({selector})")
                            continue
                        
                        await save_btn.click(timeout=5000)
                        print(f"✅ Budget saved via: {selector}")
                        await asyncio.sleep(2)
                        return True
            
            print("❌ No enabled Save button found")
            await self.take_screenshot("save_button_issue")
            return False
            
        except Exception as e:
            print(f"❌ Error saving budget: {e}")
            await self.take_screenshot("save_error")
            return False
    
    async def build_budget_for_group(self, group_name: str = None, budget_lines: list = None) -> bool:
        """
        Complete flow: Build budget using Budget Builder
        
        NOTE: Budget Builder shows GL Account categories (not budget groups).
        This method opens the Builder and adds budget to an existing GL category.
        
        Steps:
        1. Open Budget Builder tab
        2. Find an existing GL category row
        3. Add budget amount
        4. Save
        """
        print(f"\n🔨 Building budget...")
        if group_name:
            print(f"   (Budget group context: {group_name})")
        
        # Open builder
        if not await self.open_budget_builder():
            return False
        
        await asyncio.sleep(2)  # Wait for table to load
        
        # Add budget amount to a GL category row
        if budget_lines:
            # Sum all amounts for total annual budget
            total_amount = sum(line.get('amount', 0) for line in budget_lines)
            await self.add_budget_line(amount=total_amount)
        else:
            # Add a default amount
            await self.add_budget_line(amount=120000)  # $10K/month
        
        # Save
        return await self.save_budget()
    
    # ==========================================
    # VERIFICATION
    # ==========================================
    
    async def verify_budget_group_exists(self, group_name: str) -> bool:
        """Verify a budget group exists in the list"""
        try:
            # First, make sure we're on Chart Of Budget tab
            chart_tab = self.page.locator("text=Chart Of Budget").first
            if await chart_tab.count() > 0:
                await chart_tab.click()
                await asyncio.sleep(1)
            
            # Reload the page to ensure fresh data
            await self.page.reload()
            await asyncio.sleep(3)
            
            # Try using search box - look for the specific placeholder
            search_selectors = [
                "input[placeholder*='Search budget groups']",
                "input[placeholder*='Search']",
                "input[type='search']",
            ]
            
            search_input = None
            for selector in search_selectors:
                inp = self.page.locator(selector).first
                if await inp.count() > 0 and await inp.is_visible():
                    search_input = inp
                    break
            
            if search_input:
                # Clear any existing text first
                await search_input.click()
                await search_input.fill("")
                await asyncio.sleep(0.5)
                
                # Type the search term
                await search_input.fill(group_name)
                print(f"   🔍 Searching for: {group_name}")
                
                # Wait for search to filter results
                await asyncio.sleep(2)
                
                # Take screenshot to debug
                await self.take_screenshot("search_results")
            
            # Check if group appears in the table
            # Look in Name column (column 2) of the table
            group_locator = self.page.locator(f"table tbody tr:has-text('{group_name}')")
            exists = await group_locator.count() > 0
            
            if not exists:
                # Also try partial match (in case name was truncated)
                partial_name = group_name[:15] if len(group_name) > 15 else group_name
                group_locator = self.page.locator(f"table tbody tr:has-text('{partial_name}')")
                exists = await group_locator.count() > 0
            
            # Clear search
            if search_input:
                await search_input.fill("")
                await asyncio.sleep(0.5)
            
            print(f"{'✅' if exists else '❌'} Budget group '{group_name}' {'exists' if exists else 'not found'}")
            return exists
        except Exception as e:
            print(f"⚠️ Error verifying group: {e}")
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
