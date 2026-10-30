from Api.product_review.review_ import product_review
from Api.Category_Api.category_API import DarazCategoryAPI
from Api.Product_info_api.info import GetInfo
from Api.SearchApi.search_api import SearchApi

from fastapi import FastAPI


app = FastAPI(
    title="Daraz Api",
    description="Unlimited Api",
    version="0.00.1"
)

@app.get("/")
def index():
    return {
        'success': True,
        'message': 'Server online.'
    }

@app.get("/api/v1/product/info")
def get_product_info(url):
    if not url:
        return {
            'success': False, 
            'error': "Product Url Not Found!"
        }

    try:
        api = GetInfo()
        data = api.info_api(product_url=url)
        if data:
            ds = {
                'success': True,
                'message': "",
                'data': data
            }
            return ds 
        else:
            return {
                'success': False,
                'error': 'Server Error',
                'data': {}
            }
    except Exception as e :
        return {
            'success': False,
            'error': e,
            'data': {}
        }

@app.get("/api/v1/product/reviews")
def review_product(url):
    if not url:
        return {
            'success': False,
            'error': "Product Url not found!",
            'data': {}
        }
    try:
        api = product_review()
        data = api.api_data
        api.run(product_url=url)
        if data:
            ds = {
                'success':True,
                'data': data
            } 
            return ds
        else:
            return {
                'success': False, 
                'data': data
            }
    except Exception as e :
        return {
            'success': False,
            'error': e , 
            'data': {}
        }

@app.get("/api/v1/product/search")
def search(q):
    if not q:
        return {
            'success': False, 
            'error': 'Search Name not found!',
            'data': {}
        }

    try:
        api = SearchApi()
        api.run(query=q)
        data = api.api_data
        if data:
            da = {
                'success': True,
                'msg': "",
                'data': data
            }
            return da
        else:
            return {
                'success': False, 
                'error': "server error!",
                'data': {}
            }
    except:
        pass 

@app.get("/api/v1/product/category")
def send_category():
    try:
        api = DarazCategoryAPI()
        api.run()

        data = api.api_data

        if not data:
            return {
                "success": False,
                "error": "Data not found!"
            }

        return {
            "success": True,
            "data": data
        }

    except Exception as e:
        print(f"Error: {e}")

        return {
            "success": False,
            "error": str(e)
        }



if __name__ == "__main__":
    import uvicorn
    # Use "0.0.0.0" to listen on all available network interfaces
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)