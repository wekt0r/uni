#include<stdio.h>
#include<stdlib.h>

typedef struct {
    unsigned long lcm, gcd;
} result_t;

result_t lcm_gcd(unsigned long, unsigned long);

int main(int argc, char **argv){
    unsigned long a = strtoul(argv[1], NULL, 10);
    unsigned long b = strtoul(argv[2], NULL, 10);

    result_t res = lcm_gcd(a,b);
    printf("%lu, %lu\n", res.lcm, res.gcd);
    return 0;
}
