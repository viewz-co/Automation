import os
import asyncio
from datetime import datetime
from typing import Optional, Tuple

class ScreenshotHelper:
    """Helper class for capturing screenshots on test failures"""
    
    def __init__(self, screenshot_dir: str = "screenshots"):
        self.screenshot_dir = screenshot_dir
        self._ensure_directory()
    
    def _ensure_directory(self):
        """Ensure screenshot directory exists"""
        os.makedirs(self.screenshot_dir, exist_ok=True)
    
    def _generate_filename(self, test_name: str, timestamp: str) -> str:
        """Generate safe filename for screenshot"""
        safe_test_name = (test_name
                         .replace('[', '_')
                         .replace(']', '_')
                         .replace('=', '_')
                         .replace('-', '_')
                         .replace(':', '_')
                         .replace(' ', '_'))
        
        safe_timestamp = timestamp.replace(':', '-').replace(' ', '_')
        return f"failure_{safe_test_name}_{safe_timestamp}.png"
    
    async def capture_async_screenshot(self, page, test_name: str) -> Tuple[Optional[str], str]:
        """Capture screenshot from async page"""
        try:
            if not page or not hasattr(page, 'screenshot'):
                return None, "No page object available"
            
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            filename = self._generate_filename(test_name, timestamp)
            filepath = os.path.join(self.screenshot_dir, filename)
            
            # Take full page screenshot
            await page.screenshot(path=filepath, full_page=True)
            return filename, filepath
            
        except Exception as e:
            return None, f"Screenshot error: {str(e)}"
    
    def capture_sync_screenshot(self, page, test_name: str) -> Tuple[Optional[str], str]:
        """Capture screenshot from sync or async page"""
        try:
            if not page or not hasattr(page, 'screenshot'):
                return None, "No page object available"
            
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            filename = self._generate_filename(test_name, timestamp)
            filepath = os.path.join(self.screenshot_dir, filename)
            
            # Check if this is an async page (Playwright async API)
            if hasattr(page, '_impl_obj') or asyncio.iscoroutinefunction(page.screenshot):
                # This is an async page, we need to handle it properly
                try:
                    # Try to get the current event loop
                    loop = asyncio.get_event_loop()
                    if loop.is_running():
                        # We're in an async context, create a new event loop in a thread
                        import threading
                        import concurrent.futures
                        
                        def run_screenshot():
                            new_loop = asyncio.new_event_loop()
                            asyncio.set_event_loop(new_loop)
                            try:
                                return new_loop.run_until_complete(page.screenshot(path=filepath, full_page=True))
                            finally:
                                new_loop.close()
                        
                        with concurrent.futures.ThreadPoolExecutor() as executor:
                            future = executor.submit(run_screenshot)
                            future.result(timeout=10)  # 10 second timeout
                        
                        return filename, filepath
                    else:
                        # No running loop, we can use run_until_complete
                        loop.run_until_complete(page.screenshot(path=filepath, full_page=True))
                        return filename, filepath
                        
                except Exception as async_error:
                    # Fallback: try to use sync API if available
                    try:
                        # Some page objects might have both sync and async methods
                        if hasattr(page, '_sync_screenshot'):
                            page._sync_screenshot(path=filepath, full_page=True)
                            return filename, filepath
                        else:
                            return None, f"Async screenshot failed: {str(async_error)}"
                    except Exception as sync_error:
                        return None, f"Both async and sync screenshot failed: async={str(async_error)}, sync={str(sync_error)}"
            else:
                # This is a sync page
                page.screenshot(path=filepath, full_page=True)
                return filename, filepath
                
        except Exception as e:
            return None, f"Screenshot error: {str(e)}"
    
    def get_page_context(self, page) -> dict:
        """Get additional page context information"""
        context = {}
        
        try:
            if hasattr(page, 'url'):
                context['url'] = page.url
        except:
            context['url'] = 'Unknown'
        
        try:
            if hasattr(page, 'title'):
                # Handle both sync and async title
                if asyncio.iscoroutinefunction(page.title):
                    # Can't await here, so skip async title
                    context['title'] = 'Async title (not captured)'
                else:
                    context['title'] = page.title()
            else:
                context['title'] = 'Unknown'
        except:
            context['title'] = 'Error getting title'
        
        return context

# Global instance
screenshot_helper = ScreenshotHelper() 