task = """W zadaniu tym będziesz symulował Adama Mickiewicza piszącego Pana Tade- usza.
Powinieneś wczytać tekst P. Tadeusza (znajdziesz go np. na Wolnych Lekturach)
i następnie utworzyć strukturę, która dla każdego słowa pamięta listę możliwych następców tego słowa
(czyli słów, które po tym występują). Fragment tej struktury może wyglądać następująco:
  { ..., ’natenczas’ : [’wojski’, ’z’, ’i’, ’tam’], ’kociołkach’ : [’bigos’],
         ’cymbalistów’ : [’wielu’], ...}
Uznajemy znaki interpunkcyjne za prawidłowe wyrazy,
nie przejmujemy się ponadto przechodzeniem do nowego wiersza.
Symulator Adama Mickiewicza (SAM) działa tak: przyjmuje na wejście jakieś słowo,
znajduje jego następników, losuje jednego z nich, i czynności powtarza,
aż do otrzymania tekstu o pożądanej długości (albo do otrzymania słowa bez następnika).
"""

from collections import defaultdict
from random import choice

tadeusz = open("pan-tadeusz.txt").read()
for sign in ['!','?','.', '—', '-', '*', ',',';',':', '…', '«', '»', '«', '(', ')']:
	tadeusz = tadeusz.replace(sign, ' ' + sign)
tadeusz = tadeusz.replace('\n', ' ')

tadeusz = tadeusz.split(' ')
dict = defaultdict(list)
for i in range(1,len(tadeusz)):
	dict[tadeusz[i-1].lower()].append(tadeusz[i])


def Tadeo(word, length, text, dict):
	text += word + " "
	if length == 0:
		return text
	elif dict[word.lower()] == []:
		return text
	else:
		return Tadeo(choice(dict[word.lower()]),length-1,text,dict)


print (Tadeo("Ojczyzna", 10, "",dict))
