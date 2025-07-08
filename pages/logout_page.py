class LogoutPage:
    def __init__(self, page):
        self.page = page
        
        # Multiple logout selectors to try
        self.logout_selectors = [
            'button:has-text("Logout")',
            'button:has-text("Log Out")',
            'button:has-text("Sign Out")',
            'a:has-text("Logout")',
            'a:has-text("Log Out")',
            'a:has-text("Sign Out")',
            '[data-testid="logout"]',
            '[data-testid="sign-out"]',
            '[data-testid="logout-button"]',
            '.logout-btn',
            '.logout-button',
            'button[type="button"]:has-text("Logout")',
            'text=Logout',
            'text=Log Out',
            'text=Sign Out'
        ]
        
        # User menu selectors (for dropdown menus)
        self.user_menu_selectors = [
            '[data-testid="user-menu"]',
            '[data-testid="user-dropdown"]',
            '[data-testid="profile-menu"]',
            '.user-menu',
            '.user-dropdown',
            '.profile-menu',
            '.user-profile',
            'button:has-text("Profile")',
            'button:has-text("Account")',
            'button:has-text("Settings")',
            '[aria-label="User menu"]',
            '[aria-label="Profile menu"]',
            'div[role="button"]:has-text("Profile")',
            'svg + span:has-text("Profile")',  # Icon + text pattern
            'button[aria-expanded]',  # Dropdown button
        ]
        
        # Selectors that indicate successful logout
        self.logout_success_selectors = [
            'input[name="username"]',  # Login form
            'input[name="password"]',  # Login form
            'button[type="submit"]:has-text("Login")',
            'button[type="submit"]:has-text("Sign In")',
            'text=Login',
            'text=Sign In',
            'text=Welcome',
            'form[action*="login"]',
            '.login-form',
            '.signin-form'
        ]

    async def logout_direct(self):
        """Try direct logout without opening menus"""
        print("🔍 Attempting direct logout...")
        
        for selector in self.logout_selectors:
            try:
                element = self.page.locator(selector).first
                if await element.is_visible():
                    print(f"✅ Found logout element: {selector}")
                    await element.click()
                    await self.page.wait_for_timeout(2000)  # Wait for logout to process
                    return True
            except Exception as e:
                print(f"❌ Failed with selector {selector}: {str(e)}")
                continue
        
        return False

    async def logout_via_menu(self):
        """Try logout via user menu dropdown"""
        print("🔍 Attempting logout via user menu...")
        
        for menu_selector in self.user_menu_selectors:
            try:
                menu_element = self.page.locator(menu_selector).first
                if await menu_element.is_visible():
                    print(f"✅ Found user menu: {menu_selector}")
                    
                    # Click to open menu
                    await menu_element.click()
                    await self.page.wait_for_timeout(1000)  # Wait for menu to open
                    
                    # Try to find logout in the opened menu
                    for logout_selector in self.logout_selectors:
                        try:
                            logout_element = self.page.locator(logout_selector).first
                            if await logout_element.is_visible():
                                print(f"✅ Found logout in menu: {logout_selector}")
                                await logout_element.click()
                                await self.page.wait_for_timeout(2000)
                                return True
                        except Exception:
                            continue
                    
                    print(f"❌ No logout found in menu: {menu_selector}")
                    
            except Exception as e:
                print(f"❌ Failed with menu selector {menu_selector}: {str(e)}")
                continue
        
        return False

    async def logout_via_keyboard(self):
        """Try logout via keyboard shortcuts"""
        print("🔍 Attempting logout via keyboard shortcuts...")
        
        try:
            # Try common logout keyboard shortcuts
            shortcuts = [
                "Control+Shift+L",  # Common logout shortcut
                "Alt+L",           # Alternative logout shortcut
                "Escape"           # Sometimes closes session
            ]
            
            for shortcut in shortcuts:
                await self.page.keyboard.press(shortcut)
                await self.page.wait_for_timeout(1000)
                
                if await self.is_logged_out():
                    print(f"✅ Logout successful with shortcut: {shortcut}")
                    return True
            
        except Exception as e:
            print(f"❌ Keyboard logout failed: {str(e)}")
        
        return False

    async def logout_comprehensive(self):
        """Comprehensive logout attempt using all methods"""
        print("🚪 Starting comprehensive logout process...")
        
        # Method 1: Direct logout
        if await self.logout_direct():
            print("✅ Direct logout successful")
            return True
        
        # Method 2: Menu-based logout
        if await self.logout_via_menu():
            print("✅ Menu-based logout successful")
            return True
        
        # Method 3: Keyboard shortcuts
        if await self.logout_via_keyboard():
            print("✅ Keyboard logout successful")
            return True
        
        # Method 4: URL-based logout (navigate to logout endpoint)
        try:
            print("🔍 Attempting URL-based logout...")
            current_url = self.page.url
            base_url = current_url.split('/')[0] + '//' + current_url.split('/')[2]
            
            logout_urls = [
                f"{base_url}/logout",
                f"{base_url}/signout",
                f"{base_url}/auth/logout",
                f"{base_url}/api/logout"
            ]
            
            for logout_url in logout_urls:
                try:
                    await self.page.goto(logout_url)
                    await self.page.wait_for_timeout(2000)
                    
                    if await self.is_logged_out():
                        print(f"✅ URL logout successful: {logout_url}")
                        return True
                except Exception:
                    continue
                    
        except Exception as e:
            print(f"❌ URL logout failed: {str(e)}")
        
        print("❌ All logout methods failed")
        return False

    async def is_logged_out(self):
        """Check if logout was successful"""
        print("🔍 Verifying logout status...")
        
        # Wait a moment for page to update
        await self.page.wait_for_timeout(2000)
        
        # Check current URL
        current_url = self.page.url
        if any(path in current_url.lower() for path in ['/login', '/signin', '/auth']):
            print(f"✅ Logout verified - URL changed to: {current_url}")
            return True
        
        # Check for login form elements
        for selector in self.logout_success_selectors:
            try:
                element = self.page.locator(selector).first
                if await element.is_visible():
                    print(f"✅ Logout verified - login form visible: {selector}")
                    return True
            except Exception:
                continue
        
        # Check if we can no longer find logged-in indicators
        logged_in_indicators = [
            'text=Dashboard',
            'text=Profile',
            'text=Settings',
            '[data-testid="user-menu"]',
            '.user-profile',
            'main[role="main"]'
        ]
        
        logged_in_found = False
        for indicator in logged_in_indicators:
            try:
                element = self.page.locator(indicator).first
                if await element.is_visible():
                    logged_in_found = True
                    break
            except Exception:
                continue
        
        if not logged_in_found:
            print("✅ Logout verified - no logged-in indicators found")
            return True
        
        print("❌ Still appears to be logged in")
        return False

    async def wait_for_logout_completion(self, timeout=10000):
        """Wait for logout to complete"""
        print(f"⏳ Waiting for logout completion (timeout: {timeout}ms)...")
        
        try:
            # Wait for either login form to appear or URL to change
            await self.page.wait_for_function(
                """() => {
                    return window.location.href.includes('/login') || 
                           window.location.href.includes('/signin') ||
                           document.querySelector('input[name="username"]') !== null ||
                           document.querySelector('input[name="password"]') !== null;
                }""",
                timeout=timeout
            )
            print("✅ Logout completion detected")
            return True
        except Exception as e:
            print(f"❌ Logout completion timeout: {str(e)}")
            return False 