from playwright.sync_api import sync_playwright
import time 
import urllib.parse 
import json 


class GetInfo:
    def __init__(self):
        self.p = sync_playwright().start()
        self.browser = self.p.chromium.launch(headless=True)
        self.page = self.browser.new_page()
    def info_api(self, product_url):
        if not product_url:
            return {
                'success': False, 
                'error': 'Product Url not Found!',
                'data': {}
            }

        try:
            self.page.goto(product_url, wait_until="domcontentloaded")
            self.page.wait_for_selector("#module_item_gallery_1 > div > div.gallery-preview-panel > div > img")
            img_item = self.page.locator("#module_item_gallery_1 > div > div.gallery-preview-panel > div > img")
            image_url = None

            try:
                img_url = img_item.get_attribute('src')
                image_url = img_url
            except :
                pass

            title1 = None
            try:
                title = img_item.get_attribute('alt')
                if title:
                    title1 = title
            except Exception as e :
                print(f"error {e}")

            product_price = None
            try:
                price = self.page.locator("#module_product_price_1 > div > div > span").inner_text()
                if price:
                    product_price = price
            except Exception as e :
                print(f"error {e}")

            rating = None
            try:
                ratting = self.page.locator("#module_product_review_star_1 > div > a").inner_text()
                if ratting:
                    rating = ratting
            except Exception as e :
                print(f"error {e}") 

            location1 = None
            try:
                location = self.page.locator("#module_seller_delivery > div > div > div.delivery__header > div > div > div > div.location__address").inner_text()
                if location:
                    location1 = location
            except Exception as e :
                print(f"error {e}") 

            delivary = None 
            delivary_price = None 
        
            try:
                delevary = self.page.locator("#module_seller_delivery > div > div > div.delivery__content > div > div:nth-child(2) > div > div > div.delivery-option-item__info").inner_text()
                if delevary:
                    delevary_price = self.page.locator("#module_seller_delivery > div > div > div.delivery__content > div > div:nth-child(1) > div > div > div.delivery-option-item__shipping-fee.no-subtitle").inner_text()
                    delivary = delevary
                    delivary_price = delivary_price
            except Exception as e :
                print(f"error {e}") 

            returns = None 
            try:
                return_date = self.page.locator("#module_seller_warranty > div > div.warranty__options > div:nth-child(1) > div > div > div").inner_text()
                if "change of mind" in return_date.lower():
                    returns = "Change of Mind Applicable"
                elif "return" in return_date.lower():
                    returns = return_date
                else:
                    returns = "14 Days Easy Return"
            except Exception as e :
                print(f"error {e}") 
            brand_names = None 
            brand_links = None 
            more_brand_data = None 
            more_brand_urls = None 
            try:
                brand = self.page.locator("#module_product_brand_1 > div > a.pdp-link.pdp-link_size_s.pdp-link_theme_blue.pdp-product-brand__brand-link")
                if brand:
                    brand_url = brand.get_attribute("href")
                    brand_name = brand.inner_text()
                    brand_more = self.page.locator("#module_product_brand_1 > div > a.pdp-link.pdp-link_size_s.pdp-link_theme_blue.pdp-product-brand__suggestion-link")
                    more_data  = brand_more.inner_text()
                    more_url = brand_more.get_attribute('href')
                    brand_names = brand_name
                    brand_links = brand_url
                    more_brand_data = more_data
                    more_brand_urls = more_url
            except Exception as e :
                print(f"error {e}")


            value1 = None
            try:
                positive_data = self.page.locator("#module_seller_info > div > div.pdp-seller-info-pc > div:nth-child(1) > div.seller-info-title").inner_text()
                if positive_data:
                    value = self.page.locator("#module_seller_info > div > div.pdp-seller-info-pc > div:nth-child(1) > div.seller-info-value.rating-positive").inner_text()
                    if value:
                        value1 = value1

            except Exception as e :
                print(f"error {e}")

            ship_ons= None
            value2 = None 
            try:
                ship_on = self.page.locator("#module_seller_info > div > div.pdp-seller-info-pc > div:nth-child(2) > div.seller-info-title").inner_text()
                if ship_on:
                    values = self.page.locator("#module_seller_info > div > div.pdp-seller-info-pc > div:nth-child(2) > div.seller-info-value").inner_text()
                    ship_ons = ship_on
                    value2 = values
            except Exception as e :
                print(f"error {e}")

            warranty = "N/A"
            try:
                Warranty = self.page.locator("#module_seller_warranty > div > div.warranty__options > div:nth-child(2) > div > div > div > div").inner_text()
                if Warranty:
                    if "return" in Warranty.lower():
                            warranty = "Warranty not available"
                    else:
                        warranty = Warranty
            except Exception as e :
                    print(f"error {e}")

            seller_name = "N/A"
            seller_url = "N/A"

            try:
                # ১. সেলারের নাম বের করা
                seller_element = self.page.locator('div.seller-name__detail a.seller-name__detail-name').first
                seller_name = seller_element.inner_text().strip()

                # ২. সেলারের শপ ইউআরএল বের করা
                raw_url = seller_element.get_attribute("href")
                if raw_url:
                    if raw_url.startswith("//"):
                        seller_url = f"https:{raw_url}"
                    else:
                        seller_url = raw_url

            except Exception as e:
                print(f"Error extracting seller info: {e}")


            data = {
                'status': 'success', 
                'data': {
                    "product_title": title1, 
                    "product_image": image_url,
                    "product_price": product_price,
                    "rating": rating, 
                    'warranty': warranty,
                    "delivery": {
                        'location': location1,
                        'details': delivary,
                        "delivary_price": delivary_price, 
                        'return_policy': returns, 
                    },
                    "brand": {
                        "name": brand_names,
                        "url": brand_links,
                        "more_product_text": more_brand_data,
                        "more_product_url": more_brand_urls
                    },
                    "seller": {
                        "name": seller_name,
                        "url": seller_url,
                        "positive_ratings": value1,
                        "ship_on_time": value2
                    }
                }
            }
            return data

        except Exception as e :
            print(f"Error : {e}")


if __name__ == "__main__":
    api = GetInfo()
    data = api.info_api("https://www.daraz.com.bd/products/-i1586653992.html")
    print(json.dumps(data, indent=4))

