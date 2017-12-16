module WGUtilities
export NewtonPoly, newtonPolyval, newtonToPower, get_hermite_NewtonPoly, get_NewtonPoly

include("hermite_interpolation.jl")
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

function newtonToPower(w::NewtonPoly) #only to check whether hermite_newton interpolation works
    n = length(w.bs)
    a = similar(w.bs)
    a[n] = w.bs[n]
    for k in n-1:-1:1;
        a[k] = w.bs[k] - a[k+1]*w.xs[k]
        for i in k+1:n-1;
            a[i] -= a[i+1]*w.xs[k]
        end
    end
    return a # => a[1] + a[2]x + a[3]x^2 + ... a[p]x^(p-1)
end

function get_hermite_NewtonPoly(xs,ms,ys)
    return NewtonPoly(hermite_newton(xs,ms,ys), vcat([ repmat([xm[1]], xm[2]) for xm in zip(xs,ms)]...))
end

function get_NewtonPoly(xs,ys)
    return get_hermite_NewtonPoly(xs, [1 for x in xs], [(y,) for y in ys])
end

end
