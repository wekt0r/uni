import unittest
from l3z2_perfect import perfect

class TestPerfect(unittest.TestCase):
    def test_should_give_perfect_numbers_below_ten_thousand(self):
        self.assertEqual([6,28,496,8128], perfect(10000))
    def test_should_include_boundary_perfect(self):
        self.assertEqual([6,28,496], perfect(496))

if __name__ == "__main__":
    unittest.main()
