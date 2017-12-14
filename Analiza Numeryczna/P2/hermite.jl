include("hermite2.jl")
using interpolation
testcase1 = bs_HermiteNewton([-1,0,1], [3,3,3], [(2,-8,56),(1,0,0),(2,8,56)])
testpoly = NewtonPoly(testcase1, [-1,-1,-1,0,0,0,1,1,1])
result = NewtonToPower(testpoly)

my_zip(xs,ys) = [(xs[i],ys[i]) for i in 1:1:max(length(xs),length(ys))]

#runge
f(x) = 1./(1+25.*x.^2)
df(x) = -50x./(1+25.*x.^2).^2
nodes = [-1,-0.6, -0.2, 0.2, 0.6, 1]
one = NewtonToPower(NewtonPoly(newton1(6, nodes, f.(nodes)), nodes))
print("(((((())))))")
two = NewtonToPower(NewtonPoly(bs_HermiteNewton(nodes, [2,2,2,2,2,2], my_zip(f.(nodes), df.(nodes))), [-1,-1,-0.6,-0.6, -0.2,-0.2, 0.2,0.2, 0.6,0.6, 1,1]))

domain = linspace(-1,1,1000)
trace1 = [
"x" => domain
"y" => one.(domain)
]
trace2 = [
"x" => domain
"y" => two.(domain)
]
data = [trace1, trace2]
response = Plotly.plot(domain, one.(domain))


function testf(f,df,ddf,dddf):
    nodes_norm = linspace(-1,1,4N)
    nodes_hermite = linspace(-1,1,N)
