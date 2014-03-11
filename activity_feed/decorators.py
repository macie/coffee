"""
Custom decorators.

"""
from functools import wraps

from django.core.cache import cache


class cached(object):
    '''
    Sets/gets value from cache.

    Args:
        key (str): Name of cache object
        time (datetime, optional): Expiration time (in seconds). By default
                                   item never expire.

    Returns:
        Object stored in cache.

    Example:
        @classmethod
        @cached('all_articles', time=3600)
        def get_all(cls):
            return cls.objects.all()

    '''
    def __init__(self, key, time=None):
        self.key = key
        self.time = time

    def __call__(self, f):
        @wraps(f)
        def get_from_cache(*args, **kwargs):
            value = cache.get(self.key)
            if not value:  # cache object not exist
                value = f(*args, **kwargs)
                cache.set(self.key, value, self.time)
            return value
        return get_from_cache
