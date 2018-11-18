	.global approx_sqrt
	.type approx_sqrt, @function

x1 = %xmm0		
epsilon = %xmm1
x0 = %xmm2
x = %xmm3		#in xmm3 we will store original value of x
diff = %xmm4

	.section .text

approx_sqrt:
	movapd x1, x0
	movapd x1, x

	divsd x0, x1
	addsd x0, x1
	mulsd HALF, x1		#first 'iteration' to determine x_1

.loop:
	movapd x0, diff
	subsd x1, diff
	andpd SIGN_MASK, diff
	ucomisd diff, epsilon
	ja .finish
	movapd x1, x0
	movapd x, x1
	divsd x0, x1
	addsd x0, x1
	mulsd HALF, x1
	jmp .loop

.finish:
	ret

	.size approx_sqrt, . - approx_sqrt

	.section .rodata
	.type HALF, @object
HALF:
	.double 0.5
	.size HALF, 8
	
	.type SIGN_MASK, @object
SIGN_MASK:
	.8byte 0x7fffffffffffffff
	.size SIGN_MASK, 8
