import requests

class BotDetectionAPI:
    BASE_URL = "http://localhost:8080"

    def send_request(self, user_agent, headers=None):
        headers = headers or {}
        headers["User-Agent"] = user_agent
        return requests.get(self.BASE_URL, headers=headers)

    def curl_request(self):
        return self.send_request("curl/7.81.0", {"Accept": "*/*"})

    def chrome_like_request(self):
        return self.send_request("Mozilla/5.0", {
            "Accept": "text/html",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate",
            "Connection": "keep-alive"
        })