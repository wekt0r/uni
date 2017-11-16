import unittest
from l3z1_list_of_primes import primes

class TestListOfPrimes(unittest.TestCase):
    def test_should_give_primes_below_1(self):
        self.assertEqual([], primes(1))
    def test_should_give_2_3_5_7(self):
        self.assertEqual([2,3,5,7], primes(8))
    def test_should_include_boundary_prime(self):
        self.assertEqual([2,3,5,7,11,13,17,19], primes(19))
    def test_should_check_amount_of_primes(self):
        self.assertEqual(9592, len(primes(10**5))) #9592 taken from wolfram_alpha

if __name__ == "__main__":
    unittest.main()
