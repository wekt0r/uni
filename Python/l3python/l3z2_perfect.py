from functools import reduce

def perfect(n):
    return [x for x in range(2,n+1) if sum([y for y in range(1,x) if x%y == 0]) == x]

def perfect_fun(n):
    return list(filter(lambda x: reduce(lambda x,y: x+y, filter(lambda y: x%y == 0,range(1,x)), 0) == x, range(2,n+1)))
