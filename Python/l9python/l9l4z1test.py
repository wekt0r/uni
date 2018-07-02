import unittest
from l4z1_iter import *


class TestPrimes(unittest.TestCase):
    def test_should_give_primes_below_1(self):
        self.assertEqual([], primes(1))
    def test_should_give_2_3_5_7(self):
        self.assertEqual([2,3,5,7], primes(8))
    def test_should_include_boundary_prime(self):
        self.assertEqual([2,3,5,7,11,13,17,19], primes(19))
    def test_should_check_amount_of_primes(self):
        self.assertEqual(9592, len(primes(10**5))) #9592 taken from wolfram_alpha


class TestPrimesIter(unittest.TestCase):
    def test_should_give_primes_below_1(self):
        self.assertEqual([], list(primes_iter(1)))
    def test_should_give_2_3_5_7(self):
        self.assertEqual([2,3,5,7], list(primes_iter(8)))
    def test_should_include_boundary_prime(self):
        self.assertEqual([2,3,5,7,11,13,17,19], list(primes_iter(19)))
    def test_should_check_amount_of_primes(self):
        self.assertEqual(9592, len(list(primes_iter(10**5))))


class TestPrimesFun(unittest.TestCase):
    def test_should_give_primes_below_1(self):
        self.assertEqual([], primes_fun(1))
    def test_should_give_2_3_5_7(self):
        self.assertEqual([2,3,5,7], primes_fun(8))
    def test_should_include_boundary_prime(self):
        self.assertEqual([2,3,5,7,11,13,17,19], primes_fun(19))
    def test_should_check_amount_of_primes(self):
        self.assertEqual(9592, len(primes_fun(10**5)))


if __name__ == "__main__":
    test_classes_to_run = [TestPrimes, TestPrimesIter, TestPrimesFun]

    loader = unittest.TestLoader()
    suites_list = []
    for test_class in test_classes_to_run:
        suite = loader.loadTestsFromTestCase(test_class)
        suites_list.append(suite)

    big_suite = unittest.TestSuite(suites_list)

    runner = unittest.TextTestRunner()
    results = runner.run(big_suite)
