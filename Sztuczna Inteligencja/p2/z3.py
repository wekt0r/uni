from collections import namedtuple, deque
from queue import Queue, PriorityQueue
from functools import reduce

MOVES = [(-1, 0), (1, 0), (0, -1), (0, 1)]
DIRS = ['U','D','L','R']
move_to_dir = dict(zip(MOVES,DIRS))
dir_to_move = dict(zip(DIRS,MOVES))
State = namedtuple("State", ["board", "ki", "kj", "type", "moves"])

def long_jump_coordinates(moves):
    return reduce(lambda x,y: (x[0] + y[0], x[1] + y[1]), (dir_to_move[move] for move in moves), (0,0))

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
    return not any(row.count('B') for row in board)

def min_goal_dist(board, x, y): #min_goal_distance_for given box
    return min(abs(x - i) + abs(y - j) for i,row in enumerate(board) for j,char in enumerate(row) if char in 'G+')

def approximate_distance_to_solution(board, ki, kj):
    #a = (sum((min_goal_dist(board, i, j) for i,row in enumerate(board) for j,char in enumerate(row) if char == 'B'))
    #     + max([abs(i - ki) + abs(j - kj) for i,row in enumerate(board) for j,char in enumerate(row) if char == 'B'] + [0]))
    #return 0
    b = sum(row.count("B") for row in board)
    return b

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
        if board_o[ki+2*x][kj+2*y] not in 'WB*': #we dont have another immovable object behind
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
        if board_o[ki+2*x][kj+2*y] not in 'WB*': #we dont have another immovable object behind
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

def print_board(board):
    return "\n".join(["".join(row) for row in board])

def dpcp(board):
    return [list(row) for row in board]

def solve_best_first_search(initial_board):
    #print(print_board(initial_board))
    i,j, t = get_keeper_coordinates(initial_board)
    initial_state = State(initial_board, i, j, t, "")

    # g - to get here cost
    # h - approximate to finish from here cost
    def f(board, moves, ki, kj):
        return approximate_distance_to_solution(board, ki, kj)

    queue = PriorityQueue()
    queue.put((f(initial_board, "", i, j),initial_state))
    already_visited = set()
    while True:
        v,(board_o, kio, kjo, kto, moves) = queue.get_nowait()
        if repr(board_o) not in already_visited:
            if is_solved(board_o):
                #print("We have v = {} and moves = {} for \n {} \n {}".format(v, moves, print_board(board), print_board(initial_board)))
                return moves

            already_visited.add(repr(board_o))
            for (ki2, kj2, moves_to_box, move_i, move_j) in get_achievable_boxes(board_o, kio, kjo):
                #print(ki2, kj2, moves_to_box, move_i, move_j)
                board = dpcp(board_o)
                ki,kj,kt = kio,kjo,kto
                #for move in moves_to_box:
                if moves_to_box:
                    board, ki, kj, kt = make_move(board, ki, kj, kt, *long_jump_coordinates(moves_to_box))

                assert ki == ki2 and kj == kj2
                new_state = make_move(board, ki, kj, kt, move_i, move_j)
                if new_state:
                    new_moves = str(moves) + moves_to_box + move_to_dir[(move_i, move_j)]
                    new_board, new_ki, new_kj, new_kt = new_state
                    queue.put((f(new_board, new_moves, new_ki, new_kj),State(new_board, new_ki, new_kj, new_kt, new_moves)))

def get_achievable_boxes(board, ki, kj):
    row_length,column_length = len(board[0]), len(board)
    queue = deque()
    queue.append((ki, kj, ""))  #keeper_coords-i,j,moves
    already_visited = set()
    while queue:
        i,j, moves = queue.popleft()
        if (i,j) not in already_visited:
            already_visited.add((i,j))
            for (x,y),m in zip(MOVES,DIRS):
                if 0 <= i+x < column_length and 0 <= j+y < row_length:
                    if board[i+x][j+y] == 'W':
                        pass
                    elif board[i+x][j+y] in {'B','*'}:
                        yield (i,j,moves, x, y)
                    else:
                        queue.append((i+x, j+y, str(moves) + m))

with open("zad_output.txt", mode='w') as f:
    f.write(solve_best_first_search(board))
#from time import time
#t0 = time(); print(solve_bfs(board)); print(time() - t0)
#t0 = time(); print(solve_astar(board)); print(time() - t0)
