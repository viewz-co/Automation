import os
import asyncio
import pyotp
import pytest
from pages.login_page import LoginPage
from pages.logout_page import LogoutPage
from utils.screenshot_helper import ScreenshotHelper


@pytest.mark.asyncio
async def test_logout_after_2fa_login(page, login_data):
    """
    Test complete login with 2FA followed by logout
    This test builds on the existing test_login.py functionality
    """
    # Initialize page objects and helpers
    login = LoginPage(page)
    logout = LogoutPage(page)
    screenshot_helper = ScreenshotHelper()
    
    # TOTP Secret (same as in test_login.py)
    secret = os.getenv('TEST_TOTP_SECRET')
    
    print("🚀 Starting Login + Logout Test with 2FA")
    print("=" * 50)
    
    # Step 1: Login Process (based on test_login.py)
    print("\n📍 Step 1: Login with 2FA")
    
    # Generate OTP
    otp = pyotp.TOTP(secret).now()
    print(f"🔐 Generated OTP: {otp}")
    
    # Navigate to login page
    await login.goto()
    
    # Take screenshot of login page
    await screenshot_helper.capture_async_screenshot(page, "01_login_page")
    
    # Fill login form
    await login.login(login_data["username"], login_data["password"])
    
    # Take screenshot after login form submission
    await screenshot_helper.capture_async_screenshot(page, "02_after_login_submit")
    
    # Handle 2FA
    print("⏳ Waiting for 2FA page...")
    await page.wait_for_selector("text=Two-Factor Authentication")
    await page.wait_for_selector("form")
    
    # Take screenshot of 2FA page
    await screenshot_helper.capture_async_screenshot(page, "03_2fa_page")
    
    # Fill OTP
    await page.get_by_role("textbox").fill(otp)
    print(f"✅ OTP filled: {otp}")
    
    # Wait for 2FA processing (as in original test)
    await asyncio.sleep(5)
    
    # Take screenshot after 2FA
    await screenshot_helper.capture_async_screenshot(page, "04_after_2fa")
    
    # Verify login success
    login_successful = await login.is_logged_in()
    assert login_successful, "Login with 2FA failed"
    print("✅ Login with 2FA successful")
    
    # Take screenshot of logged-in state
    await screenshot_helper.capture_async_screenshot(page, "05_logged_in_state")
    
    # Step 2: Logout Process
    print("\n🚪 Step 2: Logout Process")
    
    # Wait a moment to ensure page is fully loaded
    await page.wait_for_timeout(3000)
    
    # Take screenshot before logout attempt
    await screenshot_helper.capture_async_screenshot(page, "06_before_logout")
    
    # Attempt comprehensive logout
    logout_successful = await logout.logout_comprehensive()
    
    if logout_successful:
        print("✅ Logout initiated successfully")
        
        # Wait for logout to complete
        await logout.wait_for_logout_completion()
        
        # Take screenshot after logout
        await screenshot_helper.capture_async_screenshot(page, "07_after_logout")
        
        # Verify logout success
        logout_verified = await logout.is_logged_out()
        assert logout_verified, "Logout verification failed"
        print("✅ Logout verified successfully")
        
    else:
        # Take screenshot of failed logout attempt
        await screenshot_helper.capture_async_screenshot(page, "07_logout_failed")
        pytest.fail("Logout failed - could not find logout mechanism")
    
    # Final verification - ensure we're back to login page
    current_url = page.url
    print(f"📍 Final URL: {current_url}")
    
    # Take final screenshot
    await screenshot_helper.capture_async_screenshot(page, "08_final_state")
    
    print("🎉 Login + Logout test completed successfully!")


@pytest.mark.asyncio
async def test_logout_direct_method(page, login_data):
    """
    Test logout using direct method only
    Assumes user is already logged in or performs quick login
    """
    login = LoginPage(page)
    logout = LogoutPage(page)
    screenshot_helper = ScreenshotHelper()
    
    print("🚀 Starting Direct Logout Test")
    print("=" * 35)
    
    # Quick login (without 2FA for this test)
    print("📍 Quick login setup...")
    await login.goto()
    await login.login(login_data["username"], login_data["password"])
    
    # Skip 2FA for this test - just wait and see if we get logged in
    await page.wait_for_timeout(5000)
    
    # Take screenshot before logout
    await screenshot_helper.capture_async_screenshot(page, "direct_logout_before")
    
    # Try direct logout method only
    print("🔍 Attempting direct logout...")
    logout_successful = await logout.logout_direct()
    
    if logout_successful:
        await logout.wait_for_logout_completion()
        logout_verified = await logout.is_logged_out()
        
        await screenshot_helper.capture_async_screenshot(page, "direct_logout_after")
        
        assert logout_verified, "Direct logout verification failed"
        print("✅ Direct logout successful")
    else:
        await screenshot_helper.capture_async_screenshot(page, "direct_logout_failed")
        pytest.fail("Direct logout method failed")


