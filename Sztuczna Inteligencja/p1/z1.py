from collections import namedtuple
from copy import copy
from queue import Queue

tests = """white h6 a4 d4
black b4 f3 e8
white a1 e3 b7
black h7 a2 f2
black a2 e4 a4
black g8 h1 c4
white b4 f4 d7""".split("\n")

def king_moves(i,j):
    return [(i+di, j+dj) for di in [-1,0,1] for dj in [-1,0,1] if (di != 0 or dj != 0) and 8 > i+di >= 0 and 8 > j + dj >= 0]

def rook_moves(i,j, other):
    x,y = other
    return ([(i,k) for k in (range(0,8) if x!=i else range(0 if y > j else y+1, 8 if y < j else y)) if k != j ] +
            [(k,j) for k in (range(0,8) if y!=j else range(0 if x > i else x+1, 8 if x < i else x)) if k != i ])
    #rook cannot jump over other figures, so we check if white king doesnt stand on our way
    #we dont need to check black king because it would be check-mate if it didnt move earlier

def parse_input(sentence):
    print(sentence.split(" "))
    next_turn, wk, wr, bk = sentence.split(" ")
    def parse_position(letter_number):
        return ord(letter_number[0]) - 97, int(letter_number[1]) - 1

    return next_turn, {"wk": parse_position(wk),
                       "wr": parse_position(wr),
                       "bk": parse_position(bk)}

def is_check_white(bkx, bky, wkx, wky):
    return (wkx, wky) in king_moves(bkx, bky)

def is_check(bkx, bky, wkx, wky, wrx, wry):
    return (bkx,bky) in rook_moves(wrx,wry, (wkx,wky)) or (bkx,bky) in king_moves(wkx, wky) #king_moves and rook_moves - by excluding +0,+0 move excludes

def is_check_mate(bkx,bky,wkx,wky,wrx,wry):
    return is_check(bkx, bky, wkx, wky, wrx, wry) and all(is_check(x,y, wkx, wky, wrx, wry) for x,y in king_moves(bkx, bky))

def solve(turn, figures):
    return _solve(turn, *figures["bk"], *figures["wk"], *figures["wr"], 0)

def _solve(turn_begin, bkx, bky, wkx, wky, wrx, wry, no_of_moves):
    queue = Queue()
    queue.put((no_of_moves, [turn_begin, bkx, bky, wkx, wky, wrx, wry, []]))
    already_visited = set()
    while True:
        no_of_moves, [turn, bkx, bky, wkx, wky, wrx, wry, moves] = queue.get_nowait()
        if (turn, bkx, bky, wkx, wky, wrx, wry) not in already_visited:
            moves.append((bkx,bky,wkx,wky,wrx,wry))
            if is_check_mate(bkx, bky, wkx, wky, wrx, wry):
                return no_of_moves, moves
            already_visited.add((turn, bkx, bky, wkx, wky, wrx, wry))
            if turn == "black":
                possible_moves = [turntmp for turntmp in king_moves(bkx,bky) if not is_check(*turntmp, wkx, wky, wrx, wry)]
                for turntmp in possible_moves:
                    queue.put((no_of_moves+1, ["white", *turntmp, wkx, wky, wrx, wry, copy(moves)]))
            if turn == "white":
                possible_moves_for_king = [turntmp for turntmp in king_moves(wkx,wky) if not is_check_white(bkx,bky, *turntmp)]
                for turntmp in possible_moves_for_king:
                    queue.put((no_of_moves+1,["black", bkx, bky, *turntmp, wrx, wry, copy(moves)]))
                for turntmp in rook_moves(wrx, wry, (wkx, wky)):
                    queue.put((no_of_moves+1,["black", bkx, bky, wkx, wky, *turntmp, copy(moves)]))

def solution(inp):
    return solve(*parse_input(inp))

with open("zad1_input.txt") as f:
    tests = f.read().split("\n")
with open("zad1_output.txt", mode='w') as f:
    for test in tests:
        if test:
            f.write(str(solution(test)[0]))

for test,sol in [("white h6 a4 d4",9), ("black g8 h1 c4",10)]:
    print("result {} should be {}".format(solution(test)[0], sol))
