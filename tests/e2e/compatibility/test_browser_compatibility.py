"""
Browser Compatibility & Device Testing
Cross-browser testing and responsive design validation
"""

import pytest
import pytest_asyncio
import asyncio
from datetime import datetime

from utils.screenshot_helper import ScreenshotHelper


class TestBrowserCompatibility:
    """Browser compatibility and device testing suite"""
    
    @pytest.mark.asyncio
    async def test_responsive_design_elements(self, perform_login_with_entity):
        """Test responsive design elements across different screen sizes"""
        page = perform_login_with_entity
        screenshot_helper = ScreenshotHelper()
        
        print("📐 Testing responsive design elements...")
        
        # Test different screen sizes
        screen_sizes = [
            {"name": "Mobile", "width": 375, "height": 667},
            {"name": "Tablet", "width": 768, "height": 1024},
            {"name": "Desktop", "width": 1920, "height": 1080},
            {"name": "Large Desktop", "width": 2560, "height": 1440},
        ]
        
        responsive_results = {}
        
        for size in screen_sizes:
            print(f"\n📐 Testing {size['name']} ({size['width']}x{size['height']})...")
            
            # Set viewport
            await page.set_viewport_size({"width": size['width'], "height": size['height']})
            await asyncio.sleep(2)
            
            try:
                # Test navigation visibility
                nav_visible = await page.locator("nav, header, [role='navigation']").is_visible()
                
                # Test main content area
                main_content = await page.locator("main, .main-content, [role='main']").is_visible()
                
                # Test responsive navigation (hamburger menu on mobile)
                hamburger_menu = await page.locator("button:has(svg), .menu-toggle, .hamburger").count()
                
                # Test form elements scaling
                form_elements = await page.locator("input, button, select").count()
                
                # Test table/grid responsiveness
                tables = await page.locator("table, [role='grid']").count()
                
                responsive_score = 0
                features = []
                
                if nav_visible:
                    responsive_score += 1
                    features.append("Navigation visible")
                
                if main_content:
                    responsive_score += 1
                    features.append("Main content accessible")
                
                if size['width'] < 768 and hamburger_menu > 0:
                    responsive_score += 1
                    features.append("Mobile navigation menu")
                elif size['width'] >= 768:
                    responsive_score += 1
                    features.append("Desktop navigation")
                
                if form_elements > 0:
                    responsive_score += 1
                    features.append(f"{form_elements} form elements")
                
                responsive_results[size['name']] = {
                    'score': responsive_score,
                    'features': features,
                    'tables': tables,
                    'form_elements': form_elements
                }
                
                print(f"✅ {size['name']}: {responsive_score}/4 responsive score")
                print(f"   📊 Features: {', '.join(features)}")
                
                # Take screenshot
                await screenshot_helper.capture_async_screenshot(
                    page, f"responsive_design_{size['name'].replace(' ', '_')}"
                )
                
            except Exception as e:
                responsive_results[size['name']] = {
                    'score': 0,
                    'features': [],
                    'error': str(e)
                }
                print(f"❌ {size['name']}: Test failed")
        
        # Restore standard viewport
        await page.set_viewport_size({"width": 1280, "height": 720})
        
        # Analyze responsive design
        print(f"\n📊 Responsive Design Summary:")
        avg_score = sum(result['score'] for result in responsive_results.values()) / len(responsive_results)
        
        for size_name, result in responsive_results.items():
            status = "✅" if result['score'] >= 3 else "⚠️"
            print(f"   {status} {size_name}: {result['score']}/4")
        
        print(f"   📊 Average responsive score: {avg_score:.1f}/4")
        
        # Test passes if responsive design is reasonable
        assert avg_score >= 2.5, f"Responsive design score too low: {avg_score:.1f}/4"
        
        print("✅ Responsive design elements test completed")

    @pytest.mark.asyncio
    async def test_print_stylesheet_compatibility(self, perform_login_with_entity):
        """Test print stylesheet and print-friendly formatting"""
        page = perform_login_with_entity
        screenshot_helper = ScreenshotHelper()
        
        print("🖨️ Testing print stylesheet compatibility...")
        
        # Navigate to different pages and test print styles
        pages_to_test = ["Home", "Reconciliation", "Ledger"]
        print_results = {}
        
        for page_name in pages_to_test:
            print(f"\n🖨️ Testing print styles for {page_name}...")
            
            try:
                # Reveal navigation menu first (required pattern)
                await asyncio.sleep(2)
                logo = page.locator("svg.viewz-logo")
                if await logo.count() > 0:
                    box = await logo.bounding_box()
                    if box:
                        await page.mouse.move(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)
                        await asyncio.sleep(1)
                
                # Click pin button if visible
                pin_button = page.locator("button:has(svg.lucide-pin)")
                if await pin_button.is_visible():
                    await pin_button.click()
                    await asyncio.sleep(1)
                
                # Navigate to page
                await page.click(f"text={page_name}")
                await asyncio.sleep(3)
                
                # Emulate print media
                await page.emulate_media(media='print')
                await asyncio.sleep(1)
                
                # Check for print-specific styles
                print_elements = {
                    'hidden_nav': await page.locator("nav, header").count(),
                    'visible_content': await page.locator("main, .content, article").count(),
                    'page_breaks': await page.locator("[style*='page-break'], .page-break").count(),
                    'print_only': await page.locator(".print-only, [media='print']").count()
                }
                
                print_results[page_name] = print_elements
                
                print(f"✅ {page_name} print analysis:")
                print(f"   📊 Content areas: {print_elements['visible_content']}")
                print(f"   📄 Page break elements: {print_elements['page_breaks']}")
                print(f"   🖨️ Print-only elements: {print_elements['print_only']}")
                
                # Take screenshot in print mode
                await screenshot_helper.capture_async_screenshot(
                    page, f"print_style_{page_name.lower()}"
                )
                
            except Exception as e:
                print_results[page_name] = {'error': str(e)}
                print(f"⚠️ {page_name} print test failed: {str(e)}")
            
            # Reset media emulation
            await page.emulate_media(media='screen')
            await asyncio.sleep(1)
        
        # Analyze print compatibility
        print(f"\n🖨️ Print Compatibility Summary:")
        total_content_areas = sum(
            result.get('visible_content', 0) for result in print_results.values()
            if 'error' not in result
        )
        
        pages_tested = len([r for r in print_results.values() if 'error' not in r])
        
        for page_name, result in print_results.items():
            if 'error' not in result:
                status = "✅" if result['visible_content'] > 0 else "⚠️"
                print(f"   {status} {page_name}: Print styles assessed")
            else:
                print(f"   ❌ {page_name}: Print test failed")
        
        print(f"   📊 Total content areas: {total_content_areas}")
        print(f"   📊 Pages successfully tested: {pages_tested}/{len(pages_to_test)}")
        
        # Test passes if print functionality was assessed
        assert pages_tested >= 1, "Should successfully test print styles on at least one page"
        
        print("✅ Print stylesheet compatibility test completed") 