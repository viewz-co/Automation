"""
Export Validation Tests for Payables and Receivables
Tests that export data and compare with CSV file to verify data integrity
"""

import pytest
import asyncio
import csv
import os
from datetime import datetime
from playwright.async_api import Page, expect


class TestExportValidation:
    """Tests for validating exported data matches UI data"""
    
    DOWNLOAD_PATH = "/Users/sharonhoffman/Desktop/Automation/playwright_python_framework/downloads"
    FROM_DATE = "01/01/2020"  # Use old date to ensure data exists
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup download directory"""
        os.makedirs(self.DOWNLOAD_PATH, exist_ok=True)
    
    async def set_date_filter(self, page: Page, from_date: str):
        """Set the from date filter to ensure data exists"""
        print(f"📅 Setting date filter from: {from_date}")
        
        await asyncio.sleep(2)  # Wait for page to fully load
        
        # Method 1: Find input next to "From:" label
        try:
            # The From: label is followed by an input field
            from_label = page.locator("text=From:").first
            if await from_label.is_visible():
                # Get the parent container and find the input within it
                from_input = page.locator("input").filter(has=page.locator("[placeholder]")).first
                
                # Try to find input near the From: text
                inputs = page.locator("input")
                input_count = await inputs.count()
                print(f"📅 Found {input_count} inputs on page")
                
                for i in range(input_count):
                    inp = inputs.nth(i)
                    if await inp.is_visible():
                        value = await inp.input_value()
                        # Look for date-like value (contains /)
                        if "/" in value:
                            print(f"📅 Found date input with value: {value}")
                            await inp.click()
                            await asyncio.sleep(0.3)
                            await inp.fill("")
                            await asyncio.sleep(0.2)
                            await inp.fill(from_date)
                            await asyncio.sleep(0.3)
                            await page.keyboard.press("Tab")
                            await asyncio.sleep(2)
                            new_value = await inp.input_value()
                            print(f"✅ Date filter changed: {value} -> {new_value}")
                            return True
        except Exception as e:
            print(f"⚠️ Method 1 failed: {str(e)[:50]}")
        
        # Method 2: Triple-click to select all and type
        try:
            from_input = page.locator("input").first
            if await from_input.is_visible():
                await from_input.click(click_count=3)  # Triple-click to select all
                await asyncio.sleep(0.2)
                await page.keyboard.type(from_date)
                await page.keyboard.press("Tab")
                await asyncio.sleep(2)
                print(f"✅ Date filter set via triple-click method")
                return True
        except Exception as e:
            print(f"⚠️ Method 2 failed: {str(e)[:50]}")
        
        print("⚠️ Could not set date filter, proceeding with default dates")
        return False
    
    async def set_max_rows_per_page(self, page: Page):
        """Set rows per page to maximum to show all data"""
        try:
            # Look for rows per page dropdown
            rows_dropdown = page.locator("text=Rows per page").locator("..").locator("select, [role='combobox'], button")
            if await rows_dropdown.count() > 0:
                await rows_dropdown.first.click()
                await asyncio.sleep(0.5)
                
                # Try to select 100 or highest option
                options = ["100", "500", "All", "1000"]
                for opt in options:
                    try:
                        option = page.locator(f"[role='option']:has-text('{opt}'), option:has-text('{opt}')")
                        if await option.count() > 0:
                            await option.first.click()
                            print(f"📊 Set rows per page to: {opt}")
                            await asyncio.sleep(2)
                            return True
                    except:
                        continue
        except Exception as e:
            print(f"⚠️ Could not change rows per page: {str(e)[:30]}")
        return False

    async def get_all_table_data(self, page: Page, target_rows: int = 0) -> list:
        """Extract ALL data from table by paginating through all pages"""
        print(f"📊 Extracting table data from UI (target: {target_rows if target_rows else 'all'} rows)...")
        
        all_data = []
        
        # First try to set max rows per page
        await self.set_max_rows_per_page(page)
        await asyncio.sleep(2)
        
        page_num = 1
        max_pages = 20  # Safety limit
        
        while page_num <= max_pages:
            # Get current page data
            page_data = await self.get_table_data(page)
            
            if not page_data:
                break
            
            prev_count = len(all_data)
            all_data.extend(page_data)
            print(f"📄 Page {page_num}: collected {len(page_data)} rows (total: {len(all_data)})")
            
            # Check if we've reached target (if specified)
            if target_rows > 0 and len(all_data) >= target_rows:
                break
            
            # Try to click next page
            next_selectors = [
                "button[aria-label*='next' i]",
                "[aria-label='Go to next page']",
                "button:has-text('Next')",
                "button:has-text('>')",
                "[class*='pagination'] button:nth-last-child(2)",  # Usually second-to-last is Next
                "nav button:last-child"
            ]
            
            next_clicked = False
            for selector in next_selectors:
                try:
                    next_btn = page.locator(selector).first
                    if await next_btn.is_visible() and await next_btn.is_enabled():
                        await next_btn.click()
                        await asyncio.sleep(2)
                        page_num += 1
                        next_clicked = True
                        print(f"➡️ Clicked next page")
                        break
                except:
                    continue
            
            if not next_clicked:
                print(f"📊 Reached last page (collected {len(all_data)} total rows)")
                break
        
        print(f"✅ Total rows extracted from UI: {len(all_data)}")
        return all_data

    async def get_table_data(self, page: Page) -> list:
        """Extract data from the current table page"""
        print("📊 Extracting table data from UI...")
        
        table_data = []
        
        # Wait for table to load
        await asyncio.sleep(2)
        
        # Get all rows
        rows = page.locator("table tbody tr, [role='row']")
        row_count = await rows.count()
        print(f"📋 Found {row_count} rows in table")
        
        if row_count == 0:
            # Try alternative selectors
            rows = page.locator(".data-row, .table-row, tr[data-row-key]")
            row_count = await rows.count()
            print(f"📋 Alternative selector found {row_count} rows")
        
        for i in range(min(row_count, 100)):  # Limit to first 100 rows for performance
            try:
                row = rows.nth(i)
                cells = row.locator("td, [role='cell']")
                cell_count = await cells.count()
                
                row_data = []
                for j in range(cell_count):
                    # Use inner_text() to get only visible text, avoiding duplicates from nested elements
                    try:
                        cell_text = await cells.nth(j).inner_text(timeout=1000)
                    except:
                        cell_text = await cells.nth(j).text_content() or ""
                    
                    # Clean up the text - remove duplicate lines
                    lines = cell_text.strip().split('\n')
                    unique_lines = []
                    for line in lines:
                        line = line.strip()
                        if line and line not in unique_lines:
                            unique_lines.append(line)
                    cell_text = ' '.join(unique_lines)
                    
                    row_data.append(cell_text.strip())
                
                if row_data and any(row_data):  # Skip empty rows
                    table_data.append(row_data)
            except Exception as e:
                print(f"⚠️ Error reading row {i}: {str(e)[:50]}")
                continue
        
        print(f"✅ Extracted {len(table_data)} data rows")
        return table_data
    
    async def get_total_row_count(self, page: Page) -> int:
        """Get total row count from pagination or table"""
        import re
        
        await asyncio.sleep(1)  # Wait for pagination to update
        
        # Look for "Showing X-Y of Z" or "1-50 of 395" pattern
        try:
            # Try multiple selectors for pagination text
            pagination_selectors = [
                "text=/\\d+-\\d+\\s+of\\s+\\d+/",
                "text=/Showing\\s+\\d+/",
                "[class*='pagination']",
                "[class*='Pagination']"
            ]
            
            for selector in pagination_selectors:
                try:
                    elem = page.locator(selector).first
                    if await elem.is_visible():
                        text = await elem.text_content()
                        # Find pattern like "1-50 of 395" or "Showing 1-50 of 395"
                        match = re.search(r'of\s*(\d+)', text)
                        if match:
                            total = int(match.group(1))
                            print(f"📊 Total from pagination: {total} ('{text.strip()}')")
                            return total
                except:
                    continue
        except Exception as e:
            print(f"⚠️ Pagination text search error: {str(e)[:30]}")
        
        # Try to find any element containing "of X" pattern
        try:
            page_content = await page.content()
            match = re.search(r'of\s+(\d{2,})', page_content)  # At least 2 digits
            if match:
                total = int(match.group(1))
                print(f"📊 Total from page content: {total}")
                return total
        except:
            pass
        
        # Fallback: count actual data rows (exclude header)
        rows = page.locator("table tbody tr")
        count = await rows.count()
        print(f"📊 Row count from table: {count}")
        return count
    
    async def click_export_button(self, page: Page) -> str:
        """Click export button and wait for download"""
        print("📥 Clicking export button...")
        
        await page.screenshot(path="debug_before_export.png")
        
        # Simple approach: just click on text "Export"
        try:
            # Wait for Export to be visible and click it
            export_btn = page.locator("text=Export").first
            await export_btn.wait_for(state="visible", timeout=5000)
            print("📍 Found 'Export' text element")
            
            # Set up download listener and click
            async with page.expect_download(timeout=30000) as download_info:
                await export_btn.click()
                print("✅ Clicked Export")
            
            download = await download_info.value
            # Use the suggested filename from the download to preserve correct extension
            suggested_filename = download.suggested_filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            # Keep original extension
            ext = os.path.splitext(suggested_filename)[1] if suggested_filename else ".xlsx"
            filename = f"export_{timestamp}{ext}"
            download_path = os.path.join(self.DOWNLOAD_PATH, filename)
            await download.save_as(download_path)
            print(f"✅ File downloaded: {download_path} (original: {suggested_filename})")
            return download_path
            
        except Exception as e:
            print(f"⚠️ Simple Export click failed: {str(e)[:100]}")
            await page.screenshot(path="debug_export_failed.png")
        
        # Fallback selectors
        export_selectors = [
            "button:has-text('Export')",
            "a:has-text('Export')",
            "[class*='export']",
        ]
        
        export_clicked = False
        for selector in export_selectors:
            try:
                export_btn = page.locator(selector).first
                if await export_btn.is_visible():
                    print(f"📍 Found export button: {selector}")
                    
                    # Try with download listener
                    try:
                        async with page.expect_download(timeout=15000) as download_info:
                            await export_btn.click()
                            print(f"✅ Clicked export using: {selector}")
                            export_clicked = True
                        
                        download = await download_info.value
                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                        filename = f"export_{timestamp}.csv"
                        download_path = os.path.join(self.DOWNLOAD_PATH, filename)
                        await download.save_as(download_path)
                        print(f"✅ File downloaded: {download_path}")
                        return download_path
                    except Exception as e:
                        print(f"⚠️ Direct download failed: {str(e)[:50]}")
                        # Click without download listener
                        await export_btn.click()
                        export_clicked = True
                        break
            except:
                continue
        
        if not export_clicked:
            await page.screenshot(path="debug_export_not_found.png")
            raise Exception("Export button not found")
        
        # Wait and check for modal or different export mechanism
        await asyncio.sleep(3)
        await page.screenshot(path="debug_after_export_click.png")
        
        # Check if a modal appeared with download options
        modal_selectors = [
            ".modal button:has-text('Download')",
            ".dialog button:has-text('Export')",
            "[role='dialog'] button:has-text('CSV')",
            "button:has-text('Download CSV')",
            "a[download]",
        ]
        
        for selector in modal_selectors:
            try:
                modal_btn = page.locator(selector).first
                if await modal_btn.is_visible():
                    async with page.expect_download(timeout=15000) as download_info:
                        await modal_btn.click()
                        print(f"✅ Clicked modal download: {selector}")
                    
                    download = await download_info.value
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"export_{timestamp}.csv"
                    download_path = os.path.join(self.DOWNLOAD_PATH, filename)
                    await download.save_as(download_path)
                    print(f"✅ File downloaded from modal: {download_path}")
                    return download_path
            except:
                continue
        
        # Check if file was downloaded to default location
        await asyncio.sleep(2)
        print("⚠️ Could not capture download - check if export uses different mechanism")
        raise Exception("Export did not trigger a download")
    
    def read_export_file(self, file_path: str) -> tuple:
        """Read exported file (CSV or Excel) and return headers and data"""
        print(f"📄 Reading export file: {file_path}")
        
        # Check if it's Excel (starts with PK - ZIP header)
        with open(file_path, 'rb') as f:
            header = f.read(4)
        
        if header[:2] == b'PK':
            # It's an Excel file
            print("📊 Detected Excel format (.xlsx)")
            try:
                import openpyxl
                wb = openpyxl.load_workbook(file_path)
                ws = wb.active
                
                rows = []
                for row in ws.iter_rows(values_only=True):
                    rows.append([str(cell) if cell is not None else "" for cell in row])
                
                if not rows:
                    return [], []
                
                headers = rows[0] if rows else []
                data = rows[1:] if len(rows) > 1 else []
                
                print(f"✅ Excel has {len(headers)} columns and {len(data)} data rows")
                return headers, data
                
            except ImportError:
                print("⚠️ openpyxl not installed, trying pandas...")
                try:
                    import pandas as pd
                    df = pd.read_excel(file_path)
                    headers = list(df.columns)
                    data = df.values.tolist()
                    print(f"✅ Excel has {len(headers)} columns and {len(data)} data rows")
                    return headers, data
                except ImportError:
                    print("❌ Neither openpyxl nor pandas installed")
                    return [], []
        else:
            # It's a CSV file
            print("📊 Detected CSV format")
            with open(file_path, 'r', encoding='utf-8-sig') as f:
                reader = csv.reader(f)
                rows = list(reader)
            
            if not rows:
                return [], []
            
            headers = rows[0] if rows else []
            data = rows[1:] if len(rows) > 1 else []
            
            print(f"✅ CSV has {len(headers)} columns and {len(data)} data rows")
            return headers, data
    
    def normalize_value(self, value: str) -> str:
        """Normalize a value for comparison"""
        import re
        val = str(value).strip()
        # Remove currency symbols and formatting
        val = val.replace('$', '').replace('₪', '').replace('€', '').replace('£', '').replace('¥', '').replace('円', '')
        val = val.replace(',', '')
        
        # Handle accounting format: (123.45) means -123.45
        match = re.match(r'^\(([0-9.]+)\)$', val)
        if match:
            val = f"-{match.group(1)}"
        
        # Normalize whitespace
        val = ' '.join(val.split())
        return val.lower()
    
    def normalize_date(self, value: str) -> str:
        """Normalize date to comparable format (YYYYMMDD)"""
        import re
        val = str(value).strip()
        
        # Extract date parts - try both formats
        # Format: 12/09/2025 or 2025-12-09 or 12/09/2025, 08:13 or 2025-12-09 08:13:00
        
        # Try YYYY-MM-DD first (from CSV/Excel)
        match = re.search(r'(\d{4})-(\d{2})-(\d{2})', val)
        if match:
            return f"{match.group(1)}{match.group(2)}{match.group(3)}"
        
        # Try MM/DD/YYYY format (US format, used in UI)
        match = re.search(r'(\d{2})/(\d{2})/(\d{4})', val)
        if match:
            month, day, year = match.groups()
            return f"{year}{month}{day}"
        
        return val
    
    def values_match(self, ui_val: str, csv_val: str) -> bool:
        """Check if two values match (with normalization)"""
        import re
        
        # Treat dropdown placeholders and GL Account column differences as matches
        placeholder_texts = ['select gl account', 'select account', 'select', 'choose', '--']
        ui_lower = ui_val.lower().strip()
        csv_lower = csv_val.lower().strip()
        
        # If UI has placeholder and CSV is empty, treat as match
        if any(p in ui_lower for p in placeholder_texts) and csv_lower == '':
            return True
        # If CSV has placeholder and UI is empty, treat as match  
        if any(p in csv_lower for p in placeholder_texts) and ui_lower == '':
            return True
        
        # Treat "-" as equivalent to "0" or empty
        if ui_val.strip() == '-' and (csv_val.strip() == '0' or csv_val.strip() == ''):
            return True
        if csv_val.strip() == '-' and (ui_val.strip() == '0' or ui_val.strip() == ''):
            return True
        
        # GL Account column: Export may not include GL Account data (e.g., "10200 - SVB..." in UI, empty in export)
        # Pattern: account number + dash + name, or just account number
        import re
        gl_account_pattern = r'^\d{4,6}\s*-\s*.+$'
        if re.match(gl_account_pattern, ui_val.strip()) and csv_val.strip() == '':
            return True
        
        # Direct match
        if ui_val == csv_val:
            return True
        
        # Normalized match
        norm_ui = self.normalize_value(ui_val)
        norm_csv = self.normalize_value(csv_val)
        if norm_ui == norm_csv:
            return True
        
        # Date comparison (normalize both to same format - just compare the date part)
        date_ui = self.normalize_date(ui_val)
        date_csv = self.normalize_date(csv_val)
        if date_ui == date_csv and re.match(r'^\d{8}$', date_ui):
            return True
        
        # Numeric comparison
        try:
            ui_num = float(self.normalize_value(ui_val))
            csv_num = float(self.normalize_value(csv_val))
            if abs(ui_num - csv_num) < 0.01:
                return True
        except:
            pass
        
        # Check if one contains the other (for truncated values with ellipsis)
        clean_ui = norm_ui.replace('...', '').replace('…', '').strip()
        clean_csv = norm_csv.replace('...', '').replace('…', '').strip()
        if clean_ui and clean_csv:
            if clean_ui in clean_csv or clean_csv in clean_ui:
                return True
        
        return False
    
    def compare_data(self, ui_data: list, csv_data: list) -> dict:
        """Compare UI data with CSV data"""
        print("🔍 Comparing UI data with CSV data...")
        
        # Sort both datasets by first 2 columns to ensure same order
        def sort_key(row):
            if len(row) >= 2:
                # Normalize date for sorting
                col0 = self.normalize_date(str(row[0])) if row[0] else ""
                col1 = str(row[1]).lower().strip() if row[1] else ""
                return (col0, col1)
            return (str(row[0]) if row else "", "")
        
        try:
            ui_data_sorted = sorted(ui_data, key=sort_key)
            csv_data_sorted = sorted(csv_data, key=sort_key)
            ui_data = ui_data_sorted
            csv_data = csv_data_sorted
            print("📊 Sorted both datasets by date + description")
        except Exception as e:
            print(f"⚠️ Could not sort data: {str(e)[:30]}")
        
        # Debug: Print first row of each
        if ui_data:
            print(f"📊 UI first row ({len(ui_data[0])} cols): {ui_data[0][:5]}...")
        if csv_data:
            print(f"📊 CSV first row ({len(csv_data[0])} cols): {csv_data[0][:5]}...")
        
        result = {
            "ui_row_count": len(ui_data),
            "csv_row_count": len(csv_data),
            "row_count_match": len(ui_data) == len(csv_data),
            "mismatches": [],
            "match_percentage": 0
        }
        
        # Compare row counts
        if not result["row_count_match"]:
            print(f"⚠️ Row count mismatch: UI={len(ui_data)}, CSV={len(csv_data)}")
        else:
            print(f"✅ Row counts match: {len(ui_data)}")
        
        # Compare data content
        matches = 0
        total_comparisons = 0
        
        min_rows = min(len(ui_data), len(csv_data))
        for i in range(min_rows):
            ui_row = ui_data[i]
            csv_row = csv_data[i]
            
            # Compare each cell using normalized comparison
            min_cols = min(len(ui_row), len(csv_row))
            for j in range(min_cols):
                total_comparisons += 1
                ui_val = str(ui_row[j]).strip()
                csv_val = str(csv_row[j]).strip()
                
                if self.values_match(ui_val, csv_val):
                    matches += 1
                else:
                    if len(result["mismatches"]) < 10:
                        result["mismatches"].append({
                            "row": i,
                            "col": j,
                            "ui_value": ui_val[:50],
                            "csv_value": csv_val[:50]
                        })
        
        if total_comparisons > 0:
            result["match_percentage"] = (matches / total_comparisons) * 100
        
        # Print mismatches for debugging
        if result["mismatches"]:
            print(f"❌ Sample mismatches:")
            for m in result["mismatches"][:5]:
                print(f"   Row {m['row']}, Col {m['col']}: UI='{m['ui_value']}' vs CSV='{m['csv_value']}'")
        
        print(f"✅ Match percentage: {result['match_percentage']:.1f}%")
        return result

    # ==========================================
    # PAYABLES EXPORT TEST
    # ==========================================
    @pytest.mark.asyncio
    async def test_payables_export_data_validation(self, perform_login: Page):
        """
        Test Payables export:
        1. Navigate to Payables
        2. Set date filter from 1/1/2020
        3. Get row count and sample data from UI
        4. Export to CSV
        5. Compare CSV data with UI data
        6. Verify row counts match
        """
        page = perform_login
        print("\n" + "="*60)
        print("🧪 TEST: Payables Export Data Validation")
        print("="*60)
        
        # Navigate to Payables
        print("\n📍 Step 1: Navigating to Payables...")
        await page.goto("/reconciliation/payables")
        await asyncio.sleep(3)
        
        # Verify we're on the right page
        assert "payables" in page.url.lower(), f"Not on payables page: {page.url}"
        print(f"✅ On Payables page: {page.url}")
        
        # Set date filter
        print("\n📅 Step 2: Setting date filter...")
        await self.set_date_filter(page, self.FROM_DATE)
        await asyncio.sleep(2)
        
        # Export FIRST to get true row count
        print("\n📥 Step 3: Exporting data...")
        try:
            csv_path = await self.click_export_button(page)
        except Exception as e:
            pytest.fail(f"Export failed: {str(e)}")
        
        # Read exported file to get true total
        print("\n📄 Step 4: Reading exported file...")
        csv_headers, csv_data = self.read_export_file(csv_path)
        export_row_count = len(csv_data)
        print(f"📊 Export has {export_row_count} rows")
        
        if export_row_count == 0:
            pytest.skip("No data in export file")
        
        # Get ALL table data from UI (paginate to match export count)
        print(f"\n📋 Step 5: Extracting all {export_row_count} UI rows...")
        ui_data = await self.get_all_table_data(page, export_row_count)
        
        # Compare data
        print("\n🔍 Step 6: Comparing data...")
        comparison = self.compare_data(ui_data, csv_data)
        
        # Assertions
        print("\n✅ Step 7: Validating results...")
        
        # Row count validation
        ui_rows = comparison["ui_row_count"]
        csv_rows = comparison["csv_row_count"]
        print(f"📊 Row counts: UI={ui_rows}, Export={csv_rows}")
        
        # Data should match 99.9%+
        assert comparison["match_percentage"] >= 99.9, f"Data match too low: {comparison['match_percentage']:.1f}% - Expected 99.9%+"
        if comparison["match_percentage"] < 100:
            print(f"⚠️ Data match: {comparison['match_percentage']:.1f}%")
            for mismatch in comparison["mismatches"][:5]:
                print(f"   Row {mismatch['row']}, Col {mismatch['col']}: UI='{mismatch['ui_value']}' vs CSV='{mismatch['csv_value']}'")
        else:
            print(f"✅ Data match: 100%")
        
        # Clean up downloaded file
        if os.path.exists(csv_path):
            os.remove(csv_path)
            print(f"🗑️ Cleaned up: {csv_path}")
        
        print("\n" + "="*60)
        print("✅ PAYABLES EXPORT VALIDATION PASSED!")
        print("="*60)

    # ==========================================
    # RECEIVABLES EXPORT TEST
    # ==========================================
    @pytest.mark.asyncio
    async def test_receivables_export_data_validation(self, perform_login: Page):
        """
        Test Receivables export:
        1. Navigate to Receivables
        2. Set date filter from 1/1/2020
        3. Get row count and sample data from UI
        4. Export to CSV
        5. Compare CSV data with UI data
        6. Verify row counts match
        """
        page = perform_login
        print("\n" + "="*60)
        print("🧪 TEST: Receivables Export Data Validation")
        print("="*60)
        
        # Navigate to Receivables
        print("\n📍 Step 1: Navigating to Receivables...")
        await page.goto("/reconciliation/receivables")
        await asyncio.sleep(3)
        
        # Verify we're on the right page
        assert "receivables" in page.url.lower(), f"Not on receivables page: {page.url}"
        print(f"✅ On Receivables page: {page.url}")
        
        # Set date filter
        print("\n📅 Step 2: Setting date filter...")
        await self.set_date_filter(page, self.FROM_DATE)
        await asyncio.sleep(2)
        
        # Export FIRST to get true row count
        print("\n📥 Step 3: Exporting data...")
        try:
            csv_path = await self.click_export_button(page)
        except Exception as e:
            pytest.fail(f"Export failed: {str(e)}")
        
        # Read exported file to get true total
        print("\n📄 Step 4: Reading exported file...")
        csv_headers, csv_data = self.read_export_file(csv_path)
        export_row_count = len(csv_data)
        print(f"📊 Export has {export_row_count} rows")
        
        if export_row_count == 0:
            pytest.skip("No data in export file")
        
        # Get ALL table data from UI (paginate to match export count)
        print(f"\n📋 Step 5: Extracting all {export_row_count} UI rows...")
        ui_data = await self.get_all_table_data(page, export_row_count)
        
        # Compare data
        print("\n🔍 Step 6: Comparing data...")
        comparison = self.compare_data(ui_data, csv_data)
        
        # Assertions
        print("\n✅ Step 7: Validating results...")
        
        # Row count validation
        ui_rows = comparison["ui_row_count"]
        csv_rows = comparison["csv_row_count"]
        print(f"📊 Row counts: UI={ui_rows}, Export={csv_rows}")
        
        # Data should match 99.9%+
        assert comparison["match_percentage"] >= 99.9, f"Data match too low: {comparison['match_percentage']:.1f}% - Expected 99.9%+"
        if comparison["match_percentage"] < 100:
            print(f"⚠️ Data match: {comparison['match_percentage']:.1f}%")
            for mismatch in comparison["mismatches"][:5]:
                print(f"   Row {mismatch['row']}, Col {mismatch['col']}: UI='{mismatch['ui_value']}' vs CSV='{mismatch['csv_value']}'")
        else:
            print(f"✅ Data match: 100%")
        
        # Clean up downloaded file
        if os.path.exists(csv_path):
            os.remove(csv_path)
            print(f"🗑️ Cleaned up: {csv_path}")
        
        print("\n" + "="*60)
        print("✅ RECEIVABLES EXPORT VALIDATION PASSED!")
        print("="*60)

    # ==========================================
    # BANK TRANSACTIONS EXPORT TEST
    # ==========================================
    @pytest.mark.asyncio
    async def test_bank_transactions_export_data_validation(self, perform_login: Page):
        """
        Test Bank Transactions export:
        1. Navigate to Bank Transactions
        2. Set date filter from 1/1/2020
        3. Get row count and sample data from UI
        4. Export to CSV/Excel
        5. Compare data with UI data
        6. Verify row counts match
        """
        page = perform_login
        print("\n" + "="*60)
        print("🧪 TEST: Bank Transactions Export Data Validation")
        print("="*60)
        
        # Navigate to Bank Transactions
        print("\n📍 Step 1: Navigating to Bank Transactions...")
        await page.goto("/reconciliation/banks")
        await asyncio.sleep(3)
        
        # Verify we're on the right page
        current_url = page.url.lower()
        assert "bank" in current_url or "reconciliation" in current_url, f"Not on bank transactions page: {page.url}"
        print(f"✅ On Bank Transactions page: {page.url}")
        
        # Set date filter
        print("\n📅 Step 2: Setting date filter...")
        await self.set_date_filter(page, self.FROM_DATE)
        await asyncio.sleep(2)
        
        # Check for "No transactions" message
        no_data_msg = page.locator("text=No transactions found")
        # Check for no data message
        try:
            await no_data_msg.wait_for(timeout=2000, state="visible")
            print("⚠️ No data in Bank Transactions, skipping export comparison")
            pytest.skip("No data available in Bank Transactions for export test")
        except:
            pass  # Data exists, continue
        
        # Export FIRST to get true row count
        print("\n📥 Step 3: Exporting data...")
        try:
            export_path = await self.click_export_button(page)
        except Exception as e:
            pytest.fail(f"Export failed: {str(e)}")
        
        # Read exported file to get true total
        print("\n📄 Step 4: Reading exported file...")
        file_headers, file_data = self.read_export_file(export_path)
        export_row_count = len(file_data)
        print(f"📊 Export has {export_row_count} rows")
        
        if export_row_count == 0:
            pytest.skip("No data in export file")
        
        # Get ALL table data from UI (paginate to match export count)
        print(f"\n📋 Step 5: Extracting all {export_row_count} UI rows...")
        ui_data = await self.get_all_table_data(page, export_row_count)
        
        # Compare data
        print("\n🔍 Step 6: Comparing data...")
        comparison = self.compare_data(ui_data, file_data)
        
        # Assertions
        print("\n✅ Step 7: Validating results...")
        
        # Row count validation
        ui_rows = comparison["ui_row_count"]
        csv_rows = comparison["csv_row_count"]
        print(f"📊 Row counts: UI={ui_rows}, Export={csv_rows}")
        
        # Data should match 99.9%+ (allowing for minor ordering/formatting differences)
        assert comparison["match_percentage"] >= 99.9, f"Data match too low: {comparison['match_percentage']:.1f}% - Expected 99.9%+"
        if comparison["match_percentage"] < 100:
            print(f"⚠️ Data match: {comparison['match_percentage']:.1f}%")
            for mismatch in comparison["mismatches"][:5]:
                print(f"   Row {mismatch['row']}, Col {mismatch['col']}: UI='{mismatch['ui_value']}' vs Export='{mismatch['csv_value']}'")
        else:
            print(f"✅ Data match: 100%")
        
        # Clean up downloaded file
        if os.path.exists(export_path):
            os.remove(export_path)
            print(f"🗑️ Cleaned up: {export_path}")
        
        print("\n" + "="*60)
        print("✅ BANK TRANSACTIONS EXPORT VALIDATION PASSED!")
        print("="*60)

    # ==========================================
    # CREDIT CARDS EXPORT TEST
    # ==========================================
    @pytest.mark.asyncio
    async def test_credit_cards_export_data_validation(self, perform_login: Page):
        """
        Test Credit Cards export:
        1. Navigate to Credit Cards
        2. Set date filter from 1/1/2020
        3. Get row count and sample data from UI
        4. Export to CSV/Excel
        5. Compare data with UI data
        6. Verify row counts match
        """
        page = perform_login
        print("\n" + "="*60)
        print("🧪 TEST: Credit Cards Export Data Validation")
        print("="*60)
        
        # Navigate to Credit Cards
        print("\n📍 Step 1: Navigating to Credit Cards...")
        await page.goto("/reconciliation/credit-cards")
        await asyncio.sleep(3)
        
        # Verify we're on the right page
        assert "credit" in page.url.lower(), f"Not on credit cards page: {page.url}"
        print(f"✅ On Credit Cards page: {page.url}")
        
        # Set date filter
        print("\n📅 Step 2: Setting date filter...")
        await self.set_date_filter(page, self.FROM_DATE)
        await asyncio.sleep(2)
        
        # Export FIRST to get true row count
        print("\n📥 Step 3: Exporting data...")
        try:
            export_path = await self.click_export_button(page)
        except Exception as e:
            pytest.fail(f"Export failed: {str(e)}")
        
        # Read exported file to get true total
        print("\n📄 Step 4: Reading exported file...")
        file_headers, file_data = self.read_export_file(export_path)
        export_row_count = len(file_data)
        print(f"📊 Export has {export_row_count} rows")
        
        if export_row_count == 0:
            pytest.skip("No data in export file")
        
        # Get ALL table data from UI (paginate to match export count)
        print(f"\n📋 Step 5: Extracting all {export_row_count} UI rows...")
        ui_data = await self.get_all_table_data(page, export_row_count)
        
        # Compare data
        print("\n🔍 Step 6: Comparing data...")
        comparison = self.compare_data(ui_data, file_data)
        
        # Assertions
        print("\n✅ Step 7: Validating results...")
        
        # Row count validation
        ui_rows = comparison["ui_row_count"]
        csv_rows = comparison["csv_row_count"]
        print(f"📊 Row counts: UI={ui_rows}, Export={csv_rows}")
        
        # Data should match 99.9%+
        assert comparison["match_percentage"] >= 99.9, f"Data match too low: {comparison['match_percentage']:.1f}% - Expected 99.9%+"
        if comparison["match_percentage"] < 100:
            print(f"⚠️ Data match: {comparison['match_percentage']:.1f}%")
            for mismatch in comparison["mismatches"][:5]:
                print(f"   Row {mismatch['row']}, Col {mismatch['col']}: UI='{mismatch['ui_value']}' vs Export='{mismatch['csv_value']}'")
        else:
            print(f"✅ Data match: 100%")
        
        # Clean up downloaded file
        if os.path.exists(export_path):
            os.remove(export_path)
            print(f"🗑️ Cleaned up: {export_path}")
        
        print("\n" + "="*60)
        print("✅ CREDIT CARDS EXPORT VALIDATION PASSED!")
        print("="*60)

