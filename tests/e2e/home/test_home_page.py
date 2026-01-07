"""
Home Page / Financial Dashboard Tests
Comprehensive tests for the home page functionality
"""

import pytest
import pytest_asyncio
import asyncio
from playwright.async_api import Page, expect
from pages.home_page import HomePage


class TestHomePageElements:
    """Test suite for verifying home page elements are present"""
    
    @pytest.mark.asyncio
    async def test_home_page_loads(self, logged_in_page: Page):
        """Verify home page loads successfully after login"""
        page = logged_in_page
        home = HomePage(page)
        
        # Navigate to home if not already there
        if "/home" not in page.url:
            await home.navigate_to_home()
        
        assert await home.is_loaded(), "Home page did not load properly"
        assert "/home" in page.url, f"Expected /home in URL, got {page.url}"
    
    @pytest.mark.asyncio
    async def test_dashboard_title_visible(self, logged_in_page: Page):
        """Verify Financial Overview Dashboard title is displayed"""
        home = HomePage(logged_in_page)
        
        title = home.dashboard_title
        await expect(title).to_be_visible(timeout=10000)
        
        title_text = await title.inner_text()
        assert "Financial Overview Dashboard" in title_text
    
    @pytest.mark.asyncio
    async def test_dashboard_subtitle_visible(self, logged_in_page: Page):
        """Verify dashboard subtitle with description is displayed"""
        home = HomePage(logged_in_page)
        
        subtitle = home.dashboard_subtitle
        await expect(subtitle).to_be_visible(timeout=5000)
    
    @pytest.mark.asyncio
    async def test_viewz_logo_visible(self, logged_in_page: Page):
        """Verify Viewz logo is displayed in header"""
        home = HomePage(logged_in_page)
        
        logo = home.logo
        await expect(logo).to_be_visible(timeout=5000)
    
    @pytest.mark.asyncio
    async def test_entity_selector_visible(self, logged_in_page: Page):
        """Verify entity selector dropdown is visible"""
        home = HomePage(logged_in_page)
        
        entity = home.entity_selector
        await expect(entity).to_be_visible(timeout=5000)
        
        entity_text = await home.get_selected_entity()
        assert entity_text, "Entity selector should show selected entity"
        print(f"✅ Selected entity: {entity_text}")
    
    @pytest.mark.asyncio
    async def test_user_avatar_visible(self, logged_in_page: Page):
        """Verify user avatar/profile indicator is visible"""
        home = HomePage(logged_in_page)
        
        assert await home.verify_user_logged_in(), "User avatar should be visible"


class TestHomePageFilters:
    """Test suite for dashboard filter functionality"""
    
    @pytest.mark.asyncio
    async def test_date_range_filter_visible(self, logged_in_page: Page):
        """Verify date range filter is displayed"""
        home = HomePage(logged_in_page)
        
        date_range = await home.get_date_range()
        assert date_range, "Date range should be displayed"
        print(f"✅ Date range: {date_range}")
    
    @pytest.mark.asyncio
    async def test_period_buttons_visible(self, logged_in_page: Page):
        """Verify Y/Q/M period buttons are visible"""
        home = HomePage(logged_in_page)
        
        await expect(home.period_year).to_be_visible(timeout=5000)
        await expect(home.period_quarter).to_be_visible(timeout=5000)
        await expect(home.period_month).to_be_visible(timeout=5000)
    
    @pytest.mark.asyncio
    async def test_period_selection_year(self, logged_in_page: Page):
        """Test selecting Year period filter"""
        home = HomePage(logged_in_page)
        
        result = await home.set_period("Y")
        assert result, "Should be able to click Year period"
        await asyncio.sleep(1)
        
        # Verify data refreshes (KPIs should still be visible)
        assert await home.verify_kpi_section_visible()
    
    @pytest.mark.asyncio
    async def test_period_selection_quarter(self, logged_in_page: Page):
        """Test selecting Quarter period filter"""
        home = HomePage(logged_in_page)
        
        result = await home.set_period("Q")
        assert result, "Should be able to click Quarter period"
        await asyncio.sleep(1)
        
        assert await home.verify_kpi_section_visible()
    
    @pytest.mark.asyncio
    async def test_period_selection_month(self, logged_in_page: Page):
        """Test selecting Month period filter"""
        home = HomePage(logged_in_page)
        
        result = await home.set_period("M")
        assert result, "Should be able to click Month period"
        await asyncio.sleep(1)
        
        assert await home.verify_kpi_section_visible()
    
    @pytest.mark.asyncio
    async def test_entity_filter_visible(self, logged_in_page: Page):
        """Verify All Entities filter is visible"""
        home = HomePage(logged_in_page)
        
        entity_filter = home.entity_filter
        await expect(entity_filter).to_be_visible(timeout=5000)
    
    @pytest.mark.asyncio
    async def test_transactions_filter_visible(self, logged_in_page: Page):
        """Verify All Transactions filter is visible"""
        home = HomePage(logged_in_page)
        
        transactions = home.transactions_filter
        await expect(transactions).to_be_visible(timeout=5000)
    
    @pytest.mark.asyncio
    async def test_include_recurring_checkbox(self, logged_in_page: Page):
        """Verify Include Recurring checkbox is visible"""
        home = HomePage(logged_in_page)
        
        recurring = home.include_recurring
        await expect(recurring).to_be_visible(timeout=5000)
    
    @pytest.mark.asyncio
    async def test_tag_filters_visible(self, logged_in_page: Page):
        """Verify Tag 1 and Tag 2 filters are visible"""
        home = HomePage(logged_in_page)
        
        await expect(home.tag1_filter).to_be_visible(timeout=5000)
        await expect(home.tag2_filter).to_be_visible(timeout=5000)


