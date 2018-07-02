#include<stdio.h>
#include<stdlib.h>

void insert_sort(long *first, long *last);


int main(int argc, char **argv){
	int n = argc - 1;
	long test[n];
	for(int i=0; i < n; i++){
		test[i] = strtol(argv[i+1], NULL, 10);
	}
	insert_sort(&test[0],&test[n]);
	for(int i=0; i<n; i++){
		printf("%ld ", test[i]);
	}
	printf("\n");
}
