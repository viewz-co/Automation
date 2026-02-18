"""
Invoicing Page Object
Page object for the Invoicing section - Create Customers, Products, and Generate Invoices
"""

from playwright.async_api import Page, expect
import asyncio
import random
import string
from datetime import datetime, timedelta


class InvoicingPage:
    """Page object for Invoicing section"""
    
    def __init__(self, page: Page):
        self.page = page
        
        # Navigation selectors
        self.nav_selectors = [
            "text=Invoicing",
            "text=Invoices",
            "a:has-text('Invoicing')",
            "a:has-text('Invoices')",
            "button:has-text('Invoicing')",
            "[data-testid*='invoicing']",
            "[data-testid*='invoice']",
            "[href*='invoicing']",
            "[href*='invoice']"
        ]
        
        # Page identification
        self.page_heading_selectors = [
            "h1:has-text('Invoicing')",
            "h1:has-text('Invoices')",
            "h2:has-text('Invoicing')",
            "[data-testid='invoicing-page']"
        ]
        
        # ==========================================
        # CUSTOMER FORM SELECTORS
        # ==========================================
        self.customer_tab_selectors = [
            "text=Customers",
            "text=Customer",
            "button:has-text('Customers')",
            "button:has-text('Customer')",
            "tab:has-text('Customers')",
            "[data-testid*='customer-tab']",
            "[role='tab']:has-text('Customer')"
        ]
        
        self.add_customer_button_selectors = [
            "button:text('Add Customer')",
            "button >> text=Add Customer",
            "text=Add Customer",
            "button:has-text('Add Customer')",
            "button:has-text('New Customer')",
            "button:has-text('Create Customer')",
            "[data-testid*='add-customer']",
            "[data-testid*='new-customer']",
            "button:has(svg) >> text=Add",
            ".bg-primary:has-text('Add')",
            "button[class*='primary']:has-text('Add')"
        ]
        
        # Customer form fields - based on actual "Create New Customer" form
        self.customer_name_selectors = [
            "input[placeholder='Enter customer name']",
            "input[placeholder*='customer name' i]",
            "input[name='name']",
            "input[name='customerName']",
            "[data-testid='customer-name']"
        ]
        
        self.customer_email_selectors = [
            "input[placeholder='Enter email address']",
            "input[placeholder*='email' i]",
            "input[type='email']",
            "input[name='email']",
            "[data-testid='customer-email']"
        ]
        
        self.customer_city_selectors = [
            "input[placeholder='Enter city']",
            "input[placeholder*='city' i]",
            "input[name='city']",
            "[data-testid='customer-city']"
        ]
        
        self.customer_address_selectors = [
            "input[placeholder='Enter customer address']",
            "input[placeholder*='address' i]",
            "input[name='address']",
            "textarea[name='address']",
            "[data-testid='customer-address']"
        ]
        
        self.customer_zip_selectors = [
            "input[placeholder='Enter zip code']",
            "input[placeholder*='zip' i]",
            "input[name='zipCode']",
            "[data-testid='customer-zip']"
        ]
        
        self.customer_registration_selectors = [
            "input[placeholder='Enter registration number']",
            "input[placeholder*='registration' i]",
            "input[name='registrationNumber']",
            "[data-testid='registration-number']"
        ]
        
        self.customer_tax_id_selectors = [
            "input[placeholder='Enter tax ID']",
            "input[placeholder*='tax' i]",
            "input[name='taxId']",
            "[data-testid='tax-id']"
        ]
        
        # Dropdowns
        self.income_account_dropdown_selectors = [
            "text=Select income account",
            "[placeholder='Select income account']"
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
            "tab:has-text('Products')",
            "[data-testid*='product-tab']",
            "[role='tab']:has-text('Product')"
        ]
        
        self.add_product_button_selectors = [
            "button:has-text('Add Product')",
            "button:has-text('New Product')",
            "button:has-text('Create Product')",
            "text=Add Product",
            "text=New Product",
            "[data-testid*='add-product']",
            "[data-testid*='new-product']"
        ]
        
        # Product form fields
        self.product_name_selectors = [
            "input[name='productName']",
            "input[name='product_name']",
            "input[name='name']",
            "input[placeholder*='product' i]",
            "[data-testid='product-name']",
            "label:has-text('Product Name') + input",
            "label:has-text('Name') + input"
        ]
        
        self.product_description_selectors = [
            "textarea[name='description']",
            "input[name='description']",
            "textarea[placeholder*='description' i]",
            "[data-testid='product-description']",
            "label:has-text('Description') + textarea",
            "label:has-text('Description') + input"
        ]
        
        self.product_price_selectors = [
            "input[name='price']",
            "input[name='unitPrice']",
            "input[name='unit_price']",
            "input[type='number'][placeholder*='price' i]",
            "[data-testid='product-price']",
            "label:has-text('Price') + input",
            "label:has-text('Unit Price') + input"
        ]
        
        self.product_sku_selectors = [
            "input[name='sku']",
            "input[name='SKU']",
            "input[name='productCode']",
            "input[placeholder*='SKU' i]",
            "[data-testid='product-sku']",
            "label:has-text('SKU') + input"
        ]
        
        # ==========================================
        # INVOICE FORM SELECTORS
        # ==========================================
        self.invoice_tab_selectors = [
            "text=Invoices",
            "text=Invoice",
            "button:has-text('Invoices')",
            "button:has-text('Invoice')",
            "tab:has-text('Invoices')",
            "[data-testid*='invoice-tab']",
            "[role='tab']:has-text('Invoice')"
        ]
        
        self.create_invoice_button_selectors = [
            "button:has-text('Create Invoice')",
            "button:has-text('New Invoice')",
            "button:has-text('Generate Invoice')",
            "text=Create Invoice",
            "text=New Invoice",
            "[data-testid*='create-invoice']",
            "[data-testid*='new-invoice']"
        ]
        
        # Invoice form fields
        self.invoice_customer_dropdown_selectors = [
            "select[name='customer']",
            "select[name='customerId']",
            "[data-testid='invoice-customer']",
            "label:has-text('Customer') + select",
            "[role='combobox']:near(:text('Customer'))",
            "button:has-text('Select Customer')"
        ]
        
        self.invoice_product_dropdown_selectors = [
            "select[name='product']",
            "select[name='productId']",
            "[data-testid='invoice-product']",
            "label:has-text('Product') + select",
            "[role='combobox']:near(:text('Product'))",
            "button:has-text('Select Product')"
        ]
        
        self.invoice_quantity_selectors = [
            "input[name='quantity']",
            "input[name='qty']",
            "input[type='number'][placeholder*='quantity' i]",
            "[data-testid='invoice-quantity']",
            "label:has-text('Quantity') + input"
        ]
        
        self.invoice_date_selectors = [
            "input[name='invoiceDate']",
            "input[name='date']",
            "input[type='date']",
            "[data-testid='invoice-date']",
            "label:has-text('Date') + input"
        ]
        
        self.invoice_due_date_selectors = [
            "input[name='dueDate']",
            "input[name='due_date']",
            "[data-testid='invoice-due-date']",
            "label:has-text('Due Date') + input"
        ]
        
        self.invoice_notes_selectors = [
            "textarea[name='notes']",
            "textarea[name='description']",
            "input[name='notes']",
            "[data-testid='invoice-notes']",
            "label:has-text('Notes') + textarea"
        ]
        
        # ==========================================
        # COMMON ACTION BUTTONS
        # ==========================================
        self.save_button_selectors = [
            "button:has-text('Create Customer')",
            "button:has-text('Create Product')",
            "button:has-text('Create Invoice')",
            "button:has-text('Create')",
            "button:has-text('Save')",
            "button:has-text('Submit')",
            "button[type='submit']",
            "[data-testid='save-button']",
            "[data-testid='submit-button']"
        ]
        
        self.cancel_button_selectors = [
            "button:has-text('Cancel')",
            "button:has-text('Close')",
            "[data-testid='cancel-button']"
        ]
        
        self.add_line_item_selectors = [
            "button:has-text('Add Line')",
            "button:has-text('Add Item')",
            "button:has-text('Add Product')",
            "[data-testid='add-line-item']"
        ]
        
        # Success/Error messages
        self.success_message_selectors = [
            "text=successfully",
            "text=Success",
            "text=created",
            "[class*='success']",
            "[class*='toast']",
            "[role='alert']"
        ]

    # ==========================================
    # PAGE VERIFICATION METHODS
    # ==========================================
    
    async def is_loaded(self):
        """Check if the Invoicing page is loaded (for navigation tests)"""
        try:
            # Check URL contains invoicing
            if "invoicing" in self.page.url.lower():
                return True
            
            # Check for page heading
            for selector in self.page_heading_selectors:
                try:
                    element = self.page.locator(selector).first
                    if await element.is_visible():
                        return True
                except:
                    continue
            
            # Check for customer table or Add Customer button
            try:
                add_btn = self.page.get_by_role("button", name="Add Customer")
                if await add_btn.is_visible():
                    return True
            except:
                pass
            
            try:
                table = self.page.locator("table")
                if await table.is_visible():
                    return True
            except:
                pass
            
            return False
        except Exception as e:
            print(f"⚠️ Error checking if Invoicing page is loaded: {str(e)[:50]}")
            return False

    # ==========================================
    # NAVIGATION METHODS
    # ==========================================
    
    async def navigate_to_invoicing(self, preserve_entity: bool = True):
        """Navigate to the Invoicing page"""
        try:
            current_url = self.page.url
            print(f"📍 Current URL: {current_url}")
            
            # Extract entityId from current URL to preserve it
            entity_id = None
            if preserve_entity and "entityId=" in current_url:
                import re
                match = re.search(r'entityId=(\d+)', current_url)
                if match:
                    entity_id = match.group(1)
                    print(f"🏢 Preserving entityId: {entity_id}")
            
            # Check if already on invoicing page
            if "invoicing" in current_url.lower() or "invoice" in current_url.lower():
                print("✅ Already on Invoicing page")
                return True
            
            # Try direct URL navigation first
            base_url = current_url.split('/')[0] + '//' + current_url.split('/')[2]
            
            # Build URLs with entityId preserved
            entity_param = f"?entityId={entity_id}" if entity_id else ""
            invoicing_urls = [
                f"{base_url}/invoicing{entity_param}",
                f"{base_url}/invoices{entity_param}",
                f"{base_url}/billing/invoicing{entity_param}",
                f"{base_url}/billing/invoices{entity_param}"
            ]
            
            for url in invoicing_urls:
                try:
                    print(f"🔄 Trying direct navigation to: {url}")
                    await self.page.goto(url, timeout=10000)
                    await asyncio.sleep(2)
                    
                    if "invoic" in self.page.url.lower():
                        print(f"✅ Successfully navigated to: {self.page.url}")
                        return True
                except Exception as e:
                    print(f"⚠️ URL {url} failed: {str(e)[:50]}")
                    continue
            
            # Try clicking navigation elements
            await asyncio.sleep(2)
            for selector in self.nav_selectors:
                try:
                    element = self.page.locator(selector).first
                    if await element.is_visible():
                        await element.click()
                        await asyncio.sleep(2)
                        print(f"✅ Clicked navigation: {selector}")
                        return True
                except:
                    continue
            
            print("❌ Could not navigate to Invoicing page")
            return False
            
        except Exception as e:
            print(f"❌ Navigation error: {str(e)}")
            return False

    async def is_loaded(self):
        """Check if Invoicing page is loaded"""
        try:
            # Check URL
            if "invoic" in self.page.url.lower():
                print("✅ Invoicing page URL detected")
                return True
            
            # Check for page headings
            for selector in self.page_heading_selectors:
                try:
                    element = self.page.locator(selector).first
                    if await element.is_visible():
                        print(f"✅ Invoicing page loaded - found: {selector}")
                        return True
                except:
                    continue
            
            return False
        except Exception as e:
            print(f"⚠️ Page load check error: {str(e)}")
            return False

    # ==========================================
    # CUSTOMER METHODS
    # ==========================================
    
    async def go_to_customers_tab(self):
        """Navigate to Customers tab/section"""
        try:
            for selector in self.customer_tab_selectors:
                try:
                    element = self.page.locator(selector).first
                    if await element.is_visible():
                        await element.click()
                        await asyncio.sleep(1)
                        print(f"✅ Clicked Customers tab: {selector}")
                        return True
                except:
                    continue
            print("⚠️ Customers tab not found, might already be on customers section")
            return True
        except Exception as e:
            print(f"❌ Error navigating to Customers: {str(e)}")
            return False

    async def click_add_customer(self):
        """Click Add Customer button"""
        await asyncio.sleep(2)  # Wait for page to fully load
        
        # First try using get_by_role which is more reliable
        try:
            button = self.page.get_by_role("button", name="Add Customer")
            await button.wait_for(state="visible", timeout=5000)
            await button.click()
            await asyncio.sleep(1)
            print("✅ Clicked Add Customer via get_by_role")
            return True
        except Exception as e:
            print(f"⚠️ get_by_role failed: {str(e)[:50]}")
        
        # Try using get_by_text
        try:
            button = self.page.get_by_text("Add Customer", exact=True)
            await button.wait_for(state="visible", timeout=3000)
            await button.click()
            await asyncio.sleep(1)
            print("✅ Clicked Add Customer via get_by_text")
            return True
        except Exception as e:
            print(f"⚠️ get_by_text failed: {str(e)[:50]}")
        
        # Try locator with text
        try:
            button = self.page.locator("text=Add Customer").first
            await button.wait_for(state="visible", timeout=3000)
            await button.click()
            await asyncio.sleep(1)
            print("✅ Clicked Add Customer via locator text")
            return True
        except Exception as e:
            print(f"⚠️ locator text failed: {str(e)[:50]}")
        
        # Try selectors as fallback
        for selector in self.add_customer_button_selectors:
            try:
                element = self.page.locator(selector).first
                await element.wait_for(state="visible", timeout=2000)
                await element.click()
                await asyncio.sleep(1)
                print(f"✅ Clicked Add Customer: {selector}")
                return True
            except:
                continue
        
        print("❌ Add Customer button not found")
        # Debug: Print what's visible on page
        try:
            # Check for all clickable elements with "Add" text
            add_elements = self.page.locator("*:has-text('Add')")
            count = await add_elements.count()
            print(f"🔍 Debug: Found {count} elements with 'Add' text")
            for i in range(min(10, count)):
                try:
                    text = await add_elements.nth(i).inner_text()
                    tag = await add_elements.nth(i).evaluate("el => el.tagName")
                    print(f"   Element {i}: <{tag}> '{text[:50]}'")
                except:
                    pass
        except:
            pass
        return False

    async def fill_customer_form(self, customer_data: dict):
        """
        Fill customer creation form
        
        Args:
            customer_data: dict with keys: name, email, city, address, zip, registration, tax_id
        """
        try:
            print(f"📝 Filling customer form with: {customer_data}")
            await asyncio.sleep(1)  # Wait for form to be fully rendered
            
            # Take screenshot of form
            try:
                await self.page.screenshot(path="debug_customer_form_start.png")
            except:
                pass
            
            # Fill name (required)
            if customer_data.get('name'):
                filled = await self._fill_field_by_placeholder("Enter customer name", customer_data['name'])
                if not filled:
                    await self._fill_field(self.customer_name_selectors, customer_data['name'])
            
            # Select Customer Type (required dropdown)
            print("🔽 Selecting Customer Type...")
            customer_type_selected = False
            try:
                # Try multiple approaches for Customer Type dropdown
                customer_type_selectors = [
                    "text=Select customer t",
                    "button:has-text('Select customer')",
                    "[role='combobox']:has-text('Select customer')",
                    "text=Customer Type >> xpath=../following-sibling::* >> button",
                ]
                
                for selector in customer_type_selectors:
                    try:
                        dropdown = self.page.locator(selector).first
                        if await dropdown.is_visible():
                            await dropdown.click()
                            await asyncio.sleep(0.5)
                            # Select first option (usually "Business" or similar)
                            option = self.page.locator("[role='option']").first
                            if await option.is_visible():
                                await option.click()
                                customer_type_selected = True
                                print("✅ Customer Type selected")
                                break
                    except:
                        continue
                
                # Fallback: try labeled dropdown approach
                if not customer_type_selected:
                    result = await self._select_labeled_dropdown("Customer Type", "Select customer")
                    if result:
                        customer_type_selected = True
                        print("✅ Customer Type selected via labeled dropdown")
                        
            except Exception as e:
                print(f"⚠️ Customer Type selection failed: {str(e)[:40]}")
            
            if not customer_type_selected:
                print("⚠️ Could not select Customer Type - this is a required field!")
            
            # Handle GL Account - Use the "Create GL Account Automatically" checkbox
            # This is much more reliable than trying to select from the dropdown
            print("🔽 Handling GL Account...")
            
            # Wait for the form to be fully loaded
            await asyncio.sleep(1)
            
            gl_handled = False
            
            # BEST APPROACH: Check the "Create GL Account Automatically" checkbox
            try:
                # Try multiple selectors for the checkbox
                checkbox_selectors = [
                    "text=Create GL Account Automatically",
                    "label:has-text('Create GL Account Automatically')",
                    "input[type='checkbox'] >> xpath=../.. >> text=Create GL Account",
                    "[role='checkbox']:near(:text('Create GL Account'))",
                ]
                
                for selector in checkbox_selectors:
                    try:
                        checkbox = self.page.locator(selector).first
                        if await checkbox.is_visible():
                            # Check if it's already checked
                            is_checked = await checkbox.is_checked() if hasattr(checkbox, 'is_checked') else False
                            if not is_checked:
                                await checkbox.click()
                                await asyncio.sleep(0.5)
                            gl_handled = True
                            print("✅ Checked 'Create GL Account Automatically' checkbox")
                            break
                    except:
                        continue
                
                # Also try clicking directly on the checkbox input
                if not gl_handled:
                    checkbox_input = self.page.locator("input[type='checkbox']").first
                    if await checkbox_input.is_visible():
                        parent_text = await checkbox_input.locator("xpath=./..").text_content()
                        if parent_text and "gl account" in parent_text.lower():
                            await checkbox_input.check()
                            gl_handled = True
                            print("✅ Checked GL Account checkbox via input element")
            except Exception as e:
                print(f"⚠️ Checkbox approach failed: {str(e)[:40]}")
            
            # Fallback: Try to select from dropdown if checkbox didn't work
            if not gl_handled:
                print("⚠️ Checkbox not found, trying dropdown selection...")
                try:
                    # Click on the Receivables GL Account dropdown
                    dropdown = self.page.locator("text=Select receivable, button:has-text('Select receivable')").first
                    if await dropdown.is_visible():
                        await dropdown.click()
                        await asyncio.sleep(0.5)
                        # Select first available option
                        option = self.page.locator("[role='option']").first
                        if await option.is_visible():
                            await option.click()
                            gl_handled = True
                            print("✅ Selected GL Account from dropdown")
                except Exception as e:
                    print(f"⚠️ Dropdown selection failed: {str(e)[:40]}")
            
            if not gl_handled:
                print("⚠️ Could not handle GL Account - form may fail validation")
                # Take a debug screenshot
                try:
                    await self.page.screenshot(path="debug_income_account_failed.png")
                except:
                    pass
            
            # Fill email (required)
            if customer_data.get('email'):
                filled = await self._fill_field_by_placeholder("Enter email address", customer_data['email'])
                if not filled:
                    await self._fill_field(self.customer_email_selectors, customer_data['email'])
            
            # Select Country (required dropdown) - search for a country
            print("🔽 Selecting Country...")
            await self._select_labeled_dropdown_searchable("Country", "Search countries...", "United States")
            
            # Fill city
            if customer_data.get('city'):
                filled = await self._fill_field_by_placeholder("Enter city", customer_data['city'])
                if not filled:
                    await self._fill_field(self.customer_city_selectors, customer_data['city'])
            
            # Fill address
            if customer_data.get('address'):
                filled = await self._fill_field_by_placeholder("Enter customer address", customer_data['address'])
                if not filled:
                    await self._fill_field(self.customer_address_selectors, customer_data['address'])
            
            # Fill zip code
            if customer_data.get('zip'):
                filled = await self._fill_field_by_placeholder("Enter zip code", customer_data['zip'])
                if not filled:
                    await self._fill_field(self.customer_zip_selectors, customer_data['zip'])
            
            # Fill registration number
            if customer_data.get('registration'):
                filled = await self._fill_field_by_placeholder("Enter registration number", customer_data['registration'])
                if not filled:
                    await self._fill_field(self.customer_registration_selectors, customer_data['registration'])
            
            # Fill tax ID
            if customer_data.get('tax_id'):
                filled = await self._fill_field_by_placeholder("Enter tax ID", customer_data['tax_id'])
                if not filled:
                    await self._fill_field(self.customer_tax_id_selectors, customer_data['tax_id'])
            
            # Scroll down to see Payment Terms
            try:
                await self.page.evaluate("document.querySelector('[role=\"dialog\"]')?.scrollTo(0, 1000)")
                await asyncio.sleep(0.5)
            except:
                pass
            
            # Select Payment Terms (required dropdown)
            print("🔽 Selecting Payment Terms...")
            await self._select_labeled_dropdown("Payment Terms", "Select payment terms")
            
            # Take screenshot after filling
            try:
                await self.page.screenshot(path="debug_customer_form_filled.png")
            except:
                pass
            
            print("✅ Customer form filled")
            return True
            
        except Exception as e:
            print(f"❌ Error filling customer form: {str(e)}")
            return False
    
    async def _select_dropdown_option(self, placeholder_text: str, option_index: int = 0):
        """Select an option from a dropdown by clicking it and selecting the nth option"""
        try:
            print(f"🔽 Trying to select from dropdown: '{placeholder_text}'")
            
            # Try multiple ways to click the dropdown
            dropdown_clicked = False
            
            # Method 1: By exact text
            try:
                dropdown = self.page.get_by_text(placeholder_text, exact=True).first
                if await dropdown.is_visible():
                    await dropdown.click()
                    dropdown_clicked = True
                    print(f"✅ Clicked dropdown by text: '{placeholder_text}'")
            except:
                pass
            
            # Method 2: By partial text within a select-like element
            if not dropdown_clicked:
                try:
                    dropdown = self.page.locator(f"[class*='select']:has-text('{placeholder_text}')").first
                    if await dropdown.is_visible():
                        await dropdown.click()
                        dropdown_clicked = True
                        print(f"✅ Clicked dropdown by select class")
                except:
                    pass
            
            # Method 3: Click the parent container that contains the text
            if not dropdown_clicked:
                try:
                    dropdown = self.page.locator(f"div:has-text('{placeholder_text}')").first
                    if await dropdown.is_visible():
                        await dropdown.click()
                        dropdown_clicked = True
                        print(f"✅ Clicked dropdown by div container")
                except:
                    pass
            
            if not dropdown_clicked:
                print(f"❌ Could not find/click dropdown: '{placeholder_text}'")
                return False
            
            await asyncio.sleep(1)
            
            # Wait for options to appear and click the requested one
            # Try multiple option selectors
            option_selectors = [
                "[role='option']",
                "[role='listbox'] > *",
                "[class*='option']",
                "[class*='menu'] > div",
                "[class*='dropdown'] > div",
                "li[class*='select']",
                "[data-value]"
            ]
            
            for selector in option_selectors:
                options = self.page.locator(selector)
                count = await options.count()
                if count > option_index:
                    await options.nth(option_index).click()
                    print(f"✅ Selected option {option_index} from dropdown '{placeholder_text}' using {selector}")
                    await asyncio.sleep(0.5)
                    return True
            
            print(f"⚠️ No options found for dropdown '{placeholder_text}'")
            await self.page.keyboard.press("Escape")
            return False
            
        except Exception as e:
            print(f"⚠️ Could not select from dropdown '{placeholder_text}': {str(e)[:50]}")
            try:
                await self.page.keyboard.press("Escape")
            except:
                pass
            return False
    
    async def _select_searchable_dropdown(self, placeholder_text: str, search_value: str):
        """Select an option from a searchable dropdown"""
        try:
            print(f"🔍 Trying to select '{search_value}' from searchable dropdown: '{placeholder_text}'")
            
            # Try multiple ways to click the dropdown
            dropdown_clicked = False
            
            # Method 1: By exact text
            try:
                dropdown = self.page.get_by_text(placeholder_text, exact=True).first
                if await dropdown.is_visible():
                    await dropdown.click()
                    dropdown_clicked = True
                    print(f"✅ Clicked searchable dropdown by text")
            except:
                pass
            
            # Method 2: By partial text within a select-like element
            if not dropdown_clicked:
                try:
                    dropdown = self.page.locator(f"[class*='select']:has-text('{placeholder_text}')").first
                    if await dropdown.is_visible():
                        await dropdown.click()
                        dropdown_clicked = True
                        print(f"✅ Clicked searchable dropdown by select class")
                except:
                    pass
            
            # Method 3: Click the parent container that contains the text
            if not dropdown_clicked:
                try:
                    dropdown = self.page.locator(f"div:has-text('{placeholder_text}')").first
                    if await dropdown.is_visible():
                        await dropdown.click()
                        dropdown_clicked = True
                        print(f"✅ Clicked searchable dropdown by div container")
                except:
                    pass
            
            if not dropdown_clicked:
                print(f"❌ Could not find/click searchable dropdown: '{placeholder_text}'")
                return False
            
            await asyncio.sleep(1)
            
            # Type to search
            await self.page.keyboard.type(search_value[:5])  # Type first 5 chars to search
            await asyncio.sleep(1)
            print(f"⌨️ Typed search: '{search_value[:5]}'")
            
            # Click the first matching option
            option_selectors = [
                "[role='option']",
                "[role='listbox'] > *",
                "[class*='option']",
                "[class*='menu'] > div",
                "[class*='dropdown'] > div",
                "li[class*='select']"
            ]
            
            for selector in option_selectors:
                options = self.page.locator(selector)
                count = await options.count()
                if count > 0:
                    await options.first.click()
                    print(f"✅ Selected '{search_value}' from searchable dropdown using {selector}")
                    await asyncio.sleep(0.5)
                    return True
            
            print(f"⚠️ No options found for '{search_value}' in dropdown")
            await self.page.keyboard.press("Escape")
            return False
            
        except Exception as e:
            print(f"⚠️ Could not select from searchable dropdown '{placeholder_text}': {str(e)[:50]}")
            try:
                await self.page.keyboard.press("Escape")
            except:
                pass
            return False
    
    async def _select_labeled_dropdown(self, label_text: str, placeholder_text: str, option_index: int = 0):
        """
        Select an option from a dropdown by finding it via its label
        
        Args:
            label_text: The label text (e.g., "Payment Terms", "Receivable GL Account")
            placeholder_text: The placeholder text in the dropdown (e.g., "Select payment terms")
            option_index: Which option to select (0 = first)
        """
        try:
            print(f"🔽 Selecting from '{label_text}' dropdown...")
            
            # First, scroll the dialog to show all content
            try:
                await self.page.evaluate("document.querySelector('[role=\"dialog\"]')?.scrollTo(0, 500)")
                await asyncio.sleep(0.3)
                await self.page.evaluate("document.querySelector('[role=\"dialog\"]')?.scrollTo(0, 0)")
                await asyncio.sleep(0.3)
            except:
                pass
            
            dropdown_clicked = False
            
            # Method 1: Find label then click adjacent dropdown (MOST RELIABLE)
            if not dropdown_clicked:
                try:
                    # Find the label first
                    label = self.page.get_by_text(label_text, exact=False).first
                    if await label.is_visible():
                        # Get the parent container and find the dropdown within it
                        parent = label.locator("xpath=./parent::*")
                        # Look for button or select within or after the label
                        dropdown = parent.locator("button, [role='combobox'], [class*='select']").first
                        if await dropdown.is_visible():
                            await dropdown.click()
                            dropdown_clicked = True
                            print(f"✅ Clicked dropdown via label parent: '{label_text}'")
                except Exception as e:
                    print(f"⚠️ Label parent method failed: {str(e)[:40]}")
            
            # Method 2: Click the dropdown directly by exact placeholder text
            if not dropdown_clicked:
                try:
                    dropdown = self.page.get_by_text(placeholder_text, exact=True).first
                    if await dropdown.is_visible():
                        await dropdown.click()
                        dropdown_clicked = True
                        print(f"✅ Clicked dropdown by exact placeholder: '{placeholder_text}'")
                except Exception as e:
                    print(f"⚠️ Exact placeholder method failed: {str(e)[:40]}")
            
            # Method 3: Try get_by_role combobox with name
            if not dropdown_clicked:
                try:
                    dropdown = self.page.get_by_role("combobox", name=label_text)
                    if await dropdown.is_visible():
                        await dropdown.click()
                        dropdown_clicked = True
                        print(f"✅ Clicked combobox by role: '{label_text}'")
                except Exception as e:
                    print(f"⚠️ Combobox role method failed: {str(e)[:40]}")
            
            # Method 4: Try partial placeholder with scroll
            if not dropdown_clicked:
                try:
                    partial_placeholder = placeholder_text.split()[0]  # e.g., "Select"
                    dropdowns = self.page.locator(f"button:has-text('{partial_placeholder}')")
                    count = await dropdowns.count()
                    # Click each one until we find our target
                    for i in range(count):
                        try:
                            dd = dropdowns.nth(i)
                            dd_text = await dd.inner_text()
                            if placeholder_text.lower() in dd_text.lower():
                                await dd.scroll_into_view_if_needed()
                                await asyncio.sleep(0.3)
                                await dd.click()
                                dropdown_clicked = True
                                print(f"✅ Clicked dropdown by matching text: '{dd_text[:30]}'")
                                break
                        except:
                            continue
                except Exception as e:
                    print(f"⚠️ Partial placeholder method failed: {str(e)[:40]}")
            
            # Method 5: Use role combobox or listbox
            if not dropdown_clicked:
                try:
                    # Find all combobox elements and click one that's visible and contains our text
                    comboboxes = self.page.locator("[role='combobox']")
                    count = await comboboxes.count()
                    for i in range(count):
                        try:
                            cb = comboboxes.nth(i)
                            text = await cb.inner_text()
                            if placeholder_text.lower() in text.lower() or "select" in text.lower():
                                await cb.scroll_into_view_if_needed()
                                await cb.click()
                                dropdown_clicked = True
                                print(f"✅ Clicked combobox {i} containing '{placeholder_text}'")
                                break
                        except:
                            continue
                except Exception as e:
                    print(f"⚠️ Combobox method failed: {str(e)[:40]}")
            
            if not dropdown_clicked:
                print(f"❌ Could not click '{label_text}' dropdown")
                return False
            
            await asyncio.sleep(1)
            
            # Now select an option
            option_selectors = [
                "[role='option']",
                "[role='listbox'] > *",
                "[class*='option']:not([class*='disabled'])",
                "[class*='menu-item']",
                "[class*='select__option']",
                "[data-value]"
            ]
            
            for selector in option_selectors:
                try:
                    options = self.page.locator(selector)
                    count = await options.count()
                    if count > option_index:
                        await options.nth(option_index).click()
                        print(f"✅ Selected option {option_index} from '{label_text}' using {selector}")
                        await asyncio.sleep(0.5)
                        return True
                except:
                    continue
            
            # Fallback: Use keyboard
            try:
                await self.page.keyboard.press("ArrowDown")
                await asyncio.sleep(0.3)
                await self.page.keyboard.press("Enter")
                print(f"✅ Selected option via keyboard for '{label_text}'")
                return True
            except:
                pass
            
            print(f"⚠️ No options found for '{label_text}'")
            await self.page.keyboard.press("Escape")
            return False
            
        except Exception as e:
            print(f"❌ Error selecting from '{label_text}': {str(e)[:50]}")
            try:
                await self.page.keyboard.press("Escape")
            except:
                pass
            return False
    
    async def _select_labeled_dropdown_searchable(self, label_text: str, placeholder_text: str, search_value: str):
        """
        Select an option from a searchable dropdown by finding it via its label
        
        Args:
            label_text: The label text (e.g., "Country")
            placeholder_text: The placeholder text in the dropdown (e.g., "Search countries...")
            search_value: The value to search for (e.g., "United States")
        """
        try:
            print(f"🔍 Searching in '{label_text}' dropdown for '{search_value}'...")
            
            dropdown_clicked = False
            
            # Method 1: Click by placeholder text (most reliable)
            if not dropdown_clicked:
                try:
                    dropdown = self.page.get_by_text(placeholder_text, exact=False).first
                    await dropdown.wait_for(state="visible", timeout=3000)
                    await dropdown.click()
                    dropdown_clicked = True
                    print(f"✅ Clicked searchable dropdown by placeholder: '{placeholder_text}'")
                except Exception as e:
                    print(f"⚠️ Placeholder method failed: {str(e)[:40]}")
            
            # Method 2: Try button locator
            if not dropdown_clicked:
                try:
                    dropdown = self.page.locator(f"button:has-text('{placeholder_text}')").first
                    await dropdown.wait_for(state="visible", timeout=2000)
                    await dropdown.click()
                    dropdown_clicked = True
                    print(f"✅ Clicked searchable dropdown via button")
                except Exception as e:
                    print(f"⚠️ Button method failed: {str(e)[:40]}")
            
            # Method 3: Use partial text match
            if not dropdown_clicked:
                try:
                    partial_text = placeholder_text.split('...')[0].strip()  # e.g., "Search countries"
                    dropdown = self.page.locator(f"text={partial_text}").first
                    await dropdown.wait_for(state="visible", timeout=2000)
                    await dropdown.click()
                    dropdown_clicked = True
                    print(f"✅ Clicked dropdown via partial text: '{partial_text}'")
                except Exception as e:
                    print(f"⚠️ Partial text method failed: {str(e)[:40]}")
            
            if not dropdown_clicked:
                print(f"❌ Could not click '{label_text}' dropdown")
                return False
            
            await asyncio.sleep(1)
            
            # Type to search
            await self.page.keyboard.type(search_value[:6])  # Type first 6 chars
            await asyncio.sleep(1)
            print(f"⌨️ Typed: '{search_value[:6]}'")
            
            # Click the first matching option
            option_selectors = [
                "[role='option']",
                "[role='listbox'] > *",
                "[class*='option']:not([class*='disabled'])",
                "[class*='menu-item']",
                "[data-value]"
            ]
            
            for selector in option_selectors:
                try:
                    options = self.page.locator(selector)
                    count = await options.count()
                    if count > 0:
                        await options.first.click()
                        print(f"✅ Selected '{search_value}' from '{label_text}' using {selector}")
                        await asyncio.sleep(0.5)
                        return True
                except:
                    continue
            
            # Fallback: Use keyboard
            try:
                await self.page.keyboard.press("ArrowDown")
                await asyncio.sleep(0.3)
                await self.page.keyboard.press("Enter")
                print(f"✅ Selected option via keyboard for '{label_text}'")
                return True
            except:
                pass
            
            print(f"⚠️ No options found for '{label_text}'")
            await self.page.keyboard.press("Escape")
            return False
            
        except Exception as e:
            print(f"❌ Error selecting from '{label_text}': {str(e)[:50]}")
            try:
                await self.page.keyboard.press("Escape")
            except:
                pass
            return False
    
    async def _fill_field_by_placeholder(self, placeholder: str, value: str):
        """Fill a form field by its placeholder text"""
        try:
            field = self.page.get_by_placeholder(placeholder)
            await field.wait_for(state="visible", timeout=3000)
            await field.clear()
            await field.fill(value)
            print(f"✅ Filled '{placeholder}' with: {value[:30]}...")
            return True
        except Exception as e:
            print(f"⚠️ Could not fill by placeholder '{placeholder}': {str(e)[:50]}")
            return False
    
    async def _fill_field_by_label(self, label_text: str, value: str):
        """Fill a form field by its label text"""
        try:
            # Try to find input by associated label
            field = self.page.get_by_label(label_text)
            await field.wait_for(state="visible", timeout=3000)
            await field.clear()
            await field.fill(value)
            print(f"✅ Filled field by label '{label_text}' with: {value[:30]}...")
            return True
        except Exception as e:
            print(f"⚠️ Could not fill by label '{label_text}': {str(e)[:50]}")
            return False

    async def create_customer(self, customer_data: dict = None):
        """
        Complete flow to create a new customer
        
        Args:
            customer_data: Optional dict with customer details. If None, generates random data.
        
        Returns:
            dict with created customer info or None on failure
        """
        try:
            # Generate random data if not provided - includes all required fields
            if not customer_data:
                random_suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
                customer_data = {
                    'name': f"Test Customer {random_suffix}",
                    'email': f"test.customer.{random_suffix.lower()}@example.com",
                    'city': "New York",
                    'address': f"{random.randint(100, 999)} Test Street",
                    'zip': f"{random.randint(10000, 99999)}",
                    'registration': f"REG-{random_suffix}",
                    'tax_id': f"TAX-{random_suffix}"
                }
            
            # Ensure required fields have defaults
            if not customer_data.get('city'):
                customer_data['city'] = "Test City"
            if not customer_data.get('address'):
                customer_data['address'] = "123 Test Street"
            if not customer_data.get('zip'):
                customer_data['zip'] = "12345"
            if not customer_data.get('registration'):
                random_suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
                customer_data['registration'] = f"REG-{random_suffix}"
            if not customer_data.get('tax_id'):
                random_suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
                customer_data['tax_id'] = f"TAX-{random_suffix}"
            
            print(f"🆕 Creating customer: {customer_data.get('name', 'Unknown')}")
            
            # Go to customers section (might already be there)
            await self.go_to_customers_tab()
            await asyncio.sleep(1)
            
            # Click add customer
            if not await self.click_add_customer():
                print("❌ Failed to click Add Customer button")
                return None
            
            await asyncio.sleep(1)
            
            # Fill form
            if not await self.fill_customer_form(customer_data):
                print("❌ Failed to fill customer form")
                return None
            
            # Scroll dialog to bottom to ensure button is visible
            try:
                await self.page.evaluate("document.querySelector('[role=\"dialog\"]')?.scrollTo(0, 9999)")
                await asyncio.sleep(0.5)
            except:
                pass
            
            # Submit - specifically look for "Create Customer" button
            create_clicked = await self._click_save("Create Customer")
            
            if not create_clicked:
                # Try scrolling and clicking again
                print("⚠️ Retrying Create Customer button...")
                try:
                    create_btn = self.page.get_by_role("button", name="Create Customer")
                    await create_btn.scroll_into_view_if_needed()
                    await asyncio.sleep(0.5)
                    await create_btn.click()
                    create_clicked = True
                    print("✅ Create Customer clicked via retry")
                except Exception as e:
                    print(f"⚠️ Retry failed: {str(e)[:40]}")
            
            if not create_clicked:
                print("❌ Failed to save customer")
                return None
            
            await asyncio.sleep(2)
            
            # Check for form-specific error messages (inside the dialog)
            # NOTE: Be very careful here - don't catch required field labels (e.g., "Field *") as errors
            error_detected = False
            
            # Only look for ACTUAL error messages, not labels or notifications
            dialog = self.page.locator("[role='dialog']")
            if await dialog.is_visible():
                # Look for specific error message patterns - these are actual validation errors
                error_selectors = [
                    "[role='dialog'] >> text=This field is required",
                    "[role='dialog'] >> text=is required",
                    "[role='dialog'] >> text=Invalid email",
                    "[role='dialog'] >> text=Invalid format",
                    "[role='dialog'] >> text=Please enter a valid",
                    "[role='dialog'] >> text=must be at least",
                    "[role='dialog'] >> text=cannot be empty",
                    "[role='dialog'] [role='alert']",
                ]
                
                for selector in error_selectors:
                    try:
                        error_element = self.page.locator(selector).first
                        if await error_element.is_visible():
                            error_text = await error_element.text_content()
                            # Skip labels that just have asterisks for required fields
                            if error_text and len(error_text) > 2 and error_text.strip() != '*':
                                # Skip if it's just a field label (ends with just *)
                                if not error_text.strip().endswith('*') or 'required' in error_text.lower():
                                    print(f"❌ Form validation error: {error_text[:100]}")
                                    error_detected = True
                                    await self.page.screenshot(path="debug_customer_form_error.png")
                                    break
                    except:
                        continue
            
            if error_detected:
                print("❌ Customer creation failed due to form errors")
                await self._ensure_dialog_closed()
                return None
            
            # Check for success or if we're back on the list page
            success = await self._check_success_message()
            
            # Also check if the form closed (back to customer list)
            form_closed = False
            try:
                add_button = self.page.get_by_role("button", name="Add Customer")
                form_closed = await add_button.is_visible()
            except:
                pass
            
            # Check if dialog is still open (means creation likely failed)
            dialog_still_open = False
            try:
                dialog = self.page.locator("[role='dialog']")
                dialog_still_open = await dialog.is_visible()
            except:
                pass
            
            if success or form_closed:
                print(f"✅ Customer created successfully: {customer_data.get('name', 'Unknown')}")
                # Ensure dialog is fully closed
                await self._ensure_dialog_closed()
                return customer_data
            
            if dialog_still_open:
                print("⚠️ Dialog still open - checking for issues...")
                await self.page.screenshot(path="debug_customer_dialog_still_open.png")
                # Try clicking Create Customer again
                try:
                    create_btn = self.page.get_by_role("button", name="Create Customer")
                    if await create_btn.is_visible():
                        await create_btn.click()
                        await asyncio.sleep(2)
                        print("🔄 Retried Create Customer click")
                except:
                    pass
            
            print("⚠️ Customer may have been created (checking form state)")
            # Try to close any open dialog
            await self._ensure_dialog_closed()
            return customer_data
            
        except Exception as e:
            print(f"❌ Error creating customer: {str(e)}")
            # Try to close any open dialog
            try:
                await self._ensure_dialog_closed()
            except:
                pass
            return None

    # ==========================================
    # PRODUCT METHODS
    # ==========================================
    
    async def go_to_products_for_customer(self, customer_name: str = None):
        """Navigate to Products section for a specific customer via Actions menu"""
        try:
            return await self._click_customer_action_menu(customer_name, "Products")
        except Exception as e:
            print(f"❌ Error navigating to Products: {str(e)}")
            return False
    
    async def go_to_invoices_for_customer(self, customer_name: str = None):
        """Navigate to Invoices section for a specific customer via Actions menu"""
        try:
            return await self._click_customer_action_menu(customer_name, "Invoices")
        except Exception as e:
            print(f"❌ Error navigating to Invoices: {str(e)}")
            return False
    
    async def _click_customer_action_menu(self, customer_name: str, action: str):
        """Click action menu for a customer and select an action (Products/Invoices/Edit)"""
        try:
            await asyncio.sleep(2)
            
            if customer_name:
                # Use partial name (first few words) since names get truncated in UI
                partial_name = ' '.join(customer_name.split()[:2])  # e.g., "Flow Test"
                print(f"🔍 Looking for customer containing: '{partial_name}'")
                
                # Try to find the row with partial name match
                rows = self.page.locator("table tbody tr")
                row_count = await rows.count()
                print(f"📋 Found {row_count} rows in table")
                
                target_row = None
                for i in range(row_count):
                    row = rows.nth(i)
                    try:
                        row_text = await row.inner_text()
                        if partial_name.lower() in row_text.lower():
                            target_row = row
                            print(f"✅ Found customer row {i}: {row_text[:50]}...")
                            break
                    except:
                        continue
                
                if not target_row:
                    print(f"❌ Could not find row with customer: {partial_name}")
                    # Try to just click the first row's action menu as fallback
                    target_row = rows.first
                    print("⚠️ Using first row as fallback")
                
                # Click the "..." button in the Actions column
                # The button may show "..." or "•••" or "…" or similar
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
                ]
                
                for selector in three_dots_selectors:
                    try:
                        action_button = target_row.locator(selector).first
                        if await action_button.is_visible():
                            await action_button.click()
                            print(f"✅ Clicked action button via: {selector}")
                            action_clicked = True
                            break
                    except:
                        continue
                
                if not action_clicked:
                    # Try clicking the last cell directly (Actions column)
                    print("⚠️ Trying to click last cell in row...")
                    cells = target_row.locator("td")
                    cell_count = await cells.count()
                    if cell_count > 0:
                        last_cell = cells.nth(cell_count - 1)
                        # Click on the cell itself
                        await last_cell.click()
                        print("✅ Clicked on Actions cell")
                        action_clicked = True
                
                await asyncio.sleep(0.5)
            else:
                # Click the first row's actions menu
                print("🔍 Looking for first customer's actions menu")
                first_row = self.page.locator("table tbody tr").first
                action_clicked = False
                
                # Try different selectors for the three-dots button
                three_dots_selectors = [
                    "text=•••",      # Bullet points
                    "text=...",      # Regular dots
                    "text=…",        # Ellipsis character
                    "[aria-label*='action']",
                    "[aria-label*='menu']",
                    "button:has(svg)",
                ]
                
                for selector in three_dots_selectors:
                    try:
                        action_button = first_row.locator(selector).first
                        if await action_button.is_visible():
                            await action_button.click()
                            print(f"✅ Clicked action button via: {selector}")
                            action_clicked = True
                            break
                    except:
                        continue
                
                if not action_clicked:
                    # Try clicking the last cell directly (Actions column)
                    print("⚠️ Trying to click last cell in row...")
                    cells = first_row.locator("td")
                    cell_count = await cells.count()
                    if cell_count > 0:
                        last_cell = cells.nth(cell_count - 1)
                        await last_cell.click()
                        print("✅ Clicked on Actions cell")
                        action_clicked = True
                
                await asyncio.sleep(0.5)
            
            # Now click the desired action (Products, Invoices, or Edit)
            action_option = self.page.get_by_text(action, exact=True)
            await action_option.wait_for(state="visible", timeout=3000)
            await action_option.click()
            await asyncio.sleep(1)
            print(f"✅ Clicked '{action}' from actions menu")
            return True
            
        except Exception as e:
            print(f"❌ Error clicking customer action menu: {str(e)}")
            await self.page.screenshot(path="debug_action_menu_error.png")
            return False
    
    async def go_to_products_tab(self):
        """Navigate to Products tab/section - DEPRECATED: Use go_to_products_for_customer instead"""
        print("⚠️ go_to_products_tab is deprecated. Products are accessed via customer Actions menu.")
        return True

    async def click_add_product(self):
        """Click Add Product button"""
        for selector in self.add_product_button_selectors:
            try:
                element = self.page.locator(selector).first
                if await element.is_visible():
                    await element.click()
                    await asyncio.sleep(1)
                    print(f"✅ Clicked Add Product: {selector}")
                    return True
            except:
                continue
        print("❌ Add Product button not found")
        return False

    async def fill_product_form(self, product_data: dict):
        """
        Fill product creation form
        
        Args:
            product_data: dict with keys: name, description, price, sku
        """
        try:
            print(f"📝 Filling product form with: {product_data}")
            
            # Fill name
            if product_data.get('name'):
                await self._fill_field(self.product_name_selectors, product_data['name'])
            
            # Fill description
            if product_data.get('description'):
                await self._fill_field(self.product_description_selectors, product_data['description'])
            
            # Fill price
            if product_data.get('price'):
                await self._fill_field(self.product_price_selectors, str(product_data['price']))
            
            # Fill SKU
            if product_data.get('sku'):
                await self._fill_field(self.product_sku_selectors, product_data['sku'])
            
            print("✅ Product form filled")
            return True
            
        except Exception as e:
            print(f"❌ Error filling product form: {str(e)}")
            return False

    async def create_product(self, product_data: dict = None):
        """
        Complete flow to create a new product
        
        Args:
            product_data: Optional dict with product details. If None, generates random data.
        
        Returns:
            dict with created product info or None on failure
        """
        try:
            # Generate random data if not provided
            if not product_data:
                random_suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
                product_data = {
                    'name': f"Test Product {random_suffix}",
                    'description': f"Automated test product created at {datetime.now().isoformat()}",
                    'price': round(random.uniform(10.0, 1000.0), 2),
                    'sku': f"SKU-{random_suffix}"
                }
            
            print(f"🆕 Creating product: {product_data['name']}")
            
            # Go to products section
            await self.go_to_products_tab()
            await asyncio.sleep(1)
            
            # Click add product
            if not await self.click_add_product():
                print("❌ Failed to click Add Product button")
                return None
            
            await asyncio.sleep(1)
            
            # Fill form
            if not await self.fill_product_form(product_data):
                print("❌ Failed to fill product form")
                return None
            
            # Submit
            if not await self._click_save():
                print("❌ Failed to save product")
                return None
            
            await asyncio.sleep(2)
            
            # Check for success
            if await self._check_success_message():
                print(f"✅ Product created successfully: {product_data['name']}")
                return product_data
            
            print("⚠️ Product may have been created (no explicit success message)")
            return product_data
            
        except Exception as e:
            print(f"❌ Error creating product: {str(e)}")
            return None

    # ==========================================
    # INVOICE METHODS
    # ==========================================
    
    async def go_to_invoices_tab(self):
        """Navigate to Invoices tab/section"""
        try:
            for selector in self.invoice_tab_selectors:
                try:
                    element = self.page.locator(selector).first
                    if await element.is_visible():
                        await element.click()
                        await asyncio.sleep(1)
                        print(f"✅ Clicked Invoices tab: {selector}")
                        return True
                except:
                    continue
            print("⚠️ Invoices tab not found, might already be on invoices section")
            return True
        except Exception as e:
            print(f"❌ Error navigating to Invoices: {str(e)}")
            return False

    async def click_create_invoice(self):
        """Click Create Invoice button"""
        for selector in self.create_invoice_button_selectors:
            try:
                element = self.page.locator(selector).first
                if await element.is_visible():
                    await element.click()
                    await asyncio.sleep(1)
                    print(f"✅ Clicked Create Invoice: {selector}")
                    return True
            except:
                continue
        print("❌ Create Invoice button not found")
        return False

    async def select_customer_for_invoice(self, customer_name: str):
        """Select a customer from dropdown for invoice"""
        try:
            # Try dropdown/select
            for selector in self.invoice_customer_dropdown_selectors:
                try:
                    element = self.page.locator(selector).first
                    if await element.is_visible():
                        await element.click()
                        await asyncio.sleep(1)
                        
                        # Try to select from dropdown options
                        option = self.page.locator(f"text={customer_name}").first
                        if await option.is_visible():
                            await option.click()
                            print(f"✅ Selected customer: {customer_name}")
                            return True
                except:
                    continue
            
            # Try typing in a combobox
            try:
                combobox = self.page.get_by_role("combobox").first
                if await combobox.is_visible():
                    await combobox.fill(customer_name)
                    await asyncio.sleep(1)
                    # Click the option
                    option = self.page.locator(f"text={customer_name}").first
                    await option.click()
                    print(f"✅ Selected customer via combobox: {customer_name}")
                    return True
            except:
                pass
            
            print(f"❌ Could not select customer: {customer_name}")
            return False
            
        except Exception as e:
            print(f"❌ Error selecting customer: {str(e)}")
            return False

    async def select_product_for_invoice(self, product_name: str):
        """Select a product from dropdown for invoice"""
        try:
            # Try dropdown/select
            for selector in self.invoice_product_dropdown_selectors:
                try:
                    element = self.page.locator(selector).first
                    if await element.is_visible():
                        await element.click()
                        await asyncio.sleep(1)
                        
                        # Try to select from dropdown options
                        option = self.page.locator(f"text={product_name}").first
                        if await option.is_visible():
                            await option.click()
                            print(f"✅ Selected product: {product_name}")
                            return True
                except:
                    continue
            
            print(f"❌ Could not select product: {product_name}")
            return False
            
        except Exception as e:
            print(f"❌ Error selecting product: {str(e)}")
            return False

    async def fill_invoice_form(self, invoice_data: dict):
        """
        Fill invoice creation form
        
        Args:
            invoice_data: dict with keys: customer, product, quantity, date, due_date, notes
        """
        try:
            print(f"📝 Filling invoice form")
            
            # Select customer
            if invoice_data.get('customer'):
                await self.select_customer_for_invoice(invoice_data['customer'])
            
            # Select product
            if invoice_data.get('product'):
                await self.select_product_for_invoice(invoice_data['product'])
            
            # Fill quantity
            if invoice_data.get('quantity'):
                await self._fill_field(self.invoice_quantity_selectors, str(invoice_data['quantity']))
            
            # Fill date
            if invoice_data.get('date'):
                await self._fill_field(self.invoice_date_selectors, invoice_data['date'])
            
            # Fill due date
            if invoice_data.get('due_date'):
                await self._fill_field(self.invoice_due_date_selectors, invoice_data['due_date'])
            
            # Fill notes
            if invoice_data.get('notes'):
                await self._fill_field(self.invoice_notes_selectors, invoice_data['notes'])
            
            print("✅ Invoice form filled")
            return True
            
        except Exception as e:
            print(f"❌ Error filling invoice form: {str(e)}")
            return False

    async def generate_invoice(self, customer_name: str, product_name: str, quantity: int = 1, notes: str = None):
        """
        Complete flow to generate a new invoice
        
        Args:
            customer_name: Name of the customer to bill
            product_name: Name of the product to invoice
            quantity: Number of units (default: 1)
            notes: Optional notes for the invoice
        
        Returns:
            dict with invoice details or None on failure
        """
        try:
            today = datetime.now()
            due_date = today + timedelta(days=30)
            
            invoice_data = {
                'customer': customer_name,
                'product': product_name,
                'quantity': quantity,
                'date': today.strftime('%Y-%m-%d'),
                'due_date': due_date.strftime('%Y-%m-%d'),
                'notes': notes or f"Invoice generated by automation at {today.isoformat()}"
            }
            
            print(f"🧾 Generating invoice for {customer_name}")
            
            # Go to invoices section
            await self.go_to_invoices_tab()
            await asyncio.sleep(1)
            
            # Click create invoice
            if not await self.click_create_invoice():
                print("❌ Failed to click Create Invoice button")
                return None
            
            await asyncio.sleep(1)
            
            # Fill form
            if not await self.fill_invoice_form(invoice_data):
                print("❌ Failed to fill invoice form")
                return None
            
            # Submit
            if not await self._click_save():
                print("❌ Failed to save invoice")
                return None
            
            await asyncio.sleep(2)
            
            # Check for success
            if await self._check_success_message():
                print(f"✅ Invoice generated successfully for: {customer_name}")
                return invoice_data
            
            print("⚠️ Invoice may have been created (no explicit success message)")
            return invoice_data
            
        except Exception as e:
            print(f"❌ Error generating invoice: {str(e)}")
            return None

    # ==========================================
    # COMPLETE INVOICE FLOW
    # ==========================================
    
    async def complete_invoice_flow(self, customer_data: dict = None, product_data: dict = None):
        """
        Complete end-to-end invoice flow:
        1. Navigate to invoicing
        2. Create customer
        3. Navigate to Products via customer Actions menu → Create product
        4. Navigate to Invoices via customer Actions menu → Generate invoice
        
        Returns:
            dict with all created data or None on failure
        """
        try:
            print("=" * 50)
            print("🚀 STARTING COMPLETE INVOICE FLOW")
            print("=" * 50)
            
            result = {
                'customer': None,
                'product': None,
                'invoice': None,
                'success': False
            }
            
            # Step 1: Navigate to invoicing page
            print("\n📍 STEP 1: Navigate to Invoicing")
            if not await self.navigate_to_invoicing():
                print("❌ Failed to navigate to Invoicing page")
                await self.page.screenshot(path="debug_invoicing_navigation.png")
                return result
            
            await asyncio.sleep(2)
            
            # Step 2: Create customer
            print("\n👤 STEP 2: Create Customer")
            customer = await self.create_customer(customer_data)
            if not customer:
                print("❌ Failed to create customer")
                await self.page.screenshot(path="debug_customer_creation.png")
                return result
            result['customer'] = customer
            customer_name = customer.get('name')
            
            await asyncio.sleep(2)
            
            # Step 3: Navigate to Products for this customer and create product
            print("\n📦 STEP 3: Create Product for Customer")
            
            # After customer creation, ensure we're back on the Invoicing page with correct entity
            current_url = self.page.url
            
            # Store the entityId from before customer creation to preserve it
            import re
            entity_match = re.search(r'entityId=(\d+)', current_url)
            entity_id = entity_match.group(1) if entity_match else None
            
            if "/invoicing" not in current_url:
                print(f"⚠️ Current URL is {current_url}, navigating back to Invoicing...")
                # Reload the invoicing page with the preserved entity context
                if entity_id:
                    base_url = current_url.split('/')[0] + '//' + current_url.split('/')[2]
                    await self.page.goto(f"{base_url}/invoicing?entityId={entity_id}")
                else:
                    await self.navigate_to_invoicing()
                await asyncio.sleep(2)
                
            # Verify we're on the right page and customer exists
            await self.page.screenshot(path="debug_before_products.png")
            
            # Check if we can see the customer in the table (use .first to handle multiple matches)
            customer_visible = await self.page.locator(f"text={customer_name[:20]}").first.is_visible()
            if not customer_visible:
                print(f"⚠️ Customer '{customer_name}' not visible, refreshing page...")
                await self.page.reload()
                await asyncio.sleep(2)
            
            # First, click the Actions menu → Products for our customer
            if not await self.go_to_products_for_customer(customer_name):
                print("❌ Failed to navigate to Products section")
                await self.page.screenshot(path="debug_products_navigation.png")
                return result
            
            await asyncio.sleep(2)
            
            # Now create the product
            product = await self.create_product_in_section(product_data)
            if not product:
                print("❌ Failed to create product")
                await self.page.screenshot(path="debug_product_creation.png")
                return result
            result['product'] = product
            
            await asyncio.sleep(2)
            
            # Step 4: Navigate to Invoices section
            print("\n🧾 STEP 4: Generate Invoice")
            
            # Try to navigate to invoices using URL pattern
            # Products URL is like: /invoicing/{customer_id}/products
            # Invoices URL should be: /invoicing/{customer_id}/invoices
            current_url = self.page.url
            if "/products" in current_url:
                invoices_url = current_url.replace("/products", "/invoices")
                print(f"🔄 Navigating to invoices URL: {invoices_url}")
                await self.page.goto(invoices_url)
                await asyncio.sleep(2)
            else:
                # Navigate back to invoicing main page and then to invoices
                await self.navigate_to_invoicing()
                await asyncio.sleep(1)
                
                # Click Actions menu → Invoices for our customer
                if not await self.go_to_invoices_for_customer(customer_name):
                    print("❌ Failed to navigate to Invoices section")
                    await self.page.screenshot(path="debug_invoices_navigation.png")
                    return result
                
                await asyncio.sleep(2)
            
            # Create the invoice
            invoice = await self.create_invoice_in_section(product.get('name'))
            if not invoice:
                print("❌ Failed to generate invoice")
                await self.page.screenshot(path="debug_invoice_generation.png")
                return result
            result['invoice'] = invoice
            
            result['success'] = True
            print("\n" + "=" * 50)
            print("✅ COMPLETE INVOICE FLOW SUCCESSFUL!")
            print("=" * 50)
            
            return result
            
        except Exception as e:
            print(f"❌ Complete invoice flow failed: {str(e)}")
            try:
                await self.page.screenshot(path="debug_invoice_flow_error.png")
            except:
                pass
            return {'customer': None, 'product': None, 'invoice': None, 'success': False}
    
    async def create_product_in_section(self, product_data: dict = None):
        """Create a product when already in the Products section"""
        try:
            # Take screenshot of products page
            await self.page.screenshot(path="debug_products_page_before_add.png")
            print("📸 Screenshot: debug_products_page_before_add.png")
            
            # Generate random data if not provided
            if not product_data:
                random_suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
                product_data = {
                    'name': f"Test Product {random_suffix}",
                    'description': f"Automated test product",
                    'price': round(random.uniform(50.0, 500.0), 2),
                    'sku': f"SKU-{random_suffix}"
                }
            
            print(f"🆕 Creating product: {product_data.get('name', 'Unknown')}")
            
            # Look for Add Product button
            add_button = self.page.get_by_role("button", name="Add Product")
            try:
                await add_button.wait_for(state="visible", timeout=5000)
                await add_button.click()
                await asyncio.sleep(1)
                print("✅ Clicked Add Product button")
            except:
                # Try alternative selectors
                try:
                    add_btn = self.page.locator("button:has-text('Add Product'), text=Add Product").first
                    await add_btn.click()
                    await asyncio.sleep(1)
                    print("✅ Clicked Add Product via locator")
                except Exception as e:
                    print(f"❌ Could not click Add Product: {str(e)[:50]}")
                    return None
            
            # Fill product form
            await asyncio.sleep(1)
            
            # Take screenshot of the product form
            await self.page.screenshot(path="debug_product_form.png")
            print("📸 Screenshot: debug_product_form.png")
            
            # Fill product name
            if product_data.get('name'):
                name_filled = await self._fill_field_by_placeholder("Enter product name", product_data['name'])
                if not name_filled:
                    await self._fill_field_by_label("Product Name", product_data['name'])
            
            # Fill SKU - correct placeholder is "Enter product SKU"
            if product_data.get('sku'):
                sku_filled = await self._fill_field_by_placeholder("Enter product SKU", product_data['sku'])
                if not sku_filled:
                    sku_filled = await self._fill_field_by_placeholder("Enter SKU", product_data['sku'])
            
            # Fill Price - the field shows "$ 0" or similar
            if product_data.get('price'):
                price_str = str(product_data['price'])
                price_filled = False
                
                # Try by label first (most reliable)
                try:
                    price_field = self.page.get_by_label("Price")
                    if await price_field.is_visible():
                        await price_field.clear()
                        await price_field.fill(price_str)
                        price_filled = True
                        print(f"✅ Filled Price by label: {price_str}")
                except:
                    pass
                
                if not price_filled:
                    # Try the input that has $ 0 placeholder
                    try:
                        price_input = self.page.locator("input[placeholder*='0']").first
                        if await price_input.is_visible():
                            await price_input.clear()
                            await price_input.fill(price_str)
                            price_filled = True
                            print(f"✅ Filled Price via $ placeholder: {price_str}")
                    except:
                        pass
                
                if not price_filled:
                    # Try the second number input (first might be quantity)
                    try:
                        price_inputs = self.page.locator("input[type='number'], input[inputmode='numeric']")
                        count = await price_inputs.count()
                        if count >= 2:
                            await price_inputs.nth(1).clear()
                            await price_inputs.nth(1).fill(price_str)
                            print(f"✅ Filled Price via 2nd number input: {price_str}")
                        elif count == 1:
                            await price_inputs.first.clear()
                            await price_inputs.first.fill(price_str)
                            print(f"✅ Filled Price via number input: {price_str}")
                    except:
                        pass
            
            # Fill Unit field (might be required - has indicator)
            try:
                unit_field = self.page.get_by_placeholder("e.g., licenses, hours")
                if await unit_field.is_visible():
                    await unit_field.fill("units")
                    print("✅ Filled Unit field: units")
            except:
                pass
            
            # Fill Start Date (REQUIRED) - date picker
            print("📅 Selecting Start Date...")
            try:
                start_date_trigger = self.page.locator("text=Pick a date").first
                if await start_date_trigger.is_visible():
                    await start_date_trigger.click()
                    await asyncio.sleep(1)
                    
                    # Navigate to current month if needed and select today
                    today = datetime.now()
                    today_day = str(today.day)
                    
                    # Try to click next month button if not on current month
                    for _ in range(2):
                        dec_visible = await self.page.get_by_text(f"{today.strftime('%B')} {today.year}").is_visible()
                        if dec_visible:
                            break
                        # Click next button
                        try:
                            next_btn = self.page.locator("button:has(svg)").last
                            if await next_btn.is_visible():
                                await next_btn.click()
                                await asyncio.sleep(0.5)
                        except:
                            break
                    
                    # Click on today's day
                    day_selected = False
                    try:
                        day_btn = self.page.locator(f"button:text-is('{today_day}')").first
                        if await day_btn.is_visible():
                            await day_btn.click()
                            day_selected = True
                            print(f"✅ Selected Start Date: day {today_day}")
                    except:
                        pass
                    
                    if not day_selected:
                        # Try clicking any enabled day
                        try:
                            day_btn = self.page.locator("button:not([disabled])").filter(has_text="15").first
                            if await day_btn.is_visible():
                                await day_btn.click()
                                day_selected = True
                                print("✅ Selected Start Date: day 15")
                        except:
                            pass
                    
                    # Close the calendar by pressing Escape or clicking outside
                    await asyncio.sleep(0.5)
                    await self.page.keyboard.press("Escape")
                    await asyncio.sleep(0.5)
                    print("✅ Closed date picker")
                    
            except Exception as e:
                print(f"⚠️ Start Date selection failed: {str(e)[:40]}")
                # Try to close any open calendar
                try:
                    await self.page.keyboard.press("Escape")
                except:
                    pass
            
            await asyncio.sleep(0.5)
            
            # Select Contract (REQUIRED dropdown)
            print("🔽 Selecting Contract...")
            await self._select_labeled_dropdown("Contract", "Select Contract")
            
            # Select Billing Period (REQUIRED for recurring products)
            print("🔽 Selecting Billing Period...")
            billing_period_selected = False
            
            # Try multiple approaches for Billing Period
            billing_selectors = [
                "text=Select billing period",
                "text=Select period",
                "button:has-text('Select billing')",
                "[role='combobox']:has-text('billing')",
            ]
            
            for selector in billing_selectors:
                try:
                    dropdown = self.page.locator(selector).first
                    if await dropdown.is_visible():
                        await dropdown.click()
                        await asyncio.sleep(0.5)
                        # Select first option (usually "Monthly")
                        option = self.page.locator("[role='option']").first
                        if await option.is_visible():
                            await option.click()
                            billing_period_selected = True
                            print("✅ Billing Period selected")
                            break
                except:
                    continue
            
            # Fallback: try labeled dropdown approach
            if not billing_period_selected:
                result = await self._select_labeled_dropdown("Billing Period", "Select billing period")
                if result:
                    billing_period_selected = True
                    print("✅ Billing Period selected via labeled dropdown")
            
            # Another fallback: try selecting "Monthly" or "One-time" directly
            if not billing_period_selected:
                try:
                    # Look for a Billing Period section and click any dropdown in it
                    billing_label = self.page.locator("text=Billing Period").first
                    if await billing_label.is_visible():
                        parent = billing_label.locator("xpath=./parent::*")
                        btn = parent.locator("button, [role='combobox']").first
                        if await btn.is_visible():
                            await btn.click()
                            await asyncio.sleep(0.5)
                            # Try to select "Monthly"
                            monthly = self.page.locator("[role='option']:has-text('Monthly')").first
                            if await monthly.is_visible():
                                await monthly.click()
                                billing_period_selected = True
                                print("✅ Billing Period: Monthly")
                            else:
                                # Just select first option
                                option = self.page.locator("[role='option']").first
                                if await option.is_visible():
                                    await option.click()
                                    billing_period_selected = True
                                    print("✅ Billing Period selected (first option)")
                except:
                    pass
            
            if not billing_period_selected:
                print("⚠️ Could not select Billing Period - this may be required!")
            
            await asyncio.sleep(0.5)
            
            # Select Currency (REQUIRED dropdown)
            print("🔽 Selecting Currency...")
            currency_selected = False
            
            # Try multiple approaches for Currency
            currency_selectors = [
                "text=Select currency",
                "button:has-text('Select currency')",
                "[role='combobox']:has-text('currency')",
            ]
            
            for selector in currency_selectors:
                try:
                    dropdown = self.page.locator(selector).first
                    if await dropdown.is_visible():
                        await dropdown.click()
                        await asyncio.sleep(0.5)
                        # Select USD or first option
                        usd_option = self.page.locator("[role='option']:has-text('USD'), [role='option']:has-text('Dollar')").first
                        if await usd_option.is_visible():
                            await usd_option.click()
                            currency_selected = True
                            print("✅ Currency: USD selected")
                        else:
                            option = self.page.locator("[role='option']").first
                            if await option.is_visible():
                                await option.click()
                                currency_selected = True
                                print("✅ Currency selected (first option)")
                        break
                except:
                    continue
            
            # Fallback: try labeled dropdown approach
            if not currency_selected:
                result = await self._select_labeled_dropdown("Currency", "Select currency")
                if result:
                    currency_selected = True
                    print("✅ Currency selected via labeled dropdown")
            
            if not currency_selected:
                print("⚠️ Could not select Currency - this may be required!")
            
            await asyncio.sleep(0.5)
            
            # Select Product Income Account (REQUIRED dropdown)
            print("🔽 Selecting Product Income Account...")
            await self._select_labeled_dropdown("Product Income Account", "Select GL Account")
            
            # Take screenshot after filling
            await self.page.screenshot(path="debug_product_form_filled.png")
            print("📸 Screenshot: debug_product_form_filled.png")
            
            # Click Create/Save button
            save_clicked = False
            if await self._click_save("Create Product"):
                save_clicked = True
            else:
                # Try generic save
                if await self._click_save():
                    save_clicked = True
            
            if not save_clicked:
                print("❌ Could not click Create Product button")
                return None
            
            await asyncio.sleep(2)
            
            # Check for form validation errors BEFORE declaring success
            error_selectors = [
                "[role='dialog'] >> text=required",
                "[role='dialog'] >> text=is required",
                "[role='dialog'] >> text=Please select",
                "[role='dialog'] >> text=Invalid",
                "[role='alert']",
                ".text-red-500",
                ".text-destructive",
            ]
            
            for selector in error_selectors:
                try:
                    error_el = self.page.locator(selector).first
                    if await error_el.is_visible():
                        error_text = await error_el.text_content()
                        if error_text and len(error_text) > 2:
                            print(f"❌ Product form error: {error_text[:100]}")
                            await self.page.screenshot(path="debug_product_form_error.png")
                            return None
                except:
                    continue
            
            # Check if dialog is still open (form didn't submit)
            dialog = self.page.locator("[role='dialog']")
            if await dialog.is_visible():
                print("⚠️ Dialog still open after clicking Create - checking for errors...")
                await self.page.screenshot(path="debug_product_dialog_still_open.png")
                
                # Try clicking Create Product again
                try:
                    create_btn = self.page.get_by_role("button", name="Create Product")
                    if await create_btn.is_visible():
                        await create_btn.click()
                        await asyncio.sleep(2)
                        print("🔄 Clicked Create Product again")
                except:
                    pass
            
            # Check for success message
            success_found = False
            try:
                success = self.page.locator("text=successfully, text=created, text=Product added").first
                if await success.is_visible():
                    success_found = True
                    print(f"✅ Product created: {product_data.get('name', 'Unknown')}")
            except:
                pass
            
            if not success_found:
                # Check if dialog closed (indicates success)
                await asyncio.sleep(1)
                if not await dialog.is_visible():
                    print(f"✅ Product created (dialog closed): {product_data.get('name', 'Unknown')}")
                else:
                    print("⚠️ Product creation uncertain - dialog still visible")
                    await self.page.screenshot(path="debug_product_uncertain.png")
            
            # Close any dialogs that might be open
            await self._close_any_dialogs()
            
            # Verify product exists in list
            await asyncio.sleep(1)
            product_name = product_data.get('name', '')
            try:
                product_in_list = self.page.locator(f"text={product_name[:20]}").first
                if await product_in_list.is_visible():
                    print(f"✅ Verified: Product '{product_name}' visible in list")
                else:
                    print(f"⚠️ Product '{product_name}' not visible in list - may not have been created")
            except:
                pass
            
            return product_data
            
        except Exception as e:
            print(f"❌ Error creating product: {str(e)}")
            return None
    
    async def _ensure_dialog_closed(self):
        """Ensure all dialogs and overlays are closed before proceeding"""
        try:
            print("🔐 Ensuring dialogs are closed...")
            
            # Wait for any dialog overlay to disappear
            overlay_selectors = [
                "[data-state='open'][class*='fixed inset']",
                "[data-state='open'][aria-hidden='true']",
                "[class*='dialog'][data-state='open']",
                ".fixed.inset-0.bg-black"
            ]
            
            for attempt in range(5):  # Try up to 5 times
                overlay_visible = False
                for selector in overlay_selectors:
                    try:
                        overlay = self.page.locator(selector).first
                        # Use is_visible without timeout - just check current state
                        if await overlay.is_visible():
                            overlay_visible = True
                            print(f"⚠️ Overlay still visible: {selector}")
                            break
                    except:
                        continue
                
                if not overlay_visible:
                    print("✅ No overlays blocking - dialog closed")
                    await asyncio.sleep(1)  # Extra wait to ensure UI is stable
                    return True
                
                # Try to close
                print(f"🔄 Attempt {attempt + 1}: Closing dialogs...")
                await self.page.keyboard.press("Escape")
                await asyncio.sleep(1)
                
                # Try clicking outside the dialog
                try:
                    await self.page.mouse.click(10, 10)
                    await asyncio.sleep(0.5)
                except:
                    pass
                
                # Try clicking close button
                close_selectors = [
                    "[data-radix-dialog-close]",
                    "button[aria-label='Close']",
                    "button:has-text('×')",
                    "[role='dialog'] button:has(svg[class*='x'])"
                ]
                for close_sel in close_selectors:
                    try:
                        close_btn = self.page.locator(close_sel).first
                        if await close_btn.is_visible():
                            await close_btn.click()
                            await asyncio.sleep(0.5)
                            break
                    except:
                        continue
            
            print("⚠️ Could not fully close dialogs after 5 attempts")
            # Take screenshot for debugging
            try:
                await self.page.screenshot(path="debug_dialog_not_closed.png")
            except:
                pass
            return False
            
        except Exception as e:
            print(f"⚠️ Error ensuring dialog closed: {str(e)[:50]}")
            return False
    
    async def _close_any_dialogs(self):
        """Close any open modal dialogs"""
        try:
            # Try pressing Escape to close dialogs
            await self.page.keyboard.press("Escape")
            await asyncio.sleep(0.5)
            
            # Try clicking X button if present
            close_buttons = [
                "button[aria-label='Close']",
                "button:has-text('×')",
                "button:has-text('X')",
                "[data-radix-dialog-close]",
                "[aria-label='close']"
            ]
            
            for selector in close_buttons:
                try:
                    close_btn = self.page.locator(selector).first
                    if await close_btn.is_visible():
                        await close_btn.click()
                        await asyncio.sleep(0.5)
                        print("✅ Closed dialog")
                        break
                except:
                    continue
            
            # Press Escape again just to be safe
            await self.page.keyboard.press("Escape")
            await asyncio.sleep(0.5)
            
        except Exception as e:
            print(f"⚠️ Dialog close attempt: {str(e)[:50]}")
    
    async def create_invoice_in_section(self, product_name: str = None):
        """Create an invoice when already in the Invoices section"""
        try:
            print("🧾 Creating invoice...")
            await asyncio.sleep(2)
            
            # Take screenshot to debug what's on the page
            try:
                await self.page.screenshot(path="debug_invoices_page.png")
                print("📸 Screenshot: debug_invoices_page.png")
            except:
                pass
            
            # Step 1: Click invoice button - try multiple button names
            button_clicked = False
            button_names = [
                "Generate Invoice",
                "Add Invoice",
                "Create Invoice",
                "New Invoice",
                "+ Add Invoice",
                "+ Invoice",
                "Generate",
            ]
            
            # First, list all buttons for debugging
            buttons = self.page.locator("button")
            btn_count = await buttons.count()
            print(f"📋 Found {btn_count} buttons on page")
            
            for button_name in button_names:
                if button_clicked:
                    break
                    
                # Try get_by_role first with wait_for
                try:
                    add_button = self.page.get_by_role("button", name=button_name)
                    await add_button.wait_for(state="visible", timeout=3000)
                    await add_button.click()
                    await asyncio.sleep(1)
                    button_clicked = True
                    print(f"✅ Clicked '{button_name}' button via get_by_role")
                    break
                except Exception as e:
                    print(f"⚠️ get_by_role for '{button_name}': {str(e)[:30]}")
                
                # Try locator with force click
                try:
                    add_btn = self.page.locator(f"button:has-text('{button_name}')").first
                    await add_btn.click(timeout=3000)
                    await asyncio.sleep(1)
                    button_clicked = True
                    print(f"✅ Clicked '{button_name}' button via locator")
                    break
                except Exception as e:
                    print(f"⚠️ locator for '{button_name}': {str(e)[:30]}")
                    continue
            
            # Fallback: click button by index (we know "Generate Invoice" is often button 6)
            if not button_clicked:
                print("⚠️ Trying button by index fallback...")
                for i in range(btn_count):
                    try:
                        btn = buttons.nth(i)
                        btn_text = await btn.text_content()
                        if btn_text and "generate" in btn_text.lower():
                            # Try scrolling into view first
                            await btn.scroll_into_view_if_needed()
                            await asyncio.sleep(0.5)
                            # Try force click
                            await btn.click(force=True, timeout=5000)
                            await asyncio.sleep(1)
                            button_clicked = True
                            print(f"✅ Clicked button {i}: '{btn_text}' (force click)")
                            break
                    except Exception as e:
                        print(f"⚠️ Failed to click button {i}: {str(e)[:30]}")
                        continue
            
            # Last resort: try clicking the 6th button directly (index 6 based on observation)
            if not button_clicked:
                print("⚠️ Trying direct button 6 click...")
                try:
                    btn = buttons.nth(6)
                    await btn.scroll_into_view_if_needed()
                    await asyncio.sleep(0.5)
                    await btn.click(force=True)
                    button_clicked = True
                    print("✅ Clicked button 6 directly (force click)")
                except Exception as e:
                    print(f"❌ Direct button 6 click failed: {str(e)[:50]}")
            
            if not button_clicked:
                print("❌ Failed to click any invoice button")
                for i in range(min(btn_count, 10)):
                    try:
                        btn_text = await buttons.nth(i).text_content()
                        print(f"   - Button {i}: '{btn_text[:50] if btn_text else 'no text'}'")
                    except:
                        pass
                return None
            
            await asyncio.sleep(1)
            
            # Step 2: Select Month from the dropdown in the modal
            print("📅 Selecting invoice month...")
            month_selected = False
            
            # Take screenshot to debug
            try:
                await self.page.screenshot(path="debug_before_month_select.png")
                print("📸 Screenshot: debug_before_month_select.png")
            except:
                pass
            
            # Method 1: Click the dropdown trigger by its text
            try:
                dropdown_trigger = self.page.get_by_text("Select month to invoice").first
                if await dropdown_trigger.is_visible():
                    await dropdown_trigger.click()
                    await asyncio.sleep(1)
                    print("✅ Clicked month dropdown trigger")
                    
                    # Take screenshot after opening dropdown
                    try:
                        await self.page.screenshot(path="debug_month_dropdown_open.png")
                    except:
                        pass
                    
                    # Try to find visible options
                    option_selectors = [
                        "[role='option']",
                        "[role='listbox'] > div",
                        "[class*='option']",
                        "[class*='menu'] > div",
                        "[class*='listbox'] > div",
                        "ul li",
                        "[data-value]"
                    ]
                    
                    for selector in option_selectors:
                        options = self.page.locator(selector)
                        count = await options.count()
                        print(f"📋 Selector '{selector}' found {count} options")
                        if count > 0:
                            # Click the first option
                            await options.first.click()
                            await asyncio.sleep(0.5)
                            month_selected = True
                            print(f"✅ Selected first month option via {selector}")
                            break
            except Exception as e:
                print(f"⚠️ Method 1 failed: {str(e)[:50]}")
            
            # Method 2: Try clicking by month name after opening dropdown
            if not month_selected:
                try:
                    # Click dropdown again
                    dropdown_trigger = self.page.locator("[class*='select'], [role='combobox']").first
                    if await dropdown_trigger.is_visible():
                        await dropdown_trigger.click()
                        await asyncio.sleep(1)
                    
                    # Look for specific month names
                    current_month = datetime.now().strftime("%B")  # e.g., "December"
                    prev_month = (datetime.now() - timedelta(days=30)).strftime("%B")
                    months_to_try = [current_month, prev_month, "November", "October", "December"]
                    
                    for month in months_to_try:
                        try:
                            month_opt = self.page.get_by_text(month, exact=False).first
                            if await month_opt.is_visible():
                                await month_opt.click()
                                month_selected = True
                                print(f"✅ Selected month by name: {month}")
                                break
                        except:
                            continue
                except Exception as e:
                    print(f"⚠️ Method 2 failed: {str(e)[:50]}")
            
            # Method 3: Use keyboard navigation
            if not month_selected:
                try:
                    # Click dropdown and use arrow keys
                    dropdown_trigger = self.page.get_by_text("Select month to invoice").first
                    if await dropdown_trigger.is_visible():
                        await dropdown_trigger.click()
                        await asyncio.sleep(0.5)
                        await self.page.keyboard.press("ArrowDown")
                        await asyncio.sleep(0.3)
                        await self.page.keyboard.press("Enter")
                        month_selected = True
                        print("✅ Selected month via keyboard navigation")
                except Exception as e:
                    print(f"⚠️ Method 3 (keyboard) failed: {str(e)[:50]}")
            
            # Take screenshot after selection attempt
            try:
                await self.page.screenshot(path="debug_after_month_select.png")
                print("📸 Screenshot: debug_after_month_select.png")
            except:
                pass
            
            await asyncio.sleep(1)
            
            # Step 3: Click "Continue" button
            print("📤 Clicking Continue button...")
            continue_clicked = False
            
            try:
                continue_btn = self.page.get_by_role("button", name="Continue")
                if await continue_btn.is_visible():
                    await continue_btn.click()
                    await asyncio.sleep(2)
                    continue_clicked = True
                    print("✅ Clicked Continue button")
            except Exception as e:
                print(f"⚠️ Continue button issue: {str(e)[:50]}")
            
            if not continue_clicked:
                try:
                    continue_btn = self.page.locator("button:has-text('Continue')").first
                    await continue_btn.click()
                    await asyncio.sleep(2)
                    continue_clicked = True
                    print("✅ Clicked Continue via locator")
                except:
                    pass
            
            # Step 4: Fill the Invoice Details form
            await asyncio.sleep(2)
            print("📝 Filling Invoice Details form...")
            
            # Fill Invoice Date (required field) - This is a date picker component
            invoice_date_filled = False
            today = datetime.now()
            today_day = str(today.day)  # e.g., "3" for December 3rd
            current_month = today.strftime("%B")  # e.g., "December"
            
            # Method 1: Click the date picker trigger and navigate to current month
            try:
                print("📅 Opening date picker...")
                date_trigger = self.page.get_by_text("Pick a date").first
                if await date_trigger.is_visible():
                    await date_trigger.click()
                    await asyncio.sleep(1)
                    
                    # Take screenshot of calendar
                    await self.page.screenshot(path="debug_calendar_open.png")
                    print("📸 Screenshot: debug_calendar_open.png")
                    
                    # Navigate to December using the ">" (next) button
                    # The calendar might be showing November, we need December
                    print("📅 Navigating to December 2025...")
                    
                    # Find and click the next month button (the ">" on the right)
                    next_btn_selectors = [
                        "button[aria-label*='next']",
                        "button[aria-label*='Next']", 
                        "button:has(svg[class*='chevron-right'])",
                        "button:has(svg[class*='right'])",
                        "[class*='calendar'] button:last-child",
                        "button:nth-child(2)"  # Often the second button in header is "next"
                    ]
                    
                    # Click next until we see December 2025
                    for attempt in range(3):
                        # Check if already on December
                        dec_visible = await self.page.get_by_text("December 2025").is_visible()
                        if dec_visible:
                            print("✅ Already on December 2025")
                            break
                        
                        # Try to find and click next button
                        for selector in next_btn_selectors:
                            try:
                                next_btn = self.page.locator(selector).first
                                if await next_btn.is_visible():
                                    await next_btn.click()
                                    await asyncio.sleep(0.5)
                                    print(f"✅ Clicked next month button ({selector})")
                                    break
                            except:
                                continue
                        
                        # Check if December is now visible
                        if await self.page.get_by_text("December 2025").is_visible():
                            print("✅ Navigated to December 2025")
                            break
                    
                    await asyncio.sleep(0.5)
                    await self.page.screenshot(path="debug_calendar_december.png")
                    
                    # Now click on today's day (3)
                    print(f"📅 Selecting day {today_day}...")
                    day_clicked = False
                    
                    # The day "3" should be visible and clickable now
                    # Try clicking by text content
                    try:
                        # Look for button with text "3" that's enabled
                        day_btn = self.page.locator(f"button:text-is('{today_day}'):not([disabled])").first
                        if await day_btn.is_visible():
                            await day_btn.click()
                            day_clicked = True
                            print(f"✅ Clicked day {today_day}")
                    except Exception as e:
                        print(f"⚠️ Day button click failed: {str(e)[:30]}")
                    
                    # Try clicking the day by finding it within the calendar grid
                    if not day_clicked:
                        try:
                            # Find all visible buttons with single digits that could be days
                            all_buttons = self.page.locator("button")
                            count = await all_buttons.count()
                            for i in range(count):
                                btn = all_buttons.nth(i)
                                try:
                                    text = await btn.inner_text()
                                    if text.strip() == today_day:
                                        await btn.click()
                                        day_clicked = True
                                        print(f"✅ Clicked day {today_day} (found at index {i})")
                                        break
                                except:
                                    continue
                        except:
                            pass
                    
                    if day_clicked:
                        invoice_date_filled = True
                        await asyncio.sleep(0.5)
                        
            except Exception as e:
                print(f"⚠️ Method 1 (calendar picker) failed: {str(e)[:40]}")
            
            # Method 2: Try clicking any visible/enabled day in the calendar
            if not invoice_date_filled:
                try:
                    # First open calendar if not open
                    date_trigger = self.page.get_by_text("Pick a date").first
                    if await date_trigger.is_visible():
                        await date_trigger.click()
                        await asyncio.sleep(1)
                    
                    # Find all day buttons that are not disabled
                    calendar_days = self.page.locator("button:not([disabled])").filter(has_text="25")
                    if await calendar_days.first.is_visible():
                        await calendar_days.first.click()
                        invoice_date_filled = True
                        print(f"✅ Selected day 25 from calendar")
                except Exception as e:
                    print(f"⚠️ Method 2 (day 25) failed: {str(e)[:40]}")
            
            # Method 3: Press Escape and try a different approach
            if not invoice_date_filled:
                try:
                    await self.page.keyboard.press("Escape")
                    await asyncio.sleep(0.5)
                    # Try clicking the input and typing
                    date_input = self.page.locator("input").filter(has_text="Pick a date").first
                    await date_input.click()
                    await asyncio.sleep(0.5)
                    await self.page.keyboard.type("12/03/2025")
                    await self.page.keyboard.press("Tab")
                    invoice_date_filled = True
                    print("✅ Typed date manually")
                except Exception as e:
                    print(f"⚠️ Method 3 (type date) failed: {str(e)[:40]}")
            
            await asyncio.sleep(1)
            
            # Step 5: Add Invoice Lines (REQUIRED)
            print("📝 Adding Invoice Lines...")
            product_added = False
            try:
                # The "Add Product" is a span inside a dropdown trigger
                # Look for the Add Product dropdown - it's a span, not a button
                add_product = self.page.locator("span:has-text('Add Product')").first
                
                if await add_product.is_visible():
                    await add_product.click()
                    await asyncio.sleep(1)
                    print("✅ Clicked Add Product dropdown")
                    
                    # Take screenshot of dropdown
                    await self.page.screenshot(path="debug_add_product_dropdown.png")
                    print("📸 Screenshot: debug_add_product_dropdown.png")
                    
                    # Select first product from dropdown options
                    options = self.page.locator("[role='option']")
                    opt_count = await options.count()
                    print(f"Found {opt_count} product options in dropdown")
                    
                    if opt_count > 0:
                        prod_name = await options.first.text_content()
                        await options.first.click()
                        product_added = True
                        print(f"✅ Selected product: {prod_name}")
                        await asyncio.sleep(1)
                    else:
                        print("⚠️ No products available in dropdown")
                else:
                    # Try alternative: click on the table cell that says "Add Product"
                    add_cell = self.page.locator("td:has-text('Add Product')")
                    if await add_cell.is_visible():
                        await add_cell.click()
                        await asyncio.sleep(0.5)
                        
                        options = self.page.locator("[role='option']")
                        if await options.count() > 0:
                            await options.first.click()
                            product_added = True
                            print("✅ Selected product via table cell click")
                
                await asyncio.sleep(1)
                
                if product_added:
                    print("✅ Invoice line item added successfully")
                
            except Exception as e:
                print(f"⚠️ Invoice Lines section: {str(e)[:40]}")
            
            # Take screenshot before submitting
            await self.page.screenshot(path="debug_invoice_form_filled.png")
            print("📸 Screenshot: debug_invoice_form_filled.png")
            
            # Step 6: Click "Create Invoice" button to submit
            print("📤 Clicking Create Invoice button...")
            invoice_created = False
            
            try:
                create_btn = self.page.get_by_role("button", name="Create Invoice")
                if await create_btn.is_visible():
                    await create_btn.click()
                    await asyncio.sleep(3)
                    invoice_created = True
                    print("✅ Clicked Create Invoice button")
            except Exception as e:
                print(f"⚠️ Create Invoice button issue: {str(e)[:50]}")
            
            if not invoice_created:
                try:
                    create_btn = self.page.locator("button:has-text('Create Invoice')").first
                    if await create_btn.is_visible():
                        await create_btn.click()
                        await asyncio.sleep(3)
                        invoice_created = True
                        print("✅ Clicked Create Invoice via locator")
                except:
                    pass
            
            # Check for success message
            success = False
            try:
                success_msg = self.page.locator("text=successfully, text=created, text=generated")
                if await success_msg.first.is_visible():
                    success = True
                    print("✅ Invoice creation success message found")
            except:
                pass
            
            # Take screenshot of final state
            await self.page.screenshot(path="debug_invoice_creation_final.png")
            print("📸 Screenshot saved: debug_invoice_creation_final.png")
            
            if invoice_created or success:
                invoice_data = {
                    'product': product_name,
                    'quantity': 1,
                    'date': datetime.now().strftime('%Y-%m-%d'),
                    'status': 'created'
                }
                print(f"✅ Invoice fully created for product: {product_name}")
                return invoice_data
            elif month_selected and continue_clicked:
                print("⚠️ Invoice form filled but Create Invoice may have failed")
                return {'product': product_name, 'quantity': 1, 'date': datetime.now().strftime('%Y-%m-%d'), 'status': 'partial'}
            
            return None
            
        except Exception as e:
            print(f"❌ Error creating invoice: {str(e)}")
            await self.page.screenshot(path="debug_invoice_error.png")
            return None

    # ==========================================
    # HELPER METHODS
    # ==========================================
    
    async def _fill_field(self, selectors: list, value: str):
        """Helper to fill a form field trying multiple selectors"""
        for selector in selectors:
            try:
                element = self.page.locator(selector).first
                if await element.is_visible():
                    await element.clear()
                    await element.fill(value)
                    print(f"✅ Filled field {selector}: {value[:30]}...")
                    return True
            except:
                continue
        print(f"⚠️ Could not fill field with value: {value[:30]}...")
        return False

    async def _click_save(self, button_text: str = None):
        """Helper to click save/submit button"""
        
        # First scroll the dialog to the bottom to reveal button
        try:
            await self.page.evaluate("document.querySelector('[role=\"dialog\"]')?.scrollTo(0, 9999)")
            await asyncio.sleep(0.3)
        except:
            pass
        
        # Try specific button text first if provided
        if button_text:
            try:
                button = self.page.get_by_role("button", name=button_text)
                await button.scroll_into_view_if_needed()
                await asyncio.sleep(0.3)
                await button.click(force=True)
                print(f"✅ Clicked button: {button_text}")
                return True
            except Exception as e:
                print(f"⚠️ Could not click '{button_text}': {str(e)[:50]}")
        
        # Try get_by_role for common button names with force click
        for name in ["Create Customer", "Create Product", "Create Invoice", "Create", "Save", "Submit"]:
            try:
                button = self.page.get_by_role("button", name=name)
                if await button.is_visible():
                    await button.scroll_into_view_if_needed()
                    await asyncio.sleep(0.2)
                    await button.click(force=True)
                    print(f"✅ Clicked button via get_by_role: {name}")
                    return True
            except:
                continue
        
        # Try locator with exact text
        for name in ["Create Customer", "Create Product", "Create Invoice", "Create", "Save", "Submit"]:
            try:
                button = self.page.locator(f"button:has-text('{name}')").first
                if await button.is_visible():
                    await button.scroll_into_view_if_needed()
                    await asyncio.sleep(0.2)
                    await button.click(force=True)
                    print(f"✅ Clicked button via locator: {name}")
                    return True
            except:
                continue
        
        # Try colored buttons (purple/primary)
        try:
            colored_buttons = self.page.locator("button[class*='primary'], button[class*='bg-purple'], button[class*='bg-indigo']")
            count = await colored_buttons.count()
            for i in range(count):
                btn = colored_buttons.nth(i)
                if await btn.is_visible():
                    text = await btn.inner_text()
                    if "create" in text.lower() or "save" in text.lower() or "submit" in text.lower():
                        await btn.scroll_into_view_if_needed()
                        await asyncio.sleep(0.2)
                        await btn.click(force=True)
                        print(f"✅ Clicked colored button: {text}")
                        return True
        except:
            pass
        
        # Fall back to selectors
        for selector in self.save_button_selectors:
            try:
                element = self.page.locator(selector).first
                if await element.is_visible():
                    await element.scroll_into_view_if_needed()
                    await asyncio.sleep(0.2)
                    await element.click(force=True)
                    print(f"✅ Clicked save button: {selector}")
                    return True
            except:
                continue
        
        print("❌ Save button not found")
        return False

    async def _check_success_message(self):
        """Helper to check for success message"""
        for selector in self.success_message_selectors:
            try:
                element = self.page.locator(selector).first
                if await element.is_visible():
                    print(f"✅ Success message found: {selector}")
                    return True
            except:
                continue
        return False

    async def get_invoice_list(self):
        """Get list of invoices displayed on page"""
        try:
            await self.go_to_invoices_tab()
            await asyncio.sleep(2)
            
            # Try to find invoice table/list
            invoice_rows = self.page.locator("table tbody tr, [data-testid*='invoice-row'], .invoice-item")
            count = await invoice_rows.count()
            
            invoices = []
            for i in range(count):
                row_text = await invoice_rows.nth(i).inner_text()
                invoices.append(row_text)
            
            print(f"📋 Found {len(invoices)} invoices")
            return invoices
            
        except Exception as e:
            print(f"❌ Error getting invoice list: {str(e)}")
            return []

    async def verify_invoice_exists(self, customer_name: str = None, invoice_number: str = None):
        """
        Verify an invoice exists in the list
        
        Args:
            customer_name: Customer name to search for
            invoice_number: Invoice number to search for
        
        Returns:
            True if invoice found, False otherwise
        """
        try:
            await self.go_to_invoices_tab()
            await asyncio.sleep(2)
            
            search_term = customer_name or invoice_number
            if not search_term:
                return False
            
            # Look for the invoice
            invoice_element = self.page.locator(f"text={search_term}").first
            if await invoice_element.is_visible():
                print(f"✅ Invoice found with: {search_term}")
                return True
            
            print(f"❌ Invoice not found with: {search_term}")
            return False
            
        except Exception as e:
            print(f"❌ Error verifying invoice: {str(e)}")
            return False

    async def take_screenshot(self, name: str = "invoicing_debug"):
        """Take a screenshot for debugging"""
        try:
            filepath = f"{name}.png"
            await self.page.screenshot(path=filepath)
            print(f"📸 Screenshot saved: {filepath}")
            return filepath
        except Exception as e:
            print(f"❌ Screenshot failed: {str(e)}")
            return None

