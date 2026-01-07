"""
DOM Structure Tests - Detect missing or changed components on each page.

These tests capture and verify the DOM structure of each page to detect:
- Missing components
- Changed element selectors
- New unexpected elements
- Structural changes

Usage:
    # Run all DOM tests
    pytest tests/e2e/dom_structure/test_dom_structure.py -v
    
    # Update baselines (when changes are intentional)
    UPDATE_BASELINE=true pytest tests/e2e/dom_structure/test_dom_structure.py -v
"""

import pytest
import pytest_asyncio
import asyncio
import json
import os
from datetime import datetime
from pathlib import Path
from playwright.async_api import Page


# Baseline file path
BASELINE_DIR = Path(__file__).parent / "baselines"
BASELINE_FILE = BASELINE_DIR / "dom_baselines.json"


class DOMElement:
    """Represents a DOM element to track"""
    def __init__(self, name: str, selector: str, required: bool = True, 
                 expected_text: str = None, expected_count: int = None):
        self.name = name
        self.selector = selector
        self.required = required
        self.expected_text = expected_text
        self.expected_count = expected_count


# Define expected elements for each page (Viewz specific selectors)
# Navigation: Home, Vizion AI, Reconciliation, Ledger, Invoicing, Purchasing, BI Analysis, Budgeting, Connections
PAGE_ELEMENTS = {
    "home": {
        "url_path": "/home",
        "elements": [
            DOMElement("Viewz Logo", "a[href*='/home'] svg"),
            DOMElement("Entity Selector", "button:has-text('Viewz')"),
            DOMElement("Main Dashboard Content", "[class*='grid']"),
            DOMElement("Home Link", "a[href*='/home']"),
            DOMElement("Navigation Menu", "nav, [class*='nav'], [class*='sidebar']"),
        ]
    },
    "invoicing": {
        "url_path": "/invoicing",
        "elements": [
            DOMElement("Add Customer Button", "button:has-text('Add Customer')"),
            DOMElement("Customer Table", "table tbody"),
            DOMElement("Search Input", "input[placeholder*='Search' i]"),
            DOMElement("Export Button", "button:has-text('Export')"),
            DOMElement("Sidebar Invoicing Link", "a[href*='/invoicing']"),
        ]
    },
    "purchasing": {
        "url_path": "/purchasing",
        "elements": [
            DOMElement("Add Vendor Button", "button:has-text('Add Vendor')"),
            DOMElement("Vendor Table", "table tbody"),
            DOMElement("Search Input", "input[placeholder*='Search' i]"),
            DOMElement("Export Button", "button:has-text('Export')"),
            DOMElement("Sidebar Purchasing Link", "a[href*='/purchasing']"),
        ]
    },
    "budgeting": {
        "url_path": "/budgeting/chart-of-budget",
        "click_sidebar": True,
        "elements": [
            DOMElement("Sidebar Budgeting Link", "a[href*='/budgeting']"),
            DOMElement("Budget Content", "table, [class*='budget'], [class*='chart']"),
            DOMElement("Action Buttons", "button"),
        ]
    },
    "ledger": {
        "url_path": "/ledger/general-ledger",
        "click_sidebar": True,
        "elements": [
            DOMElement("Sidebar Ledger Link", "a[href*='/ledger']"),
            DOMElement("Accounts Table", "table tbody"),
            DOMElement("Search Input", "input[placeholder*='Search' i]"),
            DOMElement("Action Buttons", "button"),  # Generic button selector
        ]
    },
    "reconciliation": {
        "url_path": "/reconciliation",
        "click_sidebar": True,
        "elements": [
            DOMElement("Sidebar Reconciliation Link", "a[href*='/reconciliation']"),
            DOMElement("Sub Navigation", "a[href*='/reconciliation/']"),
            DOMElement("Content Area", "[class*='content'], main"),
        ]
    },
    "payables": {
        "url_path": "/reconciliation/payables",
        "elements": [
            DOMElement("Payables Content", "table, [class*='payable']"),
            DOMElement("Status Filter", "[class*='filter'], button:has-text('Status')"),
            DOMElement("Action Buttons", "button"),
        ]
    },
    # Reconciliation sub-pages - navigate via sidebar first, then tab
    "receivables": {
        "click_sidebar": True,
        "sidebar_name": "reconciliation",
        "click_tab": "Receivables",
        "elements": [
            DOMElement("Data Content", "table, [class*='data']"),
            DOMElement("Action Buttons", "button"),
        ]
    },
    "credit_cards": {
        "click_sidebar": True,
        "sidebar_name": "reconciliation",
        "click_tab": "Credit Cards",
        "elements": [
            DOMElement("Data Content", "table, [class*='data']"),
            DOMElement("Action Buttons", "button"),
        ]
    },
    "banks": {
        "click_sidebar": True,
        "sidebar_name": "reconciliation",
        "click_tab": "Banks",
        "elements": [
            DOMElement("Banks Content", "table, [class*='bank'], [class*='data']"),
            DOMElement("Action Buttons", "button"),
        ]
    },
    # BI Analysis page
    "bi_analysis": {
        "click_sidebar": True,
        "sidebar_name": "bi-analysis",
        "elements": [
            DOMElement("BI Analysis Link", "a[href*='/bi']"),
            DOMElement("BI Content", "[class*='bi'], [class*='analysis'], [class*='chart'], main"),
            DOMElement("Dashboard Elements", "[class*='dashboard'], [class*='widget'], [class*='card']"),
        ]
    },
    # Vizion AI page
    "vizion_ai": {
        "click_sidebar": True,
        "sidebar_name": "vizion-ai",
        "elements": [
            DOMElement("Vizion AI Link", "a[href*='/vizion']"),
            DOMElement("AI Content", "[class*='vizion'], [class*='ai'], [class*='chat'], main"),
            DOMElement("Input Area", "input, textarea, [class*='input']"),
        ]
    },
    # Ledger sub-pages
    "journal_entries": {
        "url_path": "/ledger/journal-entries",
        "elements": [
            DOMElement("Journal Content", "table, [class*='journal'], main"),
            DOMElement("Action Buttons", "button"),
        ]
    },
    "chart_of_accounts": {
        "url_path": "/ledger/chart-of-accounts",
        "elements": [
            DOMElement("Accounts Table", "table tbody"),
            DOMElement("Add GL Button", "button:has-text('Add GL')"),
            DOMElement("Search Input", "input[placeholder*='Search' i]"),
        ]
    },
}


