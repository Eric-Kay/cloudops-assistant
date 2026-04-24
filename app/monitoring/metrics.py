import time
from functools import wraps


def track_latency(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"[METRIC] {func.__name__} latency={elapsed:.4f}s")
        return result

    return wrapper