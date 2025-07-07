from pages.access_page import AccessPage
from api.bot_detection_api import BotDetectionAPI

def test_browser_access_allowed(browser_context):
    page = browser_context.new_page()
    access_page = AccessPage(page)
    access_page.visit("http://localhost:8080")
    assert "Access granted" in access_page.get_body_text()


def test_curl_access_blocked():
    api = BotDetectionAPI()
    response = api.curl_request()
    assert response.status_code == 403
    assert "Automation Detected" in response.text


def test_browser_headers_allowed():
    api = BotDetectionAPI()
    response = api.chrome_like_request()
    assert response.status_code == 200
    assert "Access granted" in response.text
