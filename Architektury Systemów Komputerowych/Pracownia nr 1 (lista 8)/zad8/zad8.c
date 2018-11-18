#include<stdio.h>
#include<stdlib.h>

double approx_sqrt(double, double);

int main(int argc, char **argv){
    double x = strtod(argv[1], NULL);
    double eps = strtod(argv[2], NULL);
    
    double res = approx_sqrt(x, eps);
    printf("%f\n", res);
    return 0;
}
