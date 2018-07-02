#include<stdio.h>
#include<stdlib.h>

union float_repr{
	float f;
	unsigned r;
};

unsigned mulf(unsigned, unsigned);

int main(int argc, char **argv){
    float fa = strtof(argv[1], NULL);
    float fb = strtof(argv[2], NULL);

    union float_repr a;
    a.f = fa;
    union float_repr b;
    b.f = fb;
    
    //printf("we have: %x, %x \n", a.r, b.r);
    //printf("entered: %f, %f \n", a.f, b.f);
    unsigned rres = mulf(a.r,b.r);
    union float_repr res;
    res.r = rres;
    //printf("%x\n", res.r);
    printf("%f\n", res.f);
    return 0;
}
