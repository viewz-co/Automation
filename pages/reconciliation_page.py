class ReconciliationPage:
    def __init__(self, page):
        self.page = page
        self.heading = 'Reconciliation'

    async def is_loaded(self):
        locator = self.page.get_by_role('heading', name=self.heading)
        await locator.wait_for(timeout=10000)
        return await locator.is_visible()
