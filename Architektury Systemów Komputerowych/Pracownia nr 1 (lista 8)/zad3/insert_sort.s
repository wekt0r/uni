	.global insert_sort
	.type insert_sort, @function

first = %rdi
last = %rsi
pointer_i = %r11
pointer_j = %r10

	.section .text
insert_sort:
	leaq 8(first), pointer_i
.loop_i:
	cmpq pointer_i, last
	jl .sorted
   	
	movq pointer_i, pointer_j
.loop_j:
    	cmpq pointer_j, first
	je .inc_i
	movq -8(pointer_j), %r9
	movq (pointer_j), %r8
	cmpq %r9, %r8
	jge .inc_i
	movq %r8, -8(pointer_j)
	movq %r9, (pointer_j)
	leaq -8(pointer_j), pointer_j
	jmp .loop_j
.inc_i:
	leaq 8(pointer_i), pointer_i # i++
	jmp .loop_i
.sorted:
	ret

	.size insert_sort, . - insert_sort
