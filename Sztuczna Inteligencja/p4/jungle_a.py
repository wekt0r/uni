#from copy import deepcopy
from random import choice
from functools import reduce


N = 20000

grass, trap, den, water = '.#*~'

board = ['..#*#..',
         '...#...',
         '.......',
         '.~~.~~.',
         '.~~.~~.',
         '.~~.~~.',
         '.......',
         '...#...',
         '..#*#..']


h, w = 9, 7

empty = ' '
pieces_0 = rat0, cat0, dog0, wolf0, leopard0, tiger0, lion0, elephant0 = 'rcdwjtle'
pieces_1 = rat1, cat1, dog1, wolf1, leopard1, tiger1, lion1, elephant1 = pieces_0.upper()

power = {rat0: 0, cat0: 1, dog0: 2, wolf0: 3, leopard0: 4, tiger0: 5, lion0: 6, elephant0: 7,
         rat1: 0, cat1: 1, dog1: 2, wolf1: 3, leopard1: 4, tiger1: 5, lion1: 6, elephant1: 7}

den_0, den_1 = (0, 3), (8, 3)


def get_pieces_0():
    return {lion0: (0, 0), tiger0: (0, 6), dog0: (1, 1), cat0: (1, 5), rat0: (2, 0), leopard0: (2, 2), wolf0: (2, 4), elephant0: (2, 6)}


def get_pieces_1():
    return {lion1: (8, 6), tiger1: (8, 0), dog1: (7, 5), cat1: (7, 1), rat1: (6, 6), leopard1: (6, 4), wolf1: (6, 2), elephant1: (6, 0)}


def get_pieces_board():

    return [[lion0] + [empty] * 5 + [tiger0],
            [empty, dog0] + [empty] * 3 + [cat0, empty],
            [rat0, empty, leopard0, empty, wolf0, empty, elephant0],
            [empty] * 7,
            [empty] * 7,
            [empty] * 7,
            [elephant1, empty, wolf1, empty, leopard1, empty, rat1],
            [empty, cat1] + [empty] * 3 + [dog1, empty],
            [tiger1] + [empty] * 5 + [lion1]]


def print_board(pieces_board):
    print('\n'.join(''.join(row) for row in pieces_board))


def captures(attacking, attacked):
    return not (attacking in {elephant0, elephant1} and attacked in {rat0, rat1}) and power[attacking] > power[attacked] or (
            attacking in {rat0, rat1} and attacked in {elephant0, elephant1})


def on_board(y, x):
    return 0 <= y < h and 0 <= x < w


class Player:
    def __init__(self, den, pieces):
        self.den = den
        self.pieces = self.rat, self.cat, self.dog, self.wolf, self.leopard, self.tiger, self.lion, self.elephant = pieces_0
        self.piece_to_moves_generator = {self.rat: self.rat_moves, self.tiger: self.tiger_lion_moves, self.lion: self.tiger_lion_moves}  # rest is default
        self.tiger_lion_in_water = {}  # (y, x) -> (dy, dx)

    def standard_moves(self, piece, y_pos, x_pos, pieces_board):
        return {(y, x) for y, x in {(y_pos + 1, x_pos), (y_pos - 1, x_pos), (y_pos, x_pos + 1), (y_pos, x_pos - 1)} if
                on_board(y, x) and (y, x) != self.den and board[y][x] != water and (
                        pieces_board[y][x] == empty or (
                        (captures(piece, pieces_board[y][x]) or board[y][x] == trap) and pieces_board[y][x] not in self.pieces and board[y_pos][x_pos] != trap))}

    def rat_moves(self, piece, y_pos, x_pos, pieces_board):
        return {(y, x) for y, x in {(y_pos + 1, x_pos), (y_pos - 1, x_pos), (y_pos, x_pos + 1), (y_pos, x_pos - 1)} if on_board(y, x) and (y, x) != self.den and (
                pieces_board[y][x] == empty or (
                (captures(piece, pieces_board[y][x]) or board[y][x] == trap) and pieces_board[y][x] not in self.pieces and board[y_pos][x_pos] not in {water, trap}))}

    def tiger_lion_moves(self, piece, y_pos, x_pos, pieces_board):
        if (y_pos, x_pos) not in self.tiger_lion_in_water:
            a =  {(y, x) for y, x in {(y_pos + 1, x_pos), (y_pos - 1, x_pos), (y_pos, x_pos + 1), (y_pos, x_pos - 1)} if on_board(y, x) and (y, x) != self.den and (
                    pieces_board[y][x] == empty or (
                    (captures(piece, pieces_board[y][x]) or board[y][x] == trap) and pieces_board[y][x] not in self.pieces and board[y_pos][x_pos] != trap))}
            return a
        else:
            dy, dx = self.tiger_lion_in_water[(y_pos, x_pos)]
            while board[y_pos][x_pos] == water:
                if pieces_board[y_pos][x_pos] in {rat0, rat1}:
                    return set()
                y_pos, x_pos = y_pos + dy, x_pos + dx
            b = {(y_pos, x_pos)} if pieces_board[y_pos][x_pos] == empty or (
                    (captures(piece, pieces_board[y_pos][x_pos]) or board[y_pos][x_pos] == trap) and pieces_board[y_pos][x_pos] not in self.pieces) else set()
            return b

    def moves(self, pieces, pieces_board):
        return {piece: self.piece_to_moves_generator.get(piece, self.standard_moves)(piece, *pieces[piece], pieces_board) for piece in pieces}

def dpcp(matrix):
    return [list(row) for row in matrix]

