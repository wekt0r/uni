#include<stdio.h>
#include<stdlib.h>

int clz(long);

int main(int argc, char **argv){
    unsigned long n = strtol(argv[1], NULL, 10);

    int res = clz(n);
    printf("%d\n", res);
    return 0;
}
