import time

from functools import wraps
from typing import Callable, TypeVar, ParamSpec


P = ParamSpec("P")
T = TypeVar("T")


def ttl_cache(minutes: int) -> Callable[[Callable[P, T]], Callable[P, T]]:
    """
    Decorator that caches the result of a function for a specified amount of time; implements a time-to-live (TTL) cache)

    This decorator implements a time-to-live (TTL) cache for a function. It caches the result of the function for a
    specified amount of time and refreshes the cache if the function is called after the TTL has passed.

    When the function is called for the first time, it is executed and its result is cached inside a dictionary. The
    arguments and keyword arguments used to call the function are used as the key to the cache. The expiration time of the
    cached result is stored along with the value of the result of the function as a tuple in the value of the cache dictionary.

    ```
    cache = {
        (arg1, arg2, ..., kwarg1=value1, kwarg2=value2, ...): (expiration_time, result),
        ...
    }
    ```

    If the function is called again before the TTL has passed, the cached result is returned. Otherwise, the function is
    executed, and its result is cached again.

    Args:
        minutes: The amount of time in minutes to cache the result.

    Returns:
        The cached result of the function (if available) or the result of the function itself.

    Example:
        >>> @ttl_cache(minutes=1)
        ... def example_function():
        ...     return "Hello, world!"
        >>> example_function()
        'Hello, world!'
        >>> time.sleep(60)
        >>> example_function()
        'Hello, world!'
    """
    ttl_seconds = minutes * 60

    def decorator(func: Callable[P, T]) -> Callable[P, T]:
        cache: dict[tuple[object, ...], tuple[float, T]] = {}

        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
            key = args + tuple(sorted(kwargs.items()))
            now = time.time()

            if key in cache:
                expires_at, value = cache[key]
                if now < expires_at:
                    return value

            value = func(*args, **kwargs)
            cache[key] = (now + ttl_seconds, value)
            return value

        return wrapper

    return decorator
