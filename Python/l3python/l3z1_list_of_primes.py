from functools import reduce
from math import floor, sqrt

def _sq(n):
    return floor(sqrt(n)) + 1

def primes(n):
    return sorted(set(range(2,n+1)) - {y for x in range(2,_sq(n)) for y in range(x*x, n+1, x)})

def primes_fun(n):
    return sorted(set(range(2,n+1)) - reduce(lambda x,y: x | y, map(lambda x: set(range(x*x, n+1, x)),range(2, _sq(n))), set()))
