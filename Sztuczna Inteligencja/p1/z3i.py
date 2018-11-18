from functools import reduce
from operator import __mul__, __add__

choose = lambda n,k: reduce(__mul__, range(n,n-k, -1), 1)//reduce(__mul__, range(1,k+1), 1)

class ProbabilityCounter:
    def __init__(self, blotkarz_deck, figurant_deck):
        self.bdeck = blotkarz_deck
        self.fdeck = figurant_deck
        self.bdeck_len = len(self.bdeck)
        self.fdeck_len = len(self.fdeck)
        self.all_blotkarz_hands = choose(self.bdeck_len, 5)
        self.all_figurant_hands = choose(self.fdeck_len, 5)

        def _poker():
            pass

        def blotkarz_win_probability():
            return 1

ball = choose(36, 5)
fall = choose(16, 5)
res_n = [20, 9*8*4, 9*8*4*6, choose(9,5)*4 - 20, 5*(4**5) - choose(9,5)*4, 9*4*8*4*7*2, 9*6*8*6*7*2]
res_d = [fall, fall - 4*3*4, fall - 4*3*4 - 4*4*3*6, fall - 4*3*4 - 4*4*3*6, fall - 4*3*4 - 4*4*3*6, fall - 4*3*4 - 4*4*3*6 - 4*4*3*4*2*4, fall - 4*3*4 - 4*4*3*6 - 4*4*3*4*2*4 - 4*6*3*6*1*4]
print(reduce(__add__, (a*b for a,b in zip(res_n, res_d)), 1)/(fall*ball))


def get_all_n_combinations(l,n):
    if n == 0:
        return [[]]
    if not l:
        return []
    smaller_subsets = get_all_n_combinations(l[1:], n-1)
    return [[l[0]] + smaller for smaller in smaller_subsets] + get_all_n_combinations(l[1:],n)