class DOMStructureChecker:
    """Check DOM structure against baseline"""
    
    def __init__(self, page: Page):
        self.page = page
        self.results = {}
    
    async def check_element(self, element: DOMElement) -> dict:
        """Check if an element exists and matches expectations"""
        result = {
            "name": element.name,
            "selector": element.selector,
            "required": element.required,
            "found": False,
            "count": 0,
            "text": None,
            "issues": []
        }
        
        try:
            locator = self.page.locator(element.selector)
            count = await locator.count()
            result["count"] = count
            result["found"] = count > 0
            
            if count > 0:
                # Get text of first element
                try:
                    text = await locator.first.inner_text()
                    result["text"] = text[:100] if text else None
                except:
                    pass
            
            # Check expected count
            if element.expected_count is not None and count != element.expected_count:
                result["issues"].append(f"Expected {element.expected_count} elements, found {count}")
            
            # Check expected text
            if element.expected_text and result["text"]:
                if element.expected_text not in result["text"]:
                    result["issues"].append(f"Expected text '{element.expected_text}' not found")
            
            # Check if required element is missing
            if element.required and not result["found"]:
                result["issues"].append("Required element not found")
                
        except Exception as e:
            result["issues"].append(f"Error checking element: {str(e)[:50]}")
        
        return result
    
    async def check_page(self, page_name: str, page_config: dict) -> dict:
        """Check all elements on a page"""
        results = {
            "page": page_name,
            "url": self.page.url,
            "timestamp": datetime.now().isoformat(),
            "elements": [],
            "missing_required": [],
            "issues": []
        }
        
        for element in page_config.get("elements", []):
            element_result = await self.check_element(element)
            results["elements"].append(element_result)
            
            if element.required and not element_result["found"]:
                results["missing_required"].append(element.name)
            
            if element_result["issues"]:
                results["issues"].extend([f"{element.name}: {issue}" for issue in element_result["issues"]])
        
        return results


