#author: Wiktor Garbarek

module WGTrigonometricPoly
export TrigonometricPoly, derivative, value

type TrigonometricPoly
    cs
    ss
end

function derivative(t::TrigonometricPoly)
    n,m = length(t.cs), length(t.ss)
    cs = vcat(t.cs, repmat([BigFloat(0)], max(m - n,0) ))
    ss = vcat(t.ss, repmat([BigFloat(0)], max(n - m,0) ))
    new_ss = [BigFloat(0)]
    new_cs = [BigFloat(0)]
    for i in 2:1:max(n,m);
        push!(new_ss, -cs[i]*(i-1))
        push!(new_cs, ss[i]*(i-1))
    end
    return TrigonometricPoly(new_cs, new_ss)
end

function value(t::TrigonometricPoly, x)
    n,m = length(t.cs), length(t.ss)
    cs = vcat(t.cs, repmat([0], max(m - n,0) ))
    ss = vcat(t.ss, repmat([0], max(n - m,0) ))
    v = t.cs[1] + t.ss[1]
    for i in 2:1:max(n, m)
        v += cs[i]*cos((i-1)x) + ss[i]*sin((i-1)x)
    end
    return v
end

end
