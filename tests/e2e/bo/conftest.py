"""
BO Environment Conftest
Specific fixtures and configuration for BO environment testing
"""

import pytest
import pytest_asyncio
import json
import os
import asyncio
from playwright.async_api import Page, async_playwright

# Import BO-specific page objects
from pages.bo_login_page import BOLoginPage
from pages.bo_accounts_page import BOAccountsPage
from utils.screenshot_helper import screenshot_helper


async def fill_otp_boxes(page: Page, otp_code: str):
    """
    Fill OTP into multi-box input component (6 separate input boxes, 3-3 format).
    This is specifically for the relogin verification dialog.
    Works with the input-otp React component.
    """
    print(f"🔐 Filling OTP boxes with code: {otp_code}")
    
    # Wait for dialog to be visible
    await asyncio.sleep(1)
    
    # Get all input boxes in the dialog
    inputs = page.locator("input[maxlength='1'], input[type='text']")
    input_count = await inputs.count()
    print(f"   Found {input_count} input boxes")
    
    if input_count >= 6:
        # Fill each digit into its own input box
        for i, digit in enumerate(otp_code[:6]):
            try:
                input_box = inputs.nth(i)
                await input_box.click()
                await input_box.fill(digit)
                await asyncio.sleep(0.1)
            except Exception as e:
                print(f"   Warning: Could not fill box {i}: {e}")
        print(f"✅ Filled {len(otp_code)} digits into OTP boxes")
        return True
    
    # Fallback: Click first input and type each digit (auto-advance)
    print("   Trying keyboard typing approach...")
    first_input = page.locator("input").first
    await first_input.click()
    await asyncio.sleep(0.2)
    
    for digit in otp_code:
        await page.keyboard.press(digit)
        await asyncio.sleep(0.15)
    
    print(f"✅ Typed OTP via keyboard: {otp_code}")
    return True


@pytest.fixture(scope="session")
def headless_mode(request):
    """Get headless mode from command line option"""
    return request.config.getoption("--headless", default=False)


@pytest.fixture(scope="session")
def bo_config():
    """Load BO environment configuration"""
    # Check for environment selection
    test_env = os.getenv("TEST_ENV", "production").lower()
    
    if test_env == "stage":
        config_path = "/Users/sharonhoffman/Desktop/Automation/playwright_python_framework/configs/bo_stage_env_config.json"
        env_name = "BO Stage"
    else:
        config_path = "/Users/sharonhoffman/Desktop/Automation/playwright_python_framework/configs/bo_env_config.json"
        env_name = "BO Production"
    
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
        
        # Add environment info to config
        config["environment_name"] = env_name
        config["test_env"] = test_env
        
        # Handle environment variable expansion for production
        if test_env == "production" and "relogin_otp_secret" in config:
            if config["relogin_otp_secret"] == "${TEST_TOTP_SECRET}":
                config["relogin_otp_secret"] = os.getenv("TEST_TOTP_SECRET", "")
        
        print(f"🔧 BO Config loaded: {env_name} - {config['base_url']}")
        return config
        
    except FileNotFoundError:
        print(f"❌ BO config file not found: {config_path}")
        raise Exception(f"BO configuration file not found: {config_path}")


@pytest_asyncio.fixture
async def bo_page(bo_config, headless_mode):
    """Create BO-specific page with domain-specific basic authentication"""
    import base64
    
    async with async_playwright() as p:
        # Use headless_mode parameter
        launch_options = {
            "headless": headless_mode,
        }
        if not headless_mode:
            launch_options.update({
                "slow_mo": 200,
                "args": ["--start-maximized"]
            })
        
        browser = await p.chromium.launch(**launch_options)
        
        # Set up context options for BO (without http_credentials - use route interception)
        context_options = {
            "base_url": bo_config["base_url"], 
            "viewport": None
        }
        
        context = await browser.new_context(**context_options)
        
        # Set up domain-specific Basic Auth via route interception
        # BO and App have different passwords
        if "basic_auth" in bo_config and bo_config["basic_auth"]:
            basic_auth = bo_config["basic_auth"]
            bo_auth = base64.b64encode(f"{basic_auth['username']}:{basic_auth['password']}".encode()).decode()
            
            # App credentials (different from BO)
            app_auth = base64.b64encode("admin:38Uo0tuxA3pj*b0F".encode()).decode()
            
            async def handle_auth(route):
                url = route.request.url
                headers = dict(route.request.headers)
                if "bo.stage.viewz.co" in url or "bo.viewz.co" in url:
                    headers["Authorization"] = f"Basic {bo_auth}"
                elif "app.stage.viewz.co" in url or "app.viewz.co" in url:
                    headers["Authorization"] = f"Basic {app_auth}"
                await route.continue_(headers=headers)
            
            await context.route("**/*", handle_auth)
            print(f"🔐 Domain-specific Basic Auth configured (BO + App)")
        
        page = await context.new_page()
        yield page
        await context.close()
        await browser.close()

@pytest.fixture
def bo_login_page(bo_page: Page, bo_config):
    """Create BO login page object"""
    return BOLoginPage(bo_page, bo_config["base_url"])


@pytest.fixture
def bo_accounts_page(bo_page: Page):
    """Create BO accounts page object"""
    return BOAccountsPage(bo_page)


@pytest.fixture
def bo_screenshot_helper():
    """Create screenshot helper for BO tests"""
    return screenshot_helper


@pytest_asyncio.fixture
async def bo_authenticated_page(bo_page: Page, bo_config, bo_login_page):
    """
    Fixture that provides a page with completed BO authentication
    Use this fixture when you need a page that's already logged into BO
    """
    print("🔐 Performing BO authentication...")
    
    try:
        # Perform BO login
        login_success = await bo_login_page.full_bo_login(
            username=bo_config["username"],
            password=bo_config["password"],
            otp_secret=bo_config["otp_secret"]
        )
        
        if not login_success:
            raise Exception("BO authentication failed")
        
        print("✅ BO authentication successful")
        return bo_page
        
    except Exception as e:
        print(f"❌ BO authentication failed: {str(e)}")
        raise


@pytest_asyncio.fixture
async def bo_accounts_ready_page(bo_authenticated_page: Page, bo_accounts_page):
    """
    Fixture that provides a page that's logged into BO and navigated to accounts
    """
    print("🏠 Navigating to BO accounts page...")
    
    try:
        # Navigate to accounts
        navigation_success = await bo_accounts_page.navigate_to_accounts()
        
        if not navigation_success:
            print("⚠️ Accounts navigation might have failed, but continuing...")
        else:
            print("✅ BO accounts page ready")
        
        return bo_authenticated_page
        
    except Exception as e:
        print(f"❌ BO accounts navigation failed: {str(e)}")
        raise


# === Test Categories Markers ===
def pytest_configure(config):
    """Register custom markers for BO tests"""
    config.addinivalue_line(
        "markers", "bo_login: mark test as BO login test"
    )
    config.addinivalue_line(
        "markers", "bo_accounts: mark test as BO accounts test"
    )
    config.addinivalue_line(
        "markers", "bo_relogin: mark test as BO relogin test"
    )
    config.addinivalue_line(
        "markers", "bo_sanity: mark test as BO sanity test"
    )
    config.addinivalue_line(
        "markers", "bo_complete: mark test as BO complete flow test"
    )
