from playwright.sync_api import sync_playwright
import json 

class SearchApi:
    def __init__(self):
        self.p = sync_playwright().start() 
        self.browser = self.p.chromium.launch(headless=True)
        self.content = self.browser.new_context(
            locale="en-US"
        )

        self.page = self.content.new_page()
        self.api_data = []

    def capture_response(self, response):
        if response.request.resource_type not in [
                    "xhr", "fetch"
                ]:
                    return

        try:
            data = response.json()
            text = json.dumps(data, ensure_ascii=False)

            keywords = [
                  'search',
                  'catalog',
                  'mtop'
            ]

            if any(x in text for x in keywords):
                    try:
                        self.api_data.append({
                            'success': True,
                            'url': response.url,
                            'data': data
                        })
                    except:
                          pass
        except Exception as e :
              pass 

    def run(self, query):
        if not query:
            return {
                    'success': False,
                    'data': {},
                    'error': "Query not found!"
                }

        try:
            url = f'https://www.daraz.com.bd/catalog/?q={query}'
            self.page.on(
                "response",
                self.capture_response
            )

            self.page.goto(url=url, wait_until='domcontentloaded')
            self.page.wait_for_timeout(5000)
        except:
             pass 

        finally:
             self.browser.close()
             self.p.stop()



if __name__ == "__main__":
    api = SearchApi()
    api.run(query="Phones")
    data = api.api_data
    try:
         with open("check.json", 'w') as f :
              json.dump(data, f, indent=4)
    except:
         pass


