import sys, os, subprocess
result = ""

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
    return [ all_different(get_column(j)) for j in range(9)]

def get_3x3(i,j):
    return [V(j+dj, i+di) for dj in [0, 1, 2] for di in [0, 1, 2]]

def all_3x3s():
    return [ all_different(get_3x3(i,j)) for i in [0, 3, 6] for j in [0, 3, 6]]

def print_constraints(Cs, indent, d):
    global result
    position = indent
    result += ((indent - 1) * ' ')
    for c in Cs:
        result += c + ','
        position += len(c)
        if position > d:
            position = indent
            result += "\n"
            result += ((indent - 1) * ' ')


def sudoku(assigments):
    global result
    variables = [ V(i,j) for i in range(9) for j in range(9)]

    result += (':- use_module(library(clpfd)).\n')
    result += ('solve([' + ', '.join(variables) + ']) :- \n')


    cs = domains(variables) + vertical() + horizontal() + all_3x3s() #TODO: too weak contraints, add something!
    for i,j,val in assigments:
        result += '%s #= %d'.format(V(i,j), val)

    print_constraints(cs, 4, 70)
    result += "\n"
    result += ('    labeling([ff], [' +  ', '.join(variables) + ']).')
    result += "\n"
    result += (':- solve(X), write(X), nl.')



tests = ["""
89.356.1.
3...1.49.
....2985.
9.7.6432.
.........
.6389.1.4
.3298....
.78.4....
.5.637.48
""",
"""
53..7....
6..195...
.98....6.
8...6...3
4..8.3..1
7...2...6
.6....28.
...419..5
....8..79
""",
"""
3.......1
4..386...
.....1.4.
6.924..3.
..3......
......719
........6
2.7...3..
948632157
"""]

if __name__ == "__main__":
    raw = 0
    triples = []
    counter = 1
    for test in tests:
        for x in test:
            x = x.strip()
            if len(x) == 9:
                for i in range(9):
                    if x[i] != '.':
                        triples.append( (raw,i,int(x[i])) )
                raw += 1
        sudoku(triples)
        with open("solution{}.pl".format(counter), mode='w') as f:
            f.write(result)
        result = ""
        #os.system('swipl solution{}.pl >> prolog_output_result{}.txt'.format(counter,counter))
        counter += 1
