with open("words_for_ai1.txt") as f:
    words = set(f.read().split("\n"))

#MAX = max(words, key=lambda x: len(x)) => "kilkudziesięciocentymetrowych"
MAX = len("kilkudziesięciocentymetrowych")

sentence = "tamatematykapustkinieznosi"

with open("pan_tadeusz_bez_spacji.txt") as f:
    pan_tadeusz = f.read().split("\n")

def search(sentence):
    best_badness = [(0,[])]*(len(sentence)+1) # [(int, list[string])]
    for i in range(1,len(sentence) + 1):
        best_badness[i] = max([ (best_badness[j][0] + len(sentence[j:i])**2,
                                 best_badness[j][1] + [sentence[j:i]])
                                 for j in range(max(0,i-MAX), i)
                                 if sentence[j:i] in words]
                               + [(0,[])], #if it doesnt find any possible combination of spaces then we have 0 badness and no words
                              key=lambda tuple: tuple[0])
        # idea - dynamic programming -
        # under best_badness[i] we store (int, list)
        # where int is best possible sum of squared lengths of words
        # where list is list of words used to get to output
        # it represents best spaces for input[:i] (ie. best_badness[5]
        # stores the best spacing for "tamat" when arg sentence is used )
        # for best_badness[i] we check almost all below (from best_badness[i-29] to best_badness[i-1])
        # if the difference is valid word then we use it and add it to sentence - we take max by best_badness
        # we use [(0,[])] at the end for situation where we have empty sequence (no valid spaces possible)
    return (best_badness[-1])

x = input()
print(" ".join(search(x)[1]))
#with open("zad2_input.txt") as f:
    #tests = f.read().split("\n")

# print(tests)
# with open("zad2_output.txt", mode='w') as f:
#     for test in tests:
#         if test:
#             f.write(" ".join(search(test)[1]))
#             f.write("\n")
