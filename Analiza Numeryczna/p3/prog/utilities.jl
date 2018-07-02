#author: Wiktor Garbarek

module DoubleIntegralUtils
export move_function, exact_digits

function move_function(f,a,b,c,d) #instead of integrating f in [a,b] x [c,d], we integrate this function on [-1,1]x[-1,1]
    return (x,y) -> f((b-a)*(x+1)/2 + a, (d-c)*(y+1)/2 + c)*(b-a)*(d-c)/4
end

exact_digits(x, x0) = -log10(abs(x - x0))

end
