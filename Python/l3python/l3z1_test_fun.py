import unittest
from l3z1_list_of_primes import primes_fun

class TestListOfPrimes(unittest.TestCase):
    def test_should_give_primes_below_1(self):
        self.assertEqual([], primes_fun(1))
    def test_should_give_2_3_5_7(self):
        self.assertEqual([2,3,5,7], primes_fun(8))
    def test_should_include_boundary_prime(self):
        self.assertEqual([2,3,5,7,11,13,17,19], primes_fun(19))
    def test_should_check_amount_of_primes(self):
        self.assertEqual(9592, len(primes_fun(10**5))) #9592 taken from wolfram_alpha

if __name__ == "__main__":
    unittest.main()
