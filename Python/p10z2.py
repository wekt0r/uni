task = """Łamigłówką arytmetyczną jest zadanie, w którym należy literom przyporządkować (różne) cyfry w ten sposób,
by będące treścią zadania dodawianie było prawdziwe. Przykładowe zadania to:
  SEND
+ MORE
-------
 MONEY

   CIACHO
+  CIACHO
---------
  NADWAGA
Napisz program, który rozwiązuje łamigłówki arytmetyczne.
W programie powinna być funkcja, której argumentem jest napis przedstawiający zagadkę (przykładowo "send + more = money", a wynikiem słownik kodujący (jakieś) roz- wiązanie.
Gdy rozwiązanie nie istnieje, funkcja powinna zwracać pusty słownik (ew. wartość None)."""

from random import choice

def find_solution(word1,word2,word3, list_letters, solution, set_of_digits):
	if -1 not in set(solution.values()):
		number1 = 0
		number2 = 0
		number3 = 0
		for letter in word1:
			number1 = 10*number1 + solution[letter]
		for letter in word2:
			number2 = 10*number2 + solution[letter]
		for letter in word3:
			number3 = 10*number3 + solution[letter]

		if number1 + number2 == number3 and solution[word1[0]] != 0 and solution[word2[0]] != 0 and solution[word3[0]] != 0 and len(set(solution.keys())) == len(set(solution.values())):
			print (solution)
			print (number1, " + ", number2, " = ", number3)
			return True
	if list_letters != []:
		for i in list(set_of_digits):
		 	solution[list_letters[0]] = i
		 	find_solution(word1,word2,word3,list_letters[1:],solution,set_of_digits - {i})

def cryptarythm(equation):
	equation1 = equation.split(" ")
	set_of_digits = {0,1,2,3,4,5,6,7,8,9}

	word1 = list(equation1[0])
	word2 = list(equation1[2])
	word3 = list(equation1[4])

	letters = set()
	letters = set(word1) | set(word2) | set(word3)

	list_letters = list(letters)
	sol = {}
	for element in letters:
		sol[element] = -1

	find_solution(word1,word2,word3,list_letters, sol, set_of_digits)


print (cryptarythm("send + more = money"))

#x = input()
#print (cryptarythm(x))
