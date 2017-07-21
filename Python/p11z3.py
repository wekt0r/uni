task = """Zdefinujmy następujące przekształcenie na słowach
(nazwiemy je permutacyjną postacią normalną): zamieniamy litery na liczby, w ten sposób, że:
1. Tym samym literom przypisane są równe liczby, różnym literom – różne liczby.
2. Liczby przypisywane są po kolei, licząc od lewej strony.
Otrzymane liczby sklejamy w jeden napis, wstawiając na przykład znak "-" jako separator.
Przy- kładowe pary słowo i wartość przekształcenia: tak: 1-2-3, nie: 1-2-3, tata: 1-2-1-2, indianin: 1-2-3-1-4-2-1-2.
Napisz funkcję, która zwraca w wyniku wartość opisanego przekształcenia."""

def make_values(list,dict):
	if list == []:
		return 0
	if list[0] not in dict.keys():
		dict[list[0]] = max(dict.values()) + 1
	make_values(list[1:],dict)

def ppn(word):
	word = list(word)
	result = []
	values = {word[0]: 1}
	make_values(word[1:],values)
	print (values)
	for letter in word:
		result.append(str(values[letter]))
	result = "-".join(result)
	return result

print (ppn("chrząszcz"))
