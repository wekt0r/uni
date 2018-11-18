#include<stdio.h>
#include<stdlib.h>

unsigned long fibonacci(unsigned long);

int main(int argc, char **argv){
    unsigned long n = strtoul(argv[1], NULL, 10);

    unsigned long res = fibonacci(n);
    printf("%lu\n", res);
    return 0;
}
