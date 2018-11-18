from queue import PriorityQueue
from collections import namedtuple
from copy import copy,deepcopy
from random import choice
from functools import reduce

MOVES = [(-1, 0), (1, 0), (0, 1), (0, -1)]
DIRS = ['U','D','R','L']
State = namedtuple("State", ["com_cords", "moves"])

with open("zad_input.txt") as f:
    board = [list(row) for row in f.read().split("\n") if row]
    #print(board)

def print_board(board):
    return "\n".join(["".join(row) for row in board])

def dpcp(board):
    return [list(row) for row in board]

def preprocessed(board):
    com_cords = {(i,j) for i,row in enumerate(board) for j,char in enumerate(row) if char in {'S', 'B'}}
    return [[{'B': 'G', 'S': ' '}.get(char, char)
             for char in row] for row in board], com_cords

def make_move(board, com_cords, dx, dy):
    return {(x+dx,y+dy) if board[x+dx][y+dy] != '#' else (x,y) for x,y in com_cords}

def get_goals(board):
    return {(i,j) for i,row in enumerate(board) for j,char in enumerate(row) if char in {'G', 'B'}}

def avg(gen):
    x,y = reduce(lambda x,y: (x[0]+y, x[1]+1), gen, (0,0))
    return x/y

def solve(initial_board):
    board, com_cords = preprocessed(initial_board)
    goals_cords = get_goals(board)
    closest_goal = {(x,y): min([abs(x - gx) + abs(y - gy) for gx,gy in goals_cords]) for x in range(len(board)) for y in range(len(board[0]))}
    def f(moves, cc):
        return len(moves) + max(closest_goal[(cx,cy)] for cx,cy in cc)

    def is_solved(com_cords):
        return all(board[x][y] == 'G' for x,y in com_cords)
    moves = ""

    queue = PriorityQueue()
    queue.put((f(moves, com_cords),State(com_cords, moves)))
    already_visited = set()
    while queue:
        _, (com_cords, moves) = queue.get_nowait()
        #print("We check moves = {} for {} ".format(moves, len(com_cords)))
        if repr(com_cords) not in already_visited:
            already_visited.add(repr(com_cords))
            if is_solved(com_cords):
                print("we finished " + moves)
                return moves

            for move,m in zip(MOVES,DIRS):
                new_com_cords = make_move(board, com_cords, *move)
                queue.put((f(moves, new_com_cords) + 1, State(new_com_cords, str(moves) + m)))


with open("zad_output.txt", mode='w') as f:
    f.write(solve(board))
#print(solve(board))
