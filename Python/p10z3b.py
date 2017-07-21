task = """Napisz rekurencyjną funkcję, która generuje wszystkie ciągi niemalejące o długości N,
zawierające liczby od A do B."""

def seq(N,A,B):
	if N == 0:
		return [ [] ]
	return [ [e] + rest for e in range(A,B+1) for rest in seq(N-1, e, B) ]

print (seq(4,8,11))
