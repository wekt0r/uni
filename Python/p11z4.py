task = """Szyfr przestawieniowy to taki szyfr, w którym każdej literce z polskiego alfabetu przypisana jest inna literka (konsekwentnie, w ramach całego komunikatu).
W tym i kolejnym zadaniu, będziemy łamać takie szyfry (czyli pisać programy, które znajdują komunikat, w sytuacji, gdy mamy znamy jedynie szyfrogram).
Będziemy zakładać, że słowa w szyfrogramie oddzielone są spacjami i (dla zwiększenia czytelności komunikatu), między nimi czasami znajdują się znaki interpunkcyjne (niezaszyfrowane, otoczone spacjami).
Zakładamy również, że wszystkie słowa w komunikacie występują w słowniku (z polskimi słowami z jednej z poprzednich list) i że nie mamy żadnych dodatkowych informacji o języku (np. o częstościach liter, czy wyrazów).
Napisz program, który umie rozszyfrować dwa pierwsze szyfrogramy ze SKOS-u.
Uwaga: w obu tych szyfrogramach wszystkie słowa mają unikalną permutacyjną postać normalną (to znaczy, że znajomość tejże postaci pozwala jednoznacznie wybrać słowo). 
Uwaga2: każdy szyfrogram jest w osobnym wierszu, każdy był też szyfrowany osobną permutacją."""

cyphers = """fulfolfu ćtąśśótą tlźlźltą
udhufńfd ąuąuęąę yrrożdśś śdśsdtsć
uwuąpwuw uw dwnuąźhąuąa"""


def make_values(list,dict):
	if list == []:
		return 0
	if list[0] in dict.keys():
		make_values(list[1:],dict)
	else:
		dict[list[0]] = max(dict.values()) + 1
		make_values(list[1:],dict)

def ppn(word):
	word = list(word)
	result = []
	values = {word[0]: 1}
	make_values(word[1:],values)
	for letter in word:
		result.append(str(values[letter]))
	result = "-".join(result)
	return result


dict = {}
dict_gen = """for word in open("slowa.txt").read().split("\n"):
	word = word.lower()
	if ppn(word) in dict.keys():
		dict[ppn(word)].append(word)
	else:
		dict[ppn(word)] = [word]

print (dict)"""

ppns_dict = eval(open('ppns_file.py').read())

def decypher(sentence,ppns_dict):

	sentence = sentence.split(" ")
	result = ""
	for word1 in sentence:
		result = result + ppns_dict[ppn(word1)][0] + " "

	return result


print (decypher("fulfolfu ćtąśśótą tlźlźltą",ppns_dict))
print (decypher("udhufńfd ąuąuęąę yrrożdśś śdśsdtsć",ppns_dict))
#print (decypher("uwuąpwuw uw dwnuąźhąuąa",ppns_dict))
