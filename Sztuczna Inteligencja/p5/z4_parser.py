from reversi_show import *
from sklearn.externals import joblib

LEARNING_DATA_SIZE = 'bigger'
CORNER_ADJACENT = [(1,8,9), (6,14,15), (-7,-16,-15), (-2,-9,-10)]
EDGES = list(range(8)) + list(range(56,64)) + list(range(8,56,8)) + list(range(15,63,8))

EMPTY = 0
BLACK = 1
WHITE = -1

def _parse_input(entry):
    result = int(entry.split()[0])
    board = [{'_': EMPTY, '1': BLACK, '0': WHITE}[char] for char in entry.split()[1]]
    return (features(board) + board, result)

def features(board):
    #1
    def _get_balance():
        return board.count(WHITE), board.count(BLACK)
    #2
    def _get_corners():
        return [board[0], board[7], board[-8], board[-1]]

    def _get_corners_balance():
        return _get_corners().count(WHITE), _get_corners().count(BLACK)
    #3
    def _get_possible_corners():
        return [[board[c] for c in coords].count(color) if corner == EMPTY else 0
                for (corner, coords) in zip(_get_corners(), CORNER_ADJACENT)
                for color in [WHITE, BLACK]]
    #4
    def _get_edges_balance():
        return [[board[i] for i in EDGES].count(color) for color in [WHITE, BLACK]]

    #5
    def _get_number_of_moves_for_players():
        #print([[{1/2: None}.get(cell, cell) for cell in board[i:i+8]] for i in range(0,64,8)])
        game = Board([[{EMPTY: None, WHITE: 0, BLACK: 1}.get(cell, cell) for cell in board[i:i+8]] for i in range(0,64,8)])
        #print([len(game.moves(player)) for player in [WHITE, BLACK]])
        return [len(game.moves(player)) for player in [WHITE, BLACK]]


    return [*_get_balance(), *_get_corners_balance(), *_get_possible_corners(), *_get_edges_balance(), *_get_number_of_moves_for_players()]

if __name__ == "__main__":
    print("started parsing")
    with open("reversi_learning_data/{}.dat".format(LEARNING_DATA_SIZE), 'r') as f:
        data = [_parse_input(entry) for entry in f.read().split("\n") if entry]

    print("done parsing")

    joblib.dump(data,"reversi_learning_data/parsed_{}.dat".format(LEARNING_DATA_SIZE))

    print("saved")
