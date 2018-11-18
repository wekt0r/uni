from functools import reduce
from copy import deepcopy
from random import choice, shuffle
#min of hamming distances between all 01 sentences with d-ones

tests = [
   ([7,7,7,7,7,7,7], [7,7,7,7,7,7,7]),
   ([2,2,7,7,2,2,2], [2,2,7,7,2,2,2]),
   ([2,2,7,7,2,2,2], [4,4,2,2,2,5,5]),
   ([7,6,5,4,3,2,1], [1,2,3,4,5,6,7]),
   ([7,5,3,1,1,1,1], [1,2,3,7,3,2,1])
]

def hamming_distance(w,v):
    return sum(c != d for c,d in zip(w,v))

def all_1_sentences(n, d):
    for i in range(0,n-d+1):
        yield [0]*i + [1]*d + [0]*(n-i-d)

def opt_dist(l, d):
    return min([hamming_distance(l, sen) for sen in all_1_sentences(len(l),d)])

def solve(row_values, column_values):
    #row_values :: [int]
    #column_values :: [int]
    n = len(row_values)
    m = len(column_values)

    def transpose(matrix):
        return [[matrix[j][i] for j in range(n)] for i in range(m)]

    def valid(board):
        return (all(not opt_dist(row, val) for row,val in zip(board, row_values))
               and all(not opt_dist(col, val) for col, val in zip(transpose(board), column_values)))

    board = [[0 for _ in range(m)] for _ in range(n)]
    fillable_rows = [i for i,a in enumerate(row_values) if board[i] not in list(all_1_sentences(m,a)) ]
    counter = 0
    while not valid(board):
        counter += 1
        if counter == 1200:
            print("COUNTER 1200 REACHED - I'M DRAWING BOARD AGAIN")
            counter = 0
            board = [[choice([0,1]) for _ in range(m)] for _ in range(n)]
    #    print("\n".join(" ".join(map(str,row)) for row in board))
    #    print("---------------")
        i = choice(fillable_rows)
    #    print("eeeee {}".format( i))
        best_j = None
        v= opt_dist(board[i], row_values[i]) + n
        t = list(range(m))
        shuffle(t)
        for j in t:
            new_board = deepcopy(board)
            new_board[i][j] = 1 - new_board[i][j]
    #        print("Hello - i have {}, {}".format(new_board[i], row_values[i]))
            value = opt_dist(new_board[i], row_values[i])
            value += opt_dist([new_board[k][j] for k in range(n)], column_values[j])
            if value < v:
                v = value
                best_j = j
        board[i][best_j] = 1 - new_board[i][best_j]
    #    print(fillable_rows)
    print("FINALLY:")
    print(counter)
    #print("\n".join(" ".join(map(str,row)) for row in board))
    print("\n".join("".join("#" if char else "." for char in row) for row in board))
