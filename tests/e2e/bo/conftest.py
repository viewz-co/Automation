"""
BO Environment Conftest
Specific fixtures and configuration for BO environment testing
"""

import pytest
import pytest_asyncio
import json
import os
from playwright.async_api import Page, async_playwright

# Import BO-specific page objects
from pages.bo_login_page import BOLoginPage
from pages.bo_accounts_page import BOAccountsPage
from utils.screenshot_helper import screenshot_helper


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
    """Create BO-specific page with proper basic authentication"""
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
        
        # Set up context options for BO
        context_options = {
            "base_url": bo_config["base_url"], 
            "viewport": None
        }
        
        # Add BO-specific HTTP basic authentication
        if "basic_auth" in bo_config and bo_config["basic_auth"]:
            basic_auth = bo_config["basic_auth"]
            context_options["http_credentials"] = {
                "username": basic_auth["username"],
                "password": basic_auth["password"]
            }
            print(f"🔐 BO HTTP Basic Auth configured for: {basic_auth['username']}")
        
        context = await browser.new_context(**context_options)
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
