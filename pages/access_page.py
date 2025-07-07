class AccessPage:
    def __init__(self, page):
        self.page = page

    def visit(self, url):
        self.page.goto(url)

    def get_body_text(self):
        return self.page.content()