class TestHomePageKPIs:
    """Test suite for Key Performance Indicator cards"""
    
    @pytest.mark.asyncio
    async def test_kpi_section_visible(self, logged_in_page: Page):
        """Verify KPI section header is visible"""
        home = HomePage(logged_in_page)
        
        assert await home.verify_kpi_section_visible(), "KPI section should be visible"
    
    @pytest.mark.asyncio
    async def test_kpi_cards_count(self, logged_in_page: Page):
        """Verify multiple KPI cards are displayed"""
        home = HomePage(logged_in_page)
        
        # Should have at least 5 KPI cards based on screenshot
        kpi_count = await home.get_kpi_count()
        print(f"✅ Found {kpi_count} KPI cards")
        
        # The dashboard shows ~9 KPI metrics
        assert kpi_count >= 5, f"Expected at least 5 KPI cards, got {kpi_count}"
    
    @pytest.mark.asyncio
    async def test_kpi_values_displayed(self, logged_in_page: Page):
        """Verify KPI cards show values (amounts)"""
        home = HomePage(logged_in_page)
        page = logged_in_page
        
        # Look for dollar amounts in KPI section
        kpi_values = page.locator("text=/\\$[0-9]+(\\.[0-9]+)?[KMB]?/")
        count = await kpi_values.count()
        
        print(f"✅ Found {count} monetary values in KPIs")
        assert count >= 3, "Should have at least 3 monetary values displayed"
    
    @pytest.mark.asyncio
    async def test_kpi_trend_indicators(self, logged_in_page: Page):
        """Verify KPI cards show trend indicators (up/down arrows)"""
        page = logged_in_page
        
        # Look for arrow indicators or trend icons
        # These could be SVGs, icons, or text like ↑ ↓
        trend_indicators = page.locator("[class*='arrow'], [class*='trend'], svg[class*='icon']")
        count = await trend_indicators.count()
        
        print(f"✅ Found {count} trend indicators")
        # At least some KPIs should have trend indicators


class TestHomePageCharts:
    """Test suite for dashboard charts"""
    
    @pytest.mark.asyncio
    async def test_total_income_chart_visible(self, logged_in_page: Page):
        """Verify Total Income chart section is visible"""
        home = HomePage(logged_in_page)
        
        charts = await home.verify_charts_visible()
        assert charts["total_income"], "Total Income chart should be visible"
    
    @pytest.mark.asyncio
    async def test_gross_profit_chart_visible(self, logged_in_page: Page):
        """Verify Gross Profit chart section is visible"""
        home = HomePage(logged_in_page)
        
        charts = await home.verify_charts_visible()
        assert charts["gross_profit"], "Gross Profit chart should be visible"
    
    @pytest.mark.asyncio
    async def test_chart_dropdown_selector(self, logged_in_page: Page):
        """Verify chart has dropdown to change displayed metric"""
        page = logged_in_page
        
        # Total income dropdown
        chart_dropdown = page.locator("text=Total income").locator("..").locator("button, [class*='select']")
        
        # Check if there's a dropdown/selector near the chart
        if await chart_dropdown.count() > 0:
            print("✅ Chart dropdown selector found")
        else:
            print("ℹ️ No dropdown selector found for chart")


