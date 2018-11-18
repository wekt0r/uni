import subprocess as sp
import os
import re

from functools import reduce

def _avg(l):
    return sum(l)/len(l)

def avg(l):
    return _avg(sorted(l)[1:-1]) # reject smallest and biggest

PROGRAM_CALL = {
        "transpose": "./transpose -n {} -v {}",
        "bsearch":  "./bsearch -S {} -n {} -t {} -v {}",
        "matmult": "./matmult -n {} -v {}",
        "randwalk": "./randwalk -S {} -n {} -s {} -t {} -v {}"
        }

def parse_output(output):
    #tprint(output)
    return re.findall(r'([\d|\.]*) seconds', output)[0]


def test(program, *args):
    results = [float(parse_output(sp.getoutput(PROGRAM_CALL[program].format(*args)))) for _ in range(5)]
    return avg(results)

def test_transpose():
    TEST_LIST = range(48,1000, 8)
    gnuplot = "# X\tY0\tY1\n"
    for size in TEST_LIST:
        gnuplot += "{}\t{}\t{}\n".format(size ,test("transpose", size, 0), test("transpose", size, 1))

    with open("transpose.dat", 'w') as f:
        f.write(gnuplot)

    os.system("gnuplot transpose.plt > transpose.png")

def test_matmult():
    TEST_LIST = range(1024, 3000, 512)
    gnuplot = "# X\tY0\tY1\nY2\nY3\n"
    for size in TEST_LIST:
        gnuplot += "{}\t{}\t{}\t{}\t{}\n".format(size,
                                                test("matmult", size, 0),
                                                test("matmult", size, 1),
                                                test("matmult", size, 2),
                                                test("matmult", size, 3))
    with open("matmult.dat", 'w') as f:
        f.write(gnuplot)

    os.system("gnuplot matmult.plt > matmult.png")

def test_randwalk():
    TEST_LIST = range(1, 16)
    gnuplot = "# X\tY0\tY1\n"
    for size in TEST_LIST:
        gnuplot += "{}\t{}\t{}\n".format(size,
                                      test("randwalk", "0xea3495cc76b34acc", 11, 15, size, 0),
                                      test("randwalk", "0xea3495cc76b34acc", 11, 15, size, 1))
    with open("randwalk.dat", 'w') as f:
        f.write(gnuplot)

    os.system("gnuplot randwalk.plt > randwalk.png")

def test_bsearch():
    TEST_LIST = range(15,25)
    gnuplot = "# X\tY0\tY1\n"
    for size in TEST_LIST:
        gnuplot += "{}\t{}\t{}\n".format(size,
                                      test("bsearch", "0xea3495cc76b34acc", size, 21, 0),
                                      test("bsearch", "0xea3495cc76b34acc", size, 21, 1))
    with open("bsearch.dat", 'w') as f:
        f.write(gnuplot)

    os.system("gnuplot bsearch.plt > bsearch.png")


if __name__ == "__main__":
    programs = ["transpose", "bsearch", "matmult", "randwalk"]
    program = input("Program to test: ")
    while program not in programs:
        program = input("Program to test: ")

    {"transpose":   test_transpose,
     "matmult":     test_matmult,
     "randwalk":    test_randwalk,
     "bsearch":     test_bsearch
     }[program]()
# test_transpose()
