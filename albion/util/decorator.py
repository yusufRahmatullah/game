def cache(name: str):
    _cache = {}

    def inner_func(func):
        def wrapper(*args, **kwargs):
            if name in _cache:
                return _cache[name]

            res = func(*args, **kwargs)
            _cache[name] = res
            return res
        return wrapper
    return inner_func
