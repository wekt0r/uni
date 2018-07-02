from functools import reduce
from math import floor, sqrt
from time import time
from decimal import *

getcontext().prec = 4


def _sq(n):
    """
    Returns floor of square root of n increased by 1.
    """
    return floor(sqrt(n)) + 1


def primes(n):
    """
    Returns list of prime numbers less or equal to n.
    :param n: int
    :return: list of prime numbers less or equal to n
    """
    return sorted(set(range(2, n + 1)) -
                  {y for x in range(2, _sq(n)) for y in range(x * x, n + 1, x)})


def primes_fun(n):
    """
    Returns list of prime numbers less or equal to n.
    """
    return sorted(set(range(2, n + 1)) - reduce(lambda x, y: x | y,
                                                map(lambda x: set(range(x * x, n + 1, x)), range(2, _sq(n))), set()))


def primes_iter(n):
    """
    Returns generator of prime numbers less or equal to n.
    """
    composite = set()
    for i in range(2, n + 1):
        if i not in composite:
            composite |= set(range(i * i, n + 1, i))
            yield i

if __name__ == '__main__':
    ROW = "{0} \t | {1} \t| {2} \t| {3} \t| {4}"

    def timer(function, argument, additional_function=None):
        begin = time()
        additional_function = additional_function or (lambda x: x)
        additional_function(function(argument))
        return Decimal(time()) - Decimal(begin)

    def timetester(*args):
        print(" \t | skladana \t| funkcyjna \t| iterator \t| listed iter")
        for arg in args:
            print(ROW.format(arg, timer(primes, arg),
                             timer(primes_fun, arg),
                             timer(primes_iter, arg),
                             timer(primes_iter, arg, list)))

    #timetester(1000, 10000, 100000, 200000)
