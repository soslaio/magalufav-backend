
import requests


def request_product_details(product_id):
    try:
        product_detail_url = f'http://challenge-api.luizalabs.com/api/product/{product_id}'
        response = requests.get(product_detail_url)
        response.raise_for_status()
        return response.status_code, response.json()
    except requests.exceptions.HTTPError:
        return response.status_code, ''
