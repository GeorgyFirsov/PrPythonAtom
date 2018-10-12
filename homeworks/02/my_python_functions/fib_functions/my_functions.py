def cache_decorator(func):
    cache = {}
    def fnc(arg):
        if arg not in cache:
            cache[arg] = func(arg)
        return cache[arg]
    return fnc

@cache_decorator
def fib(n):
    if n < 3:
        return 1
    else:
        return fib(n - 1) + fib(n - 2)
