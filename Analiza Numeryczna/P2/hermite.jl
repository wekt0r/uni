include("doc/hermite2.jl")
using interpolation
testcase1 = bs_HermiteNewton([-1,0,1], [3,3,3], [(2,-8,56),(1,0,0),(2,8,56)])
testpoly = NewtonPoly(testcase1, [-1,-1,-1,0,0,0,1,1,1])
result = NewtonToPower(testpoly)
