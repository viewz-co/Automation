"""
Home Page Object Model
Financial Overview Dashboard with KPIs, filters, and charts
"""

import asyncio
from playwright.async_api import Page, expect
from datetime import datetime
from typing import Optional, Dict, List


class HomePage:
    """Page Object for the Home/Dashboard page"""
    
    def __init__(self, page: Page):
        self.page = page
        
        # === HEADER ELEMENTS ===
        self.logo = page.locator("a[href*='/home'] svg").first
        self.entity_selector = page.locator("button:has-text('Viewz'), [class*='entity']").first
        self.user_avatar = page.locator("[class*='avatar'], button:has-text('Ss')").first
        
        # === SIDEBAR NAVIGATION ===
        self.sidebar = page.locator("nav, [class*='sidebar']").first
        self.nav_home = page.locator("a[href*='/home']").first
        self.nav_vizion = page.locator("a[href*='/vizion']").first
        self.nav_reconciliation = page.locator("a[href*='/reconciliation']").first
        self.nav_ledger = page.locator("a[href*='/ledger']").first
        self.nav_invoicing = page.locator("a[href*='/invoicing']").first
        self.nav_purchasing = page.locator("a[href*='/purchasing']").first
        self.nav_bi = page.locator("a[href*='/bi']").first
        self.nav_budgeting = page.locator("a[href*='/budgeting']").first
        self.nav_connections = page.locator("a[href*='/connections']").first
        
        # === DASHBOARD HEADER ===
        self.dashboard_title = page.locator("h1:has-text('Financial Overview Dashboard')")
        self.dashboard_subtitle = page.locator("text=Real-time insights")
        
        # === FILTERS ===
        self.entity_filter = page.locator("text=All Entities").first
        self.date_range = page.locator("[class*='date'], button:has-text('Jan')").first
        # Period buttons (single letter buttons)
        self.period_year = page.locator("button").filter(has_text="Y").first
        self.period_quarter = page.locator("button").filter(has_text="Q").first
        self.period_month = page.locator("button").filter(has_text="M").first
        self.transactions_filter = page.locator("text=All Transactions").first
        self.include_recurring = page.locator("text=Include Recurring").first
        self.tag1_filter = page.locator("text=All Tag 1").first
        self.tag2_filter = page.locator("text=All Tag 2").first
        
        # === KPI CARDS ===
        self.kpi_section = page.locator("text=Key Performance Indicators").first
        self.kpi_cards = page.locator("[class*='card'], [class*='kpi']")
        
        # === CHARTS ===
        self.total_income_chart = page.locator("text=Total income").first
        self.gross_profit_chart = page.locator("text=Gross Profit").first
    
    async def is_loaded(self) -> bool:
        """Check if home page is fully loaded"""
        try:
            await self.dashboard_title.wait_for(state="visible", timeout=10000)
            return True
        except:
            return False
    
    async def navigate_to_home(self):
        """Navigate to home page via sidebar"""
        await self.nav_home.click()
        await asyncio.sleep(2)
        await self.page.wait_for_load_state("networkidle")
    
    # === ENTITY SELECTOR METHODS ===
    
    async def get_selected_entity(self) -> str:
        """Get currently selected entity name"""
        return await self.entity_selector.inner_text()
    
    async def change_entity(self, entity_name: str) -> bool:
        """Change selected entity"""
        try:
            await self.entity_selector.click()
            await asyncio.sleep(1)
            entity_option = self.page.locator(f"text={entity_name}").first
            await entity_option.click()
            await asyncio.sleep(2)
            return True
        except Exception as e:
            print(f"Failed to change entity: {e}")
            return False
    
    # === FILTER METHODS ===
    
    async def get_date_range(self) -> str:
        """Get current date range"""
        date_element = self.page.locator("[class*='date'] button, button:has-text('Jan')").first
        return await date_element.inner_text()
    
    async def set_period(self, period: str) -> bool:
        """Set period filter (Y=Year, Q=Quarter, M=Month)"""
        try:
            # Use exact text match for single letter buttons
            period_btn = self.page.locator("button").filter(has_text=period).first
            if await period_btn.is_visible():
                await period_btn.click()
                await asyncio.sleep(1)
                return True
            return False
        except Exception as e:
            print(f"Failed to set period {period}: {e}")
            return False
    
    async def get_active_period(self) -> str:
        """Get currently active period (Y/Q/M)"""
        for period in ['Y', 'Q', 'M']:
            btn = self.page.locator(f"button:has-text('{period}')").first
            classes = await btn.get_attribute("class") or ""
            if "active" in classes or "selected" in classes:
                return period
        return "M"  # Default
    
    async def toggle_recurring(self) -> bool:
        """Toggle Include Recurring checkbox"""
        try:
            await self.include_recurring.click()
            await asyncio.sleep(1)
            return True
        except:
            return False
    
    # === KPI METHODS ===
    
    async def get_kpi_count(self) -> int:
        """Get number of KPI cards displayed"""
        return await self.kpi_cards.count()
    
    async def get_kpi_values(self) -> Dict[str, str]:
        """Get all KPI card values"""
        kpis = {}
        try:
            kpi_elements = self.page.locator("[class*='kpi'], [class*='metric']")
            count = await kpi_elements.count()
            
            for i in range(min(count, 10)):
                try:
                    element = kpi_elements.nth(i)
                    text = await element.inner_text()
                    lines = text.strip().split('\n')
                    if len(lines) >= 2:
                        kpis[lines[0]] = lines[1]
                except:
                    continue
        except:
            pass
        
        return kpis
    
    async def verify_kpi_section_visible(self) -> bool:
        """Verify KPI section is visible"""
        return await self.kpi_section.is_visible()
    
    # === CHART METHODS ===
    
    async def verify_charts_visible(self) -> Dict[str, bool]:
        """Verify chart sections are visible"""
        return {
            "total_income": await self.total_income_chart.is_visible(),
            "gross_profit": await self.gross_profit_chart.is_visible()
        }
    
    async def get_total_income_value(self) -> str:
        """Get Total Income chart value"""
        try:
            income_section = self.page.locator("text=Total income").locator("..").locator("..")
            value = await income_section.locator("[class*='value'], text=/\\$[0-9]+/").first.inner_text()
            return value
        except:
            return ""
    
    # === NAVIGATION METHODS ===
    
    async def get_sidebar_links(self) -> List[str]:
        """Get all sidebar navigation link texts"""
        links = []
        nav_links = self.page.locator("nav a, [class*='sidebar'] a")
        count = await nav_links.count()
        
        for i in range(count):
            try:
                text = await nav_links.nth(i).inner_text()
                if text.strip():
                    links.append(text.strip())
            except:
                continue
        
        return links
    
    async def click_sidebar_link(self, link_text: str) -> bool:
        """Click a sidebar navigation link"""
        try:
            link = self.page.locator(f"a:has-text('{link_text}')").first
            await link.click()
            await asyncio.sleep(2)
            return True
        except:
            return False
    
    # === UTILITY METHODS ===
    
    async def take_screenshot(self, name: str = "home_page"):
        """Take a screenshot of the current page state"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        await self.page.screenshot(path=f"{name}_{timestamp}.png", full_page=True)
    
    async def get_page_title(self) -> str:
        """Get the page title"""
        return await self.page.title()
    
    async def get_current_url(self) -> str:
        """Get current URL"""
        return self.page.url
    
    async def refresh_dashboard(self):
        """Refresh the dashboard data"""
        await self.page.reload()
        await self.page.wait_for_load_state("networkidle")
        await asyncio.sleep(2)
    
    async def verify_user_logged_in(self) -> bool:
        """Verify user avatar/profile is visible"""
        return await self.user_avatar.is_visible()
