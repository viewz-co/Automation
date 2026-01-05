"""
Refactored Navigation Tests with Entity Selection
Demonstrates the new pattern: Login > Entity Selection > Test Execution
"""

import pytest
import asyncio
from pages.home_page import HomePage
from pages.vizion_AI_page import VizionAIPage
from pages.reconciliation_page import ReconciliationPage
from pages.ledger_page import LedgerPage
from pages.BI_analysis_page import BIAnalysisPage
from pages.invoicing_page import InvoicingPage
from pages.purchasing_page import PurchasingPage
from pages.budgeting_page import BudgetingPage

# Test data for parametrized tests
# Note: Connections is disabled, Purchasing and Budgeting were added
tab_test_data = [
    ("Home", HomePage),
    ("Vizion AI", VizionAIPage),
    ("Reconciliation", ReconciliationPage),
    ("Ledger", LedgerPage),
    ("Invoicing", InvoicingPage),
    ("Purchasing", PurchasingPage),
    ("BI Analysis", BIAnalysisPage),
    ("Budgeting", BudgetingPage),
]

@pytest.mark.parametrize("text,page_class", tab_test_data, ids=[f"text={text}-{page_class.__name__}" for text, page_class in tab_test_data])
@pytest.mark.asyncio
async def test_tab_navigation_with_entity(perform_login_with_entity, text, page_class):
    """
    Refactored test: Login > Entity Selection > Tab Navigation
    
    This test demonstrates the new pattern where:
    1. User logs in with 2FA
    2. Entity is selected automatically
    3. Test proceeds with navigation
    """
    page = perform_login_with_entity
    
    print(f"🚀 Starting navigation test for {text} tab (with entity selection)")
    
    try:
        # Entity selection is already handled by the fixture
        print(f"✅ Entity selection completed, proceeding with {text} navigation")
        
        # 📌 Menu handling (existing pattern)
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
        
        print(f"✅ Successfully navigated to {text} tab with entity context")
        
    except Exception as e:
        print(f"❌ Failed to navigate to {text} tab: {str(e)}")
        raise


@pytest.mark.asyncio
async def test_entity_selection_validation(perform_login_with_entity):
    """
    Test to validate that entity selection is working correctly
    """
    page = perform_login_with_entity
    
    print("🧪 Testing entity selection validation...")
    
    # Import here to avoid circular imports
    from pages.entity_selector_page import EntitySelectorPage
    
    entity_selector = EntitySelectorPage(page)
    
    # Verify entity is selected
    entity_verified = await entity_selector.verify_entity_selected("Viewz Demo INC")
    assert entity_verified, "Entity selection verification failed"
    
    # Get available entities (for debugging)
    available_entities = await entity_selector.get_available_entities()
    print(f"📋 Available entities: {available_entities}")
    
    print("✅ Entity selection validation passed")


@pytest.mark.asyncio
async def test_tabs_navigation_single_login_with_entity(perform_login_with_entity):
    """
    Refactored single login test with entity selection
    Tests all tabs in one session with proper entity context
    """
    page = perform_login_with_entity

    print("🚀 Starting comprehensive navigation test with entity selection")

    # 📌 Menu handling
    await asyncio.sleep(3)
    logo = page.locator("svg.viewz-logo")
    box = await logo.bounding_box()
    await page.mouse.move(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)
    await asyncio.sleep(1)

    pin_button = page.locator("button:has(svg.lucide-pin)")
    if await pin_button.is_visible():
        await pin_button.click()

    tabs = [
        ("text=Home", HomePage),
        ("text=Vizion AI", VizionAIPage),
        ("text=Reconciliation", ReconciliationPage),
        ("text=Ledger", LedgerPage),
        ("text=Invoicing", InvoicingPage),
        ("text=Purchasing", PurchasingPage),
        ("text=BI Analysis", BIAnalysisPage),
        ("text=Budgeting", BudgetingPage),
    ]

    results = []

    for tab_selector, page_class in tabs:
        try:
            print(f"🔍 Testing {tab_selector} with entity context...")
            await page.click(tab_selector)
            page_obj = page_class(page)
            loaded = await page_obj.is_loaded()
            if loaded:
                results.append((tab_selector, page_class.__name__, 'PASS'))
                print(f"✅ {tab_selector} - PASSED")
            else:
                results.append((tab_selector, page_class.__name__, 'FAIL: Not visible'))
                print(f"❌ {tab_selector} - FAILED: Not visible")
        except Exception as e:
            results.append((tab_selector, page_class.__name__, f'FAIL: {str(e)}'))
            print(f"❌ {tab_selector} - FAILED: {str(e)}")

    print(f"\n📊 Navigation Results with Entity Selection:")
    print(f"=" * 50)
    for tab_selector, page_class_name, result in results:
        status_icon = "✅" if result.startswith('PASS') else "❌"
        print(f"{status_icon} {tab_selector} | {page_class_name} | {result}")

    failed = [r for r in results if not r[2].startswith('PASS')]
    assert not failed, f"Some tabs failed with entity selection: {failed}"
    
    print(f"🎉 All tabs navigation tests passed with entity selection!")


