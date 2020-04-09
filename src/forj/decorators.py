from .middleware import get_current_request


def get_request_cache():
    return getattr(get_current_request(), "cache", None)


cache_args_kwargs_marker = object()


def cache_calculate_key(*args, **kwargs):
    key = args + (cache_args_kwargs_marker,) + tuple(sorted(kwargs.items()))
    return str(key)


def cache_for_request(fn):
    def wrapper(*args, **kwargs):
        cache = get_request_cache()

        if not cache:
            return fn(*args, **kwargs)

        key = cache_calculate_key(fn.__name__, *args, **kwargs)
        result = getattr(cache, key, None)

        if not result:
            result = fn(*args, **kwargs)
            setattr(cache, key, result)

        return result

    return wrapper
