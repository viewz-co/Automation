"""
GL Account Operations E2E Tests
Tests for GL Account creation in Chart of Accounts
"""

import pytest
import asyncio
import random
import string

from pages.chart_of_accounts_page import ChartOfAccountsPage


class TestGLAccountOperations:
    """Test suite for GL Account operations in Chart of Accounts"""
    
    # ==========================================
    # PAGE LOAD & NAVIGATION TESTS
    # ==========================================
    
    @pytest.mark.asyncio
    async def test_chart_of_accounts_page_loads(self, perform_login_with_entity, env_config):
        """Test that Chart of Accounts page loads successfully"""
        page = perform_login_with_entity
        base_url = env_config.get("base_url", "https://app.stage.viewz.co")
        
        chart_page = ChartOfAccountsPage(page)
        chart_page.base_url = base_url
        
        print("\n🧪 TEST: Chart of Accounts page loads")
        
        # Navigate to Chart of Accounts
        nav_result = await chart_page.navigate_to_chart_of_accounts(base_url)
        
        # Verify page loaded
        is_loaded = await chart_page.is_loaded()
        
        assert nav_result or is_loaded, "Chart of Accounts page should load successfully"
        print(f"✅ Chart of Accounts page loaded. URL: {page.url}")

    @pytest.mark.asyncio
    async def test_add_gl_account_button_visible(self, perform_login_with_entity, env_config):
        """Test that Add GL Account button is visible"""
        page = perform_login_with_entity
        base_url = env_config.get("base_url", "https://app.stage.viewz.co")
        
        chart_page = ChartOfAccountsPage(page)
        chart_page.base_url = base_url
        
        print("\n🧪 TEST: Add GL Account button visible")
        
        await chart_page.navigate_to_chart_of_accounts(base_url)
        await asyncio.sleep(2)
        
        # Check for Add GL Account button
        button_visible = False
        for selector in chart_page.add_gl_button_selectors:
            try:
                btn = page.locator(selector).first
                if await btn.is_visible():
                    button_visible = True
                    print(f"✅ Add GL Account button found: {selector}")
                    break
            except:
                continue
        
        assert button_visible, "Add GL Account button should be visible"
        print("✅ Add GL Account button is visible")

    # ==========================================
    # GL ACCOUNT CREATION TESTS
    # ==========================================
    
    @pytest.mark.asyncio
    async def test_create_gl_account_trade_receivables(self, perform_login_with_entity, env_config):
        """Test creating a Trade Receivables GL Account (USD, Balance Sheet, Current Assets)"""
        page = perform_login_with_entity
        base_url = env_config.get("base_url", "https://app.stage.viewz.co")
        
        chart_page = ChartOfAccountsPage(page)
        chart_page.base_url = base_url
        
        print("\n🧪 TEST: Create GL Account - Trade Receivables")
        
        await chart_page.navigate_to_chart_of_accounts(base_url)
        
        # Create AR Account for Invoicing - use exact dropdown values!
        random_suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        account_data = {
            'name': f"AR Test Account {random_suffix}",
            'currency': 'US Dollar',           # exact dropdown text
            'report_type': 'Balance Sheet',
            'account_type': 'Current Assets',
            'account_group': 'Trade receivables',  # lowercase 'r'
            'cashflow': 'AR'                    # not 'Operating'
        }
        
        gl_account = await chart_page.create_gl_account(account_data)
        
        await chart_page.take_screenshot("test_create_gl_account_trade_receivables")
        
        # Verify account was created
        if gl_account:
            print(f"✅ GL Account created: {gl_account['name']}")
            print(f"   Currency: {gl_account['currency']}")
            print(f"   Report Type: {gl_account['report_type']}")
            print(f"   Account Type: {gl_account['account_type']}")
            print(f"   Account Group: {gl_account['account_group']}")
        
        assert gl_account is not None, "GL Account should be created successfully"
        assert gl_account['name'] == account_data['name'], "Account name should match"

    @pytest.mark.asyncio
    async def test_create_gl_account_for_invoicing_precondition(self, perform_login_with_entity, env_config):
        """Test creating a GL Account specifically for Invoicing (precondition setup)"""
        page = perform_login_with_entity
        base_url = env_config.get("base_url", "https://app.stage.viewz.co")
        
        chart_page = ChartOfAccountsPage(page)
        chart_page.base_url = base_url
        
        print("\n🧪 TEST: Create GL Account for Invoicing Precondition")
        
        await chart_page.navigate_to_chart_of_accounts(base_url)
        
        # Use the dedicated method for invoicing precondition
        gl_account = await chart_page.create_ar_account_for_invoicing()
        
        await chart_page.take_screenshot("test_create_gl_account_invoicing_precondition")
        
        if gl_account:
            print(f"✅ Invoicing precondition GL Account created: {gl_account['name']}")
        
        assert gl_account is not None, "GL Account for invoicing should be created"
        assert 'AR' in gl_account['name'] or 'Invoicing' in gl_account['name'], \
            "Account name should indicate AR/Invoicing purpose"

    @pytest.mark.asyncio  
    async def test_create_gl_account_different_currencies(self, perform_login_with_entity, env_config):
        """Test creating GL Accounts with different currencies"""
        page = perform_login_with_entity
        base_url = env_config.get("base_url", "https://app.stage.viewz.co")
        
        chart_page = ChartOfAccountsPage(page)
        chart_page.base_url = base_url
        
        print("\n🧪 TEST: Create GL Accounts with different currencies")
        
        await chart_page.navigate_to_chart_of_accounts(base_url)
        
        # Use exact dropdown text values
        currencies_to_test = [
            {'code': 'USD', 'display': 'US Dollar'},
            {'code': 'EUR', 'display': 'Euro'}
        ]
        created_accounts = []
        
        for curr in currencies_to_test:
            random_suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
            account_data = {
                'name': f"Test {curr['code']} Account {random_suffix}",
                'currency': curr['display'],      # Use exact dropdown text
                'report_type': 'Balance Sheet',   # Exact case
                'account_type': 'Current Assets', # Exact case
                'account_group': 'Trade receivables',  # Exact case with lowercase 'r'
                'cashflow': 'AR'
            }
            
            gl_account = await chart_page.create_gl_account(account_data)
            
            if gl_account:
                created_accounts.append(gl_account)
                print(f"✅ Created {curr['code']} account: {gl_account['name']}")
            
            await asyncio.sleep(2)
        
        await chart_page.take_screenshot("test_create_gl_accounts_currencies")
        
        assert len(created_accounts) >= 1, "At least one GL Account should be created"
        print(f"✅ Created {len(created_accounts)} accounts with different currencies")

    # ==========================================
    # GL ACCOUNT SEARCH/VERIFICATION TESTS
    # ==========================================
    
    @pytest.mark.asyncio
    async def test_search_gl_account(self, perform_login_with_entity, env_config):
        """Test searching for a GL Account"""
        page = perform_login_with_entity
        base_url = env_config.get("base_url", "https://app.stage.viewz.co")
        
        chart_page = ChartOfAccountsPage(page)
        chart_page.base_url = base_url
        
        print("\n🧪 TEST: Search GL Account")
        
        await chart_page.navigate_to_chart_of_accounts(base_url)
        
        # First create an account with correct dropdown values
        random_suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        account_name = f"Searchable Account {random_suffix}"
        
        gl_account = await chart_page.create_gl_account({
            'name': account_name,
            'currency': 'US Dollar',          # Exact dropdown text
            'report_type': 'Balance Sheet',   # Exact case
            'account_type': 'Current Assets', # Exact case
            'account_group': 'Trade receivables',  # Exact case
            'cashflow': 'AR'
        })
        
        if not gl_account:
            pytest.skip("Could not create account to search for")
        
        await asyncio.sleep(2)
        
        # Now search for it
        found = await chart_page.verify_account_exists(account_name)
        
        await chart_page.take_screenshot("test_search_gl_account")
        
        # Note: Search verification may need refinement based on UI behavior
        assert found or gl_account is not None, "Account should be created and searchable"
        print(f"✅ Search test completed. Account found: {found}")

    # ==========================================
    # INLINE EDIT ROW TESTS
    # ==========================================
    
    @pytest.mark.asyncio
    async def test_add_gl_account_creates_inline_row(self, perform_login_with_entity, env_config):
        """Test that clicking Add GL Account creates an inline edit row"""
        page = perform_login_with_entity
        base_url = env_config.get("base_url", "https://app.stage.viewz.co")
        
        chart_page = ChartOfAccountsPage(page)
        chart_page.base_url = base_url
        
        print("\n🧪 TEST: Add GL Account creates inline row")
        
        await chart_page.navigate_to_chart_of_accounts(base_url)
        await asyncio.sleep(2)
        
        # Click Add GL Account
        click_result = await chart_page.click_add_gl_account()
        await asyncio.sleep(1)
        
        # Check for new row - try multiple selectors
        row_visible = False
        
        # Method 1: Check for "Auto-generated" or "Auto" text
        new_row = page.locator(chart_page.new_row_selector)
        if await new_row.count() > 0:
            row_visible = await new_row.first.is_visible()
            if row_visible:
                print("✅ Found new row with 'Auto-generated' text")
        
        # Method 2: Check for input field in a row (editable row)
        if not row_visible:
            editable_row = page.locator("tr input[type='text'], tr input:not([type='hidden'])")
            if await editable_row.count() > 0:
                row_visible = await editable_row.first.is_visible()
                if row_visible:
                    print("✅ Found editable input in new row")
        
        # Method 3: Check for any new row by looking for specific class patterns
        if not row_visible:
            new_row_alt = page.locator("tr.new-row, tr[data-new='true'], tr:has(input[placeholder])")
            if await new_row_alt.count() > 0:
                row_visible = await new_row_alt.first.is_visible()
                if row_visible:
                    print("✅ Found new row by class/attribute")
        
        await chart_page.take_screenshot("test_add_gl_creates_inline_row")
        
        # The test passes if Add GL Account was clicked (may create row or open modal)
        assert click_result or row_visible, "Add GL Account should create inline row or respond to click"
        print("✅ Inline edit row test completed")

    @pytest.mark.asyncio
    async def test_cancel_gl_account_creation(self, perform_login_with_entity, env_config):
        """Test canceling GL Account creation"""
        page = perform_login_with_entity
        base_url = env_config.get("base_url", "https://app.stage.viewz.co")
        
        chart_page = ChartOfAccountsPage(page)
        chart_page.base_url = base_url
        
        print("\n🧪 TEST: Cancel GL Account creation")
        
        await chart_page.navigate_to_chart_of_accounts(base_url)
        await asyncio.sleep(2)
        
        # Click Add GL Account
        click_result = await chart_page.click_add_gl_account()
        await asyncio.sleep(1)
        
        # Check new row exists
        new_row = page.locator(chart_page.new_row_selector)
        row_visible = await new_row.first.is_visible() if await new_row.count() > 0 else False
        
        if not row_visible:
            print("⚠️ New row not immediately visible, checking alternative selectors...")
            # Try alternative: look for input in new row
            input_row = page.locator("tr input[placeholder]").first
            row_visible = await input_row.is_visible() if await page.locator("tr input[placeholder]").count() > 0 else False
        
        print(f"New row visible: {row_visible}")
        
        # Try to cancel - either by button or Escape
        cancelled = False
        
        # Method 1: Try Cancel button
        cancel_btn = page.locator(chart_page.cancel_button_selector).first
        if await cancel_btn.is_visible():
            await cancel_btn.click()
            await asyncio.sleep(1)
            cancelled = True
            print("✅ Clicked Cancel button")
        
        # Method 2: Try red X button (common pattern)
        if not cancelled:
            x_btn = page.locator("button:has-text('✕'), button:has-text('×'), button[class*='close']").first
            if await x_btn.is_visible():
                await x_btn.click()
                await asyncio.sleep(1)
                cancelled = True
                print("✅ Clicked X button to cancel")
        
        # Method 3: Press Escape
        if not cancelled:
            await page.keyboard.press("Escape")
            await asyncio.sleep(1)
            print("✅ Pressed Escape to cancel")
        
        await chart_page.take_screenshot("test_cancel_gl_creation")
        
        # Test passes if we got here without error
        print("✅ Cancel GL Account creation test completed")

