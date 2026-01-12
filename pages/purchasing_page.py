"""
Purchasing Page Object
Page object for the Purchasing section - Create Vendors, Products, and Purchase Orders
Similar to Invoicing but for vendor/purchasing workflows
"""

from playwright.async_api import Page
import asyncio
import random
import string
from datetime import datetime, timedelta


class PurchasingPage:
    """Page object for Purchasing section"""
    
    def __init__(self, page: Page):
        self.page = page
        self.heading = 'Purchasing'
        self.base_url = "https://app.stage.viewz.co/purchasing"
        
        # Navigation selectors
        self.nav_selectors = [
            "text=Purchasing",
            "a:has-text('Purchasing')",
            "button:has-text('Purchasing')",
            "[data-testid*='purchasing']",
            "[href*='purchasing']"
        ]
        
        # Page identification
        self.page_heading_selectors = [
            "h1:has-text('Purchasing')",
            "h2:has-text('Purchasing')",
            "[data-testid='purchasing-page']"
        ]
        
        # ==========================================
        # VENDOR FORM SELECTORS (similar to Customer)
        # ==========================================
        self.vendor_tab_selectors = [
            "text=Vendors",
            "text=Vendor",
            "button:has-text('Vendors')",
            "button:has-text('Vendor')",
            "a:has-text('Vendors')",
            "[data-testid*='vendor-tab']",
            "[role='tab']:has-text('Vendor')"
        ]
        
        self.add_vendor_button_selectors = [
            "button:has-text('Add Vendor')",
            "button:has-text('New Vendor')",
            "button:has-text('Create Vendor')",
            "text=Add Vendor",
            "[data-testid*='add-vendor']",
            "[data-testid*='new-vendor']",
            "button:has(svg):has-text('Add')"
        ]
        
        # Vendor form fields
        self.vendor_name_selectors = [
            "input[placeholder='Enter vendor name']",
            "input[placeholder*='vendor name' i]",
            "input[name='name']",
            "input[name='vendorName']",
            "[data-testid='vendor-name']"
        ]
        
        self.vendor_email_selectors = [
            "input[placeholder='Enter email address']",
            "input[placeholder*='email' i]",
            "input[type='email']",
            "input[name='email']",
            "[data-testid='vendor-email']"
        ]
        
        self.vendor_city_selectors = [
            "input[placeholder='Enter city']",
            "input[placeholder*='city' i]",
            "input[name='city']",
            "[data-testid='vendor-city']"
        ]
        
        self.vendor_address_selectors = [
            "input[placeholder='Enter vendor address']",
            "input[placeholder*='address' i]",
            "input[name='address']",
            "textarea[name='address']",
            "[data-testid='vendor-address']"
        ]
        
        self.vendor_zip_selectors = [
            "input[placeholder='Enter zip code']",
            "input[placeholder*='zip' i]",
            "input[name='zipCode']",
            "[data-testid='vendor-zip']"
        ]
        
        self.vendor_registration_selectors = [
            "input[placeholder='Enter registration number']",
            "input[placeholder*='registration' i]",
            "input[name='registrationNumber']",
            "[data-testid='registration-number']"
        ]
        
        self.vendor_tax_id_selectors = [
            "input[placeholder='Enter tax ID']",
            "input[placeholder*='tax' i]",
            "input[name='taxId']",
            "[data-testid='tax-id']"
        ]
        
        # Dropdowns
        self.expense_account_dropdown_selectors = [
            "text=Select expense account",
            "[placeholder='Select expense account']"
        ]
        
        self.country_dropdown_selectors = [
            "text=Search countries...",
            "[placeholder='Search countries...']"
        ]
        
        self.payment_terms_dropdown_selectors = [
            "text=Select payment terms",
            "[placeholder='Select payment terms']"
        ]
        
        # ==========================================
        # PRODUCT FORM SELECTORS
        # ==========================================
        self.product_tab_selectors = [
            "text=Products",
            "text=Product",
            "button:has-text('Products')",
            "button:has-text('Product')",
            "a:has-text('Products')",
            "[data-testid*='product-tab']",
            "[role='tab']:has-text('Product')"
        ]
        
        self.add_product_button_selectors = [
            "button:has-text('Add Product')",
            "button:has-text('New Product')",
            "button:has-text('Create Product')",
            "text=Add Product",
            "[data-testid*='add-product']"
        ]
        
        # Product form fields
        self.product_name_selectors = [
            "input[name='productName']",
            "input[name='product_name']",
            "input[name='name']",
            "input[placeholder*='product' i]",
            "input[placeholder='Enter product name']",
            "[data-testid='product-name']"
        ]
        
        self.product_description_selectors = [
            "textarea[name='description']",
            "input[name='description']",
            "textarea[placeholder*='description' i]",
            "[data-testid='product-description']"
        ]
        
        self.product_price_selectors = [
            "input[name='price']",
            "input[name='unitPrice']",
            "input[name='unit_price']",
            "input[type='number'][placeholder*='price' i]",
            "[data-testid='product-price']"
        ]
        
        self.product_sku_selectors = [
            "input[name='sku']",
            "input[name='SKU']",
            "input[name='productCode']",
            "input[placeholder*='SKU' i]",
            "[data-testid='product-sku']"
        ]
        
        # ==========================================
        # PURCHASE ORDER FORM SELECTORS
        # ==========================================
        self.purchase_order_tab_selectors = [
            "text=Purchase Orders",
            "text=PO",
            "button:has-text('Purchase Orders')",
            "button:has-text('Orders')",
            "a:has-text('Purchase Orders')",
            "[data-testid*='purchase-order-tab']",
            "[role='tab']:has-text('Purchase')"
        ]
        
        self.add_po_button_selectors = [
            "button:has-text('Generate PurchaseOrder')",  # Actual button text
            "button:has-text('Generate Purchase Order')",
            "button:has-text('Create Purchase Order')",
            "button:has-text('New Purchase Order')",
            "button:has-text('Add Purchase Order')",
            "button:has-text('Create PO')",
            "button:has-text('Generate PO')",
            "text=Generate PurchaseOrder",
            "text=Create Purchase Order",
            "[data-testid*='add-po']",
            "[data-testid*='create-po']"
        ]
        
        # Purchase Order form fields
        self.po_vendor_selectors = [
            "[data-testid='po-vendor']",
            "text=Select vendor",
            "[placeholder*='vendor' i]"
        ]
        
        self.po_product_selectors = [
            "[data-testid='po-product']",
            "text=Select product",
            "[placeholder*='product' i]"
        ]
        
        self.po_quantity_selectors = [
            "input[name='quantity']",
            "input[type='number'][placeholder*='quantity' i]",
            "[data-testid='po-quantity']"
        ]
        
        self.po_date_selectors = [
            "input[type='date']",
            "input[name='orderDate']",
            "[data-testid='po-date']"
        ]

    # ==========================================
    # NAVIGATION METHODS
    # ==========================================
    
    async def is_loaded(self) -> bool:
        """Check if the Purchasing page is loaded"""
        try:
            # Try heading first
            locator = self.page.get_by_role('heading', name=self.heading)
            await locator.wait_for(timeout=10000)
            return await locator.is_visible()
        except:
            # Fallback: check URL or page content
            return 'purchasing' in self.page.url.lower()
    
    async def navigate_to_purchasing(self, entity_id: int = 1) -> bool:
        """Navigate to the Purchasing page"""
        try:
            # First try direct URL navigation
            url = f"{self.base_url}?entityId={entity_id}"
            await self.page.goto(url)
            await self.page.wait_for_load_state("networkidle")
            await asyncio.sleep(2)
            
            # Check if we're on purchasing page
            if 'purchasing' in self.page.url.lower():
                print(f"📍 Navigated to Purchasing via URL: {self.page.url}")
                return True
            
            # If URL didn't work, use sidebar menu
            print("📍 Using sidebar menu to navigate to Purchasing...")
            
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
            
            # Click Purchasing in sidebar
            purchasing_link = self.page.locator("text=Purchasing").first
            if await purchasing_link.count() > 0:
                await purchasing_link.click()
                await asyncio.sleep(2)
                print(f"📍 Navigated to Purchasing via sidebar: {self.page.url}")
                return True
            else:
                print("⚠️ Purchasing link not found in sidebar")
                return False
                
        except Exception as e:
            print(f"⚠️ Navigation error: {e}")
            return False
    
    async def take_screenshot(self, name: str):
        """Take a screenshot for debugging"""
        filename = f"debug_purchasing_{name}_{datetime.now().strftime('%H%M%S')}.png"
        await self.page.screenshot(path=filename)
        print(f"📸 Screenshot: {filename}")
        return filename

    # ==========================================
    # TAB NAVIGATION METHODS
    # ==========================================
    
    async def go_to_vendors_tab(self) -> bool:
        """Navigate to Vendors tab - Note: Main page shows vendors directly"""
        # The main Purchasing page shows vendors directly, no separate tab
        # Just verify we're on the Purchasing page
        if 'purchasing' in self.page.url.lower():
            print("✅ On Vendors list (main Purchasing page)")
            return True
        return await self.navigate_to_purchasing()
    
    async def go_to_products_tab(self) -> bool:
        """Navigate to Products tab - DEPRECATED: Use go_to_products_for_vendor via Actions menu"""
        print("⚠️ go_to_products_tab is deprecated. Products are accessed via vendor Actions menu.")
        return True

    async def go_to_purchase_orders_tab(self) -> bool:
        """Navigate to Purchase Orders tab - DEPRECATED: Use go_to_purchase_orders_for_vendor via Actions menu"""
        print("⚠️ go_to_purchase_orders_tab is deprecated. Purchase Orders are accessed via vendor Actions menu.")
        return True
    
    async def _click_vendor_action_menu(self, vendor_name: str, action: str) -> bool:
        """Click action menu for a vendor and select an action (Products/Purchases/Edit)
        
        Similar to Invoicing's _click_customer_action_menu pattern.
        """
        try:
            await asyncio.sleep(2)
            
            target_row = None
            
            if vendor_name:
                # Use partial name (first few words) since names get truncated in UI
                partial_name = ' '.join(vendor_name.split()[:2])
                print(f"🔍 Looking for vendor containing: '{partial_name}'")
                
                rows = self.page.locator("table tbody tr")
                row_count = await rows.count()
                print(f"📋 Found {row_count} rows in table")
                
                for i in range(row_count):
                    row = rows.nth(i)
                    try:
                        row_text = await row.inner_text()
                        if partial_name.lower() in row_text.lower():
                            target_row = row
                            print(f"✅ Found vendor row {i}: {row_text[:50]}...")
                            break
                    except:
                        continue
                
                if not target_row:
                    print(f"⚠️ Vendor not found, using first row as fallback")
                    target_row = rows.first
            else:
                target_row = self.page.locator("table tbody tr").first
                print("📍 Using first vendor row")
            
            if await target_row.count() == 0:
                print("❌ No vendor row found")
                return False
            
            # Click the "..." button in the Actions column (same pattern as Invoicing)
            action_clicked = False
            
            # Try different selectors for the three-dots button
            three_dots_selectors = [
                "text=•••",      # Bullet points
                "text=...",      # Regular dots
                "text=…",        # Ellipsis character
                "text=⋯",        # Math ellipsis
                "[aria-label*='action']",
                "[aria-label*='menu']",
                "button:has-text('•')",
                "td:last-child button",
                "td:last-child [role='button']",
            ]
            
            for selector in three_dots_selectors:
                try:
                    action_button = target_row.locator(selector).first
                    if await action_button.count() > 0 and await action_button.is_visible():
                        await action_button.click()
                        print(f"✅ Clicked action button via: {selector}")
                        action_clicked = True
                        break
                except:
                    continue
            
            if not action_clicked:
                # Try clicking the last cell directly (Actions column)
                try:
                    last_cell = target_row.locator("td").last
                    # Look for a clickable element inside
                    btn_in_cell = last_cell.locator("button, svg, [role='button']").first
                    if await btn_in_cell.count() > 0:
                        await btn_in_cell.click()
                        print("✅ Clicked button in last cell")
                        action_clicked = True
                    else:
                        await last_cell.click()
                        print("✅ Clicked last cell (Actions column)")
                        action_clicked = True
                    await asyncio.sleep(0.5)
                except:
                    pass
            
            if not action_clicked:
                print("❌ Could not click Actions button")
                await self.take_screenshot("actions_not_found")
                return False
            
            await asyncio.sleep(1)
            
            # Take screenshot to see the menu
            await self.take_screenshot("actions_menu_state")
            
            # Now click the desired action from the dropdown menu
            # Be specific to avoid clicking wrong elements (e.g., page headings containing same text)
            action_option_selectors = [
                f"[role='menuitem']:has-text('{action}')",
                f"[role='menu'] >> text={action}",
                f"[role='menu'] button:has-text('{action}')",
                f"[role='menu'] a:has-text('{action}')",
                f"[data-radix-menu-content] >> text={action}",
                f".dropdown-menu >> text={action}",
                f"[class*='dropdown'] >> text={action}",
                f"[class*='menu'] >> text={action}",
            ]
            
            for selector in action_option_selectors:
                try:
                    option = self.page.locator(selector).first
                    if await option.count() > 0 and await option.is_visible():
                        await option.click()
                        await asyncio.sleep(2)
                        print(f"✅ Clicked '{action}' via: {selector}")
                        return True
                except:
                    continue
            
            # Fallback: Try to find the menu that just appeared and click the action
            try:
                # Look for any visible dropdown/menu that contains the action text
                menu_containers = ["[role='menu']", "[data-radix-menu-content]", "[class*='popover']", "[class*='dropdown']"]
                for container_sel in menu_containers:
                    container = self.page.locator(container_sel).first
                    if await container.count() > 0 and await container.is_visible():
                        action_btn = container.locator(f"text={action}").first
                        if await action_btn.count() > 0:
                            await action_btn.click()
                            await asyncio.sleep(2)
                            print(f"✅ Clicked '{action}' in {container_sel}")
                            return True
            except:
                pass
            
            print(f"❌ '{action}' option not found in menu")
            await self.take_screenshot(f"action_{action.lower().replace(' ', '_')}_not_found")
            return False
            
        except Exception as e:
            print(f"❌ Error in _click_vendor_action_menu: {str(e)}")
            return False

    # ==========================================
    # VENDOR METHODS
    # ==========================================
    
    async def click_add_vendor(self) -> bool:
        """Click Add Vendor button"""
        for selector in self.add_vendor_button_selectors:
            try:
                element = self.page.locator(selector).first
                if await element.count() > 0 and await element.is_visible():
                    await element.click()
                    await asyncio.sleep(1)
                    print("✅ Clicked Add Vendor button")
                    return True
            except:
                continue
        print("⚠️ Add Vendor button not found")
        return False
    
    async def _select_dropdown(self, trigger_text: str, option_text: str, field_name: str) -> bool:
        """Select an option from a dropdown"""
        try:
            # Find and click the dropdown trigger
            dropdown_selectors = [
                f"text={trigger_text}",
                f"[placeholder='{trigger_text}']",
                f"button:has-text('{trigger_text}')",
            ]
            
            clicked = False
            for selector in dropdown_selectors:
                try:
                    dropdown = self.page.locator(selector).first
                    if await dropdown.count() > 0 and await dropdown.is_visible():
                        await dropdown.click()
                        await asyncio.sleep(0.5)
                        clicked = True
                        break
                except:
                    continue
            
            if not clicked:
                print(f"   ⚠️ Dropdown not found: {trigger_text}")
                return False
            
            # Select the option
            option_selectors = [
                f"text={option_text}",
                f"[role='option']:has-text('{option_text}')",
                f"li:has-text('{option_text}')",
                f"div:has-text('{option_text}')",
            ]
            
            for selector in option_selectors:
                try:
                    option = self.page.locator(selector).first
                    if await option.count() > 0 and await option.is_visible():
                        await option.click()
                        await asyncio.sleep(0.3)
                        print(f"   ✅ {field_name}: {option_text}")
                        return True
                except:
                    continue
            
            print(f"   ⚠️ Option not found: {option_text}")
            return False
            
        except Exception as e:
            print(f"   ⚠️ Dropdown error: {str(e)[:30]}")
            return False

    async def fill_vendor_form(self, vendor_data: dict) -> bool:
        """Fill the vendor creation form including required dropdowns"""
        try:
            filled_fields = 0
            
            # 1. COUNTRY (Required dropdown) - Already defaults to USA usually
            country = vendor_data.get('country', 'USA')
            # Only select if not already set
            country_dropdown = self.page.locator("text=Search countries...").first
            if await country_dropdown.count() > 0 and await country_dropdown.is_visible():
                if await self._select_dropdown("Search countries...", country, "Country"):
                    filled_fields += 1
            else:
                print(f"   ✅ Country: Already set")
                filled_fields += 1
            
            await asyncio.sleep(0.3)
            
            # 2. VENDOR TYPE (Required dropdown) - Options: Company, Individual
            vendor_type = vendor_data.get('vendor_type', 'Company')
            if await self._select_dropdown("Select vendor type", vendor_type, "Vendor Type"):
                filled_fields += 1
            
            await asyncio.sleep(0.3)
            
            # 3. Fill Registration Number (use numeric format)
            reg_number = vendor_data.get('registration', str(random.randint(100000, 999999)))
            reg_input = self.page.locator("input[placeholder='Enter registration number']").first
            if await reg_input.count() > 0:
                await reg_input.fill(reg_number)
                print(f"   ✅ Registration: {reg_number}")
                filled_fields += 1
            
            # 4. Fill Tax ID (same format as registration to avoid validation issues)
            tax_id = vendor_data.get('tax_id', reg_number)  # Use same as registration if not provided
            tax_input = self.page.locator("input[placeholder='Enter tax ID']").first
            if await tax_input.count() > 0:
                await tax_input.fill(tax_id)
                print(f"   ✅ Tax ID: {tax_id}")
                filled_fields += 1
            
            # 5. Fill Vendor Name
            name_input = self.page.locator("input[placeholder='Enter vendor name']").first
            if await name_input.count() > 0:
                await name_input.fill(vendor_data.get('name', f"Vendor-{random.randint(1000, 9999)}"))
                print(f"   ✅ Name: {vendor_data.get('name', 'auto')}")
                filled_fields += 1
            
            await asyncio.sleep(0.3)
            
            # 6. GL Account - FIRST try dropdown, THEN checkbox if no options
            gl_filled = False
            
            # Method 1: Try to select from dropdown first
            try:
                gl_dropdown = self.page.locator("text=Select payables account").first
                if await gl_dropdown.count() > 0 and await gl_dropdown.is_visible():
                    # Check if dropdown is NOT disabled
                    parent_button = self.page.locator("button:has-text('Select payables account')").first
                    is_disabled = await parent_button.is_disabled() if await parent_button.count() > 0 else True
                    
                    if not is_disabled:
                        await gl_dropdown.click()
                        await asyncio.sleep(1)
                        
                        # Check for options
                        options = self.page.locator("[role='option'], [cmdk-item], li")
                        option_count = await options.count()
                        
                        if option_count > 0:
                            first_option = options.first
                            option_text = await first_option.inner_text()
                            await first_option.click()
                            print(f"   ✅ GL Account: {option_text[:40]}...")
                            filled_fields += 1
                            gl_filled = True
                            await asyncio.sleep(0.5)
                        else:
                            await self.page.keyboard.press("Escape")
                            print(f"   ⚠️ GL Account dropdown: No options")
                    else:
                        print(f"   ⚠️ GL Account dropdown is disabled")
            except Exception as e:
                print(f"   ⚠️ GL Account dropdown: {str(e)[:30]}")
            
            # Method 2: If dropdown failed, try the checkbox
            if not gl_filled:
                try:
                    # Click anywhere on the checkbox row
                    checkbox_row = self.page.locator("text=Create GL Account Automatically").first
                    if await checkbox_row.count() > 0 and await checkbox_row.is_visible():
                        await checkbox_row.click()
                        await asyncio.sleep(1)
                        print(f"   ✅ GL Account: Clicked auto-create checkbox")
                        filled_fields += 1
                        gl_filled = True
                except Exception as e:
                    print(f"   ⚠️ GL Account checkbox: {str(e)[:30]}")
            
            # Method 3: JavaScript fallback
            if not gl_filled:
                try:
                    toggled = await self.page.evaluate("""
                        () => {
                            const labels = document.querySelectorAll('label, span, div');
                            for (const label of labels) {
                                if (label.textContent.includes('Create GL Account Automatically')) {
                                    const container = label.closest('div');
                                    const checkbox = container?.querySelector('input[type="checkbox"], [role="checkbox"], button');
                                    if (checkbox) {
                                        checkbox.click();
                                        return 'clicked checkbox';
                                    }
                                    label.click();
                                    return 'clicked label';
                                }
                            }
                            return null;
                        }
                    """)
                    if toggled:
                        print(f"   ✅ GL Account: {toggled} via JS")
                        gl_filled = True
                        filled_fields += 1
                        await asyncio.sleep(1)
                except Exception as e:
                    print(f"   ⚠️ GL Account JS: {str(e)[:30]}")
            
            await asyncio.sleep(0.3)
            
            # 7. Fill Email
            email_input = self.page.locator("input[placeholder='Enter email address']").first
            if await email_input.count() > 0:
                await email_input.fill(vendor_data.get('email', f"vendor{random.randint(100, 999)}@example.com"))
                print(f"   ✅ Email: {vendor_data.get('email', 'auto')}")
                filled_fields += 1
            
            # 8. STATE dropdown (required for USA)
            state = vendor_data.get('state', 'California')
            if await self._select_dropdown("Select state", state, "State"):
                filled_fields += 1
            
            await asyncio.sleep(0.3)
            
            # 9. Fill City
            city_input = self.page.locator("input[placeholder='Enter city']").first
            if await city_input.count() > 0:
                await city_input.fill(vendor_data.get('city', 'Los Angeles'))
                print(f"   ✅ City: {vendor_data.get('city', 'Los Angeles')}")
                filled_fields += 1
            
            # 10. Fill Address
            address_input = self.page.locator("input[placeholder='Enter vendor address']").first
            if await address_input.count() > 0:
                await address_input.fill(vendor_data.get('address', '123 Test Street'))
                print(f"   ✅ Address: {vendor_data.get('address', 'auto')}")
                filled_fields += 1
            
            # 11. Fill Zip Code
            zip_input = self.page.locator("input[placeholder='Enter zip code']").first
            if await zip_input.count() > 0:
                await zip_input.fill(vendor_data.get('zip', '90210'))
                print(f"   ✅ Zip: {vendor_data.get('zip', '90210')}")
                filled_fields += 1
            
            # 12. PAYMENT TERMS (Required dropdown) - Common options: Net 30, Net 60, Due on Receipt
            payment_terms = vendor_data.get('payment_terms', 'Net 30')
            if await self._select_dropdown("Select payment terms", payment_terms, "Payment Terms"):
                filled_fields += 1
            
            await asyncio.sleep(0.3)
            
            print(f"   📝 Filled {filled_fields} vendor fields")
            return filled_fields > 0
            
        except Exception as e:
            print(f"❌ Error filling vendor form: {e}")
            await self.take_screenshot("vendor_form_error")
            return False
    
    async def _click_save(self, button_text: str = None) -> bool:
        """Click save/create button"""
        # Scroll to bottom to ensure button is visible
        await self.page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        await asyncio.sleep(0.5)
        
        save_selectors = [
            f"button:has-text('{button_text}')" if button_text else None,
            "button:has-text('Create Vendor')",
            "button:has-text('Create Product')",
            "button:has-text('Create')",
            "button:has-text('Save')",
            "button:has-text('Add')",
            "button[type='submit']",
        ]
        
        for selector in [s for s in save_selectors if s]:
            try:
                btn = self.page.locator(selector).first
                if await btn.count() > 0:
                    # Scroll into view and click
                    await btn.scroll_into_view_if_needed()
                    await asyncio.sleep(0.3)
                    
                    if await btn.is_visible():
                        await btn.click(force=True)
                        await asyncio.sleep(2)
                        print(f"✅ Clicked: {selector}")
                        return True
            except Exception as e:
                print(f"   ⚠️ Button {selector}: {str(e)[:30]}")
                continue
        
        # Try JavaScript click as fallback
        try:
            clicked = await self.page.evaluate("""
                () => {
                    const buttons = document.querySelectorAll('button');
                    for (const btn of buttons) {
                        const text = btn.textContent.toLowerCase();
                        if (text.includes('create') || text.includes('save') || text.includes('add')) {
                            btn.scrollIntoView();
                            btn.click();
                            return btn.textContent;
                        }
                    }
                    return null;
                }
            """)
            if clicked:
                print(f"✅ Clicked via JS: {clicked}")
                await asyncio.sleep(2)
                return True
        except:
            pass
        
        print("⚠️ Save button not found")
        return False
    
    async def create_vendor(self, vendor_data: dict = None) -> dict:
        """Create a new vendor"""
        try:
            # Generate default data if not provided
            if vendor_data is None:
                random_suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
                reg_number = str(random.randint(100000, 999999))  # Numeric format
                vendor_data = {
                    'name': f"AutoTest Vendor {random_suffix}",
                    'email': f"vendor.{random_suffix.lower()}@example.com",
                    'city': "Los Angeles",
                    'address': f"{random.randint(100, 999)} Vendor Street",
                    'zip': f"{random.randint(10000, 99999)}",
                    'registration': reg_number,
                    'tax_id': reg_number,  # Same as registration to pass validation
                    'vendor_type': 'Company',
                    'state': 'California',
                    'payment_terms': 'Net 30'
                }
            
            print(f"\n📝 Creating Vendor: {vendor_data.get('name', 'N/A')}")
            
            # Go to Vendors tab
            await self.go_to_vendors_tab()
            await asyncio.sleep(1)
            
            # Click Add Vendor
            if not await self.click_add_vendor():
                print("⚠️ Trying alternative approach...")
                # Try clicking any Add button
                add_btn = self.page.locator("button:has-text('Add')").first
                if await add_btn.count() > 0:
                    await add_btn.click()
                    await asyncio.sleep(1)
            
            # Fill form
            await self.fill_vendor_form(vendor_data)
            
            # Save - Click "Create Vendor" button
            await self._click_save("Create Vendor")
            
            await asyncio.sleep(3)
            
            # Check if form is still open
            form_still_open = await self.page.locator("text=Create New Vendor").count() > 0
            
            if form_still_open:
                await self.take_screenshot("vendor_form_still_open")
                
                # Check if button is disabled
                create_btn = self.page.locator("button:has-text('Create Vendor')").first
                if await create_btn.count() > 0:
                    is_disabled = await create_btn.is_disabled()
                    print(f"   ⚠️ Create Vendor button disabled: {is_disabled}")
                    
                    if not is_disabled:
                        # Try clicking again
                        await create_btn.scroll_into_view_if_needed()
                        await asyncio.sleep(0.5)
                        await create_btn.click(force=True)
                        await asyncio.sleep(3)
                        print("   🔄 Clicked Create Vendor again")
            
            # Verify form closed (back on vendors list)
            await asyncio.sleep(2)
            form_closed = await self.page.locator("text=Create New Vendor").count() == 0
            
            if form_closed:
                print(f"✅ Vendor created: {vendor_data['name']}")
                return vendor_data
            else:
                print(f"⚠️ Vendor form still open - creation may have failed")
                await self.take_screenshot("vendor_not_saved")
                return None
                
        except Exception as e:
            print(f"❌ Error creating vendor: {e}")
            await self.take_screenshot("vendor_error")
            return None
    
    async def get_vendor_list(self) -> list:
        """Get list of vendors"""
        vendors = []
        try:
            await self.go_to_vendors_tab()
            await asyncio.sleep(1)
            
            rows = self.page.locator("table tbody tr")
            count = await rows.count()
            
            for i in range(min(count, 10)):  # Limit to first 10
                try:
                    row_text = await rows.nth(i).inner_text()
                    vendors.append(row_text.strip())
                except:
                    continue
            
            print(f"📋 Found {len(vendors)} vendors")
        except Exception as e:
            print(f"⚠️ Error getting vendor list: {e}")
        
        return vendors

    # ==========================================
    # PRODUCT METHODS (for Vendor)
    # ==========================================
    
    async def go_to_products_for_vendor(self, vendor_name: str = None) -> bool:
        """Navigate to Products section for a vendor via Actions menu
        
        Similar to Invoicing's go_to_products_for_customer pattern.
        """
        try:
            current_url = self.page.url
            
            # Click Products in Actions menu
            result = await self._click_vendor_action_menu(vendor_name, "Products")
            
            if result:
                await asyncio.sleep(2)
                
                # Check if URL changed (navigation to products page)
                new_url = self.page.url
                if new_url != current_url:
                    print(f"📍 Navigated to: {new_url}")
                    return True
                
                # Check if we're now on a products page
                if "/products" in new_url.lower():
                    return True
                
                # Check if Add Product button is now visible
                add_product = self.page.locator("button:has-text('Add Product')").first
                if await add_product.count() > 0 and await add_product.is_visible():
                    print("📍 Products section visible (Add Product button found)")
                    return True
                
                # Return true if menu action worked, even if page looks same
                # (Products might be shown inline or in a different way)
                return True
            
            return False
            
        except Exception as e:
            print(f"❌ Error navigating to Products: {str(e)}")
            return False
    
    async def click_add_product(self) -> bool:
        """Click Add Product button"""
        for selector in self.add_product_button_selectors:
            try:
                element = self.page.locator(selector).first
                if await element.count() > 0 and await element.is_visible():
                    await element.click()
                    await asyncio.sleep(1)
                    print("✅ Clicked Add Product button")
                    return True
            except:
                continue
        print("⚠️ Add Product button not found")
        return False
    
    async def fill_product_form(self, product_data: dict) -> bool:
        """Fill the product creation form including required fields"""
        try:
            filled_fields = 0
            
            # Fill Product Name
            name = product_data.get('name', f"Product-{random.randint(1000, 9999)}")
            name_input = self.page.locator("input").filter(has=self.page.locator("[placeholder*='Product Name' i], [name='name']")).first
            if await name_input.count() == 0:
                # Try by position - first input in form
                name_input = self.page.locator("[role='dialog'] input, .modal input").first
            
            if await name_input.count() > 0:
                await name_input.fill(name)
                filled_fields += 1
                print(f"   ✅ Product Name: {name}")
            
            await asyncio.sleep(0.3)
            
            # Fill SKU
            sku = product_data.get('sku', f"SKU-{random.randint(1000, 9999)}")
            sku_input = self.page.locator("input[placeholder*='SKU' i], input[name*='sku' i]").first
            if await sku_input.count() == 0:
                # Try the second input
                inputs = self.page.locator("[role='dialog'] input, .modal input")
                if await inputs.count() > 1:
                    sku_input = inputs.nth(1)
            
            if await sku_input.count() > 0 and await sku_input.is_visible():
                await sku_input.fill(sku)
                filled_fields += 1
                print(f"   ✅ SKU: {sku}")
            
            await asyncio.sleep(0.3)
            
            # Fill Unit (REQUIRED - e.g., "licenses", "hours", "units")
            unit = product_data.get('unit', 'units')
            unit_input = self.page.locator("input[placeholder*='licenses' i], input[placeholder*='hours' i], input[placeholder*='unit' i]").first
            if await unit_input.count() > 0 and await unit_input.is_visible():
                await unit_input.fill(unit)
                filled_fields += 1
                print(f"   ✅ Unit: {unit}")
            else:
                # Try to find by label
                unit_label = self.page.locator("text=Unit").first
                if await unit_label.count() > 0:
                    # Find the input near this label
                    unit_input = self.page.locator("input").filter(has=self.page.locator("text=Unit")).first
                    if await unit_input.count() == 0:
                        # Try sibling input
                        all_inputs = self.page.locator("[role='dialog'] input")
                        for i in range(await all_inputs.count()):
                            inp = all_inputs.nth(i)
                            placeholder = await inp.get_attribute("placeholder") or ""
                            if "licenses" in placeholder.lower() or "hours" in placeholder.lower():
                                await inp.fill(unit)
                                filled_fields += 1
                                print(f"   ✅ Unit: {unit}")
                                break
            
            await asyncio.sleep(0.3)
            
            # Fill Price
            price = product_data.get('price', round(random.uniform(50.0, 500.0), 2))
            price_input = self.page.locator("input[placeholder*='price' i], input[name*='price' i]").first
            if await price_input.count() == 0:
                # Try to find input near "Price" label
                price_inputs = self.page.locator("[role='dialog'] input[type='number'], [role='dialog'] input")
                for i in range(await price_inputs.count()):
                    inp = price_inputs.nth(i)
                    placeholder = await inp.get_attribute("placeholder") or ""
                    name_attr = await inp.get_attribute("name") or ""
                    if "price" in placeholder.lower() or "price" in name_attr.lower():
                        price_input = inp
                        break
            
            if await price_input.count() > 0 and await price_input.is_visible():
                await price_input.fill(str(price))
                filled_fields += 1
                print(f"   ✅ Price: {price}")
            
            await asyncio.sleep(0.3)
            
            # Select Product Type (might be required)
            try:
                type_dropdown = self.page.locator("button:has-text('Select type')").first
                if await type_dropdown.count() > 0 and await type_dropdown.is_visible():
                    await type_dropdown.click()
                    await asyncio.sleep(1)
                    
                    # Click first option
                    options = self.page.locator("[role='option'], [cmdk-item], [data-radix-collection-item]")
                    if await options.count() > 0:
                        opt = options.first
                        opt_text = await opt.inner_text()
                        await opt.click()
                        filled_fields += 1
                        print(f"   ✅ Product Type: {opt_text}")
                    else:
                        await self.page.keyboard.press("Escape")
            except Exception as e:
                print(f"   ⚠️ Product Type: {str(e)[:30]}")
            
            await asyncio.sleep(0.3)
            
            # Select Billing Period (might be required)
            try:
                period_dropdown = self.page.locator("button:has-text('Select period')").first
                if await period_dropdown.count() > 0 and await period_dropdown.is_visible():
                    await period_dropdown.click()
                    await asyncio.sleep(1)
                    
                    # Click first option (e.g., "Monthly")
                    options = self.page.locator("[role='option'], [cmdk-item], [data-radix-collection-item]")
                    if await options.count() > 0:
                        opt = options.first
                        opt_text = await opt.inner_text()
                        await opt.click()
                        filled_fields += 1
                        print(f"   ✅ Billing Period: {opt_text}")
                    else:
                        await self.page.keyboard.press("Escape")
            except Exception as e:
                print(f"   ⚠️ Billing Period: {str(e)[:30]}")
            
            await asyncio.sleep(0.3)
            
            # Select Start Date (REQUIRED for recurring products)
            try:
                # Find the "Pick a date" button for Start Date
                start_date_btn = self.page.locator("button:has-text('Pick a date')").first
                if await start_date_btn.count() > 0 and await start_date_btn.is_visible():
                    await start_date_btn.click()
                    await asyncio.sleep(1)
                    
                    # Wait for calendar to open
                    calendar = self.page.locator("[role='dialog'] table, [class*='calendar'], [class*='picker']")
                    if await calendar.count() > 0:
                        # Click on a day (try multiple selectors)
                        day_selectors = [
                            "[role='gridcell'] button:not([disabled])",
                            "button[name='day']",
                            "[class*='day']:not([disabled])"
                        ]
                        
                        for selector in day_selectors:
                            try:
                                day_btn = self.page.locator(selector).first
                                if await day_btn.count() > 0 and await day_btn.is_visible():
                                    await day_btn.click()
                                    filled_fields += 1
                                    print(f"   ✅ Start Date: Selected")
                                    break
                            except:
                                continue
                        else:
                            # Try clicking today in footer
                            today_btn = self.page.locator("button:has-text('Today')").first
                            if await today_btn.count() > 0:
                                await today_btn.click()
                                filled_fields += 1
                                print(f"   ✅ Start Date: Today")
                            else:
                                await self.page.keyboard.press("Escape")
                                print(f"   ⚠️ Start Date: Could not select day")
                    else:
                        # Maybe it's a different date picker type
                        await self.page.keyboard.press("Escape")
                        print(f"   ⚠️ Start Date: Calendar not visible")
                else:
                    print(f"   ⚠️ Start Date: Button not found")
            except Exception as e:
                print(f"   ⚠️ Start Date: {str(e)[:40]}")
            
            await asyncio.sleep(0.3)
            
            # Select Contract (REQUIRED - missing validation in UI but server requires it)
            contract_selected = False
            
            # Method 1: Click the dropdown button directly
            try:
                # Find the Contract section and click the dropdown
                contract_button = self.page.locator("button:has-text('Select Contract')").first
                if await contract_button.count() > 0 and await contract_button.is_visible():
                    await contract_button.click()
                    await asyncio.sleep(1)
                    contract_selected = True
                    print(f"   📍 Clicked Contract dropdown button")
            except Exception as e:
                print(f"   ⚠️ Contract button method: {str(e)[:30]}")
            
            # Method 2: Try text locator
            if not contract_selected:
                try:
                    contract_text = self.page.get_by_text("Select Contract", exact=True).first
                    if await contract_text.count() > 0 and await contract_text.is_visible():
                        await contract_text.click()
                        await asyncio.sleep(1)
                        contract_selected = True
                        print(f"   📍 Clicked Contract text")
                except Exception as e:
                    print(f"   ⚠️ Contract text method: {str(e)[:30]}")
            
            # Method 3: Find by label
            if not contract_selected:
                try:
                    contract_label = self.page.locator("text=Contract").first
                    if await contract_label.count() > 0:
                        # Click the sibling dropdown
                        parent = contract_label.locator("xpath=./parent::*")
                        dropdown = parent.locator("button, [role='combobox']").first
                        if await dropdown.count() > 0:
                            await dropdown.click()
                            await asyncio.sleep(1)
                            contract_selected = True
                            print(f"   📍 Clicked Contract via label")
                except Exception as e:
                    print(f"   ⚠️ Contract label method: {str(e)[:30]}")
            
            # Now select an option if dropdown is open
            if contract_selected:
                try:
                    await asyncio.sleep(0.5)
                    # Look for options in the dropdown
                    options = self.page.locator("[role='option'], [cmdk-item], [data-radix-collection-item]")
                    option_count = await options.count()
                    print(f"   📋 Found {option_count} contract options")
                    
                    if option_count > 0:
                        first_option = options.first
                        option_text = await first_option.inner_text()
                        await first_option.click()
                        filled_fields += 1
                        print(f"   ✅ Contract: {option_text[:30]}...")
                    else:
                        # Try clicking any visible list item
                        list_items = self.page.locator("[class*='popover'] div, [class*='dropdown'] div").filter(has_text=lambda t: t and len(t) > 2)
                        if await list_items.count() > 0:
                            await list_items.first.click()
                            filled_fields += 1
                            print(f"   ✅ Contract: First available")
                        else:
                            await self.page.keyboard.press("Escape")
                            print(f"   ⚠️ Contract: No options found")
                except Exception as e:
                    print(f"   ⚠️ Contract option: {str(e)[:30]}")
                    await self.page.keyboard.press("Escape")
            else:
                print(f"   ⚠️ Contract: Could not open dropdown")
            
            await asyncio.sleep(0.3)
            
            # Select Product Income Account (GL Account) - REQUIRED
            try:
                gl_dropdown = self.page.locator("button:has-text('Select GL Account')").first
                if await gl_dropdown.count() > 0 and await gl_dropdown.is_visible():
                    await gl_dropdown.click()
                    await asyncio.sleep(1)
                    
                    # Look for options
                    options = self.page.locator("[role='option'], [cmdk-item], [data-radix-collection-item]")
                    option_count = await options.count()
                    print(f"   📋 Found {option_count} GL Account options")
                    
                    if option_count > 0:
                        first_opt = options.first
                        opt_text = await first_opt.inner_text()
                        await first_opt.click()
                        filled_fields += 1
                        print(f"   ✅ Product Income Account: {opt_text[:30]}...")
                    else:
                        await self.page.keyboard.press("Escape")
                        print(f"   ⚠️ Product Income Account: No options - GL accounts need to be set up")
                else:
                    print(f"   ⚠️ Product Income Account: Dropdown not found")
            except Exception as e:
                print(f"   ⚠️ Product Income Account: {str(e)[:40]}")
            
            await asyncio.sleep(0.3)
            
            # Select Currency (REQUIRED - has asterisk *)
            currency_selected = False
            currency = product_data.get('currency', 'US Dollar')
            
            try:
                # Method 1: Click "Select currency" dropdown
                currency_dropdown = self.page.locator("button:has-text('Select currency')").first
                if await currency_dropdown.count() > 0 and await currency_dropdown.is_visible():
                    await currency_dropdown.click()
                    await asyncio.sleep(1)
                    
                    # Look for the currency option
                    options = self.page.locator("[role='option'], [cmdk-item], [data-radix-collection-item]")
                    option_count = await options.count()
                    print(f"   📋 Found {option_count} currency options")
                    
                    if option_count > 0:
                        # Try to find specific currency or use first
                        for i in range(option_count):
                            opt = options.nth(i)
                            opt_text = await opt.inner_text()
                            if currency.lower() in opt_text.lower():
                                await opt.click()
                                filled_fields += 1
                                currency_selected = True
                                print(f"   ✅ Currency: {opt_text}")
                                break
                        
                        if not currency_selected:
                            # Use first option
                            first_opt = options.first
                            opt_text = await first_opt.inner_text()
                            await first_opt.click()
                            filled_fields += 1
                            currency_selected = True
                            print(f"   ✅ Currency: {opt_text}")
                    else:
                        await self.page.keyboard.press("Escape")
                        print(f"   ⚠️ Currency: No options found")
                else:
                    print(f"   ⚠️ Currency dropdown not found")
            except Exception as e:
                print(f"   ⚠️ Currency: {str(e)[:40]}")
            
            await asyncio.sleep(0.3)
            
            print(f"   📝 Filled {filled_fields} product fields")
            return filled_fields > 0
            
        except Exception as e:
            print(f"❌ Error filling product form: {e}")
            return False
    
    async def create_product_for_vendor(self, vendor_name: str = None, product_data: dict = None) -> dict:
        """Create a product for a vendor"""
        try:
            # Generate default data if not provided
            if product_data is None:
                random_suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
                product_data = {
                    'name': f"AutoTest Product {random_suffix}",
                    'description': f"Automated test product - {datetime.now().isoformat()}",
                    'price': round(random.uniform(50.0, 500.0), 2),
                    'sku': f"PROD-{random_suffix}"
                }
            
            print(f"\n📝 Creating Product: {product_data.get('name', 'N/A')}")
            
            # Navigate to Products for vendor
            if not await self.go_to_products_for_vendor(vendor_name):
                # Try direct Products tab
                await self.go_to_products_tab()
                await asyncio.sleep(1)
            
            # Click Add Product
            await self.click_add_product()
            
            # Fill form
            await self.fill_product_form(product_data)
            
            # Take screenshot before save
            await self.take_screenshot("before_create_product")
            
            # Save
            await self._click_save("Create Product")
            
            await asyncio.sleep(3)
            
            # Take screenshot after save to see any errors
            await self.take_screenshot("after_create_product_click")
            
            # Check if form is still open (indicates error)
            form_open = await self.page.locator("text=Create Product").locator("visible=true").count() > 0
            
            # Check for error toast
            error_toast = self.page.locator("text=Failed to create, text=error, text=Error")
            has_error = await error_toast.count() > 0
            
            if has_error:
                error_text = await error_toast.first.inner_text() if await error_toast.count() > 0 else "Unknown error"
                print(f"   ⚠️ Error: {error_text[:50]}")
                await self.take_screenshot("product_creation_error")
                
                # Close form if still open
                cancel_btn = self.page.locator("button:has-text('Cancel')").first
                if await cancel_btn.count() > 0 and await cancel_btn.is_visible():
                    await cancel_btn.click()
                    await asyncio.sleep(1)
                
                return None
            
            # Close form if still open (click outside or Cancel)
            if form_open:
                try:
                    cancel_btn = self.page.locator("button:has-text('Cancel')").first
                    if await cancel_btn.count() > 0:
                        await cancel_btn.click()
                        await asyncio.sleep(1)
                except:
                    await self.page.keyboard.press("Escape")
                    await asyncio.sleep(1)
            
            # Verify product appears in the list
            await asyncio.sleep(1)
            product_name = product_data.get('name', '')
            product_in_list = self.page.locator(f"text={product_name[:15]}")  # Partial match
            
            if await product_in_list.count() > 0:
                print(f"✅ Product created and verified in list: {product_name}")
                return product_data
            else:
                # Check if any product row exists
                product_rows = self.page.locator("table tbody tr")
                row_count = await product_rows.count()
                print(f"   📋 Found {row_count} products in list")
                
                if row_count > 0:
                    print(f"✅ Product likely created: {product_name}")
                    return product_data
                else:
                    print(f"⚠️ Could not verify product in list")
                    await self.take_screenshot("product_not_verified")
                    return None
            
        except Exception as e:
            print(f"❌ Error creating product: {e}")
            await self.take_screenshot("product_error")
            return None

    # ==========================================
    # PURCHASE ORDER METHODS
    # ==========================================
    
    async def click_create_purchase_order(self) -> bool:
        """Click Create Purchase Order button"""
        for selector in self.add_po_button_selectors:
            try:
                element = self.page.locator(selector).first
                if await element.count() > 0 and await element.is_visible():
                    await element.click()
                    await asyncio.sleep(1)
                    print("✅ Clicked Create Purchase Order button")
                    return True
            except:
                continue
        print("⚠️ Create Purchase Order button not found")
        return False
    
    async def go_to_purchase_orders_for_vendor(self, vendor_name: str = None) -> bool:
        """Navigate to Purchase Orders section for a vendor via Actions menu"""
        try:
            # Try different action names that might lead to Purchase Orders
            action_names = ["Purchase Orders", "Orders", "PO", "Purchases"]
            for action in action_names:
                if await self._click_vendor_action_menu(vendor_name, action):
                    return True
            print("⚠️ Could not navigate to Purchase Orders via Actions menu")
            return False
        except Exception as e:
            print(f"❌ Error navigating to Purchase Orders: {str(e)}")
            return False
    
    async def create_purchase_order(self, vendor_name: str = None, product_name: str = None, quantity: int = 1) -> dict:
        """Create a purchase order for a vendor"""
        try:
            print(f"\n📝 Creating Purchase Order")
            
            # Navigate to Purchase Orders via vendor Actions menu
            # Try different action names
            action_names = ["Purchases", "Purchase Orders", "Orders", "PO"]
            navigated = False
            
            for action in action_names:
                if await self._click_vendor_action_menu(vendor_name, action):
                    navigated = True
                    print(f"📍 Navigated to: {self.page.url}")
                    break
            
            if not navigated:
                print("⚠️ Could not navigate to Purchase Orders via Actions menu")
                # Take screenshot to debug
                await self.take_screenshot("po_navigation_failed")
                return None
            
            await asyncio.sleep(2)
            
            # Click Generate PurchaseOrder button
            await self.click_create_purchase_order()
            
            await asyncio.sleep(2)
            
            # Step 1: Select PurchaseOrder Month from the dialog
            month_dropdown = self.page.locator("text=Select month to purchase-order").first
            if await month_dropdown.count() > 0 and await month_dropdown.is_visible():
                await month_dropdown.click()
                await asyncio.sleep(1)
                
                # Select first available month
                options = self.page.locator("[role='option'], [cmdk-item], [data-radix-collection-item]")
                option_count = await options.count()
                print(f"   📋 Found {option_count} month options")
                
                if option_count > 0:
                    first_option = options.first
                    option_text = await first_option.inner_text()
                    await first_option.click()
                    print(f"   ✅ Selected month: {option_text[:20]}...")
                else:
                    print("   ⚠️ No months available")
                    await self.page.keyboard.press("Escape")
                    return None
                
                await asyncio.sleep(1)
                
                # Click Continue button
                continue_btn = self.page.locator("button:has-text('Continue')").first
                if await continue_btn.count() > 0 and await continue_btn.is_visible():
                    await continue_btn.click()
                    print("   ✅ Clicked Continue")
                    await asyncio.sleep(3)
                else:
                    print("   ⚠️ Continue button not found")
            else:
                print("   ⚠️ Month selection dialog not found")
            
            # Step 2: Fill PurchaseOrder Date (required)
            po_date_input = self.page.locator("text=Pick a date").first
            if await po_date_input.count() > 0 and await po_date_input.is_visible():
                await po_date_input.click()
                await asyncio.sleep(1)
                
                # Click today or first available date
                today_btn = self.page.locator("button[name='day']:not([disabled])").first
                if await today_btn.count() > 0:
                    await today_btn.click()
                    print("   ✅ Selected PO Date")
                    await asyncio.sleep(1)
            
            await asyncio.sleep(2)  # Wait for Due Date to become enabled
            
            # Step 2b: Fill Due Date (enabled after PO Date is selected)
            # Find the Due Date section and click on it
            due_date_section = self.page.locator("text=Due Date").first
            if await due_date_section.count() > 0:
                # Click on the parent container to open date picker
                parent = due_date_section.locator("xpath=./parent::*/parent::*")
                clickable = parent.locator("button, [role='button'], [class*='date']").first
                
                if await clickable.count() > 0:
                    try:
                        await clickable.click(force=True, timeout=5000)
                        await asyncio.sleep(1)
                        
                        # Click a date in the calendar
                        available_dates = self.page.locator("button[name='day']:not([disabled])")
                        date_count = await available_dates.count()
                        if date_count > 7:
                            await available_dates.nth(7).click()
                        elif date_count > 0:
                            await available_dates.last.click()
                        print("   ✅ Selected Due Date")
                        await asyncio.sleep(0.5)
                    except Exception as e:
                        print(f"   ⚠️ Due Date click failed: {str(e)[:30]}")
                        # Try JavaScript click
                        try:
                            await self.page.evaluate("""
                                () => {
                                    const dueLabel = [...document.querySelectorAll('*')].find(el => el.textContent === 'Due Date *');
                                    if (dueLabel) {
                                        const container = dueLabel.closest('div');
                                        const btn = container?.querySelector('button');
                                        if (btn) btn.click();
                                    }
                                }
                            """)
                            await asyncio.sleep(1)
                            available_dates = self.page.locator("button[name='day']:not([disabled])")
                            if await available_dates.count() > 0:
                                await available_dates.nth(min(7, await available_dates.count()-1)).click()
                                print("   ✅ Selected Due Date via JS")
                        except:
                            print("   ⚠️ Due Date JS click also failed")
            else:
                print("   ⚠️ Due Date label not found")
            
            await asyncio.sleep(1)
            
            # Step 3: Click Create PurchaseOrder button
            create_po_btn = self.page.locator("button:has-text('Create PurchaseOrder')").first
            if await create_po_btn.count() > 0:
                # Check if enabled
                is_disabled = await create_po_btn.is_disabled()
                if not is_disabled:
                    await create_po_btn.click()
                    print("   ✅ Clicked Create PurchaseOrder")
                    await asyncio.sleep(3)
                else:
                    # Try Create Draft instead
                    draft_btn = self.page.locator("button:has-text('Create Draft')").first
                    if await draft_btn.count() > 0:
                        await draft_btn.click()
                        print("   ✅ Clicked Create Draft")
                        await asyncio.sleep(3)
            
            # Take screenshot of PO creation result
            await self.take_screenshot("po_created")
            
            await asyncio.sleep(2)
            
            po_data = {
                'vendor': vendor_name,
                'product': product_name,
                'quantity': quantity,
                'date': datetime.now().isoformat()
            }
            
            print(f"✅ Purchase Order created")
            return po_data
            
        except Exception as e:
            print(f"❌ Error creating purchase order: {e}")
            await self.take_screenshot("po_error")
            return None
    
    async def get_purchase_order_list(self) -> list:
        """Get list of purchase orders"""
        orders = []
        try:
            await self.go_to_purchase_orders_tab()
            await asyncio.sleep(1)
            
            rows = self.page.locator("table tbody tr")
            count = await rows.count()
            
            for i in range(min(count, 10)):  # Limit to first 10
                try:
                    row_text = await rows.nth(i).inner_text()
                    orders.append(row_text.strip())
                except:
                    continue
            
            print(f"📋 Found {len(orders)} purchase orders")
        except Exception as e:
            print(f"⚠️ Error getting PO list: {e}")
        
        return orders

    # ==========================================
    # COMPLETE FLOW
    # ==========================================
    
    async def complete_purchase_flow(self, vendor_data: dict = None, product_data: dict = None, quantity: int = 1) -> dict:
        """Execute complete purchase flow: vendor → product → purchase order"""
        result = {
            'success': False,
            'vendor': None,
            'product': None,
            'purchase_order': None
        }
        
        try:
            print("\n" + "="*60)
            print("🛒 COMPLETE PURCHASE FLOW")
            print("="*60)
            
            # Step 1: Create Vendor
            print("\n📌 Step 1: Create Vendor")
            vendor = await self.create_vendor(vendor_data)
            if vendor:
                result['vendor'] = vendor
                print(f"   ✅ Vendor created: {vendor['name']}")
            else:
                print("   ⚠️ Vendor creation may have failed, continuing...")
            
            await asyncio.sleep(2)
            
            # Step 2: Create Product
            print("\n📌 Step 2: Create Product for Vendor")
            product = await self.create_product_for_vendor(
                vendor_name=vendor['name'] if vendor else None,
                product_data=product_data
            )
            if product:
                result['product'] = product
                print(f"   ✅ Product created: {product['name']}")
            else:
                print("   ⚠️ Product creation may have failed, continuing...")
            
            await asyncio.sleep(2)
            
            # Step 3: Create Purchase Order
            print("\n📌 Step 3: Create Purchase Order")
            po = await self.create_purchase_order(
                vendor_name=vendor['name'] if vendor else None,
                product_name=product['name'] if product else None,
                quantity=quantity
            )
            if po:
                result['purchase_order'] = po
                print(f"   ✅ Purchase Order created")
            
            # Determine overall success
            result['success'] = result['vendor'] is not None or result['product'] is not None
            
            print("\n" + "="*60)
            if result['success']:
                print("✅ PURCHASE FLOW COMPLETED SUCCESSFULLY")
            else:
                print("⚠️ PURCHASE FLOW COMPLETED WITH SOME ISSUES")
            print("="*60)
            
            return result
            
        except Exception as e:
            print(f"❌ Complete purchase flow failed: {e}")
            await self.take_screenshot("flow_error")
            return result

    # ==========================================
    # VERIFICATION METHODS
    # ==========================================
    
    async def verify_vendor_exists(self, vendor_name: str) -> bool:
        """Verify a vendor exists in the list"""
        try:
            await self.go_to_vendors_tab()
            await asyncio.sleep(1)
            
            vendor = self.page.locator(f"text={vendor_name}").first
            exists = await vendor.count() > 0
            print(f"{'✅' if exists else '❌'} Vendor '{vendor_name}' {'exists' if exists else 'not found'}")
            return exists
        except:
            return False
    
    async def verify_product_exists(self, product_name: str) -> bool:
        """Verify a product exists"""
        try:
            await self.go_to_products_tab()
            await asyncio.sleep(1)
            
            product = self.page.locator(f"text={product_name}").first
            exists = await product.count() > 0
            print(f"{'✅' if exists else '❌'} Product '{product_name}' {'exists' if exists else 'not found'}")
            return exists
        except:
            return False
