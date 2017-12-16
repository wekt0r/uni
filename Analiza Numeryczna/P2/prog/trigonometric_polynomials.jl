#author: Wiktor Garbarek

module WGTrigonometricPoly
export TrigonometricPoly, derivative, value

type TrigonometricPoly
    cs
    ss
end

function derivative(t::TrigonometricPoly)
    new_ss = [0]
    new_cs = [0]
    for i in 2:1:max(length(t.cs),length(t.ss));
        push!(new_ss, -t.cs[i]/(i-1))
        push!(new_cs, t.ss[i]/(i-1))
    end
    return TrigonometricPoly(new_cs, new_ss)
end

function value(t::TrigonometricPoly, x)
    v = t.cs[1] + t.ss[1]
    for i in 2:1:max(length(t.cs), length(t.ss))
        v += t.cs[i]*cos((i-1)x) + t.ss[i]*sin((i-1)x)
    end
    return v
end

end
