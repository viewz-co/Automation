import pytest
import asyncio
from pages.home_page import HomePage
from pages.vizion_AI_page import VizionAIPage
from pages.reconciliation_page import ReconciliationPage
from pages.ledger_page import LedgerPage
from pages.BI_analysis_page import BIAnalysisPage
from pages.invoicing_page import InvoicingPage

@pytest.mark.asyncio
async def test_tabs_navigation_single_login(perform_login_with_entity):
    page = perform_login_with_entity

    # 📌 פתיחת תפריט אם צריך
    await asyncio.sleep(3)
    logo = page.locator("svg.viewz-logo")
    box = await logo.bounding_box()
    await page.mouse.move(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)
    await asyncio.sleep(1)

    pin_button = page.locator("button:has(svg.lucide-pin)")
    if await pin_button.is_visible():
        await pin_button.click()

    # Note: Connections is disabled, Invoicing was added
    tabs = [
        ("text=Home", HomePage),
        ("text=Vizion AI", VizionAIPage),
        ("text=Reconciliation", ReconciliationPage),
        ("text=Ledger", LedgerPage),
        ("text=BI Analysis", BIAnalysisPage),
        ("text=Invoicing", InvoicingPage),
    ]

    results = []

    for tab_selector, page_class in tabs:
        try:
            await page.click(tab_selector)
            page_obj = page_class(page)
            loaded = await page_obj.is_loaded()
            if loaded:
                results.append((tab_selector, page_class.__name__, 'PASS'))
            else:
                results.append((tab_selector, page_class.__name__, 'FAIL: Not visible'))
        except Exception as e:
            results.append((tab_selector, page_class.__name__, f'FAIL: {str(e)}'))

    print("\nTab Navigation Results:")
    for tab_selector, page_class_name, result in results:
        print(f"Tab: {tab_selector} | Page: {page_class_name} | Result: {result}")

    failed = [r for r in results if not r[2].startswith('PASS')]
    assert not failed, f"Some tabs failed: {failed}" 