@pytest.mark.asyncio
async def test_navigate_to_invoicing(perform_login_with_entity):
    """
    Test dedicated navigation to Invoicing page
    Verifies the Invoicing page loads correctly with all expected elements
    """
    page = perform_login_with_entity
    
    print("🧪 Testing dedicated Invoicing page navigation...")
    
    # Import InvoicingPage
    from pages.invoicing_page import InvoicingPage
    
    invoicing_page = InvoicingPage(page)
    
    # Navigate to Invoicing
    await invoicing_page.navigate_to_invoicing()
    await asyncio.sleep(2)
    
    # Verify page loaded
    is_loaded = await invoicing_page.is_loaded()
    assert is_loaded, "Invoicing page should load successfully"
    
    # Verify URL contains invoicing
    current_url = page.url
    assert "invoicing" in current_url.lower(), f"URL should contain 'invoicing', got: {current_url}"
    
    # Check for key page elements
    elements_found = []
    
    # Check for Customer table
    try:
        table = page.locator("table")
        if await table.is_visible():
            elements_found.append("Customer Table")
            print("✅ Customer table is visible")
    except:
        pass
    
    # Check for Add Customer button
    try:
        add_btn = page.get_by_role("button", name="Add Customer")
        if await add_btn.is_visible():
            elements_found.append("Add Customer Button")
            print("✅ Add Customer button is visible")
    except:
        pass
    
    # Check for Customers tab
    try:
        customers_tab = page.get_by_text("Customers")
        if await customers_tab.is_visible():
            elements_found.append("Customers Tab")
            print("✅ Customers tab is visible")
    except:
        pass
    
    # Check for Invoices tab
    try:
        invoices_tab = page.get_by_text("Invoices")
        if await invoices_tab.is_visible():
            elements_found.append("Invoices Tab")
            print("✅ Invoices tab is visible")
    except:
        pass
    
    # Take screenshot
    await page.screenshot(path="test_navigate_to_invoicing.png")
    print(f"📸 Screenshot saved: test_navigate_to_invoicing.png")
    
    # At least some key elements should be present
    assert len(elements_found) >= 2, f"Expected at least 2 key elements, found: {elements_found}"
    
    print(f"✅ Invoicing page navigation successful!")
    print(f"📋 Elements found: {elements_found}")


@pytest.mark.asyncio
async def test_navigate_to_purchasing(perform_login_with_entity):
    """
    Test dedicated navigation to Purchasing page
    Verifies the Purchasing page loads correctly with all expected elements
    """
    page = perform_login_with_entity
    
    print("🧪 Testing dedicated Purchasing page navigation...")
    
    # Open menu if needed
    await asyncio.sleep(3)
    logo = page.locator("svg.viewz-logo")
    box = await logo.bounding_box()
    if box:
        await page.mouse.move(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)
        await asyncio.sleep(1)
    
    pin_button = page.locator("button:has(svg.lucide-pin)")
    if await pin_button.is_visible():
        await pin_button.click()
    
    # Navigate to Purchasing
    await page.click("text=Purchasing")
    await asyncio.sleep(2)
    
    # Import and verify page loaded
    from pages.purchasing_page import PurchasingPage
    purchasing_page = PurchasingPage(page)
    
    is_loaded = await purchasing_page.is_loaded()
    assert is_loaded, "Purchasing page should load successfully"
    
    # Verify URL contains purchasing
    current_url = page.url
    assert "purchasing" in current_url.lower(), f"URL should contain 'purchasing', got: {current_url}"
    
    # Check for key page elements
    elements_found = []
    
    # Check for table
    try:
        table = page.locator("table")
        if await table.is_visible():
            elements_found.append("Data Table")
            print("✅ Data table is visible")
    except:
        pass
    
    # Check for heading
    try:
        heading = page.get_by_role("heading", name="Purchasing")
        if await heading.is_visible():
            elements_found.append("Purchasing Heading")
            print("✅ Purchasing heading is visible")
    except:
        pass
    
    # Take screenshot
    await page.screenshot(path="test_navigate_to_purchasing.png")
    print(f"📸 Screenshot saved: test_navigate_to_purchasing.png")
    
    print(f"✅ Purchasing page navigation successful!")
    print(f"📋 Elements found: {elements_found}")


@pytest.mark.asyncio
async def test_navigate_to_budgeting(perform_login_with_entity):
    """
    Test dedicated navigation to Budgeting page
    Verifies the Budgeting page loads correctly with all expected elements
    """
    page = perform_login_with_entity
    
    print("🧪 Testing dedicated Budgeting page navigation...")
    
    # Open menu if needed
    await asyncio.sleep(3)
    logo = page.locator("svg.viewz-logo")
    box = await logo.bounding_box()
    if box:
        await page.mouse.move(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)
        await asyncio.sleep(1)
    
    pin_button = page.locator("button:has(svg.lucide-pin)")
    if await pin_button.is_visible():
        await pin_button.click()
    
    # Navigate to Budgeting
    await page.click("text=Budgeting")
    await asyncio.sleep(2)
    
    # Import and verify page loaded
    from pages.budgeting_page import BudgetingPage
    budgeting_page = BudgetingPage(page)
    
    is_loaded = await budgeting_page.is_loaded()
    assert is_loaded, "Budgeting page should load successfully"
    
    # Verify URL contains budget
    current_url = page.url
    assert "budget" in current_url.lower(), f"URL should contain 'budget', got: {current_url}"
    
    # Check for key page elements
    elements_found = []
    
    # Check for table
    try:
        table = page.locator("table")
        if await table.is_visible():
            elements_found.append("Data Table")
            print("✅ Data table is visible")
    except:
        pass
    
    # Check for heading
    try:
        heading = page.get_by_role("heading", name="Budgeting")
        if await heading.is_visible():
            elements_found.append("Budgeting Heading")
            print("✅ Budgeting heading is visible")
    except:
        pass
    
    # Take screenshot
    await page.screenshot(path="test_navigate_to_budgeting.png")
    print(f"📸 Screenshot saved: test_navigate_to_budgeting.png")
    
    print(f"✅ Budgeting page navigation successful!")
    print(f"📋 Elements found: {elements_found}")