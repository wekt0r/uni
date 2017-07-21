task = """Parę słów nazwiemy parą cesarską (a występujące w niej słowa cesarskimi),
jeżeli są one wzajemnie swoimi szyfrogramami w szyfrze Cezara
(tzn. każde z nich otrzymujemy z drugiego za pomocą odpowiedniego przesunięcia wszystkich liter;
oczywiście przesunięcie powinno być nietrywialne, czyli nie może być identycznością).
Napisz program, który znajduje najdłuższe polskie słowo cesarskie
(jeżeli więcej niż jedno osiąga maksymalną długość powinieneś wypisać je wszystkie)."""

from collections import defaultdict
from random import sample

letters = "a ą b c ć d e ę f g h i j k l ł m n ń o ó p q r s ś t u v w x y z ź ż".split(" ")
numbers = {}
i = 0

for letter in letters:
	numbers[letter] = i
	i+= 1

#print (dict)

def distance(word):

	word = list(word)
	code = list()

	if "|" in word or "-" in word or "'" in word or ":" in word or "_" in word or "+" in word:
		return (0,0)
	else:
		for i in range(1,len(word)):
			code.append(str((numbers[word[i]] - numbers[word[i-1]])%35))
		code = tuple(code)
	return code


dict = defaultdict(lambda: set())
for word in open("slowa.txt").read().split("\n"):
	word = word.lower()
	dict[distance(word)].add(word)

candidates = list()
for key in dict.keys():

	if len(dict[key]) >= 2:
		candidates.append(key)

candidates = sorted(candidates, key = lambda x: -len(x))
print (list(dict[candidates[0]]))
i = 1
while len((list(dict[candidates[i]]))[0]) == len((list(dict[candidates[0]]))[0]):
	print(list(dict[candidates[i]]))
	i+=1
