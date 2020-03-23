
import requests
import collections
from django.core.cache import cache
from django.conf import settings



FavoriteWithProduct = collections.namedtuple(
    'FavoriteWithProduct',
    ['id', 'title', 'image', 'price', 'link', 'reviewScore']
)


def cache_api(func):
    """
    Decorator que verifica se os dados do produto estão presentes no cache.
    Caso não esteja, efetua a consulta à api remota e armazena no cache.
    """
    def wrapper(product_id):
        key = f'product-{product_id}'
        cached_response = cache.get(key)
        if cached_response:
            return 200, cached_response
        status_code, dict_response = func(product_id)
        if status_code == 200:
            cache_timeout = getattr(settings, 'CACHE_TIMEOUT', 86400)
            cache.set(key, dict_response, cache_timeout)
        return status_code, dict_response
    return wrapper


def fill_favorites(data):
    favorites_with_products = []
    for favorite in data:
        _, details = request_product_details(favorite.product_id)
        fwp = FavoriteWithProduct(
            id=favorite.id,
            title=details.get('title'),
            image=details.get('image'),
            price=details.get('price'),
            link=favorite.url,
            reviewScore=details.get('reviewScore')
        )
        favorites_with_products.append(fwp)
    return favorites_with_products


@cache_api
def request_product_details(product_id):
    try:
        product_detail_url = f'http://challenge-api.luizalabs.com/api/product/{product_id}'
        response = requests.get(product_detail_url)
        response.raise_for_status()
        return response.status_code, response.json()
    except requests.exceptions.HTTPError:
        return response.status_code, ''
