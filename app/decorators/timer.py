import time


def timer_method(func):
    def wrapper(self, *args, **kwargs):
        start = time.time()
        res = func(self, *args, **kwargs)
        print(f"{func.__name__} -> {(time.time() - start)}")
        return res

    return wrapper


def timer(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        res = func(*args, **kwargs)
        print(f"{func.__name__} -> {(time.time() - start)}")
        return res

    return wrapper