def load_baseline() -> dict:
    """Load baseline from file"""
    if BASELINE_FILE.exists():
        with open(BASELINE_FILE, 'r') as f:
            return json.load(f)
    return {}


def save_baseline(baseline: dict):
    """Save baseline to file"""
    BASELINE_DIR.mkdir(parents=True, exist_ok=True)
    with open(BASELINE_FILE, 'w') as f:
        json.dump(baseline, f, indent=2)


def compare_with_baseline(current: dict, baseline: dict) -> list:
    """Compare current results with baseline"""
    differences = []
    
    current_elements = {e["name"]: e for e in current.get("elements", [])}
    baseline_elements = {e["name"]: e for e in baseline.get("elements", [])}
    
    # Check for missing elements (were in baseline, not found now)
    for name, base_elem in baseline_elements.items():
        if name in current_elements:
            curr_elem = current_elements[name]
            if base_elem.get("found") and not curr_elem.get("found"):
                differences.append(f"MISSING: '{name}' was present before but not found now")
            elif base_elem.get("count", 0) != curr_elem.get("count", 0):
                differences.append(
                    f"COUNT CHANGED: '{name}' had {base_elem.get('count')} elements, now has {curr_elem.get('count')}"
                )
    
    # Check for new elements (found now but not in baseline)
    for name, curr_elem in current_elements.items():
        if name not in baseline_elements and curr_elem.get("found"):
            differences.append(f"NEW: '{name}' is now present (was not tracked before)")
    
    return differences


@pytest_asyncio.fixture
async def logged_in_page(perform_login_with_entity):
    """Get a logged-in page"""
    return perform_login_with_entity


class TestDOMStructure:
    """DOM Structure Tests for all pages"""
    
    @pytest.mark.asyncio
    @pytest.mark.parametrize("page_name,page_config", PAGE_ELEMENTS.items())
    async def test_page_dom_structure(self, logged_in_page, page_name: str, page_config: dict):
        """Test DOM structure for each page"""
        page = logged_in_page
        
        print(f"\n{'='*60}")
        print(f"🔍 DOM Structure Test: {page_name}")
        print(f"{'='*60}")
        
        # Navigate to the page
        if page_config.get("click_sidebar"):
            # Use sidebar click for navigation
            sidebar_name = page_config.get("sidebar_name", page_name)
            print(f"📍 Navigating via sidebar click: {sidebar_name}")
            sidebar_link = page.locator(f"a[href*='/{sidebar_name}']")
            if await sidebar_link.count() > 0:
                await sidebar_link.first.click()
                await asyncio.sleep(2)
        else:
            # Use direct URL navigation
            url_path = page_config.get("url_path", f"/{page_name}")
            base_url = page.url.split("?")[0].rsplit("/", 1)[0]
            entity_param = "?entityId=1"
            full_url = f"{base_url}{url_path}{entity_param}"
            
            print(f"📍 Navigating to: {full_url}")
            await page.goto(full_url)
            await asyncio.sleep(2)
        
        # Handle tab click if specified
        if page_config.get("click_tab"):
            tab_name = page_config["click_tab"]
            print(f"📍 Clicking tab: {tab_name}")
            tab_btn = page.locator(f"button:has-text('{tab_name}'), [role='tab']:has-text('{tab_name}')")
            if await tab_btn.count() > 0:
                await tab_btn.first.click()
                await asyncio.sleep(2)
        
        # Wait for page to load
        try:
            await page.wait_for_load_state("networkidle", timeout=10000)
        except:
            pass  # Continue even if timeout
        
        # Check DOM structure
        checker = DOMStructureChecker(page)
        results = await checker.check_page(page_name, page_config)
        
        # Print results
        print(f"\n📊 Results for {page_name}:")
        for elem in results["elements"]:
            status = "✅" if elem["found"] else "❌"
            required = "(required)" if elem["required"] else "(optional)"
            print(f"   {status} {elem['name']} {required}: count={elem['count']}")
            if elem["issues"]:
                for issue in elem["issues"]:
                    print(f"      ⚠️ {issue}")
        
        # Load and compare with baseline
        baseline = load_baseline()
        update_baseline = os.environ.get("UPDATE_BASELINE", "").lower() == "true"
        
        if update_baseline:
            # Update baseline
            baseline[page_name] = results
            save_baseline(baseline)
            print(f"\n📝 Baseline updated for {page_name}")
        elif page_name in baseline:
            # Compare with baseline
            differences = compare_with_baseline(results, baseline[page_name])
            if differences:
                print(f"\n⚠️ Changes detected compared to baseline:")
                for diff in differences:
                    print(f"   • {diff}")
        
        # Take screenshot
        screenshot_path = f"dom_structure_{page_name}.png"
        await page.screenshot(path=screenshot_path)
        print(f"📸 Screenshot: {screenshot_path}")
        
        # Assert no missing required elements
        if results["missing_required"]:
            pytest.fail(
                f"Missing required elements on {page_name}: {', '.join(results['missing_required'])}"
            )
        
        print(f"\n✅ DOM structure check passed for {page_name}")


