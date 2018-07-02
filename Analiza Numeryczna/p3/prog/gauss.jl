#author: Wiktor Garbarek

module DoubleIntegralGauss
export double_gauss_chebyshev

function double_gauss_chebyshev(f,n,m) #returns approximate value of \int_{-1}^{1} \int_{-1}^{1} f(x,y) * 1/sqrt(1-x^2) * 1/sqrt(1-y^2) dydx
    return sum([f(cos((2k+1)/(2n+2)*pi),cos((2j+1)/(2m+2)*pi)) for k in 0:1:n for j in 0:1:m])*pi*pi/((n+1)*(m+1))
end

end
