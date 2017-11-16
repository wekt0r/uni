class Formula:
    def __init__(self):
        pass
    def evaluate(self, variables):
        pass
    def __str__(self):
        pass

class True_(Formula):
    def __init__(self):
        pass
    def evaluate(self, variables):
        return True
    def __str__(self):
        return "⊤"


class False_(Formula):
    def __init__(self):
        pass
    def evaluate(self, variables):
        return False
    def __str__(self):
        return "⊥"


class Var(Formula):
    def __init__(self, name):
        self.name = name
    def evaluate(self, variables):
        return variables[self.name]
    def __str__(self):
        return str(self.name)

class Not(Formula):
    def __init__(self, p):
        self.p = p
    def evaluate(self, variables):
        return not self.p.evaluate(variables)
    def __str__(self):
        return "¬ {}".format(self.p)

class _BinaryFormula(Formula):
    def __init__(self, p, q):
        self.p = p
        self.q = q

    def __str__(self, operator=""):
        return "{} {} {}".format(self.p, operator, self.q)


class Or(_BinaryFormula):
    def __init__(self, p, q):
        super(Or, self).__init__(p, q)
    def evaluate(self, variables):
        return self.p.evaluate(variables) or self.q.evaluate(variables)
    def __str__(self):
        return super(Or, self).__str__("∨")


class And(_BinaryFormula):
    def __init__(self, p, q):
        super(And, self).__init__(p, q)
    def evaluate(self, variables):
        return self.p.evaluate(variables) and self.q.evaluate(variables)
    def __str__(self):
        return super(And, self).__str__("∧")


class Impl(_BinaryFormula):
    def __init__(self, p, q):
        super(Impl, self).__init__(p, q)
    def evaluate(self, variables):
        return not self.p.evaluate(variables) or self.q.evaluate(variables)
    def __str__(self):
        return super(Impl, self).__str__("→")


class Equiv(_BinaryFormula):
    def __init__(self, p, q):
        super(Equiv, self).__init__(p, q)
    def evaluate(self, variables):
        p_value = self.p.evaluate(variables)
        q_value = self.q.evaluate(variables)
        return (p_value and q_value) or (not p_value and not q_value)
    def __str__(self):
        return super(Equiv, self).__str__("↔")

class TautologyChecker:
    @staticmethod
    def _every_possible_val(ls):
        if not ls:
            return [{}]
        else:
            tail = TautologyChecker._every_possible_val(ls[1:])
            return [dict({ls[0]: False}, **vals_dict) for vals_dict in tail] + [dict({ls[0] : True}, **vals_dict) for vals_dict in tail]

    @staticmethod
    def _variables_list(f):
        if isinstance(f, True_) or isinstance(f, False_) or not f:
            return set()
        if isinstance(f, Var):
            return {f.name}
        if isinstance(f, Not):
            return TautologyChecker._variables_list(f.p)
        return TautologyChecker._variables_list(f.p) | TautologyChecker._variables_list(f.q)

    @staticmethod
    def is_tautology(formula):
        return all(formula.evaluate(vars_dict) for vars_dict in TautologyChecker._every_possible_val(list(TautologyChecker._variables_list(formula))))
