class HomePage:
    def __init__(self, page):
        self.page = page
        self.home_unique_selector = '#radix-\\:r4b\\:'

    async def is_loaded(self):
        locator = self.page.locator(self.home_unique_selector)
        await locator.wait_for(timeout=10000)
        return await locator.is_visible()
