task = """Zadanie z przelewaniem definiujemy w następujący sposób: mamy dwa wiadra (o pojemności X i Y litrów), początkowo puste. Celem jest doprowadzenie do sytuacji, w której w którymś wiadrze znajdzie się K litrów. Można wykonywać następujące ruchy:
a) Napełnić jedno wiadro (czyli doprowadzić do sytuacji, w której znajduje się w nim dokładnie tyle wody, ile wynosi jego pojemność).
b) Wylać całą wodę z wiadra na podłogę.
c) Przelać wodę z wiadra A do wiadra B. Można przelać albo całą wodę (jeżeli pojemność i napeł- nienie wiadra B na to pozwala), albo też przelać dokładnie tyle wody, żeby napełnić całkowicie wiadro B (wówczas reszta wody pozostaje w wiadrze A).
Wykorzystaj przeszukiwanie grafu w głąb do stworzenia funkcji, która dla zadanych pojemności wiader i zadanego celu zwraca ciąg stanów, prowadzący do sukcesu (czyli do stanu z co najmniej jednym wiadrem zawierającym K litrów). Jeżeli taki ciąg nie istnieje, funkcja powinna zwracać listę pustą. Stany powinieneś reprezentować jako pary liczb (krotki lub listy dwuelementowe)."""

#fx - napełnienie x #fill
#ex - opróżnienie x #empty
#xmy - przelanie x do y #move

def move1(X,Y,b1,b2):			#jeśli b2+b1 > Y to wtedy drugie wiadro wypełnia się do maksimum
								#a pierwsze wiadro jest sumą obu (suma się nie zmieni) minus wypełnione drugie wiadro
	if b2 + b1 <= Y:
		return (0,b1+b2)
	else:
		return (b1+b2-Y,Y)

def dfs(X,Y,K,bckts,moves,visited,sol):
	bckt0 = bckts[0]
	bckt1 = bckts[1]
	if K in bckts:
		visited.add(K)
		print ("-".join(moves), " a poziomy wody to ", bckts)
		return moves
	if bckts in visited or bckt0 > X or bckt1 > Y or K in visited:			#mały trik - przy skończeniu wyżej dodajemy K jako liczbę do setu i tu sprawdzamy czy już wcześniej nie skończyliśmy
		pass
	else:
		visited.add(bckts)
		dfs(X,Y,K,(X,bckt1),moves + ['f1'],visited,sol)
		dfs(X,Y,K,(bckt0,Y),moves + ['f2'],visited,sol)
		dfs(X,Y,K,(0,bckt1),moves + ['e1'],visited,sol)
		dfs(X,Y,K,(bckt0,0),moves + ['e2'],visited,sol)
		dfs(X,Y,K,move1(X,Y,bckt0,bckt1),moves + ['1m2'],visited,sol)
		dfs(X,Y,K,move1(Y,X,bckt1,bckt0),moves + ['2m1'],visited,sol)

def goal(X,Y,K):
	bckts_beg = (0,0)
	return dfs(X,Y,K,bckts_beg,[],set(),[])

goal(9,5,3)
goal(5,9,2)
goal(1,7,4)
goal(13,2,-1)
