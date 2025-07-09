import pytest
import asyncio  # ← חובה אם אתה משתמש ב-sleep
# אין צורך ב-import locator אם לא משתמשים בו
from pages.home_page import HomePage
from pages.vizion_AI_page import VizionAIPage
from pages.reconciliation_page import ReconciliationPage
from pages.ledger_page import LedgerPage
from pages.BI_analysis_page import BIAnalysisPage
from pages.connection_page import ConnectionPage

# Test data for parametrized tests
tab_test_data = [
    ("Home", HomePage),
    ("Vizion AI", VizionAIPage),
    ("Reconciliation", ReconciliationPage),
    ("Ledger", LedgerPage),
    ("BI Analysis", BIAnalysisPage),
    ("Connections", ConnectionPage),
]

@pytest.mark.parametrize("text,page_class", tab_test_data, ids=[f"text={text}-{page_class.__name__}" for text, page_class in tab_test_data])
@pytest.mark.asyncio
async def test_tab_navigation(perform_login, text, page_class):
    """Test navigation to different tabs and verify they load correctly"""
    page = perform_login
    
    try:
        # 📌 פתיחת תפריט אם צריך
        await asyncio.sleep(3)
        logo = page.locator("svg.viewz-logo")
        box = await logo.bounding_box()
        await page.mouse.move(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)
        await asyncio.sleep(1)

        pin_button = page.locator("button:has(svg.lucide-pin)")
        if await pin_button.is_visible():
            await pin_button.click()
        
        # Navigate to the tab
        await page.click(f"text={text}")
        await asyncio.sleep(2)  # Give time for page to load
        
        # Create page object and verify it loaded
        page_obj = page_class(page)
        
        # Check if the page loaded correctly
        is_loaded = await page_obj.is_loaded()
        assert is_loaded, f"Failed to load {text} tab - page validation failed"
        
        print(f"✅ Successfully navigated to {text} tab")
        
    except Exception as e:
        print(f"❌ Failed to navigate to {text} tab: {str(e)}")
        raise
