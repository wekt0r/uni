from queue import PriorityQueue
from heapq import *
from collections import namedtuple
from copy import copy,deepcopy
from random import choice
from functools import reduce
from math import sqrt

MOVES = [(-1, 0), (1, 0), (0, 1), (0, -1)]
DIRS = ['U','D','R','L']
#OPPOSITE_MOVE = {'U': 'D', 'D': 'U', 'L': 'R', 'R': 'L'}
DIR_TO_MOVE = dict(zip(DIRS,MOVES))
NEG_MOVE = {'U': 'D', 'D': 'U', 'L': 'R', 'R': 'L'}

State = namedtuple("State", ["visiter", "com_cords", "moves"])

with open("zad_input.txt") as f:
    board = [list(row) for row in f.read().split("\n") if row]
    #print(board)

def print_board(board):
    return "\n".join(["".join(row) for row in board])

def dpcp(board):
    return [list(row) for row in board]

def preprocessed(board):
    com_cords = {(i,j) for i,row in enumerate(board) for j,char in enumerate(row) if char in 'SB'}
    return [[{'B': 'G', 'S': ' '}.get(char, char)
             for char in row] for row in board], com_cords

def make_move(board, com_cords, dx, dy):
    return {(x+dx,y+dy) if board[x+dx][y+dy] != '#' else (x,y) for x,y in com_cords}

def get_goals(board):
    return {(i,j) for i,row in enumerate(board) for j,char in enumerate(row) if char in 'GB'}

def avg(gen):
    x,y = reduce(lambda x,y: (x[0]+y, x[1]+1), gen, (0,0))
    return x/y

def dijkstra_for_distances(board, goals_cords, x,y):
    q = PriorityQueue()
    q.put( (0,(x,y)) )
    been = set()
    #print(goals_cords)
    while not q.empty():
        c,(x1,y1) = q.get_nowait()
        #print(c, x1, y1)
        if (x1,y1) not in been and board[x1][y1] != '#':
            been.add((x1,y1))
            if (x1,y1) in goals_cords:
                return c
            for dx,dy in MOVES:
                if board[x1+dx][y1+dy] != '#':
                    q.put((c+1,(x1+dx,y1+dy)))


def solve(initial_board):
    #counter = 0
    board, com_cords = preprocessed(initial_board)
    goals_cords = get_goals(board)
    #print(print_board(board))
    closest_goal = [[dijkstra_for_distances(board, goals_cords, x, y) for y in range(len(board[0]))] for x in range(len(board))]
    def f(moves, cc):
        return len(moves) + 2*max(closest_goal[cx][cy] for cx,cy in cc)
    #def f(moves, cc):
    #    return len(moves) + sum(min(abs(cx - gx) + abs(cy - gy) for gx,gy in goals_cords) for cx,cy in cc)/(len(cc)*len(goals_cords))

    def is_solved(com_cords):
        #return all(board[x][y] == 'G' for x,y in com_cords)
        return com_cords <= goals_cords
    moves = ""

    # for _ in range(5):
    #     m = choice([char for char in DIRS if char != NEG_MOVE[moves[-1]]] if len(moves) else DIRS)
    #     #m = min(DIRS, key=lambda m: len(make_move(board, com_cords, *DIR_TO_MOVE[m])))
    #     moves += m
    #     com_cords = make_move(board, com_cords, *DIR_TO_MOVE[m])

    pqueue = [(f(moves, com_cords),State(tuple(sorted(list(com_cords))),com_cords, moves))]
    already_visited = set()
    while pqueue:
        #print(moves)
        _, (visiter, com_cords_n, moves) = heappop(pqueue)
        #counter += 1
        if visiter not in already_visited:
            already_visited.add(visiter)
            if is_solved(com_cords_n):
                print("we finished " + moves)
                #print(counter)
                return moves

            for move,m in zip(MOVES,DIRS):
                new_com_cords = make_move(board, com_cords_n, *move)
                new_visiter = tuple(sorted(list(new_com_cords)))
                if new_visiter not in already_visited:
                    heappush(pqueue, (f(moves, new_com_cords) + 1, State(new_visiter, new_com_cords, str(moves) + m)))


with open("zad_output.txt", mode='w') as f:
    f.write(solve(board))
#print(solve(board))
