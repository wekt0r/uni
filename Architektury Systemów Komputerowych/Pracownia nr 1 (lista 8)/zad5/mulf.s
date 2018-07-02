	.global mulf
	.type mulf, @function

a = %edi
b = %esi

sign_a = %r9d
sign_b = %r10d
exp_a = %r11d
exp_b = %r12d
man_a = %r13d
man_b = %r14d
SIGN_MASK = 0x80000000
EXPONENT_MASK = 0x7f800000
MANTISA_MASK = 0x007fffff
MANTISA_LENGTH = 23
EXPONENT_BIAS = 127
MANTISA_ONE_MASK = 0x00800000
MANTISA_NORM_MASK = 0x01000000

	.section .text

mulf:
	#we consider a = (-1)^sign_a * 2^(exp_a - 127)*(1+2^(-23)*man_a)
	#by analogy, b = (-1)^sign_b ...
	#where a^b is a to power of b
	#a*b = (sign_a xor sign_b) * 2^(exp_a + exp_b - 127 + X) * (1 + 2^(-23)*(2^(-23)*man_a*man_b))
	#where X is 1 when multiplication of mantissas produced number bigger than 2 and 0 otherwise
	#(rounding to zero)
	movl a, sign_a
	andl $SIGN_MASK, sign_a
	movl b, sign_b
	andl $SIGN_MASK, sign_b
	xorl sign_a, sign_b	#we store sign of product in sign_b

	movl a, exp_a
	andl $EXPONENT_MASK, exp_a
	shrl $MANTISA_LENGTH, exp_a
	movl b, exp_b
	andl $EXPONENT_MASK, exp_b
	shrl $MANTISA_LENGTH, exp_b
	addl exp_a, exp_b
	subl $EXPONENT_BIAS, exp_b
	shll $MANTISA_LENGTH, exp_b
	andl $EXPONENT_MASK, exp_b
				#we store exp_a + exp_b in exp_b		
	movl a, man_a
	andl $MANTISA_MASK, man_a
	movl b, man_b
	andl $MANTISA_MASK, man_b
	
	orl $MANTISA_ONE_MASK, man_a
	orl $MANTISA_ONE_MASK, man_b	#we add ones to mantisas (as 1 + bits)	
	movq %r13, %rax
	mulq %r14		#we have now (1+2^(-23)man_a)(1+2^(-23)man_b)
	shrq $MANTISA_LENGTH, %rax	#trunacate last 23 bits	
	movq %rax, %r13			#we save product in man_a (aka r13)
	andl $MANTISA_NORM_MASK, man_a	#if mantisas product had 1 on 24 bit it means we had mantisa product > 2 (note: m1*m2 < 4, so we have case 1 <=  m1*m2 < 2 and 2 <= m1*m2 < 4)
	shrl $1, man_a			
	addl man_a, exp_b		#as we moved it on 23-th bit and added to exponent, then exp_b' = exp_a + exp_b + X as mentioned above 
	shrl $MANTISA_LENGTH, man_a	
	testl man_a, man_a		#if it happened we normalize mantissa
	jz .dont_norm
	shrq $1, %rax

.dont_norm:
	andl $MANTISA_MASK, %eax	#eax stores proper mantissa
	orl exp_b, %eax			
	orl sign_b, %eax		#we set exponent and sign

	ret

	.size mulf, . - mulf
