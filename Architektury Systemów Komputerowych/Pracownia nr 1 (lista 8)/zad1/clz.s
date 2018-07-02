  .globl clz
  .type clz, @function

  .section .text


clz:
    testq %rdi, %rdi
    jz t1_0
    movl $63, %eax
test32:
    movq %rdi, %rsi
    shrq $32, %rsi
    testq %rsi, %rsi
    jnz t1_32

test16:
    movq %rdi, %rsi
    shrq $16, %rsi
    testq %rsi, %rsi
    jnz t1_16

test8:
    movq %rdi, %rsi
    shrq $8, %rsi
    testq %rsi, %rsi
    jnz t1_8

test4:
    movq %rdi, %rsi
    shrq $4, %rsi
    testq %rsi, %rsi
    jnz t1_4

test2:
    movq %rdi, %rsi
    shrq $2, %rsi
    testq %rsi, %rsi
    jnz t1_2

test1:
    movq %rdi, %rsi
    shrq $1, %rsi
    testq %rsi, %rsi
    jnz t1_1
    ret

t1_32:
    subl $32, %eax
    movq %rsi, %rdi
    jmp test16
t1_16:
    subl $16, %eax
    movq %rsi, %rdi
    jmp test8
t1_8:
    subl $8, %eax
    movq %rsi, %rdi
    jmp test4
t1_4:
    subl $4, %eax
    movq %rsi, %rdi
    jmp test2
t1_2:
    subl $2, %eax
    movq %rsi, %rdi
    jmp test1
t1_1:
    subl $1, %eax
    movq %rsi, %rdi
    ret
t1_0:
    movl $64, %eax
    ret

    .size clz, . - clz
