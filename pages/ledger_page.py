class LedgerPage:
    def __init__(self, page):
        self.page = page
        self.heading = 'General Ledger'

    async def is_loaded(self):
        locator = self.page.get_by_role('heading', name=self.heading)
        await locator.wait_for(timeout=10000)
        return await locator.is_visible()
