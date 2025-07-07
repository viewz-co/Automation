import pytest
import asyncio  # ← חובה אם אתה משתמש ב-sleep
# אין צורך ב-import locator אם לא משתמשים בו
from pages.home_page import HomePage
from pages.vizion_AI_page import VizionAIPage
from pages.reconciliation_page import ReconciliationPage
from pages.ledger_page import LedgerPage
from pages.BI_analysis_page import BIAnalysisPage
from pages.connection_page import ConnectionPage

@pytest.mark.asyncio
@pytest.mark.parametrize("tab_selector, page_class", [
    ("text=Home", HomePage),
    ("text=Vizion AI", VizionAIPage),
    ("text=Reconciliation", ReconciliationPage),
    ("text=Ledger", LedgerPage),
    ("text=BI Analysis", BIAnalysisPage),
    ("text=Connections", ConnectionPage),
])
async def test_tab_navigation(perform_login, tab_selector, page_class):
    page = perform_login

    # 📌 פתיחת תפריט אם צריך
    await asyncio.sleep(3)
    logo = page.locator("svg.viewz-logo")
    box = await logo.bounding_box()
    await page.mouse.move(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)
    await asyncio.sleep(1)

    pin_button = page.locator("button:has(svg.lucide-pin)")
    if await pin_button.is_visible():
        await pin_button.click()

    # 🧭 בדיקת הטאב with error handling
    try:
        await page.click(tab_selector)
        await asyncio.sleep(2)  # Give time for page to load
        page_obj = page_class(page)
        
        # Use a more robust check with timeout handling
        try:
            loaded = await page_obj.is_loaded()
            assert loaded, f"Page {page_class.__name__} did not load properly"
        except Exception as e:
            # For debugging: print what we actually see on the page
            print(f"\nDebugging {page_class.__name__}:")
            print(f"Current URL: {page.url}")
            print(f"Error: {str(e)}")
            
            # Re-raise the assertion error with more context
            raise AssertionError(f"Tab {tab_selector} -> {page_class.__name__} failed to load: {str(e)}")
            
    except Exception as e:
        pytest.fail(f"Tab navigation failed for {tab_selector}: {str(e)}")
