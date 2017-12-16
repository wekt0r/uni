include("utilities.jl")

module WGPolyTesting
export horner, generate_polynomial_for_hermite, run_polytest, chebyshev_nodes

using WGUtilities

function horner( a, z )
    n   = length(a)
    p   = a[n-2] + z*(a[n-1] + z*a[n])
    dp  = a[n-1] + 2*z*a[n]
    ddp = a[n]
    dddp = zero( z )
    for k in n-3:-1:1;
        dddp = ddp + z*dddp
        ddp = dp   + z*ddp
        dp  = p    + z*dp
        p   = a[k] + z*p
    end
    return p, dp, ddp*2, dddp*6
end
chebyshev_nodes(n) = [cos((BigFloat(2*i-1)pi)/(2*n)) for i in 1:1:n]

function generate_polynomial_for_hermite(hnodes, cnodes,degree_list, coeffs_list)
    degree = rand(degree_list)
    coeffs = [rand(coeffs_list) for i in 0:1:degree]
    #Hermite
    msh = [2 for i in hnodes]
    ysh = [horner(coeffs, x) for x in hnodes]
    #Newton
    ysc = [horner(coeffs, x)[1] for x in cnodes]
    return [coeffs, [hnodes,msh,ysh], [cnodes,ysc]]
end

function run_polytest(N1,nodes_type="equally_spaced")
    AMOUNT1 = 200
    DEGREE1list = 2*N1:1:(2*N1+10);
    if nodes_type == "chebyshev"
        NODES1hermite = chebyshev_nodes(N1)
        NODES1classic = chebyshev_nodes(2*N1)
    else
        NODES1hermite = linspace(BigFloat(-1),BigFloat(1),N1)
        NODES1classic = linspace(BigFloat(-1),BigFloat(1),2*N1)
    end

    COEFFS1list = linspace(BigFloat(-4),BigFloat(4),100)

    domain = linspace(BigFloat(-1),BigFloat(1), 100) #more points makes program much slower
    hermite_errors = Dict()
    newton_errors = Dict()
    hermite_errors_list = []
    newton_errors_list = []

    testcase = generate_polynomial_for_hermite(NODES1hermite, NODES1classic,DEGREE1list, COEFFS1list)
    hermite = get_hermite_NewtonPoly(testcase[2]...)
    newton = get_NewtonPoly(testcase[3]...)
    for x in domain
        hermite_errors[x] = [abs(horner(testcase[1],x)[1] - newtonPolyval(hermite, x))]
        newton_errors[x] = [abs(horner(testcase[1],x)[1] - newtonPolyval(newton, x))]
    end
    for i in 1:1:99;
        testcase = generate_polynomial_for_hermite(NODES1hermite, NODES1classic,DEGREE1list, COEFFS1list)
        hermite = get_hermite_NewtonPoly(testcase[2]...)
        newton = get_NewtonPoly(testcase[3]...)
        for x in domain
            push!(hermite_errors[x], abs(horner(testcase[1],x)[1] - newtonPolyval(hermite, x)))
            push!(newton_errors[x],  abs(horner(testcase[1],x)[1] - newtonPolyval(newton, x)))
        end
    end

    for x in domain
        push!(hermite_errors_list, mean(hermite_errors[x]))
        push!(newton_errors_list, mean(newton_errors[x]))
    end
    return hermite_errors_list, newton_errors_list
end
#save("polynomial_tests_errors.jld", "hermite", hermite_errors, "newton", newton_errors)
end