class Agent(Player):
    def __init__(self, den, pieces):
        super().__init__(den, pieces)

    def play(self, pieces, pieces_board):
        possibilities = self.moves(pieces, pieces_board)
        possibilities = sum(([(piece, pos) for pos in possibilities[piece]] for piece in pieces), [])
        if not possibilities:
            return None, (None, None)

        quality = {}  # (piece, pos) -> wins/loses

        moves = 0
        while moves < N:
            piece,pos = choice(possibilities)
            quality[(piece, pos)] = quality.get((piece,pos), 0)
            player0, player1 = RandomPlayer(den_0, get_pieces_0()), RandomPlayer(den_1, get_pieces_1())
            if self.den == den_1:
                player0, player1 = player1, player0
            result,m = play(RandomPlayer(self.den, get_pieces_0()), RandomPlayer(den_1, get_pieces_1()), dpcp(pieces_board), mcts=True)
            moves += m

            if result == (0 if self.den == den_0 else 1):
                quality[(piece, pos)] += 1

        move = max(quality, key = lambda x: quality.get(x, 0))
        return move


class RandomPlayer(Player):
    def play(self, pieces, pieces_board):
        possibilities = self.moves(pieces, pieces_board)
        possibilities = sum(([(piece, pos) for pos in possibilities[piece]] for piece in pieces), [])

        if possibilities:
            return choice(possibilities)
        else:
            return None, (None, None)


def den_manhattan_distance(friendly_den, pieces, pieces_board, piece, pos):
    den = den_0 if friendly_den == den_1 else den_1
    return manhattan_distance(*pos, *den)


class HeuristicAgent(Player):
    def __init__(self, den, pieces, heuristic):
        super().__init__(den, pieces)
        self.heuristic = heuristic

    def play(self, pieces, pieces_board):
        possibilities = self.moves(pieces, pieces_board)
        possibilities = sum(([(piece, pos) for pos in possibilities[piece]] for piece in pieces), [])

        if possibilities:
            return min(possibilities, key = lambda x: self.heuristic(self.den, pieces, pieces_board, *x))
        else:
            return None, (None, None)


def move(piece, y, x, pieces0, pieces1, pieces_board):
    if piece in pieces0:
        old_y, old_x = pieces0[piece]
        pieces_board[old_y][old_x] = empty
        pieces0[piece] = y, x
        pieces_board[y][x] = piece
        pieces1 = {piece: pos for piece, pos in pieces1.items() if pos != (y, x)}
    else:
        old_y, old_x = pieces1[piece]
        pieces_board[old_y][old_x] = empty
        pieces1[piece] = y, x
        pieces_board[y][x] = piece
        pieces0 = {piece: pos for piece, pos in pieces0.items() if pos != (y, x)}

    return pieces0, pieces1, pieces_board


def manhattan_distance(y0, x0, y1, x1):
    return abs(y0 - y1) + abs(x0 - x1)


def determine_winner(player0, player1, pieces0, pieces1, pieces_board):
    for piece_0, piece_1 in zip(reversed(pieces_0), reversed(pieces_1)):
        if piece_0 in pieces0.keys() and piece_1 not in pieces1.keys():
            return 0
        if piece_1 in pieces1.keys() and piece_0 not in pieces0.keys():
            return 1

    dists0 = tuple(sorted(manhattan_distance(*pos, *player1.den) for pos in pieces0.values()))
    dists1 = tuple(sorted(manhattan_distance(*pos, *player0.den) for pos in pieces1.values()))
    return dists0 > dists1 if dists0 != dists1 else 1
    #lexicographical order


def play(player0, player1, pieces_board, mcts = False):
    pieces0, pieces1 = get_pieces_0(), get_pieces_1()
    turns_without_capture = 0
    player0turn = True

    moves = 0
    while not mcts or moves < N:
        piece, (y, x) = player0.play(pieces0, pieces_board) if player0turn else player1.play(pieces1, pieces_board)
        moves += 1

        if not piece:
            turns_without_capture += 1

            if turns_without_capture >= 50:
                return (determine_winner(player0, player1, pieces0, pieces1, pieces_board), moves)

            player0turn = not player0turn
            continue

        if board[y][x] == den:
            return (0 if player0turn else 1,moves)

        new_pieces_0, new_pieces_1, pieces_board = move(piece, y, x, pieces0, pieces1, pieces_board)

        if not new_pieces_0:
            return (1,moves)
        elif not new_pieces_1:
            return (0, moves)
        elif len(new_pieces_0) + len(new_pieces_1) == len(pieces0) + len(pieces1):
            turns_without_capture += 1

            if turns_without_capture >= 50:
                return (determine_winner(player0, player1, pieces0, pieces1, pieces_board), moves)
        else:
            turns_without_capture = 0

        pieces0, pieces1 = new_pieces_0, new_pieces_1

        player0turn = not player0turn
    return (0, N)


def play_default(player0, player1):
    return play(player0, player1, get_pieces_board())[0]


def play_agent_vs_random():
    return play_default(Agent(den_0, get_pieces_0()), RandomPlayer(den_1, get_pieces_1()))


def play_heuristic_vs_agent(heuristic):
    return play_default(HeuristicAgent(den_0, get_pieces_0(), heuristic), Agent(den_1, get_pieces_1()))


def test_n(n):
    lost = 0

    for i in range(1,n+1):
        lost += play_agent_vs_random()
        #lost += play_heuristic_vs_agent(den_manhattan_distance)

        #function play_agent_vs_random() is from assignment p4.2
        #function play_heuristic_vs_agent is from p4.3
        print(lost, i)

test_n(10)
