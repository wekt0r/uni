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

def dpcp(tab):
    return [list(l) for l in tab]

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

def allowable(row):
    def _and_pixel(x,y):
        return x if x == y else 2
    return reduce(lambda a, b: [_and_pixel(x,y) for x, y in zip(a, b)], row)

def show(m):
    return "\n".join("".join(".#?"[i] for i in x) for x in m)

def _can_fit(x,y):
    return x == y or x == 2 or y == 2

def fits(a, b):
    return all(_can_fit(x,y) for x, y in zip(a, b))


def deduce(w, h, rows, cols, can_do):
    def fix_col(n):
        c = [x[n] for x in can_do]
        cols[n] = [x for x in cols[n] if fits(x, c)]
        if not cols[n]:
            return 1
        for i, x in enumerate(allowable(cols[n])):
            if x != can_do[i][n]:
                fillable_rows.add(i)
                can_do[i][n] = x if _can_fit(x, can_do[i][n]) else 2

    def fix_row(n):
        c = can_do[n]
        rows[n] = [x for x in rows[n] if fits(x, c)]
        if not rows[n]:
            return 1
        for i, x in enumerate(allowable(rows[n])):
            if x != can_do[n][i]:
                fillable_cols.add(i)
                can_do[n][i] = x if _can_fit(x, can_do[n][i]) else 2

    fillable_rows, fillable_cols = set(), set(range(w))
    while fillable_cols:
        for i in fillable_cols:
            t = fix_col(i)
            if t == 1:
                return None, None, None
        fillable_cols = set()
        for i in fillable_rows:
            t = fix_row(i)
            if t == 1:
                return None, None, None
        fillable_rows = set()
    #print(show(can_do))
    #print("***")
    return can_do, rows, cols


def solved(board):
    return sum(row.count(2) for row in board) == 0

def solve(row_values, column_values):
    w, h = len(column_values), len(row_values)
    rows_all = [generate_all(w, x) for x in row_values]
    cols_all = [generate_all(h, x) for x in column_values]
    can_do = [allowable(row) for row in rows_all]

    can_do, rows_all, cols_all = deduce(w, h, rows_all, cols_all, can_do)
    stack = deque()
    stack.append((can_do, rows_all, cols_all))
    while stack:
        board, rows, cols = stack.pop()
        #board, rows, cols = deduce(w,h, rows, cols, board)
        if board:
            try:
                i,j = next((i,j) for i,row in enumerate(board) for j,p in enumerate(row) if p == 2)
            except StopIteration:
                print("hooorrraaayyyy!")
                print(show(board))
                return show(board)

            board_0 = dpcp(board)
            board_0[i][j] = 0
            rows_0, cols_0 = dpcp(rows), dpcp(cols)
            rows_0[i] = [row for row in rows[i] if row[j] == 0]#fits(board[i], row)]
            cols_0[j] = [col for col in cols[j] if col[i] == 0]#fits([row[j] for row in board], col)]
            if all(row for row in rows_0) and all(col for col in cols_0):
                board_0, rows_0, cols_0 = deduce(w,h, rows_0, cols_0, board_0)
                if board_0:
                    stack.append((board_0,rows_0, cols_0))

            board_1 = dpcp(board)
            board_1[i][j] = 1
            rows_1,cols_1 = dpcp(rows), dpcp(cols)
            rows_1[i] = [row for row in rows[i] if row[j] == 1]#fits(board[i], row)]
            cols_1[j] = [col for col in cols[j] if col[i] == 1]#fits([row[j] for row in board], col)]
            if all(row for row in rows_1) and all(col for col in cols_1):
                board_1, rows_1, cols_1 = deduce(w,h, rows_1, cols_1, board_1)
                if board_1:
                    stack.append((board_1,rows_1, cols_1))

    print("whopsyyy")



def print_board(board):
    return "\n".join(["".join(map(str,row)) for row in board])

with open("zad_output.txt", mode='w') as f:
    f.write(solve(rows,columns))
