module WGTrigTesting
export generate_trigpoly_for_hermite, run_trigtest

include("trigonometric_polynomials.jl")
importall WGTrigonometricPoly

function generate_trigpoly_for_hermite(hnodes, cnodes, degree_list, coeffs_list)
    degree = rand(degree_list)
    cos_coeffs = [rand(coeffs_list) for i in 0:1:degree]
    degree = rand(degree_list)
    sin_coeffs = [rand(coeffs_list) for i in 0:1:degree]
    tp = TrigonometricPoly(cos_coeffs, sin_coeffs)
    #Hermite
    msh = [2 for i in hnodes]
    ysh = [(value(tp, x),value(derivative(tp),x)) for x in hnodes]
    #Newton
    ysc = [value(tp, x) for x in cnodes]
    return [tp, [hnodes,msh,ysh], [cnodes,ysc]]
end

function run_trigtest(N1, nodes_type="equally_spaced")
    AMOUNT1 = 200
    DEGREE1list = N1:1:(2*N1+10);
    if nodes_type == "chebyshev"
        NODES1hermite = chebyshev_nodes(N1)
        NODES1classic = chebyshev_nodes(2*N1)
    else
        NODES1hermite = linspace(BigFloat(-1),BigFloat(1),N1)
        NODES1classic = linspace(BigFloat(-1),BigFloat(1),2*N1)
    end
    COEFFS1list = linspace(BigFloat(-5),BigFloat(5),100)
    domain = linspace(BigFloat(-1),BigFloat(1), 100) #more points makes program much slower
    hermite_errors = Dict()
    newton_errors = Dict()
    hermite_errors_list = []
    newton_errors_list = []

    testcase = generate_trigpoly_for_hermite(NODES1hermite, NODES1classic,DEGREE1list, COEFFS1list)
    hermite = get_hermite_NewtonPoly(testcase[2]...)
    newton = get_NewtonPoly(testcase[3]...)
    for x in domain
        hermite_errors[x] = [abs(value(testcase[1],x) - newtonPolyval(hermite, x))]
        newton_errors[x] = [abs(value(testcase[1],x) - newtonPolyval(newton, x))]
    end
    for i in 1:1:99;
        testcase = generate_polynomial_for_hermite(NODES1hermite, NODES1classic,DEGREE1list, COEFFS1list)
        hermite = get_hermite_NewtonPoly(testcase[2]...)
        newton = get_NewtonPoly(testcase[3]...)
        for x in domain
            push!(hermite_errors[x], abs(value(testcase[1],x)[1] - newtonPolyval(hermite, x)))
            push!(newton_errors[x],  abs(value(testcase[1],x)[1] - newtonPolyval(newton, x)))
        end
    end

    for x in domain
        push!(hermite_errors_list, mean(hermite_errors[x]))
        push!(newton_errors_list, mean(newton_errors[x]))
    end
    return hermite_errors_list, newton_errors_list
end

end
