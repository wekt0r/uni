def ceasar(word,key):
	letters = "a ą b c ć d e ę f g h i j k l ł m n ń o ó p r s ś t u w y z ź ż".split(" ") #32 litery
	#letters = "a ą b c ć d e ę f g h i j k l ł m n ń o ó p q r s ś t u w v x y z ź ż".split(" ") #35 liter
	shifted = {}
	for i in range(len(letters)):
		shifted[letters[i]] = letters[(i+key)%32]
	word = list(word)
	for i in range(len(word)):
		if word[i] != " ":
			word[i] = shifted[word[i]]
	word = "".join(word)
	return word

print (ceasar("ople",5))
