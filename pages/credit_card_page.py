from playwright.async_api import Page, expect
import asyncio

class CreditCardPage:
    """Page Object for Credit Cards section under Reconciliation"""
    
    def __init__(self, page: Page):
        self.page = page
        
        # Page elements
        self.page_title = page.locator("h1, h2, h3").filter(has_text="Credit Card")
        self.credit_card_table = page.locator("table, [role='grid'], .data-grid")
        self.transaction_list = page.locator("[data-testid='transaction-list'], .transaction-list")
        
        # Card selection
        self.card_selector = page.locator("select[name='card'], [data-testid='card-selector']")
        self.card_dropdown = page.locator("button:has-text('Select Card'), .card-dropdown")
        
        # Upload functionality
        self.upload_button = page.locator("button:has-text('Upload')")
        self.upload_input = page.locator("input[type='file']")
        self.upload_area = page.locator("[data-testid='upload-area'], .upload-dropzone")
        
        # Transaction elements
        self.transaction_rows = page.locator("tr[data-testid='transaction-row'], .transaction-row")
        self.transaction_amount = page.locator("[data-testid='transaction-amount']")
        self.transaction_date = page.locator("[data-testid='transaction-date']")
        self.transaction_description = page.locator("[data-testid='transaction-description']")
        
        # Search and filter
        self.search_input = page.locator("input[type='search'], input[placeholder*='search' i]")
        self.filter_button = page.locator("button:has-text('Filter')")
        self.date_filter = page.locator("input[type='date'], [data-testid='date-filter']")
        
        # Action buttons
        self.reconcile_button = page.locator("button:has-text('Reconcile')")
        self.match_button = page.locator("button:has-text('Match')")
        self.action_buttons = page.locator("button:has-text('Edit'), button:has-text('Delete'), button:has-text('View')")
        
        # Status indicators
        self.status_badges = page.locator(".status-badge, [data-testid='status']")
        self.reconciliation_status = page.locator("[data-testid='reconciliation-status']")
        
        # Financial info
        self.account_balance = page.locator("[data-testid='account-balance'], .balance-display")
        self.available_credit = page.locator("[data-testid='available-credit']")
        self.statement_balance = page.locator("[data-testid='statement-balance']")
        
        # Settings
        self.settings_button = page.locator("button:has-text('Settings')")
        self.settings_panel = page.locator("[data-testid='settings-panel'], .settings-container")
        
        # Empty state
        self.empty_state = page.locator(".empty-state, [data-testid='empty-state']")
        
        # Sorting
        self.sort_headers = page.locator("th[role='columnheader'], .sortable-header")
    
    async def navigate_to_credit_cards(self):
        """Navigate to Credit Cards section"""
        try:
            print("🏦 Navigating to Credit Cards section...")
            
            # Ensure we're not on the login page
            current_url = self.page.url
            if '/login' in current_url:
                print("⚠️ Currently on login page, waiting for authentication...")
                await asyncio.sleep(3)
                current_url = self.page.url
            
            # Check if already on credit cards page
            if 'credit-card' in current_url.lower():
                print(f"✅ Already on Credit Cards page: {current_url}")
                return
            
            # Determine the base URL (works for both stage and production)
            if 'stage.viewz.co' in current_url:
                base_url = 'https://app.stage.viewz.co'
            elif 'viewz.co' in current_url:
                base_url = 'https://app.viewz.co'
            else:
                # Fallback: extract base from current URL
                from urllib.parse import urlparse
                parsed = urlparse(current_url)
                base_url = f"{parsed.scheme}://{parsed.netloc}"
            
            # Try to navigate using UI first (preserves session better)
            try:
                # Look for Reconciliation menu
                reconciliation = self.page.locator("text=Reconciliation").first
                if await reconciliation.is_visible(timeout=5000):
                    await reconciliation.click()
                    await asyncio.sleep(1)
                    print("✅ Clicked Reconciliation menu")
                    
                    # Try to find Credit Cards link
                    credit_card_link = self.page.locator("[href*='credit-card']").first
                    if await credit_card_link.is_visible(timeout=5000):
                        await credit_card_link.click()
                        await asyncio.sleep(2)
                        print("✅ Clicked Credit Cards link")
                        return
            except Exception as e:
                print(f"⚠️ UI navigation failed: {e}, trying direct URL...")
            
            # Fallback: Navigate directly to Credit Cards page
            credit_cards_url = f"{base_url}/reconciliation/credit-cards"
            print(f"🔗 Navigating to: {credit_cards_url}")
            
            await self.page.goto(credit_cards_url, wait_until='domcontentloaded', timeout=30000)
            await asyncio.sleep(3)
            
            # Check if we got redirected to login
            final_url = self.page.url
            if '/login' in final_url:
                print(f"⚠️ Redirected to login page - session may have been lost")
            else:
                print(f"✅ Successfully navigated to: {final_url}")
            
        except Exception as e:
            print(f"⚠️ Error navigating to Credit Cards: {e}")
            # Continue anyway - we might already be on the page
    
    async def verify_page_loads(self):
        """Verify Credit Cards page loads successfully"""
        try:
            # Check for page title or main content
            await self.page.wait_for_load_state('networkidle', timeout=10000)
            
            # Check if URL contains credit-cards
            current_url = self.page.url
            if 'credit-card' in current_url.lower():
                print(f"✅ On Credit Cards page: {current_url}")
                return True
            
            # Look for any credit card related content
            is_loaded = (
                await self.page_title.count() > 0 or
                await self.credit_card_table.count() > 0 or
                await self.transaction_list.count() > 0 or
                await self.empty_state.count() > 0 or
                await self.page.locator("text=/credit.*card/i").count() > 0 or
                await self.page.locator("[data-testid*='credit'], [class*='credit']").count() > 0
            )
            
            if is_loaded:
                print(f"✅ Credit Cards page content detected")
            else:
                print(f"⚠️ No Credit Cards content found on page: {current_url}")
            
            return is_loaded
        except Exception as e:
            print(f"⚠️ Error verifying page load: {e}")
            return False
    
    async def verify_transaction_display(self):
        """Verify credit card transactions are displayed"""
        try:
            count = await self.transaction_rows.count()
            return count > 0
        except Exception as e:
            print(f"⚠️ Error verifying transaction display: {e}")
            return False
    
    async def select_credit_card(self, card_name: str = None):
        """Select a credit card from dropdown"""
        try:
            # Try dropdown
            if await self.card_dropdown.is_visible(timeout=3000):
                await self.card_dropdown.click()
                await asyncio.sleep(1)
                
                if card_name:
                    option = self.page.locator(f"text={card_name}").first
                    if await option.is_visible(timeout=2000):
                        await option.click()
                        return True
            
            # Try select element
            if await self.card_selector.is_visible(timeout=3000):
                if card_name:
                    await self.card_selector.select_option(label=card_name)
                else:
                    await self.card_selector.select_option(index=0)
                return True
                
            return False
        except Exception as e:
            print(f"⚠️ Error selecting credit card: {e}")
            return False
    
    async def get_financial_info(self):
        """Get credit card financial information"""
        try:
            info = {}
            
            if await self.account_balance.is_visible(timeout=3000):
                info['balance'] = await self.account_balance.text_content()
            
            if await self.available_credit.is_visible(timeout=3000):
                info['available_credit'] = await self.available_credit.text_content()
            
            if await self.statement_balance.is_visible(timeout=3000):
                info['statement_balance'] = await self.statement_balance.text_content()
            
            return info
        except Exception as e:
            print(f"⚠️ Error getting financial info: {e}")
            return {}
    
    async def filter_by_date(self, start_date: str = None, end_date: str = None):
        """Filter transactions by date"""
        try:
            if await self.date_filter.is_visible(timeout=3000):
                if start_date:
                    await self.date_filter.first.fill(start_date)
                if end_date:
                    await self.date_filter.last.fill(end_date)
                
                if await self.filter_button.is_visible(timeout=2000):
                    await self.filter_button.click()
                
                return True
            return False
        except Exception as e:
            print(f"⚠️ Error filtering by date: {e}")
            return False
    
    async def search_transactions(self, search_term: str):
        """Search for transactions"""
        try:
            if await self.search_input.is_visible(timeout=3000):
                await self.search_input.fill(search_term)
                await asyncio.sleep(1)
                return True
            return False
        except Exception as e:
            print(f"⚠️ Error searching transactions: {e}")
            return False
    
    async def verify_upload_area(self):
        """Verify statement upload area is available"""
        try:
            return (
                await self.upload_button.is_visible(timeout=5000) or
                await self.upload_area.is_visible(timeout=5000) or
                await self.upload_input.count() > 0
            )
        except Exception as e:
            print(f"⚠️ Error verifying upload area: {e}")
            return False
    
    async def upload_statement(self, file_path: str):
        """Upload credit card statement"""
        try:
            # Try to find file input
            if await self.upload_input.count() > 0:
                await self.upload_input.first.set_input_files(file_path)
                await asyncio.sleep(2)
                return True
            
            # Try upload button
            if await self.upload_button.is_visible(timeout=3000):
                await self.upload_button.click()
                await asyncio.sleep(1)
                
                # Look for file input after clicking
                if await self.upload_input.count() > 0:
                    await self.upload_input.first.set_input_files(file_path)
                    await asyncio.sleep(2)
                    return True
            
            return False
        except Exception as e:
            print(f"⚠️ Error uploading statement: {e}")
            return False
    
    async def get_reconciliation_status(self):
        """Get reconciliation status"""
        try:
            if await self.reconciliation_status.is_visible(timeout=3000):
                return await self.reconciliation_status.text_content()
            
            if await self.status_badges.count() > 0:
                return await self.status_badges.first.text_content()
            
            return None
        except Exception as e:
            print(f"⚠️ Error getting reconciliation status: {e}")
            return None
    
    async def verify_action_buttons(self):
        """Verify action buttons are available"""
        try:
            count = await self.action_buttons.count()
            return count > 0
        except Exception as e:
            print(f"⚠️ Error verifying action buttons: {e}")
            return False
    
    async def sort_transactions(self, column_name: str):
        """Sort transactions by column"""
        try:
            header = self.page.locator(f"th:has-text('{column_name}')").first
            
            if await header.is_visible(timeout=3000):
                await header.click()
                await asyncio.sleep(1)
                return True
            return False
        except Exception as e:
            print(f"⚠️ Error sorting transactions: {e}")
            return False
    
    async def verify_empty_state(self):
        """Verify empty state is displayed"""
        try:
            return await self.empty_state.is_visible(timeout=5000)
        except Exception as e:
            print(f"⚠️ Error verifying empty state: {e}")
            return False
    
    async def open_settings(self):
        """Open credit card settings"""
        try:
            if await self.settings_button.is_visible(timeout=3000):
                await self.settings_button.click()
                await asyncio.sleep(1)
                
                return await self.settings_panel.is_visible(timeout=5000)
            return False
        except Exception as e:
            print(f"⚠️ Error opening settings: {e}")
            return False
    
    async def get_transaction_count(self):
        """Get number of transactions displayed"""
        try:
            return await self.transaction_rows.count()
        except Exception as e:
            print(f"⚠️ Error getting transaction count: {e}")
            return 0

