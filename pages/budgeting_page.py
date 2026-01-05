class BudgetingPage:
    def __init__(self, page):
        self.page = page
        self.heading = 'Budgeting'

    async def is_loaded(self):
        """Check if the Budgeting page is loaded"""
        try:
            # Try heading first
            locator = self.page.get_by_role('heading', name=self.heading)
            await locator.wait_for(timeout=10000)
            return await locator.is_visible()
        except:
            # Fallback: check URL or page content
            return 'budget' in self.page.url.lower()

