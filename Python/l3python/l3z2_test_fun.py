import unittest
from l3z2_perfect import perfect_fun

class TestPerfect(unittest.TestCase):
    def test_should_give_perfect_numbers_below_ten_thousand(self):
        self.assertEqual([6,28,496,8128], perfect_fun(10000))
    def test_should_include_boundary_perfect(self):
        self.assertEqual([6,28,496], perfect_fun(496))

if __name__ == "__main__":
    unittest.main()
