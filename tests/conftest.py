import pytest
import pytest_asyncio
from playwright.async_api import async_playwright
from playwright.sync_api import sync_playwright
import pyotp
import json
import os
import asyncio
from pages.login_page import LoginPage

# ---------- ENV CONFIG ---------- #
def load_config():
    env = os.getenv("ENV", "dev")  # export ENV=stage
    with open("configs/env_config.json") as f:
        return json.load(f)[env]

@pytest.fixture(scope="session")
def env_config():
    return load_config()

# ---------- ASYNC PAGE FIXTURE ---------- #
@pytest_asyncio.fixture
async def page(env_config):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, slow_mo=200, args=["--start-maximized"])
        context = await browser.new_context(base_url=env_config["base_url"], viewport=None)
        page = await context.new_page()
        yield page
        await context.close()
        await browser.close()

# ---------- SYNC CONTEXT FIXTURE (optional) ---------- #
@pytest.fixture(scope="session")
def sync_browser_context():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        yield context
        browser.close()

# ---------- LOGIN DATA FIXTURE ---------- #
@pytest.fixture
def login_data():
    fixture_path = os.path.join(
        os.path.dirname(__file__), "../fixtures/test_data.json"
    )
    with open(fixture_path) as f:
        return json.load(f)["login"]

# ---------- PERFORM LOGIN WITH OTP FIXTURE ---------- #
@pytest_asyncio.fixture
async def perform_login(page, login_data):
    login = LoginPage(page)
    await login.goto()
    await login.login(login_data["username"], login_data["password"])

    # הזנת OTP
    secret = "HA2ECLBIKYUEEI2GPUUSMN3XIMXFETRQ"  # החלף אם צריך
    otp = pyotp.TOTP(secret).now()

    await page.wait_for_selector("text=Two-Factor Authentication", timeout=5000)
    await page.get_by_role("textbox").fill(otp)
    await asyncio.sleep(1)
    #await page.get_by_role("button", name="Verify").click()
    await page.wait_for_selector("text=SuccessOTP verified successfully", timeout=5000)

    return page
