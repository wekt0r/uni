from functools import reduce, lru_cache
from random import choice, shuffle, randrange, randint
from collections import deque
from queue import PriorityQueue
#min of hamming distances between all 01 sentences with d-ones

with open("zad_input.txt") as f:
    inp = [[int(c) for c in row.split(" ") if c] for row in f.read().split("\n") if row]
    [K,M] = inp[0]
    rows = inp[1:K+1]
    columns = inp[-M:]

def transpose(matrix):
    return [[matrix[a][b] for a in range(len(matrix))] for b in range(len(matrix[0]))]

def generate_all(n,a):
    if n <= 0:
        if not a:
            return [[]]
        else:
            return []
    if not a:
        return [[0]*n]
    [a1, *at] = a
    return [[0]*i + [1]*a1 + ([0] if at else []) + other for i in range(0, n) for other in generate_all(n-a1-i-(1 if at else 0), at) if len([0]*i + [1]*a1 + ([0] if at else []) + other) == n]

def solve(row_values, column_values):

    def allowable(row):
        def _and_pixel(x,y):
            return x if x == y else 2
        return reduce(lambda a, b: [_and_pixel(x,y) for x, y in zip(a, b)], row)

    def show(m):
        return "\n".join("".join(".#?"[i] for i in x) for x in m)

    w, h = len(column_values), len(row_values)
    rows = [generate_all(w, x) for x in row_values]
    cols = [generate_all(h, x) for x in column_values]
    can_do = [allowable(row) for row in rows]

    def _can_fit(x,y):
        return x == y or x == 2 or y == 2

    def fits(a, b):
        return all(_can_fit(x,y) for x, y in zip(a, b))

    def fix_col(n):
        c = [x[n] for x in can_do]
        cols[n] = [x for x in cols[n] if fits(x, c)]
        for i, x in enumerate(allowable(cols[n])):
            if x != can_do[i][n]:
                fillable_rows.add(i)
                can_do[i][n] = x if _can_fit(x, can_do[i][n]) else 2

    def fix_row(n):
        c = can_do[n]
        rows[n] = [x for x in rows[n] if fits(x, c)]
        for i, x in enumerate(allowable(rows[n])):
            if x != can_do[n][i]:
                fillable_cols.add(i)
                can_do[n][i] = x if _can_fit(x, can_do[n][i]) else 2

    fillable_rows, fillable_cols = set(), set(range(w))

    while fillable_cols:
        for i in fillable_cols:
            fix_col(i)
        fillable_cols = set()
        for i in fillable_rows:
            fix_row(i)
        fillable_rows = set()

    return show(can_do)


def print_board(board):
    return "\n".join(["".join(map(str,row)) for row in board])

with open("zad_output.txt", mode='w') as f:
    f.write(solve(rows,columns))
