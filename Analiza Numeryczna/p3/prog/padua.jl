#author: Wiktor Garbarek
#adapted from "Padua2DM: fast interpolation
#and cubature at the Padua points in Matlab/Octave"
#M. Caliari, S. De Marchi, A. Sommariva, M. Vianello

module DoubleIntegralPadua
export padua

function padua(f,n)
    function uncurry(f)
        return t -> f(t[1],t[2])
    end

    f1 = uncurry(f)
    L1,L2 = paduaweights(n)

    return sum(L1.*f1.(Padua1(n))) + sum(L2.*f1.(Padua2(n)))
end

function paduaweights(n)
    W1,W2 = _weights1(n),_weights2(n)

    argn1 = linspace(0,pi,n+1)
    argn2 = linspace(0,pi,n+2)
    k = transpose([0:2:n;])
    l = Int((n-mod(n,2))/2+1)

    TE1 = transpose(cos.(k.*argn1[1:2:n+1]))
    TE1[2:l,:] = TE1[2:l,:]*sqrt(2)
    TO1 = transpose(cos.(k.*argn1[2:2:n+1]))
    TO1[2:l,:] = TO1[2:l,:]*sqrt(2)
    TE2 = transpose(cos.(k.*argn2[1:2:n+2]))
    TE2[2:l,:] = TE2[2:l,:]*sqrt(2)
    TO2 = transpose(cos.(k.*argn2[2:2:n+2]))
    TO2[2:l,:] = TO2[2:l,:]*sqrt(2)
    # compute the modified Chebyshev even-moment matrix
    mom = 2*sqrt(2)./(1-k.^2)
    mom[1] = 2
    M1,M2 = meshgrid(mom)
    M = M1.*M2
    M0 = fliplr(triu(fliplr(M)))
    # extract the upper left triangular part
    if (n % 2 == 0)
      M0[Int(n/2+1),1] = M0[Int(n/2+1),1]/2
    end
    # compute the cubature weights on the two subgrids
    L1 = W1.*transpose(transpose(TE1)*M0*TO2)
    L2 = W2.*transpose(transpose(TO1)*M0*TE2)
    return L1,L2
end

function Padua1(n)
    CE = [cos((j-1)*pi/n) for j in 1:2:(n+1)]
    CO = [cos((j-1)*pi/(n+1)) for j in 2:2:(n+2)]
    return hcat([[(x1,x2) for x2 in CO] for x1 in CE]...)
end

function Padua2(n)
    CO = [cos((j-1)*pi/n) for j in 2:2:(n+1)]
    CE = [cos((j-1)*pi/(n+1)) for j in 1:2:(n+2)]
    return hcat([[(x1,x2) for x2 in CE] for x1 in CO]...)
end

function _weights1(n)
    result = map(x -> 1, Padua1(n))
    result = 2.*result./(n*(n+1))
    if n % 2 == 0
        result[:,1] = result[:,1]./2
        result[:,end] = result[:,end]./2
        result[end, :] = result[end, :]./2
    else
        result[:,1] = result[1,:]./2
    end
    return result
end

function _weights2(n)
    result = map(x -> 1, Padua2(n))
    result = 2.*result./(n*(n+1))
    if n % 2 == 0
        result[1,:] = result[1,:]./2
    else
        result[1,:] = result[1,:]./2
        result[end,:] = result[end,:]./2
        result[:,end] = result[:,end]./2
    end
    return result
end

function fliplr(M)
    return hcat([ M[:,i] for i in size(M)[2]:-1:1 ]...)
end


function meshgrid(table)
    t1 = vcat([table for i in 1:1:length(table)]...)
    return transpose(t1),t1
end

end
