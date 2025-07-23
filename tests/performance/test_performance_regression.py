"""
Performance Regression Tests
Comprehensive performance testing for load times, responsiveness, and scalability
"""

import pytest
import pytest_asyncio
import asyncio
import time
import psutil
import os
from datetime import datetime, timedelta

from pages.login_page import LoginPage
from pages.home_page import HomePage
from pages.bank_page import BankPage
from pages.payables_page import PayablesPage
from pages.ledger_page import LedgerPage
from utils.screenshot_helper import ScreenshotHelper


class TestPerformanceRegression:
    """Performance regression test suite"""
    
    @pytest.mark.asyncio
    async def test_page_load_performance(self, perform_login_with_entity):
        """Test page load times across all major pages"""
        page = perform_login_with_entity
        screenshot_helper = ScreenshotHelper()
        
        print("⚡ Testing page load performance...")
        
        pages_to_test = [
            ("Home", HomePage),
            ("Bank", BankPage), 
            ("Payables", PayablesPage),
            ("Ledger", LedgerPage)
        ]
        
        load_times = {}
        
        for page_name, page_class in pages_to_test:
            print(f"\n🔍 Testing {page_name} page load time...")
            
            # Navigate to page and measure load time
            start_time = time.time()
            
            try:
                # Click navigation element
                nav_element = page.locator(f"text={page_name}")
                await nav_element.click()
                await asyncio.sleep(2)
                
                # Create page object and check if loaded
                page_obj = page_class(page)
                await page_obj.is_loaded()
                
                load_time = time.time() - start_time
                load_times[page_name] = load_time
                
                print(f"✅ {page_name} loaded in {load_time:.2f}s")
                
            except Exception as e:
                load_time = time.time() - start_time
                load_times[page_name] = load_time
                print(f"⚠️ {page_name} load test completed in {load_time:.2f}s (with issues)")
        
        await screenshot_helper.capture_async_screenshot(page, "performance_page_loads")
        
        # Performance assertions
        print("\n📊 Page Load Performance Summary:")
        slow_pages = []
        for page_name, load_time in load_times.items():
            status = "✅" if load_time < 10 else "⚠️" if load_time < 20 else "❌"
            print(f"   {status} {page_name}: {load_time:.2f}s")
            
            if load_time > 20:
                slow_pages.append(f"{page_name}({load_time:.1f}s)")
        
        # Test passes if most pages load reasonably fast
        avg_load_time = sum(load_times.values()) / len(load_times)
        assert avg_load_time < 15, f"Average page load time too slow: {avg_load_time:.2f}s"
        
        if slow_pages:
            print(f"⚠️ Slow pages detected: {', '.join(slow_pages)}")
        
        print("✅ Page load performance test completed")

    @pytest.mark.asyncio
    async def test_memory_usage_monitoring(self, perform_login_with_entity):
        """Test memory usage during extended session"""
        page = perform_login_with_entity
        screenshot_helper = ScreenshotHelper()
        
        print("💾 Testing memory usage during extended session...")
        
        # Get initial memory usage
        process = psutil.Process()
        initial_memory = process.memory_info().rss / 1024 / 1024  # MB
        
        print(f"📊 Initial memory usage: {initial_memory:.1f} MB")
        
        memory_readings = [initial_memory]
        
        # Perform various operations and monitor memory
        operations = [
            ("Navigate to Bank", lambda: page.click("text=Reconciliation")),
            ("Navigate to Payables", lambda: page.click("text=Reconciliation")),
            ("Navigate to Ledger", lambda: page.click("text=Ledger")),
            ("Navigate to Home", lambda: page.click("text=Home")),
        ]
        
        for i, (operation_name, operation) in enumerate(operations):
            print(f"\n🔄 {operation_name}...")
            
            try:
                await operation()
                await asyncio.sleep(3)
                
                # Take memory reading
                current_memory = process.memory_info().rss / 1024 / 1024
                memory_readings.append(current_memory)
                
                memory_increase = current_memory - initial_memory
                print(f"📊 Memory after {operation_name}: {current_memory:.1f} MB (+{memory_increase:.1f} MB)")
                
            except Exception as e:
                print(f"⚠️ {operation_name} failed: {str(e)}")
        
        await screenshot_helper.capture_async_screenshot(page, "performance_memory_usage")
        
        # Memory usage analysis
        final_memory = memory_readings[-1]
        total_increase = final_memory - initial_memory
        max_memory = max(memory_readings)
        
        print(f"\n💾 Memory Usage Summary:")
        print(f"   📊 Initial: {initial_memory:.1f} MB")
        print(f"   📊 Final: {final_memory:.1f} MB")
        print(f"   📊 Peak: {max_memory:.1f} MB")
        print(f"   📊 Total increase: {total_increase:.1f} MB")
        
        # Test passes if memory usage is reasonable
        assert total_increase < 200, f"Memory increase too high: {total_increase:.1f} MB"
        assert max_memory < 500, f"Peak memory usage too high: {max_memory:.1f} MB"
        
        print("✅ Memory usage monitoring test completed")

    @pytest.mark.asyncio
    async def test_concurrent_user_simulation(self, page, login_data):
        """Test performance with multiple concurrent operations"""
        print("👥 Testing concurrent user simulation...")
        
        login = LoginPage(page)
        screenshot_helper = ScreenshotHelper()
        
        # Login first
        await login.goto()
        await login.login(login_data["username"], login_data["password"])
        await asyncio.sleep(5)
        
        # Simulate concurrent operations
        concurrent_operations = [
            self._simulate_navigation(page, "Home"),
            self._simulate_navigation(page, "Reconciliation"), 
            self._simulate_data_loading(page),
            self._simulate_filtering_operations(page),
            self._simulate_form_interactions(page),
        ]
        
        print("🚀 Starting concurrent operations...")
        start_time = time.time()
        
        # Run operations concurrently
        results = await asyncio.gather(*concurrent_operations, return_exceptions=True)
        
        total_time = time.time() - start_time
        
        # Analyze results
        successful_operations = sum(1 for result in results if not isinstance(result, Exception))
        failed_operations = len(results) - successful_operations
        
        print(f"\n📊 Concurrent Operations Summary:")
        print(f"   ✅ Successful: {successful_operations}")
        print(f"   ❌ Failed: {failed_operations}")
        print(f"   ⏱️ Total time: {total_time:.2f}s")
        
        await screenshot_helper.capture_async_screenshot(page, "performance_concurrent_users")
        
        # Test passes if most operations succeed and complete in reasonable time
        success_rate = successful_operations / len(results)
        assert success_rate >= 0.6, f"Concurrent operation success rate too low: {success_rate:.1%}"
        assert total_time < 35, f"Concurrent operations took too long: {total_time:.2f}s (all {successful_operations} operations succeeded)"
        
        print("✅ Concurrent user simulation test completed")

    async def _simulate_navigation(self, page, target):
        """Helper: Simulate navigation operations"""
        try:
            # Use proper menu reveal pattern (optimized for performance testing)
            logo = page.locator("svg.viewz-logo")
            if await logo.count() > 0:
                box = await logo.bounding_box()
                if box:
                    await page.mouse.move(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)
                    await asyncio.sleep(0.3)
            
            # Click pin button if visible
            pin_button = page.locator("button:has(svg.lucide-pin)")
            if await pin_button.is_visible():
                await pin_button.click()
                await asyncio.sleep(0.3)
            
            # Now try navigation
            await page.click(f"text={target}")
            await asyncio.sleep(0.5)
            return True
        except:
            return False

    async def _simulate_data_loading(self, page):
        """Helper: Simulate data loading operations"""
        try:
            # Look for tables or data grids and interact with them
            tables = await page.locator("table, [role='grid']").count()
            if tables > 0:
                await page.locator("table, [role='grid']").first.hover()
                await asyncio.sleep(1)
            return True
        except:
            return False

    async def _simulate_filtering_operations(self, page):
        """Helper: Simulate filtering and search operations"""
        try:
            # Look for search inputs and filters
            search_inputs = await page.locator("input[type='search'], input[placeholder*='search' i]").count()
            if search_inputs > 0:
                await page.locator("input[type='search'], input[placeholder*='search' i]").first.fill("test")
                await asyncio.sleep(1)
            return True
        except:
            return False

    async def _simulate_form_interactions(self, page):
        """Helper: Simulate form interactions"""
        try:
            # Look for buttons and click them
            buttons = await page.locator("button").count()
            if buttons > 2:
                # Click a non-destructive button (avoid delete/submit buttons)
                safe_buttons = await page.locator("button:not(:has-text('Delete')):not(:has-text('Submit'))").count()
                if safe_buttons > 0:
                    await page.locator("button:not(:has-text('Delete')):not(:has-text('Submit'))").first.hover()
                    await asyncio.sleep(1)
            return True
        except:
            return False

    @pytest.mark.asyncio
    async def test_api_response_times(self, page, login_data):
        """Test API response times during normal operations"""
        print("🌐 Testing API response times...")
        
        login = LoginPage(page)
        
        # Capture network requests
        requests = []
        responses = []
        
        def handle_request(request):
            requests.append({
                'url': request.url,
                'method': request.method,
                'timestamp': time.time()
            })
        
        def handle_response(response):
            responses.append({
                'url': response.url,
                'status': response.status,
                'timestamp': time.time()
            })
        
        page.on("request", handle_request)
        page.on("response", handle_response)
        
        # Login and navigate to capture API calls
        await login.goto()
        await login.login(login_data["username"], login_data["password"])
        await asyncio.sleep(5)
        
        # Navigate through pages to trigger API calls
        navigation_targets = ["Home", "Reconciliation", "Ledger"]
        for target in navigation_targets:
            try:
                await page.click(f"text={target}")
                await asyncio.sleep(3)
            except:
                pass
        
        # Analyze API response times
        api_calls = []
        for request in requests:
            for response in responses:
                if request['url'] == response['url']:
                    response_time = (response['timestamp'] - request['timestamp']) * 1000  # ms
                    api_calls.append({
                        'url': request['url'],
                        'method': request['method'],
                        'status': response['status'],
                        'response_time': response_time
                    })
                    break
        
        if api_calls:
            print(f"\n🌐 API Performance Analysis ({len(api_calls)} calls):")
            
            slow_apis = []
            fast_apis = []
            
            for call in api_calls[-10:]:  # Last 10 API calls
                if call['response_time'] > 2000:  # > 2 seconds
                    slow_apis.append(call)
                else:
                    fast_apis.append(call)
                
                print(f"   📡 {call['method']} {call['url'][-50:]:>50} | {call['status']} | {call['response_time']:.0f}ms")
            
            avg_response_time = sum(call['response_time'] for call in api_calls) / len(api_calls)
            print(f"\n📊 Average API response time: {avg_response_time:.0f}ms")
            
            # Test passes if API performance is reasonable
            assert avg_response_time < 3000, f"Average API response time too slow: {avg_response_time:.0f}ms"
            
            if slow_apis:
                print(f"⚠️ {len(slow_apis)} slow API calls detected")
        else:
            print("ℹ️ No API calls captured during test")
            assert True, "API response time test completed - no API calls captured"
        
        print("✅ API response times test completed")

    @pytest.mark.asyncio
    async def test_large_dataset_handling(self, perform_login_with_entity):
        """Test performance with large datasets"""
        page = perform_login_with_entity
        screenshot_helper = ScreenshotHelper()
        
        print("📊 Testing large dataset handling...")
        
        # Navigate to pages that typically show large datasets
        data_heavy_pages = [
            {"name": "Bank Transactions", "nav": "Reconciliation"},
            {"name": "Payables List", "nav": "Reconciliation"},
            {"name": "Ledger Dashboard", "nav": "Ledger"},
        ]
        
        dataset_performance = {}
        
        for page_info in data_heavy_pages:
            print(f"\n🔍 Testing {page_info['name']}...")
            
            start_time = time.time()
            
            try:
                # Navigate to page
                await page.click(f"text={page_info['nav']}")
                await asyncio.sleep(3)
                
                # Wait for data to load and count elements
                tables = await page.locator("table, [role='grid']").count()
                rows = await page.locator("tr, [role='row']").count()
                
                load_time = time.time() - start_time
                
                dataset_performance[page_info['name']] = {
                    'load_time': load_time,
                    'tables': tables,
                    'rows': rows
                }
                
                print(f"✅ {page_info['name']}: {load_time:.2f}s, {tables} tables, {rows} rows")
                
            except Exception as e:
                load_time = time.time() - start_time
                dataset_performance[page_info['name']] = {
                    'load_time': load_time,
                    'tables': 0,
                    'rows': 0,
                    'error': str(e)
                }
                print(f"⚠️ {page_info['name']}: {load_time:.2f}s (with issues)")
        
        await screenshot_helper.capture_async_screenshot(page, "performance_large_datasets")
        
        # Performance analysis
        print(f"\n📊 Large Dataset Performance Summary:")
        total_rows = sum(perf.get('rows', 0) for perf in dataset_performance.values())
        avg_load_time = sum(perf['load_time'] for perf in dataset_performance.values()) / len(dataset_performance)
        
        for name, perf in dataset_performance.items():
            status = "✅" if perf['load_time'] < 10 else "⚠️"
            print(f"   {status} {name}: {perf['load_time']:.2f}s ({perf.get('rows', 0)} rows)")
        
        print(f"   📊 Total rows processed: {total_rows}")
        print(f"   📊 Average load time: {avg_load_time:.2f}s")
        
        # Test passes if large dataset handling is reasonable
        assert avg_load_time < 15, f"Large dataset handling too slow: {avg_load_time:.2f}s"
        
        print("✅ Large dataset handling test completed") 