#reversi chosen

from time import time
import random
import sys
from collections import defaultdict as dd

def initial_board():
    B = [ [None] * M for i in range(M)]
    B[3][3] = 1
    B[4][4] = 1
    B[3][4] = 0
    B[4][3] = 0
    return B

M=8

CORNERS = {(0,0), (0,M-1), (M-1,0), (M-1,M-1)}
BUFFER = {(1,0),(0,1),(1,1), (M-2,0), (M-2, 1), (M-1,1), (M-1, M-2),(M-2,M-1), (M-2,M-2), (0,M-2), (1,M-2), (1,M-1)}
EDGES = {(i,0) for i in range(M)} | {(i, M-1) for i in range(M)} | {(0, i) for i in range(M)} | {(M-1, i) for i in range(M)}
FIRST_LAYER = {(i,1) for i in range(1,M-1)} | {(i, M-2) for i in range(1,M-1)} | {(1, i) for i in range(1,M-1)} | {(M-2, i) for i in range(1,M-1)}
SECOND_LAYER = {(i,2) for i in range(2,M-2)} | {(i, M-3) for i in range(2,M-2)} | {(2, i) for i in range(2,M-2)} | {(M-3, i) for i in range(2,M-2)}

# PRIORITIES = [[5,1,3,3,3,3,1,5],
#               [1,1,2,2,2,2,1,1],
#               [3,2,4,4,4,4,2,3],
#               [3,2,4,None,None,4,2,3],
#               [3,2,4,None,None,4,2,3],
#               [3,2,4,4,4,4,2,3],
#               [1,1,2,2,2,2,1,1],
#               [5,1,3,3,3,3,1,5]]
class Board:
    dirs  = [ (0,1), (1,0), (-1,0), (0,-1), (1,1), (-1,-1), (1,-1), (-1,1) ]


    def __init__(self):
        self.board = initial_board()
        self.fields = set()
        self.move_list = []
        self.history = []
        for i in range(M):
            for j in range(M):
                if self.board[i][j] == None:
                    self.fields.add( (j,i) )

    def draw(self):
        for i in range(M):
            res = []
            for j in range(M):
                b = self.board[i][j]
                if b == None:
                    res.append('.')
                elif b == 1:
                    res.append('#')
                else:
                    res.append('o')
            print(''.join(res))
        print()


    def moves(self, player):
        res = []
        for (x,y) in self.fields:
            if any( self.can_beat(x,y, direction, player) for direction in Board.dirs):
                res.append( (x,y) )
        if not res:
            return [None]
        return res

    def can_beat(self, x,y, d, player):
        dx,dy = d
        x += dx
        y += dy
        cnt = 0
        while self.get(x,y) == 1-player:
            x += dx
            y += dy
            cnt += 1
        return cnt > 0 and self.get(x,y) == player

    def get(self, x,y):
        if 0 <= x < M and 0 <=y < M:
            return self.board[y][x]
        return None

    def do_move(self, move, player):
        self.history.append([x[:] for x in self.board])
        self.move_list.append(move)

        if move == None:
            return
        x,y = move
        x0,y0 = move
        self.board[y][x] = player
        self.fields -= set([move])
        for dx,dy in self.dirs:
            x,y = x0,y0
            to_beat = []
            x += dx
            y += dy
            while self.get(x,y) == 1-player:
              to_beat.append( (x,y) )
              x += dx
              y += dy
            if self.get(x,y) == player:
                for (nx,ny) in to_beat:
                    self.board[ny][nx] = player

    def result(self):
        res = 0
        for y in range(M):
            for x in range(M):
                b = self.board[y][x]
                if b == 0:
                    res -= 1
                elif b == 1:
                    res += 1
        return res

    def terminal(self):
        if not self.fields:
            return True
        if len(self.move_list) < 2:
            return False
        return self.move_list[-1] == self.move_list[-2] == None

    def random_move(self, player):
        ms = self.moves(player)
        if ms:
            return random.choice(ms)
        return [None]

    def get_agent_move(self, player):
        ms = self.moves(player)
        return max(ms if ms else [None], key=lambda x: self.get_score_from_n_games(8,16,x,player))


    def get_score_from_n_games(self, n, moves_forward, move, player):
        ov_score = 0
        tmp_game1 = Board()
        tmp_game1.board = dpcp(self.board)
        tmp_game1.fields = set(self.fields)
        tmp_game1.move_list = list(self.move_list)
        tmp_game1.history = list(self.history)
        tmp_game1.do_move(move, player)
        for _ in range(n):
            tmp_game = Board()
            tmp_game.board = dpcp(tmp_game1.board)
            tmp_game.fields = set(tmp_game1.fields)
            tmp_game.move_list = list(tmp_game1.move_list)
            tmp_game.history = list(tmp_game1.history)
            tmp_player = 0

            for _ in range(moves_forward):
                m = tmp_game.random_move(tmp_player)
                tmp_game.do_move(m, tmp_player)
                tmp_player = 1-tmp_player
                if tmp_game.terminal():
                    break
            ov_score += tmp_game.result()
        return ov_score

    def has_corners_after_moved(self, move, player):
        tmp_game1 = Board()
        tmp_game1.board = dpcp(self.board)
        tmp_game1.fields = set(self.fields)
        tmp_game1.move_list = list(self.move_list)
        tmp_game1.history = list(self.history)
        tmp_game1.do_move(move, player)
        return bool(CORNERS & set(tmp_game1.moves(1 - player)))


def dpcp(board):
    return [list(row) for row in board]

lost = 0
for i in range(5):
    player = 0
    B = Board()
    print("random starts")
    while True:
        if not player:
            m = B.random_move(player)
            B.do_move(m, player)
        else:
            #begin = time()
            m = B.get_agent_move(player)
            #print("it took {}".format(time() - begin))
            B.do_move(m, player)
        player = 1-player
        #raw_input()
        if B.terminal():
            break

    if B.result() < 0:
        #print("I've lost game no {}".format(i))
        lost += 1

    print(lost)
    
    player = 0
    B = Board()
    print("agent starts")
    while True:
        if player:
            m = B.random_move(player)
            B.do_move(m, player)
        else:
            #begin = time()
            m = B.get_agent_move(player)
            #print("it took {}".format(time() - begin))
            B.do_move(m, player)
        player = 1-player
        #raw_input()
        if B.terminal():
            break

    if B.result() < 0:
        #print("I've lost game no {}".format(i))
        lost += 1

    print(lost)


print("I've lost {}".format(lost))
