#now working
#author: Wiktor Garbarek
module interpolation
export newton1, bs_HermiteNewton, NewtonPoly, NewtonPolyval, NewtonToPower, bslin_HermiteNewton
using Polynomials

function newton1(n, xs, ys)
    bs = hcat(xs,ys)
    print(bs)
    for i in 3:1:(n+1);
        bs = hcat(bs, vcat([(bs[j+1, i-1] - bs[j, i-1])/(bs[j+i-2, 1] - bs[j, 1]) for j in 1:1:(n-(i-2)) ], [nothing for j in 1:1:(i-2)]) )
    end
    return [bs[1,i] for i in 2:1:(n+1)]
end

function newton(n, xs, ys)
    bs = hcat(xs,ys)
    print(bs)
    for i in 3:1:(n+1);
        bs = hcat(bs, vcat([nothing for j in 1:1:(i-2) ],
                        [(bs[j, i-1] - bs[j-1, i-1])/(bs[j,1] - bs[j-i+2, 1]) for j in (i-1):1:n ]))
    end
    return bs
end

function bs_HermiteNewton(xs, ms, ys)
    n = sum(ms)
    col1bs = vcat([ repmat([xm[1]], xm[2]) for xm in zip(xs,ms)]...)
    col2bs = vcat([ repmat([ym[1][1]], ym[2]) for ym in zip(ys,ms)]...)

    xsDict = Dict(zip(xs,ys))
    function diff_quotient(i, j)
        if bs[j+i-2, 1] == bs[j,1]
            return xsDict[col1bs[j]][i-1]/factorial(i-2)
        end
        return (bs[j+1, i-1] - bs[j, i-1])/(bs[j+i-2, 1] - bs[j, 1])
    end

    bs = hcat(col1bs, col2bs)
    for i in 3:1:(n+1);
        bs = hcat(bs, vcat([ diff_quotient(i,j) for j in 1:1:(n-(i-2)) ], [nothing for j in 1:1:(i-2)]) )
    end
    return [bs[1,i] for i in 2:1:(n+1)]
end

function bslin_HermiteNewton(xs, ms, ys)
    n = sum(ms)
    col1bs = vcat([ repmat([xm[1]], xm[2]) for xm in zip(xs,ms)]...)
    bs = vcat([ repmat([ym[1][1]], ym[2]) for ym in zip(ys,ms)]...)

    xsDict = Dict(zip(xs,ys))
    function diff_quotient(i, j)
        if bs1[j] == bs1[j-i+1]
            return xsDict[col1bs[j]][i]/factorial(i-1)
        end
        return (bs[j] - bs[j-1])/(bs1[j] - bs1[j-i+1])
    end
    for i in 2:1:n+1;
        for j in n+1:-1:i;
            bs[j] = diff_quotient(i,j)
        end
    end
    return bs

end

type NewtonPoly
    bs::Array{Float64} # b0, b1, b2, ..., b_n
    xs::Array{Float64} # x0, x1, x2, ..., x_n
end

function NewtonToPower(w::NewtonPoly)
    n = length(w.bs)
    a = similar(w.bs)
    a[n] = w.bs[n]
    for k in n-1:-1:1;
        a[k] = w.bs[k] - a[k+1]*w.xs[k]
        for i in k+1:n-1;
            a[i] -= a[i+1]*w.xs[k]
        end
    end
    print(a)
    return Polynomials.Poly(a)
end

function NewtonPolyval(w::NewtonPoly,x::Float64)
    #not yet working
    v = w.bs[end]
    for k in (length(w.bs)-1):1:0;
        v = v*(x-w.xs[k]) + w.bs[k]
    end
    return v
end


end