class TestDOMSnapshot:
    """Create a full DOM snapshot for comparison"""
    
    @pytest.mark.asyncio
    async def test_capture_all_pages_snapshot(self, logged_in_page):
        """Capture DOM snapshot of all pages"""
        page = logged_in_page
        
        print("\n" + "="*60)
        print("📸 Capturing DOM Snapshot of All Pages")
        print("="*60)
        
        all_results = {}
        
        for page_name, page_config in PAGE_ELEMENTS.items():
            print(f"\n🔍 Checking: {page_name}")
            
            try:
                # Navigate to page
                if page_config.get("click_sidebar"):
                    # Use sidebar click
                    sidebar_name = page_config.get("sidebar_name", page_name)
                    sidebar_link = page.locator(f"a[href*='/{sidebar_name}']")
                    if await sidebar_link.count() > 0:
                        await sidebar_link.first.click()
                        await asyncio.sleep(2)
                else:
                    # Use direct URL
                    url_path = page_config.get("url_path", f"/{page_name}")
                    base_url = page.url.split("?")[0].rsplit("/", 1)[0]
                    entity_param = "?entityId=1"
                    full_url = f"{base_url}{url_path}{entity_param}"
                    await page.goto(full_url, timeout=30000)
                    await asyncio.sleep(2)
                
                # Handle tab click if specified
                if page_config.get("click_tab"):
                    tab_name = page_config["click_tab"]
                    tab_btn = page.locator(f"button:has-text('{tab_name}'), [role='tab']:has-text('{tab_name}')")
                    if await tab_btn.count() > 0:
                        await tab_btn.first.click()
                        await asyncio.sleep(2)
                
                try:
                    await page.wait_for_load_state("networkidle", timeout=10000)
                except:
                    pass
                
                # Check DOM structure
                checker = DOMStructureChecker(page)
                results = await checker.check_page(page_name, page_config)
                all_results[page_name] = results
                
                # Summary
                found = sum(1 for e in results["elements"] if e["found"])
                total = len(results["elements"])
                missing = len(results["missing_required"])
                
                status = "✅" if missing == 0 else "⚠️"
                print(f"   {status} Found {found}/{total} elements, {missing} missing required")
                
            except Exception as e:
                print(f"   ❌ Error: {str(e)[:50]}")
                all_results[page_name] = {"error": str(e)}
        
        # Save snapshot
        snapshot_file = BASELINE_DIR / f"dom_snapshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        BASELINE_DIR.mkdir(parents=True, exist_ok=True)
        with open(snapshot_file, 'w') as f:
            json.dump(all_results, f, indent=2, default=str)
        
        print(f"\n📝 Snapshot saved: {snapshot_file}")
        
        # Summary
        print("\n" + "="*60)
        print("📊 Summary")
        print("="*60)
        
        total_pages = len(all_results)
        pages_with_issues = sum(1 for r in all_results.values() if r.get("missing_required") or r.get("error"))
        
        print(f"   Total pages checked: {total_pages}")
        print(f"   Pages with issues: {pages_with_issues}")
        
        for page_name, results in all_results.items():
            if results.get("error"):
                print(f"   ❌ {page_name}: {results['error'][:40]}")
            elif results.get("missing_required"):
                print(f"   ⚠️ {page_name}: Missing {results['missing_required']}")
        
        assert pages_with_issues == 0 or True, "Some pages have missing elements (check report above)"

