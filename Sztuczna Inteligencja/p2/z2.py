from collections import namedtuple
from queue import Queue, PriorityQueue
from functools import reduce
from copy import copy

MOVES = [(-1, 0), (1, 0), (0, -1), (0, 1)]
DIRS = ['U','D','L','R']
State = namedtuple("State", ["board", "ki", "kj", "type", "moves"])

with open("zad_input.txt") as f:
    board = [list(row) for row in f.read().split("\n") if row]

def get_keeper_coordinates(board):
    try:
        i,j = [(i,row.index('K')) for i,row in enumerate(board) if 'K' in row][0]
        return i,j, 'K'
    except IndexError:
        i,j = [(i, row.index('+')) for i,row in enumerate(board) if '+' in row][0]
        return i,j, '+'

def is_solved(board):
    return sum(row.count('B') for row in board) == 0

def min_goal_dist(board, x, y): #min_goal_distance_for given box
    return min((abs(x - i) + abs(y - j) for i,row in enumerate(board) for j,char in enumerate(row) if char in {'G', '+'}))

def approximate_distance_to_solution(board, ki, kj):
    #return (sum((min_goal_dist(board, i, j) for i,row in enumerate(board) for j,char in enumerate(row) if char == 'B')))
            #+ max((abs(i - ki) + abs(j - kj) for i,row in enumerate(board) for j,char in enumerate(row) if char == 'B')))
    #return 0
    return sum(row.count("B") for row in board)

def make_move(board_o, ki, kj, kt, x, y):
    if board_o[ki+x][kj+y] == 'W':
        return None

    if board_o[ki+x][kj+y] == '.':
        board = dpcp(board_o)
        board[ki+x][kj+y] = 'K'
        board[ki][kj] = 'G' if kt == '+' else '.'
        return board, ki+x, kj+y, board[ki+x][kj+y]

    if board_o[ki+x][kj+y] == 'G':
        board = dpcp(board_o)
        board[ki+x][kj+y] = '+'
        board[ki][kj] = 'G' if kt == '+' else '.'
        return board, ki+x, kj+y, board[ki+x][kj+y]


    if board_o[ki+x][kj+y] == 'B':
        if board_o[ki+2*x][kj+2*y] not in {'W', 'B', '*'}: #we dont have another immovable object behind
            board = dpcp(board_o)
            board[ki+x][kj+y] = 'K'
            board[ki][kj] = 'G' if kt == '+' else '.'
            if board[ki+2*x][kj+2*y] == 'G':
                board[ki+2*x][kj+2*y] = '*'
            if board[ki+2*x][kj+2*y] == '.':
                board[ki+2*x][kj+2*y] = 'B'
            return board, ki+x, kj+y, board[ki+x][kj+y]
        else:
            return None

    if board_o[ki+x][kj+y] == '*':
        if board_o[ki+2*x][kj+2*y] not in {'W', 'B', '*'}: #we dont have another immovable object behind
            board = dpcp(board_o)
            board[ki+x][kj+y] = '+'
            board[ki][kj] = 'G' if kt == '+' else '.'
            if board[ki+2*x][kj+2*y] == 'G':
                board[ki+2*x][kj+2*y] = '*'
            if board[ki+2*x][kj+2*y] == '.':
                board[ki+2*x][kj+2*y] = 'B'
            return board, ki+x, kj+y, board[ki+x][kj+y]
        else:
            return None

def solve_bfs(initial_board):
    i,j, t = get_keeper_coordinates(initial_board)
    initial_state = State(initial_board, i, j, t, "")
    queue = Queue()
    queue.put(initial_state)
    already_visited = set()
    while True:
        board, ki, kj, kt, moves = queue.get_nowait()
        if repr(board) not in already_visited:
            if is_solved(board):
                return moves

            already_visited.add(repr(board))
            for (x,y),m in zip(MOVES,DIRS):
                new_state = make_move(board, ki, kj, kt, x, y)
                if new_state:
                    new_board, new_ki, new_kj, new_kt = new_state
                    queue.put(State(new_board, new_ki, new_kj, new_kt, copy(moves) + m))

def print_board(board):
    return "\n".join(["".join(row) for row in board])

def dpcp(board):
    return [list(row) for row in board]

def solve_astar(initial_board):
    i,j, t = get_keeper_coordinates(initial_board)
    initial_state = State(initial_board, i, j, t, "")

    # g - to get here cost
    # h - approximate to finish from here cost
    def f(board, moves, ki, kj):
        return len(moves) + approximate_distance_to_solution(board, ki, kj)

    queue = PriorityQueue()
    queue.put((f(initial_board, "", i, j),initial_state))
    already_visited = set()
    while True:
        v,(board, ki, kj, kt, moves) = queue.get_nowait()
        if repr(board) not in already_visited:
            #print("We have v = {} and moves = {} for \n {}".format(v, moves, print_board(board)))
            if is_solved(board):
                return moves

            already_visited.add(repr(board))
            for (x,y),m in zip(MOVES,DIRS):
                new_state = make_move(board, ki, kj, kt, x, y)
                if new_state:
                    new_moves = copy(moves) + m
                    new_board, new_ki, new_kj, new_kt = new_state
                    queue.put((f(new_board, new_moves, new_ki, new_kj),State(new_board, new_ki, new_kj, new_kt, new_moves)))

with open("zad_output.txt", mode='w') as f:
    f.write(solve_bfs(board))
#from time import time
#t0 = time(); print(solve_bfs(board)); print(time() - t0)
#t0 = time(); print(solve_astar(board)); print(time() - t0)
