class LoginPage:
    def __init__(self, page):
        self.page = page
        self.username_input = 'input[name="username"]'
        self.password_input = 'input[name="password"]'
        self.login_button = 'button[type="submit"]'
        # Use the same reliable selectors that work for home page
        self.logged_in_selectors = [
            'main',  # This works for home page
            'div[role="main"]',  # Main role fallback
            'svg.viewz-logo',  # Logo appears when logged in
        ]

    async def goto(self):
        await self.page.goto("/login")

    async def login(self, username, password):
        await self.page.fill(self.username_input, username)
        await self.page.fill(self.password_input, password)
        await self.page.click(self.login_button)

    async def is_logged_in(self):
        # Try multiple selectors to check if logged in
        for selector in self.logged_in_selectors:
            try:
                locator = self.page.locator(selector)
                await locator.wait_for(timeout=3000)
                if await locator.is_visible():
                    return True
            except Exception:
                continue
        return False