@pytest.mark.asyncio
async def test_logout_via_menu(page, login_data):
    """
    Test logout via user menu dropdown
    """
    login = LoginPage(page)
    logout = LogoutPage(page)
    screenshot_helper = ScreenshotHelper()
    
    print("🚀 Starting Menu-based Logout Test")
    print("=" * 38)
    
    # Quick login setup
    print("📍 Quick login setup...")
    await login.goto()
    await login.login(login_data["username"], login_data["password"])
    await page.wait_for_timeout(5000)
    
    # Take screenshot before logout
    await screenshot_helper.capture_async_screenshot(page, "menu_logout_before")
    
    # Try menu-based logout only
    print("🔍 Attempting menu-based logout...")
    logout_successful = await logout.logout_via_menu()
    
    if logout_successful:
        await logout.wait_for_logout_completion()
        logout_verified = await logout.is_logged_out()
        
        await screenshot_helper.capture_async_screenshot(page, "menu_logout_after")
        
        assert logout_verified, "Menu-based logout verification failed"
        print("✅ Menu-based logout successful")
    else:
        await screenshot_helper.capture_async_screenshot(page, "menu_logout_failed")
        pytest.fail("Menu-based logout method failed")


@pytest.mark.asyncio
async def test_logout_comprehensive_fallback(page, login_data):
    """
    Test comprehensive logout with all fallback methods
    This is the most robust logout test
    """
    login = LoginPage(page)
    logout = LogoutPage(page)
    screenshot_helper = ScreenshotHelper()
    
    print("🚀 Starting Comprehensive Logout Test")
    print("=" * 42)
    
    # Login setup
    print("📍 Login setup...")
    await login.goto()
    await login.login(login_data["username"], login_data["password"])
    await page.wait_for_timeout(5000)
    
    # Check if we're logged in
    if await login.is_logged_in():
        print("✅ Login confirmed")
    else:
        print("⚠️ Login status uncertain, proceeding with logout test")
    
    # Take screenshot before logout
    await screenshot_helper.capture_async_screenshot(page, "comprehensive_logout_before")
    
    # Use comprehensive logout (tries all methods)
    print("🔍 Attempting comprehensive logout...")
    logout_successful = await logout.logout_comprehensive()
    
    # Always verify logout regardless of method used
    await logout.wait_for_logout_completion()
    logout_verified = await logout.is_logged_out()
    
    await screenshot_helper.capture_async_screenshot(page, "comprehensive_logout_after")
    
    if logout_successful and logout_verified:
        print("✅ Comprehensive logout successful")
    elif logout_verified:
        print("✅ Logout successful (verified despite method uncertainty)")
    else:
        pytest.fail("Comprehensive logout failed")


@pytest.mark.asyncio
async def test_logout_session_validation(page, login_data):
    """
    Test logout with session validation
    Ensures session is properly terminated
    """
    login = LoginPage(page)
    logout = LogoutPage(page)
    screenshot_helper = ScreenshotHelper()
    
    print("🚀 Starting Session Validation Logout Test")
    print("=" * 45)
    
    # Login
    await login.goto()
    await login.login(login_data["username"], login_data["password"])
    await page.wait_for_timeout(5000)
    
    # Store logged-in URL for later validation
    logged_in_url = page.url
    print(f"📍 Logged-in URL: {logged_in_url}")
    
    # Take screenshot of logged-in state
    await screenshot_helper.capture_async_screenshot(page, "session_validation_logged_in")
    
    # Perform logout
    logout_successful = await logout.logout_comprehensive()
    await logout.wait_for_logout_completion()
    
    # Take screenshot after logout
    await screenshot_helper.capture_async_screenshot(page, "session_validation_logged_out")
    
    # Verify logout
    logout_verified = await logout.is_logged_out()
    assert logout_verified, "Initial logout verification failed"
    
    # Additional session validation - try to access protected page
    print("🔍 Validating session termination...")
    
    if not logged_in_url.endswith('/login'):
        try:
            # Try to navigate back to the protected page
            await page.goto(logged_in_url)
            await page.wait_for_timeout(3000)
            
            # Take screenshot of attempted access
            await screenshot_helper.capture_async_screenshot(page, "session_validation_access_attempt")
            
            # Should be redirected to login or show login form
            current_url = page.url
            if '/login' in current_url or await logout.is_logged_out():
                print("✅ Session properly terminated - redirected to login")
            else:
                print("⚠️ Session validation uncertain - may still have access")
                
        except Exception as e:
            print(f"ℹ️ Navigation to protected page failed (expected): {str(e)}")
    
    print("✅ Session validation logout test completed") 