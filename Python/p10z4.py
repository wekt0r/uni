task = """Jesteś pisarzem literatury fantastycznej (raczej użytkowej, niż artystycznej, szczerze mówiąc).
Cał- kiem dobrze sobie z tym radzisz, ale masz kłopot z wymyślaniem imion dla bohaterów.
To zadanie ma być użytecznym narzędziem rozwiązującym taki problem, czyli wspomagającym twórczy proces wymyślania imion (nazwisk) dla tego typu literatury.
Należy rozwiązać je w następujący sposób:
• Imię będziemy losować znak po znaku.
• Jak zobaczysz, wygodnie przyjąć, że każde imię zaczyna się od pary znaków ^^ a kończy znakiem $ (oczywiście
można tu wybrać inne oznaczenia, nie powinieneś również tych dziwnych znaków pokazywać użytkownikowi)
• Imię powinno mieć pewną długość minimalną, przykładowo 4 znaki.
• Prawdopodobieństwo wylosowania znaku na pozycji i powinno zależeć od znaków i-1 oraz i-2.
• Prawdopodobieństwa te powinieneś szacować przeglądając plik z rzeczywistymi imionami (podany na kno, możesz skorzystać z innego – na przykład jednoznacznie słowiańskiego, jeżeli uda Ci się taki odnaleźć).
Przykładowo, gdyby jedynymi imionami były Paweł i Ewelina, wówczas dla znaków we możliwe byłyby tylko dwie kontynuacje, mianowicie ł oraz l, każda z prawdopodobieństwem 1/2.
Twój program powinien wczytać listę imion, oszacować na jej podstawie prawdopodobieństwo losowania znaków, następnie wylosować kilkanaście imion zgodnych z powyżej naszkicowanymi zasadami."""

from random import choice
letters = "a ą á b c ć d e ę é f g h i í j k l ł m n ń o ó p q r s ś š t u ü w v x y z ź ż".split(" ")
prob_letters = {(a,b): [] for a in letters for b in letters}

for name in open('imiona.txt').read().split(' \n'):
	name = list(name)
	name.append('$')
	for i in range(len(name)-2):
		prob_letters[(name[i],name[i+1])].append(name[i+2])

def make_name():
	name = []
	name.append(choice(letters))
	name.append(choice(letters))
	i = 1
	while name[i] != '$':
		i+= 1
		list_to_find = prob_letters[(name[i-2],name[i-1])]
		if list_to_find == []:
			break
		to_append = choice(list_to_find)
		name.append(to_append)
	if name != [] and (len(name) < 5 or len(name) > 20):
		return make_name()
	else:
		name = name[:-1]
		return "".join(name)

for i in range(10):
	print (make_name())
