#author: Wiktor Garbarek

module DoubleIntegralMonteCarlo
export monte_carlo

function average_monte_carlo(f,a,b,c,d,max,n, tries)
    return mean([monte_carlo(f,a,b,c,d,max,n) for i in 1:1:tries])
end

function monte_carlo(f,a,b,c,d,max,n) # works when for all x,y in [a,b]x[c,d] f(x,y) >= 0
    integral = 0
    for i in 1:1:n;
        x,y,z = rand()*(b-a) + a, rand()*(d-c) + c, rand()*max
        if f(x,y) >= z
            integral += 1
        end
    end
    return (integral/n) * (b-a)*(d-c)*max
end

end
