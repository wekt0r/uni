from random import choice
import re

with open("words_for_ai1.txt") as f:
    words = set(f.read().split("\n"))

#MAX = max(words, key=lambda x: len(x)) => "kilkudziesięciocentymetrowych"
MAX = len("kilkudziesięciocentymetrowych")

with open("pan_tadeusz_bez_spacji.txt") as f:
    pan_tadeusz = f.read().split("\n")

def random_search(sentence):
    best_badness = [(0,[])]*(len(sentence)+1) # [(int, list[string])]
    for i in range(1,len(sentence) + 1):
        smaller_possibilities = [ (best_badness[j][0] + len(sentence[j:i])**2,
                                 best_badness[j][1] + [sentence[j:i]])
                                 for j in range(max(0,i-MAX), i)
                                 if sentence[j:i] in words and (best_badness[j] != (0,[]) or j == 0)]
        best_badness[i] = choice(smaller_possibilities) if smaller_possibilities else (0,[])
    #return (best_badness[-1])
    return " ".join(best_badness[-1][1])

def basic_search(sentence):
    best_badness = [(0,[])]*(len(sentence)+1) # [(int, list[string])]
    for i in range(1,len(sentence) + 1):
        best_badness[i] = max([ (best_badness[j][0] + len(sentence[j:i])**2,
                                 best_badness[j][1] + [sentence[j:i]])
                                 for j in range(max(0,i-MAX), i)
                                 if sentence[j:i] in words]
                               + [(0,[])], #if it doesnt find any possible combination of spaces then we have 0 badness and no words
                              key=lambda tuple: tuple[0])
    #return (best_badness[-1])
    return " ".join(best_badness[-1][1])

with open("pan_tadeusz_bez_spacji.txt") as f:
    pan_tadeusz = [line for line in f.read().split("\n") if line]

with open("pan-tadeusz2.txt") as f:
    pan_tadzio = f.read().split("\n")

better_tadzio = [re.sub(r'\s+'," ", re.sub(r'[…:,;!?«»—.()*-]', "", line.lower()).strip()) for line in pan_tadzio if line and "1" not in line]

def find_different():
    good_random = 0
    good_basic = 0
    all_sentences = len(better_tadzio)
    for s_orig, s_bare in zip(better_tadzio, pan_tadeusz):
        good_random += s_orig == random_search(s_bare)
        good_basic += s_orig == basic_search(s_bare)

    return good_random/all_sentences, good_basic/all_sentences
