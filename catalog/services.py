from catalog.models import Catalog,Product
from django.core.cache import cache
from django.conf import settings


def cached_categories():
        if settings.CACHE_ENABLED:
            key = 'categories_list'
            categories_list = cache.get(key)
            if categories_list is None:
                categories_list = Catalog.objects.all()
                cache.set(key,categories_list)
        else:
            categories_list = Catalog.objects.all()
        return categories_list


def cached_products():
    if settings.CACHE_ENABLED:
        key = 'products_list'
        products_list = cache.get(key)
        if products_list is None:
            products_list = Product.objects.all()
            cache.set(key, products_list)
    else:
        products_list = Product.objects.all()
    return products_list