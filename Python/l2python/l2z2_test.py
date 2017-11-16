import unittest
from l2z2_formula import *

FI1 = Impl(And(Var("x"), Var("y")),Or(Var("x"), Var("y")))
FI2 = Or(Var("p"), Var("q"))
FI3 = Impl(Not(Var("p")),Impl(Var("p"),Var("q")))
FI4 = Equiv(Not(Var("p")), Var("p"))

class TestFormula(unittest.TestCase):
    def test_simple_implication_evaluation(self):
        self.assertTrue(FI3.evaluate({"p": False, "q": False}))

    def test_simple_or_evaluation(self):
        self.assertTrue(FI2.evaluate({"p": False, "q": True}))

    def test_equivalence_evaluation(self):
        self.assertFalse(FI4.evaluate({"p": True}))

    def test_simple_tautology_and_implies_or(self):
        self.assertTrue(TautologyChecker.is_tautology(FI1))

    def test_not_tautology(self):
        self.assertFalse(TautologyChecker.is_tautology(FI2))

    def test_duns_scotus_law(self):
        self.assertTrue(TautologyChecker.is_tautology(FI3))


if __name__ == "__main__":
    for formula in [FI1, FI2, FI3, FI4]:
        print(formula)

    unittest.main()
