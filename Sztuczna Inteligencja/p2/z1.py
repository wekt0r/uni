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

def is_prefix(a,b):
    return a == b[:len(a)]

def block_values(line):
    result = []
    counter = 0
    for i in line:
        if i:
            counter += 1
        else:
            if counter:
                result.append(counter)
                counter = 0
    return result + [counter] if counter != 0 else result

def matching_prefix(line, values):
    bv = block_values(line)
    if len(line) > 0:
        if line[-1] and len(bv) <= len(values):
            return is_prefix(bv[:-1],values) and bv[-1 if len(bv) > 0 else 0] <= values[len(bv) - 1 if len(bv) > 0 else 0]
    return is_prefix(bv, values)

def dpcp(board):
    return [list(row) for row in board]

def hamming_distance(w,v):
    return sum(c != d for c,d in zip(w,v))

def generate_all(a,n):
    if n <= 0:
        if not a:
            return [tuple()]
        else:
            return []
    if not a:
        return [(0,)*n]
    [a1, *at] = a
    return [(0,)*i + (1,)*a1 + ((0,) if at else tuple()) + other for i in range(0, n) for other in generate_all(at, n-a1-i-(1 if at else 0)) if len((0,)*i + (1,)*a1 + ((0,) if at else tuple()) + other) == n]

def opt_dist(l, possiblilites=[]):
    return min(hamming_distance(l, sen) for sen in possiblilites)

def transpose(matrix):
    return [[matrix[a][b] for a in range(len(matrix))] for b in range(len(matrix[0]))]

def solve(rows, columns, row_values, column_values):
    len_of_row = columns
    len_of_column = rows
    preprocessed_rows = tuple(set(generate_all(row_values[i], len_of_row)) for i in range(0,rows))
    preprocessed_columns = tuple(set(generate_all(column_values[i], len_of_column)) for i in range(0,columns))
    to_be_filled = (sum(sum(row) for row in row_values))
    seed = [1]*to_be_filled + [0]*(columns*rows - to_be_filled)

    fillable_rows = list(range(0,rows))
    fillable_columns = list(range(0,columns))

    def _get_board(ls=[0],fun=lambda x:x[0]):
        return [[fun(ls) for _ in range(len_of_row)] for _ in range(len_of_column)]
    def _get_empty_board():
        return [[0 for _ in range(len_of_row)] for _ in range(len_of_column)]

    def valid(board):
        return (all(block_values(row) == val for row,val in zip(board, row_values))
               and all(block_values(col) == val for col, val in zip(transpose(board), column_values)))

    board = _get_board(seed, choice)
    retries = 0
    while not valid(board):
        retries += 1
        if retries > rows*columns*10 or not fillable_rows or not fillable_columns:
            retries = 0
            #print("retrying")
            #print("\n".join("".join("#" if char else "." for char in row) for row in board))
            for _ in range(int(sum(opt_dist(board[i], preprocessed_rows[i]) for i in range(0,rows)) + sum(opt_dist([board[t][j] for t in range(0, rows)], preprocessed_columns[j]) for j in range(0,columns))//(1.7))):
                i,j = randint(0,rows-1),randint(0,columns-1)
                board[i][j] = 1 - board[i][j]
            fillable_rows = list(range(0,rows))
            fillable_columns = list(range(0,columns))
            #board = _get_board(seed, choice)

        i = choice(fillable_rows)
        j_to_set, diff = None, 0
        shuffle(fillable_columns)
        for j in fillable_columns:
            cur_dist = opt_dist(board[i], preprocessed_rows[i]) + opt_dist([board[t][j] for t in range(0, rows)], preprocessed_columns[j])
            board[i][j] = 1 - board[i][j]
            new_dist = opt_dist(board[i], preprocessed_rows[i]) + opt_dist([board[t][j] for t in range(0, rows)], preprocessed_columns[j])
            board[i][j] = 1 - board[i][j]

            j_to_set, diff = (j, cur_dist - new_dist) if cur_dist - new_dist > diff else (j_to_set, diff)

        #print("*\n")
        #print("\n".join("".join("#" if char else "." for char in row) for row in board))
        if j_to_set is not None:
            board[i][j_to_set] = 1 - board[i][j_to_set]

            if not opt_dist(board[i], preprocessed_rows[i]):
                fillable_rows.remove(i)
            if not opt_dist([board[t][j_to_set] for t in range(0, rows)], preprocessed_columns[j_to_set]):
                fillable_columns.remove(j_to_set)

        #print("&\n")
        #print("\n".join("".join("#" if char else "." for char in row) for row in board))
        if choice([0]*1 + [1]):
            i,j = randint(0,rows-1),randint(0,columns-1)
            board[i][j] = 1 - board[i][j]
            if i not in fillable_rows:
                fillable_rows.append(i)
            if j not in fillable_columns:
                fillable_columns.append(j)

        #print("****")
#    print("\n".join("".join("#" if char else "." for char in row) for row in board))
#    print(retries)
    return "\n".join("".join("#" if char else "." for char in row) for row in board)

def print_board(board):
    return "\n".join(["".join(map(str,row)) for row in board])

with open("zad_output.txt", mode='w') as f:
    f.write(solve(K,M,rows,columns))
