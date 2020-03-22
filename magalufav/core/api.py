
import requests


def request_product_details(product_id):
    product_detail_url = f'http://challenge-api.luizalabs.com/api/product/{product_id}'
    response = requests.get(product_detail_url)
    return response.status_code, response
