import sys, os, subprocess
result = ""

def B(i,j):
    return 'B_{}_{}'.format(i,j)

def domains(Bs):
    return [ q + ' in 0..1' for q in Bs ]

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

def storms(rows, cols, triples):
    global result
    R = len(rows)
    C = len(cols)

    def row(row_constraint, i):
        return " + ".join(B(i,j) for j in range(C)) + ' #= {}'.format(row_constraint)

    def column(column_constraint, j):
        return " + ".join(B(i,j) for i in range(R)) + " #= {}".format(column_constraint)

    def _1x3_rects(i,j): #makes 2x2 size assured
        return ("({} #= 1) #==> ({} + {} #> 0), ".format(B(i,j), B(i-1,j), B(i+1,j))
                + "({} #= 1) #==> ({} + {} #> 0)".format(B(i,j), B(i,j-1), B(i,j+1)))

    def _2x2_rects(i,j): #makes corners assured
        return ("({} + {} #= 2) #<==> ({} + {} #=2)".format(B(i,j), B(i+1,j+1), B(i+1,j), B(i, j+1)) )

    bs = [ B(i,j) for i in range(R) for j in range(C)]
    result += (':- use_module(library(clpfd)).\n')
    result += ('solve([' + ', '.join(bs) + ']) :- \n')


    cs = domains(bs)   #TODO: too weak contraints, add something!
    for i,row_constraint in enumerate(rows):
        cs.append(row(row_constraint, i))

    for j,col_con in enumerate(cols):
        cs.append(column(col_con, j))

    for i,j,val in triples:
        cs.append( '%s #= %d' % (B(i,j), val) )

    for i in range(1,R-1):
        for j in range(1, C-1):
            cs.append(_1x3_rects(i,j))

    for i in range(R-1):
        for j in range(C-1):
            cs.append(_2x2_rects(i,j))

    print_constraints(cs, 4, 70)
    result += "\n"
    result += ('    labeling([ff], [' +  ', '.join(bs) + ']).')
    result += "\n"
    result += (':- solve(X), write(X), nl.')



tests = [
"""
4 4 0 5 5 5
5 5 3 5 5 0
5 5 0
""",
"""
3 8 5 3 3 5 5 5 2 2
0 2 7 7 2 2 0 7 7 7
0 5 0
0 6 0
1 5 1
1 6 0
""",
"""
2 2 7 7 4 4 3 5 2 8 8 8 8 6 0
4 4 6 6 2 9 9 9 2 0 2 7 7 7 0
13 10 0
13 11 1
14 10 0
14 11 0
3 0 1
3 1 1
4 0 1
4 1 1
3 13 0
3 14 0
4 13 1
4 14 0
9 4 0
9 5 1
10 4 0
10 5 1
2 1 1
2 2 0
3 1 1
3 2 0
""",
"""
4 4 12 10 8 0 8 11 8 7 11 7 7 5 0
10 10 3 9 9 3 8 8 5 4 10 6 9 5 3
13 11 1
13 12 1
14 11 0
14 12 0
3 9 1
3 10 1
4 9 0
4 10 0
2 0 1
2 1 1
3 0 0
3 1 0
11 13 0
11 14 0
12 13 0
12 14 0
7 6 1
7 7 1
8 6 1
8 7 1
""",
"""
11 11 3 5 5 11 8 8 10 8 6 4 0 7 12 7 7 7
0 5 9 9 9 4 8 10 9 11 6 4 13 13 10 7 3 0
2 1 0
2 2 0
3 1 0
3 2 0
3 3 0
3 4 0
4 3 0
4 4 0
13 1 0
13 2 1
14 1 0
14 2 1
15 1 0
15 2 0
16 1 0
16 2 0
1 3 1
1 4 1
2 3 0
2 4 0
15 5 0
15 6 0
16 5 0
16 6 0
14 10 0
14 11 1
15 10 0
15 11 1
0 2 1
0 3 1
1 2 1
1 3 1
9 2 1
9 3 1
10 2 0
10 3 0
7 13 0
7 14 0
8 13 0
8 14 0
"""

]

if __name__ == "__main__":
    counter = 1
    for test in tests:
        test = test.split("\n")[1:-1]
        #print(test)
        rows = [int(c) for c in test[0].strip().split(" ")]
        columns = [int(c) for c in test[1].strip().split(" ")]
        #print(test[2].strip().split(" "))
        already_set = [tuple([int(t) for t in triple.strip().split(" ")])  for triple in test[2:]]
        storms(rows,columns,already_set)
        with open("solution{}.pl".format(counter), mode='w') as f:
            f.write(result)
        result = ""
        subprocess.getoutput('swipl -c solution{}.pl > prolog_output_result{}.txt'.format(counter,counter))
        diff = subprocess.getoutput("diff prolog_output_result{}.txt answer{}".format(counter, counter))
        if diff:
            print("Wrong answer on case {} - diff {}".format(counter, diff))
        else:
            print("Case {} OK".format(counter))
        counter += 1
