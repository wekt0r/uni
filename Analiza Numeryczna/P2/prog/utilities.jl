include("hermite_interpolation.jl")

module WGUtilities
export NewtonPoly, newtonPolyval, get_hermite_NewtonPoly, get_NewtonPoly

using WGHermiteInterpolation: hermite_newton

type NewtonPoly
    bs # b0, b1, b2, ..., b_n
    xs # x0, x1, x2, ..., x_n
end

function newtonPolyval(w::NewtonPoly, x)
    n = length(w.bs)
    v = w.bs[n]
    for k in (n-1):(-1):1;
        v = v*(x-w.xs[k]) + w.bs[k]
    end
    return v
end

function get_hermite_NewtonPoly(xs,ms,ys)
    return NewtonPoly(hermite_newton(xs,ms,ys), vcat([ repmat([xm[1]], xm[2]) for xm in zip(xs,ms)]...))
end

function get_NewtonPoly(xs,ys)
    return get_hermite_NewtonPoly(xs, [1 for x in xs], [(y,) for y in ys])
end

end
