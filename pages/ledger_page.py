class LedgerPage:
    def __init__(self, page):
        self.page = page
        self.heading_selectors = [
            'General Ledger',
            'Ledger',
            'GL',
            'General'
        ]

    async def is_loaded(self):
        # Try multiple heading variants
        for heading in self.heading_selectors:
            try:
                locator = self.page.get_by_role('heading', name=heading)
                await locator.wait_for(timeout=3000)  # Shorter timeout per attempt
                if await locator.is_visible():
                    return True
            except Exception:
                continue
        
        # Fallback: check for any ledger-related content
        try:
            # Look for common ledger page elements
            ledger_selectors = [
                'text=Ledger',
                'text=General Ledger', 
                '[data-testid*="ledger"]',
                '.ledger',
                'h1:has-text("Ledger")',
                'h2:has-text("Ledger")',
                'h3:has-text("Ledger")'
            ]
            
            for selector in ledger_selectors:
                element = self.page.locator(selector)
                if await element.is_visible():
                    return True
                    
        except Exception:
            pass
            
        return False
