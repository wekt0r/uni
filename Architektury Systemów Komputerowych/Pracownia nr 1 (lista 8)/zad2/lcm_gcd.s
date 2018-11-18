    .globl lcm_gcd
    .type lcm_gcd, @function

    .section .text

a = %r11
b = %r10

lcm_gcd:
        movq %rdi, a
        movq %rsi, b
.loop:
        testq b, b          #if b == 0
        je .return          #   skoncz
        movq a, %rax        # c = a
        cqto
	divq b              # c %= b
        movq b, a           # a := b
        movq %rdx, b        # b := c (w rdx mamy resztę, w raxie wynik)
        jmp .loop
.return:
        movq %rdi, %rax     # rax <- a
        cqto
	divq a              # rax /= gcd
        mulq %rsi           # rax *= b
        movq a, %rdx        # rdx <- gcd
        ret

	.size lcm_gcd, . - lcm_gcd
