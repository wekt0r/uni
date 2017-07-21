task = """a) Napisz rekurencyjną funkcję, która generuje zbiór wszystkich sum podzbiorów listy liczb L
(czyli jeżeli L była równa [1,2,3,100], to funkcja powinna zwrócić zbiór
set([0,1,2,3,4,5,6, 100, 101, 102, 103, 104, 105, 106])"""

def powerset(list):
	if list == []:
		return [[]]
	A = powerset(list[1:])
	return [ [list[0]] + rest for rest in A ] + A


L = [1,2,3,100]
L1 = map(sum,powerset(L))
print (sorted(L1))
