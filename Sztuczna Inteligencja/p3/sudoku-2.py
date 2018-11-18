import sys

file = open("sudoku.pl", "w+")

def V(i,j):
    return 'V%d_%d' % (i,j)

def domains(Vs):
    return [ q + ' in 1..9' for q in Vs ]

def all_different(Qs):
    return 'all_distinct([' + ', '.join(Qs) + '])'

def get_column(j):
    return [V(i,j) for i in range(9)]

def get_raw(i):
    return [V(i,j) for j in range(9)]

def horizontal():
    return [ all_different(get_raw(i)) for i in range(9)]

def vertical():
    return [all_different(get_column(j)) for j in range(9)]

def get_3x3(i,j):
    return [V(j+dj, i+di) for dj in [0, 1, 2] for di in [0, 1, 2]]

def all_3x3s():
    return [ all_different(get_3x3(i,j)) for i in [0, 3, 6] for j in [0, 3, 6]]


def print_constraints(Cs, indent, d):
    position = indent
    file.write((indent - 1) * ' ')
    for c in Cs:
        file.write(c + ',')
        position += len(c)
        if position > d:
            position = indent
            file.write('\n')
            file.write( (indent - 1) * ' ')

def formatOutput():
    file.write("""formatOutput([]) :- !.
    formatOutput(X) :-
    [H1,H2,H3,H4,H5,H6,H7,H8,H9|T] = X,
    write([H1, H2, H3, H4, H5, H6, H7, H8, H9]),
    write('\\n'),
    formatOutput(T).""")

def sudoku(assigments):
    variables = [ V(i,j) for i in range(9) for j in range(9)]

    file.write(':- use_module(library(clpfd)).')
    file.write('\n')
    file.write('solve([' + ', '.join(variables) + ']) :- ')

    cs = domains(variables) + vertical() + horizontal() + all_3x3s() #here
    for i,j,val in assigments:
        cs.append( '%s #= %d' % (V(i,j), val) )

    print_constraints(cs, 4, 70),
    file.write('\n')
    file.write('    labeling([ff], [' +  ', '.join(variables) + ']).')
    file.write('\n')

    file.write('\n')
    formatOutput()
    file.write('\n')
    file.write(':- solve(X), formatOutput(X), nl.')

if __name__ == "__main__":
    raw = 0
    triples = []

    for x in sys.stdin:
        x = x.strip()
        if len(x) == 9:
            for i in range(9):
                if x[i] != '.':
                    triples.append( (raw,i,int(x[i])) )
            raw += 1
            if raw == 9:
                break
    sudoku(triples)

file.close()

"""
89.356.1.
3...1.49.
....2985.
9.7.6432.
.........
.6389.1.4
.3298....
.78.4....
.5.637.48

53..7....
6..195...
.98....6.
8...6...3
4..8.3..1
7...2...6
.6....28.
...419..5
....8..79

3.......1
4..386...
.....1.4.
6.924..3.
..3......
......719
........6
2.7...3..
"""