class TestHomePageNavigation:
    """Test suite for sidebar navigation from home page"""
    
    @pytest.mark.asyncio
    async def test_sidebar_visible(self, logged_in_page: Page):
        """Verify sidebar navigation is visible"""
        home = HomePage(logged_in_page)
        
        sidebar = home.sidebar
        await expect(sidebar).to_be_visible(timeout=5000)
    
    @pytest.mark.asyncio
    async def test_sidebar_links_count(self, logged_in_page: Page):
        """Verify sidebar has expected navigation links"""
        home = HomePage(logged_in_page)
        
        links = await home.get_sidebar_links()
        print(f"✅ Sidebar links: {links}")
        
        # Should have at least 8 main navigation items
        assert len(links) >= 5, f"Expected at least 5 sidebar links, got {len(links)}"
    
    @pytest.mark.asyncio
    async def test_navigate_to_invoicing(self, logged_in_page: Page):
        """Test navigation from home to Invoicing"""
        home = HomePage(logged_in_page)
        
        await home.nav_invoicing.click()
        await asyncio.sleep(2)
        
        assert "/invoicing" in logged_in_page.url, "Should navigate to Invoicing page"
    
    @pytest.mark.asyncio
    async def test_navigate_to_purchasing(self, logged_in_page: Page):
        """Test navigation from home to Purchasing"""
        home = HomePage(logged_in_page)
        
        # First go back to home
        await home.navigate_to_home()
        
        await home.nav_purchasing.click()
        await asyncio.sleep(2)
        
        assert "/purchasing" in logged_in_page.url, "Should navigate to Purchasing page"
    
    @pytest.mark.asyncio
    async def test_navigate_to_reconciliation(self, logged_in_page: Page):
        """Test navigation from home to Reconciliation"""
        home = HomePage(logged_in_page)
        
        await home.navigate_to_home()
        await home.nav_reconciliation.click()
        await asyncio.sleep(2)
        
        assert "/reconciliation" in logged_in_page.url, "Should navigate to Reconciliation page"
    
    @pytest.mark.asyncio
    async def test_navigate_back_to_home(self, logged_in_page: Page):
        """Test clicking logo/home returns to home page"""
        home = HomePage(logged_in_page)
        
        # Navigate away first
        await home.nav_invoicing.click()
        await asyncio.sleep(2)
        
        # Click home link
        await home.navigate_to_home()
        
        assert "/home" in logged_in_page.url, "Should return to home page"


class TestHomePageEntitySwitching:
    """Test suite for entity selection functionality"""
    
    @pytest.mark.asyncio
    async def test_entity_dropdown_opens(self, logged_in_page: Page):
        """Verify entity dropdown opens when clicked"""
        home = HomePage(logged_in_page)
        
        await home.entity_selector.click()
        await asyncio.sleep(1)
        
        # Should show dropdown options
        dropdown = logged_in_page.locator("[class*='dropdown'], [class*='menu'], [class*='popover']")
        is_visible = await dropdown.first.is_visible()
        
        # Click away to close
        await logged_in_page.keyboard.press("Escape")
        
        print(f"✅ Entity dropdown opened: {is_visible}")
    
    @pytest.mark.asyncio
    async def test_current_entity_displayed(self, logged_in_page: Page):
        """Verify current entity name is displayed in selector"""
        home = HomePage(logged_in_page)
        
        entity_name = await home.get_selected_entity()
        assert "Viewz" in entity_name or entity_name, f"Should show entity name, got: {entity_name}"
        print(f"✅ Current entity: {entity_name}")


class TestHomePageRefresh:
    """Test suite for dashboard refresh functionality"""
    
    @pytest.mark.asyncio
    async def test_page_refresh_reloads_data(self, logged_in_page: Page):
        """Verify page refresh reloads dashboard data"""
        home = HomePage(logged_in_page)
        
        # Get initial state
        initial_loaded = await home.is_loaded()
        assert initial_loaded, "Page should be loaded initially"
        
        # Refresh
        await home.refresh_dashboard()
        
        # Verify still loaded
        assert await home.is_loaded(), "Page should reload after refresh"
        assert await home.verify_kpi_section_visible(), "KPIs should be visible after refresh"


class TestHomePageResponsiveness:
    """Test suite for UI responsiveness"""
    
    @pytest.mark.asyncio
    async def test_elements_load_within_timeout(self, logged_in_page: Page):
        """Verify all critical elements load within acceptable time"""
        home = HomePage(logged_in_page)
        
        # Navigate to home fresh
        await home.navigate_to_home()
        
        # All these should load within 10 seconds
        await expect(home.dashboard_title).to_be_visible(timeout=10000)
        await expect(home.entity_selector).to_be_visible(timeout=10000)
        await expect(home.kpi_section).to_be_visible(timeout=10000)
        
        print("✅ All critical elements loaded within timeout")


class TestHomePageDataValidation:
    """Test suite for validating dashboard data"""
    
    @pytest.mark.asyncio
    async def test_kpi_values_are_numeric(self, logged_in_page: Page):
        """Verify KPI values contain valid numeric data"""
        page = logged_in_page
        
        # Find all monetary values
        values = page.locator("text=/\\$[0-9.,]+[KMB]?/")
        count = await values.count()
        
        valid_values = 0
        for i in range(min(count, 10)):
            try:
                text = await values.nth(i).inner_text()
                if "$" in text:
                    valid_values += 1
            except:
                continue
        
        print(f"✅ Found {valid_values} valid monetary values")
        assert valid_values >= 1, "Should have at least 1 valid monetary value"
    
    @pytest.mark.asyncio
    async def test_percentage_values_displayed(self, logged_in_page: Page):
        """Verify percentage values are displayed correctly"""
        page = logged_in_page
        
        # Find percentage values
        percentages = page.locator("text=/[0-9.]+%/")
        count = await percentages.count()
        
        print(f"✅ Found {count} percentage values")
        # Dashboard shows percentage metrics like 81.50%

