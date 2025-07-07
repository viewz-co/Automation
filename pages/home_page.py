class HomePage:
    def __init__(self, page):
        self.page = page
        # Use the working selector as primary, with fallbacks
        self.home_selectors = [
            'main',  # This works!
            'div[role="main"]',  # Main role fallback
            '#radix-\\:r4b\\:',  # Original selector as fallback
            'div.displayAreaViewport',  # Another fallback
        ]

    async def is_loaded(self):
        # Try multiple selectors to find one that works
        for selector in self.home_selectors:
            try:
                locator = self.page.locator(selector)
                await locator.wait_for(timeout=5000)
                if await locator.is_visible():
                    return True
            except Exception:
                continue  # Try next selector
        
        # If none of the selectors worked, return False
        return False
