    .global fibonacci
    .type fibonacci, @function

    .section .text

fibonacci:
    movq %rsp, %rbp

    cmpq $1, %rdi
    jle .base_case
    decq %rdi
    pushq %rdi	      #save argument n-1 for later
    callq fibonacci   #takes current n decreased by 1 straight from %rdi
    
    popq %rdi	      #now we take n-1 from stack...
    decq %rdi	      #...aaand make it n-2
    pushq %rax	      #we save result from earlier call
    callq fibonacci   #called with n-2
    popq %r9	      #here we take fibonacci(n-1)
    addq %r9, %rax    # fib(n-2) += fib(n-1)
    ret

.base_case:
    movq %rdi, %rax
    ret

    .size fibonacci, . - fibonacci
