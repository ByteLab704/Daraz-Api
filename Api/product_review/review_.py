from playwright.sync_api import sync_playwright
import json 

from urllib.parse import urlparse, parse_qs

def is_review_api(url):
    parsed = urlparse(url)
    params = parse_qs(parsed.query)

    api_name = params.get("api", [""])[0].lower()

    return (
        "mtop.global.detail.web.getdetailinfo" in
        parsed.path.lower()
        or api_name == "mtop.global.detail.web.getdetailinfo"
    )

class product_review:
    def __init__(self):
        self.p = sync_playwright().start()
        self.browser = self.p.chromium.launch(headless=True)

        self.context = self.browser.new_context(
                    locale="en-US"
                )
        
        self.page = self.context.new_page()

        self.api_data = []
    
    def capture_response(self, response):

        if response.request.resource_type not in ['xhr', 'fetch']:
            return

        try:
            data = response.json()

            keywords = [
                "review",
                "rating",
                "feedback"
            ]

            text = json.dumps(
                data,
                ensure_ascii=False
            ).lower()

            if not any(keyword in text for keyword in keywords):
                return

            if is_review_api(response.url):
                self.api_data.append({
                                "success": True,
                                "status": response.status,
                                "data": data
                            })
        except Exception as e:
            pass

    
    def run(self, product_url):

        try:
            # Register API response listener
            self.page.on(
                "response",
                self.capture_response
            )

            # Open Daraz product page
            self.page.goto(
                product_url,
                wait_until="domcontentloaded",
                timeout=60000
            )

            self.page.wait_for_timeout(5000)

            # Scroll to reviews section
            try:
                review = self.page.locator(
                    "#module_product_review"
                )

                if review.count() > 0:
                    review.scroll_into_view_if_needed()
                    self.page.wait_for_timeout(3000)

            except Exception as e:
                print("Review section:", e)

            # Scroll page to trigger lazy loading
            for i in range(3):
                self.page.mouse.wheel(0, 700)
                self.page.wait_for_timeout(2000)

            print("\nTotal APIs Found:", len(self.api_data))

        except Exception as e:
            print("Run Error:", e)

        finally:
            self.browser.close()
            self.p.stop()

if __name__ == "__main__":
    api = product_review()
    api.run(product_url="https://www.daraz.com.bd/products/-i561264691-s2594850611.html?scm=1007.51610.379274.0&pvid=0a9d0b7a-943a-4af1-bf90-175586cf8126&search=flashsale&spm=a2a0e.tm80335411.FlashSale.d_561264691")

    data = api.api_data
    print(json.dumps(data, indent=4))
