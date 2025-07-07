class LoginPage:
    def __init__(self, page):
        self.page = page
        self.username_input = 'input[name="username"]'
        self.password_input = 'input[name="password"]'
        self.login_button = 'button[type="submit"]'
        self.dashboard_header = 'text=Dashboard'  # or any element that appears only after login

    async def goto(self):
        await self.page.goto("/login")

    async def login(self, username, password):
        await self.page.fill(self.username_input, username)
        await self.page.fill(self.password_input, password)
        await self.page.click(self.login_button)

    async def is_logged_in(self):
        return await self.page.locator(self.dashboard_header).is_visible()

