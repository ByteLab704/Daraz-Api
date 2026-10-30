
from playwright.sync_api import sync_playwright
import json
import time


class DarazCategoryAPI:

    def __init__(self):

        self.p = sync_playwright().start()

        self.browser = self.p.chromium.launch(
            headless=True
        )

        self.context = self.browser.new_context(
            locale="en-US"
        )

        self.page = self.context.new_page()

        self.api_data = []
        self.categories = {}

    # Capture API Responses
    def capture_response(self, response):

        if response.request.resource_type not in [
            "xhr", "fetch"
        ]:
            return

        try:

            data = response.json()

            text = json.dumps(
                data,
                ensure_ascii=False
            ).lower()

            if any(x in text for x in [
                "category",
                "categories",
                "catid",
                "categoryid"
            ]):

                self.api_data.append({
                    "success": True, 
                    "data": data
                })

        except Exception:
            pass

    # Get Token
    def get_token(self):

        cookies = self.context.cookies(
            ["https://www.daraz.com.bd"]
        )

        tokens = {}

        for cookie in cookies:

            if cookie["name"] in [
                "_m_h5_tk",
                "_m_h5_tk_enc"
            ]:

                tokens[cookie["name"]] = cookie["value"]

        # print("Token status:", {
        #     key: bool(value)
        #     for key, value in tokens.items()
        # })

        return tokens

    # Get Homepage Categories
    def get_categories(self):

        items = self.page.locator(
            "#js_categories a.card-categories-li"
        )

        for i in range(items.count()):

            item = items.nth(i)

            category_id = item.get_attribute("id")

            if not category_id:
                continue

            name = item.get_attribute("name")

            url = item.get_attribute("href")

            image = item.locator(
                "img"
            ).get_attribute("src")

            self.categories[category_id] = {
                "id": category_id,
                "name": name,
                "url": url,
                "image": image
            }

            # print("CATEGORY:", name)

    # Automatic Menu Interaction
    def explore_menu(self):

        selectors = [
            "#Level_1_Category_No1",
            ".lzd-site-menu-nav",
            "[data-spm='cate']"
        ]

        for selector in selectors:

            try:

                element = self.page.locator(
                    selector
                ).first

                if element.count() > 0:

                    element.hover(timeout=3000)

                    self.page.wait_for_timeout(1500)

            except Exception:
                continue

        # Capture visible category links
        links = self.page.locator(
            "a[href*='daraz.com.bd/']"
        )

        for i in range(min(links.count(), 300)):

            item = links.nth(i)

            try:

                name = item.inner_text(timeout=1000).strip()
                url = item.get_attribute("href")

                if name and url and "daraz.com.bd" in url:

                    key = url.split("?")[0]

                    self.categories.setdefault(
                        key,
                        {
                            "name": name,
                            "url": url
                        }
                    )

            except Exception:
                continue

    # Save JSON
    def save(self):

        with open(
            "categories.json",
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                list(self.categories.values()),
                f,
                ensure_ascii=False,
                indent=4
            )

        with open(
            "category_apis.json",
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                self.api_data,
                f,
                ensure_ascii=False,
                indent=4
            )

        print("\nTotal Categories:", len(self.categories))
        print("Total APIs:", len(self.api_data))

    def run(self):

        try:

            self.page.on(
                "response",
                self.capture_response
            )

            self.page.goto(
                "https://www.daraz.com.bd/",
                wait_until="domcontentloaded",
                timeout=60000
            )

            self.page.wait_for_timeout(5000)

            self.get_token()

            self.get_categories()

            self.explore_menu()

            self.page.wait_for_timeout(5000)

            self.get_token()

        finally:

            self.browser.close()
            self.p.stop()


# if __name__ == "__main__":

#     api = DarazCategoryAPI()
#     data = api.api_data
#     api.run()
#     try:
#         with open("MIT.json", "w") as f :
#             json.dump(data, f ,  indent=4)
#     except:
#         pass
