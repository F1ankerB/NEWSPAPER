from functools import lru_cache
@lru_cache(None)
def f(n):
    if n <= 1:
        return n
    if n > 1 and n % 3 == 0:
        return f(n//3)
    if n > 1 and n % 3 != 0:
        return n+f(n+2)
print(f(17))
