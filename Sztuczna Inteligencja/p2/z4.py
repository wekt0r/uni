#from queue import Queue
from collections import namedtuple, deque
from copy import copy,deepcopy
from random import choice

MOVES = [(-1, 0), (1, 0), (0, -1), (0, 1)]
DIRS = ['U','D','L','R']
DIR_TO_MOVE = dict(zip(DIRS,MOVES))
NEG_MOVE = {'U': 'D', 'D': 'U', 'L': 'R', 'R': 'L'}

State = namedtuple("State", ["com_cords", "moves"])

with open("zad_input.txt") as f:
    board = [list(row.replace("B", "G")) for row in f.read().split("\n") if row]
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

def solve(initial_board):
    board, com_cords = preprocessed(initial_board)

    def is_solved(com_cords):
        return all(board[x][y] == 'G' for x,y in com_cords)
    moves = ""
    while len(com_cords) > 2:
        m = choice([char for char in DIRS if char != NEG_MOVE[moves[-1]]] if len(moves) else DIRS)
        #m = min(DIRS, key=lambda m: len(make_move(board, com_cords, *DIR_TO_MOVE[m])))
        moves += m
        com_cords = make_move(board, com_cords, *DIR_TO_MOVE[m])

    queue = deque()
    queue.append(State(com_cords, moves))
    already_visited = set()
    while queue:
        com_cords, moves = queue.popleft()
        #print("We check moves = {} for {} ".format(moves, len(com_cords)))
        if repr(com_cords) not in already_visited:
            already_visited.add(repr(com_cords))
            if is_solved(com_cords):
                print("we finished " + moves)
                return moves

            for move,m in zip(MOVES,DIRS):
                new_com_cords = make_move(board, com_cords, *move)
                if len(moves) < 150:
                    queue.append(State(new_com_cords, str(moves) + m))

    return solve(initial_board)


with open("zad_output.txt", mode='w') as f:
    f.write(solve(board))
#print(solve(board))
