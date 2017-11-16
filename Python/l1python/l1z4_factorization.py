from math import sqrt, floor

def factorize(n):
    for i in range(2,floor(sqrt(n)) + 1):
        if not n % i:
            return [i] + factorize(n//i)
    return [n]

def factorize_formatted(n):
    list_of_prime_factors = factorize(n)
    return sorted(list({(i, list_of_prime_factors.count(i)) for i in list_of_prime_factors}))

print(factorize_formatted(756))
