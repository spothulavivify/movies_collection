from threading import Lock
from django.core.cache import cache

class RequestCountMiddleware:
    _lock = Lock()
    CACHE_KEY = 'request_count'

    def __init__(self, get_response):
        self.get_response = get_response

        # Initialize the counter in cache if it doesn't exist
        if cache.get(self.CACHE_KEY) is None:
            cache.set(self.CACHE_KEY, 0)

    def __call__(self, request):
        with self._lock:

            # Ensure the key exists before incrementing
            if cache.get(self.CACHE_KEY) is None:
                cache.set(self.CACHE_KEY, 0)

            # Atomic increment of request count
            cache.incr(self.CACHE_KEY)

        response = self.get_response(request)
        return response

    @classmethod
    def get_request_count(cls):
        return cache.get(cls.CACHE_KEY, 0)

    @classmethod
    def reset_request_count(cls):
        with cls._lock:
            cache.set(cls.CACHE_KEY, 0)
