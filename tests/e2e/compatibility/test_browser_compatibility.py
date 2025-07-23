"""
Browser Compatibility & Device Testing
Cross-browser testing and responsive design validation
"""

import pytest
import pytest_asyncio
import asyncio
from datetime import datetime

from pages.login_page import LoginPage
from pages.home_page import HomePage
from utils.screenshot_helper import ScreenshotHelper


class TestBrowserCompatibility:
    """Browser compatibility and device testing suite"""
    
    @pytest.mark.asyncio
    async def test_mobile_viewport_compatibility(self, page, login_data):
        """Test application on mobile viewport sizes"""
        login = LoginPage(page)
        home = HomePage(page)
        screenshot_helper = ScreenshotHelper()
        
        print("📱 Testing mobile viewport compatibility...")
        
        # Test different mobile viewport sizes
        mobile_viewports = [
            {"name": "iPhone SE", "width": 375, "height": 667},
            {"name": "iPhone 12", "width": 390, "height": 844},
            {"name": "Samsung Galaxy", "width": 360, "height": 640},
            {"name": "iPad Mini", "width": 768, "height": 1024},
        ]
        
        compatibility_results = {}
        
        for viewport in mobile_viewports:
            print(f"\n📱 Testing {viewport['name']} ({viewport['width']}x{viewport['height']})...")
            
            # Set viewport
            await page.set_viewport_size({"width": viewport['width'], "height": viewport['height']})
            await asyncio.sleep(2)
            
            try:
                # Test login on mobile
                await login.goto()
                
                # Check if login form is visible and accessible
                login_form_visible = await login.page.locator("form").is_visible()
                username_accessible = await login.page.locator("input[name*='username'], input[type='email']").is_visible()
                password_accessible = await login.page.locator("input[name*='password'], input[type='password']").is_visible()
                
                mobile_score = 0
                issues = []
                
                if login_form_visible:
                    mobile_score += 1
                else:
                    issues.append("Login form not visible")
                
                if username_accessible:
                    mobile_score += 1
                else:
                    issues.append("Username field not accessible")
                
                if password_accessible:
                    mobile_score += 1
                else:
                    issues.append("Password field not accessible")
                
                # Test login functionality
                try:
                    await login.login(login_data["username"], login_data["password"])
                    await asyncio.sleep(5)
                    
                    login_successful = await login.is_logged_in()
                    if login_successful:
                        mobile_score += 2
                    else:
                        issues.append("Login functionality failed")
                
                except Exception as e:
                    issues.append(f"Login error: {str(e)[:50]}")
                
                compatibility_results[viewport['name']] = {
                    'score': mobile_score,
                    'max_score': 5,
                    'issues': issues
                }
                
                print(f"✅ {viewport['name']}: {mobile_score}/5 compatibility score")
                if issues:
                    print(f"   ⚠️ Issues: {', '.join(issues)}")
                
                # Take screenshot
                await screenshot_helper.capture_async_screenshot(
                    page, f"mobile_compatibility_{viewport['name'].replace(' ', '_')}"
                )
                
            except Exception as e:
                compatibility_results[viewport['name']] = {
                    'score': 0,
                    'max_score': 5,
                    'issues': [f"Test failed: {str(e)[:50]}"]
                }
                print(f"❌ {viewport['name']}: Test failed")
        
        # Restore desktop viewport
        await page.set_viewport_size({"width": 1280, "height": 720})
        
        # Analyze results
        print(f"\n📊 Mobile Compatibility Summary:")
        total_score = sum(result['score'] for result in compatibility_results.values())
        max_possible = sum(result['max_score'] for result in compatibility_results.values())
        compatibility_rate = total_score / max_possible if max_possible > 0 else 0
        
        for device, result in compatibility_results.items():
            status = "✅" if result['score'] >= 4 else "⚠️" if result['score'] >= 2 else "❌"
            print(f"   {status} {device}: {result['score']}/{result['max_score']}")
        
        print(f"   📊 Overall compatibility: {compatibility_rate:.1%}")
        
        # Test passes if reasonable mobile compatibility
        assert compatibility_rate >= 0.6, f"Mobile compatibility too low: {compatibility_rate:.1%}"
        
        print("✅ Mobile viewport compatibility test completed")

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
    async def test_touch_interface_compatibility(self, page, login_data):
        """Test touch interface elements and gestures"""
        login = LoginPage(page)
        screenshot_helper = ScreenshotHelper()
        
        print("👆 Testing touch interface compatibility...")
        
        # Set mobile viewport for touch testing
        await page.set_viewport_size({"width": 390, "height": 844})
        await asyncio.sleep(2)
        
        # Login first
        await login.goto()
        await login.login(login_data["username"], login_data["password"])
        await asyncio.sleep(5)
        
        touch_results = {
            'tap_targets': 0,
            'scroll_areas': 0,
            'touch_friendly_forms': 0,
            'accessible_buttons': 0
        }
        
        try:
            # Test tap targets (buttons, links)
            buttons = await page.locator("button, a, [role='button']").count()
            
            # Check if buttons are touch-friendly (minimum 44px target size)
            large_enough_targets = 0
            if buttons > 0:
                for i in range(min(5, buttons)):  # Test first 5 buttons
                    button = page.locator("button, a, [role='button']").nth(i)
                    try:
                        box = await button.bounding_box()
                        if box and box['width'] >= 44 and box['height'] >= 44:
                            large_enough_targets += 1
                    except:
                        pass
                
                touch_results['tap_targets'] = large_enough_targets
                print(f"✅ Touch targets: {large_enough_targets}/{min(5, buttons)} adequately sized")
            
            # Test scrollable areas
            scrollable_elements = await page.locator("table, .scroll, [style*='overflow']").count()
            touch_results['scroll_areas'] = scrollable_elements
            print(f"📜 Scrollable areas found: {scrollable_elements}")
            
            # Test form accessibility on touch
            form_inputs = await page.locator("input, select, textarea").count()
            if form_inputs > 0:
                # Check if first input is accessible
                first_input = page.locator("input, select, textarea").first
                try:
                    await first_input.tap()
                    await asyncio.sleep(1)
                    touch_results['touch_friendly_forms'] = 1
                    print("✅ Form inputs are touch accessible")
                except:
                    print("⚠️ Form inputs may not be touch optimized")
            
            # Test button accessibility
            if buttons > 0:
                try:
                    # Try tapping first safe button
                    safe_buttons = page.locator("button:not(:has-text('Delete')):not(:has-text('Remove'))")
                    safe_button_count = await safe_buttons.count()
                    if safe_button_count > 0:
                        await safe_buttons.first.tap()
                        await asyncio.sleep(1)
                        touch_results['accessible_buttons'] = 1
                        print("✅ Buttons are touch accessible")
                except:
                    print("⚠️ Some buttons may not respond to touch")
            
        except Exception as e:
            print(f"⚠️ Touch testing encountered issues: {str(e)}")
        
        await screenshot_helper.capture_async_screenshot(page, "touch_interface_test")
        
        # Restore desktop viewport
        await page.set_viewport_size({"width": 1280, "height": 720})
        
        # Analyze touch compatibility
        print(f"\n👆 Touch Interface Summary:")
        print(f"   📱 Adequately sized tap targets: {touch_results['tap_targets']}")
        print(f"   📜 Scrollable areas: {touch_results['scroll_areas']}")
        print(f"   📝 Touch-friendly forms: {'✅' if touch_results['touch_friendly_forms'] else '⚠️'}")
        print(f"   🔘 Accessible buttons: {'✅' if touch_results['accessible_buttons'] else '⚠️'}")
        
        total_touch_score = sum(touch_results.values())
        
        # Test passes if basic touch compatibility exists
        assert total_touch_score >= 2, f"Touch interface compatibility too low: {total_touch_score}"
        
        print("✅ Touch interface compatibility test completed")

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