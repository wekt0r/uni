include("utilities.jl")

module WGFunTesting
export test_function

importall WGUtilities


function test_function(f, df, ddf, hnodes, cnodes, level)
    hermite = get_hermite_NewtonPoly(hnodes, [level for x in hnodes],[(f(x), df(x), ddf(x)) for x in hnodes])
    newton = get_NewtonPoly(cnodes, [f(x) for x in cnodes])
    return [f, hermite, newton]
end

end
