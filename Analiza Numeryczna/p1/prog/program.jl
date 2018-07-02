setprecision(256)
module PiFormulas
    export formula1, formula2, formula3

    function formula1(n, precision=BigFloat)
        x1 = precision(2)
        for i=[2:1:n;]
            x1 = precision(2.0)^(i-1)*sqrt(2*(1 - sqrt(1 - (x1/precision(2.0)^(i-1))^2)))
        end
        return x1
    end

    function formula2(n, precision=BigFloat)
        x1 = precision(2)
        for i=[2:1:n;]
            x1 = 2*x1/sqrt(2*(1 + sqrt(1-(x1/precision(2.0)^(i-1))^2)))
        end
        return x1
    end

    function formula3(n, precision=BigFloat)
        x1 = precision(2)
        x2 = precision(2)sqrt(precision(2))
        for i=[3:1:n;]
            xt = x1
            x1 = x2
            x2 = x2*sqrt(2*x2/(x2 + xt))
        end
        if n == 1
            return precision(2)
        end
        return x2
    end
end

module TestFunctions
    export test_formula, latex_table_generator, relative_error_to_pi, exact_digits, rate_of_convergence_step, linear_convergence_step

    function test_formula(formula, precision, iterations)
        for i=[1:1:iterations;]
            @printf("x_%d = %.24f with relative_error δ = %.4e \n", i, formula(i, precision), relative_error_to_pi(formula(i, precision)))
        end
    end

    function latex_table_generator(formula, precision, iterations)
        for i=[1:1:iterations;]
            @printf("%d & %.24f & %.4e \\\\ \\hline \n", i, formula(i, precision), relative_error_to_pi(formula(i, precision)))
        end
    end

    relative_error_to_pi(x) = abs(BigFloat(x) - pi)/pi

    function exact_digits(formula, precision)
        f(n) = -log10(abs(BigFloat(formula(n, precision)) - pi))
        return f
    end

    function rate_of_convergence_step(formula,precision)
         f(n) = log(abs((formula(n+1, precision) - formula(n,precision))/(formula(n, precision) - formula(n-1,precision))))/log(abs((formula(n, precision) - formula(n-1, precision))/(formula(n-1, precision) - formula(n-2, precision))))
         return f
    end

    function linear_convergence_step(formula,precision)
        f(n) = abs(formula(n+1, precision) - pi)/abs(formula(n, precision) - pi)
        return f
    end

end
