#author: Wiktor Garbarek

module WGHermiteInterpolation
export hermite_newton

function hermite_newton(xs, ms, ys)
    n = sum(ms)
    bs1 = vcat([ repmat([xm[1]], xm[2]) for xm in zip(xs,ms)]...)
    bs = vcat([ repmat([BigFloat(ym[1][1])], ym[2]) for ym in zip(ys,ms)]...)
    xsDict = Dict(zip(xs,ys))
    function diff_quotient(i, j)
        if bs1[j] == bs1[j-i+1]
            return xsDict[bs1[j]][i]/factorial(i-1)
        end
        return (bs[j] - bs[j-1])/(bs1[j] - bs1[j-i+1])
    end
    for i in 2:1:n+1;
        for j in n:-1:i;
            bs[j] = diff_quotient(i,j)
        end
    end
    return bs

end

function hermite_newton_in_quadratic_memory(xs, ms, ys)
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

# for newton interpolation we can of course use hermite interpolation algorithm for ms = [1,1,1,...,1]

end
