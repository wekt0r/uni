from collections import namedtuple, defaultdict, Counter
from itertools import combinations
from random import sample, choice
from functools import reduce
from operator import __mul__, __add__
from copy import deepcopy

choose = lambda n,k: reduce(__mul__, range(n,n-k, -1), 1)//reduce(__mul__, range(1,k+1), 1)

COLORS = ["♣","♦","♥","♠"]
FIGURES = ["2","3","4","5","6","7","8","9","10","J","Q","K","A"]
FIGURES_VALUES = dict(zip(FIGURES, range(13)))

Card = namedtuple("Card", ["figure","color"])

def _hand_numbers(hand):
    hand_figures = [card.figure for card in hand]
    hand_numbers = defaultdict(set)
    for figure in hand_figures:
        hand_numbers[hand_figures.count(figure)].add(figure)
    return hand_numbers

def is_hand_poker(hand):
    return is_hand_color(hand) and is_hand_straight(hand)

def is_hand_color(hand):
    return len({card.color for card in hand}) == 1

def is_hand_straight(hand):
    return {card.figure for card in hand} in [{"2","3","4","5","6"}, {"3","4","5","6","7"},
                                              {"4","5","6","7","8"}, {"5","6","7","8","9"},
                                              {"6","7","8","9","10"}]

def is_hand_caret(hand_numbers):
    return 4 in hand_numbers

def is_hand_full(hand_numbers):
    return 3 in hand_numbers and 2 in hand_numbers

def is_hand_three_of_a_kind(hand_numbers):
    return 3 in hand_numbers

def is_hand_two_pairs(hand_numbers):
    return len(hand_numbers[2]) == 2

def is_hand_pair(hand_numbers):
#we dont need to check for pairs - we know from pigeonhole principle that figurant has at least one pair, which is better than blotkarz's pair
    return 2 in hand_numbers

def compare_two_hands(p, q):
    #p is blotkarz, q is figurant
    if is_hand_poker(p):
        return True

    p_numbers, q_numbers = _hand_numbers(p), _hand_numbers(q)
    for possible_hand in [is_hand_caret, is_hand_full]:
        if possible_hand(p_numbers):
            return not possible_hand(q_numbers)
        if possible_hand(q_numbers):
            return False

    if is_hand_straight(p) or is_hand_color(p):
        return True

    for possible_hand in [is_hand_three_of_a_kind, is_hand_two_pairs]:
        if possible_hand(p_numbers):
            return not possible_hand(q_numbers)
        if possible_hand(q_numbers):
            return False

    return False #better card decides


def get_figurant_hand_power(hand):
    hand_numbers = _hand_numbers(hand)
    return ("caret" if is_hand_caret(hand_numbers) else
           "full" if is_hand_full(hand_numbers) else
           "three" if is_hand_three_of_a_kind(hand_numbers) else
           "double_pair" if is_hand_two_pairs(hand_numbers) else
           "pair")

def get_blotkarz_hand_power(hand):
    hand_numbers = _hand_numbers(hand)
    return ("poker" if is_hand_poker(hand) else
           "caret" if is_hand_caret(hand_numbers) else
           "full" if is_hand_full(hand_numbers) else
           "color" if is_hand_color(hand) else
           "straight" if is_hand_straight(hand) else
           "three" if is_hand_three_of_a_kind(hand_numbers) else
           "double_pair" if is_hand_two_pairs(hand_numbers) else
           "pair" if is_hand_pair(hand_numbers) else
           "nothing")

colors = ["♣","♦","♥","♠"]
figures = ["2","3","4","5","6","7","8","9","10","J","Q","K","A"]
blotki = ["2","3","4","5","6","7","8","9","10"]
better_blotki = ["2","10","3","9","4","8","5","7","6"]
ordered_by_figure = [Card(f,c) for f in blotki for c in colors]
ordered_by_color = [Card(f,c) for c in colors for f in blotki]
better_ordered_by_figure = [Card(f,c) for f in better_blotki for c in colors]
deck = [Card(f,c) for f in figures for c in colors]
blotkarz_deck = deck[:-16]
figurant_deck = deck[-16:]

def estimate_probability(tries, b_deck=blotkarz_deck, f_deck=figurant_deck):
    return sum(1 for _ in range(tries) if compare_two_hands(sample(b_deck, 5), sample(f_deck,5)))/tries

#estimate_probability(10000)

def find_all_combinations_for_blotkarz(b_deck=blotkarz_deck):
    return Counter(get_blotkarz_hand_power(hand) for hand in combinations(b_deck, 5))

def find_all_combinations_for_figurant(f_deck=figurant_deck):
    return Counter(get_figurant_hand_power(hand) for hand in combinations(f_deck, 5))

def compute_probability(b_deck=blotkarz_deck, f_deck=figurant_deck):
    b_all = choose(len(b_deck), 5)
    f_all = choose(len(f_deck), 5)
    blotkarz_counter = find_all_combinations_for_blotkarz(b_deck)
    figurant_counter = find_all_combinations_for_figurant(f_deck)

    b = [blotkarz_counter[power] for power in ["poker", "caret", "full", "color", "straight", "three", "double_pair"]]
    f = [f_all - figurant_counter["caret"], f_all - figurant_counter["caret"] - figurant_counter["full"],
         f_all - figurant_counter["caret"] - figurant_counter["full"] - figurant_counter["three"],
         f_all - figurant_counter["caret"] - figurant_counter["full"] - figurant_counter["three"] - figurant_counter["double_pair"]]

    return (b[0]*f_all + b[1]*f[0] + (b[2] + b[3] + b[4])*f[1] + b[5]*f[2] + b[6]*f[3])/(b_all*f_all)

def compute_probability_for_basic_deck():
    b_all = choose(36, 5)
    f_all = choose(16, 5)

    blotkarz_counter = {"poker": 5*choose(4,1), "caret": 9*8*choose(4,1), "full": 9*8*choose(4,1)*choose(4,2),
                        "color": choose(9,5)*4 - 5*choose(4,1), "straight": 5*4**5 - 5*choose(4,1),
                        "three": 9*choose(4,3)*choose(8,2)*4*4, "double_pair": choose(9,2)*(choose(4,2)**2)*7*4}

    figurant_counter = {"caret": 4*3*choose(4,1), "full":4*choose(4,1)*3*choose(4,2), "three": 4*choose(4,1)*choose(3,2)*(4**2), "double_pair": choose(4,2)*(choose(4,2)**2)*2*4}

    b = [blotkarz_counter[power] for power in ["poker", "caret", "full", "color", "straight", "three", "double_pair"]]
    f = [f_all - figurant_counter["caret"], f_all - figurant_counter["caret"] - figurant_counter["full"],
         f_all - figurant_counter["caret"] - figurant_counter["full"] - figurant_counter["three"],
         f_all - figurant_counter["caret"] - figurant_counter["full"] - figurant_counter["three"] - figurant_counter["double_pair"]]

    return (b[0]*f_all + b[1]*f[0] + (b[2] + b[3] + b[4])*f[1] + b[5]*f[2] + b[6]*f[3])/(b_all*f_all)

# def find_fine_deck(tries):
#     for k in range(10,23):
#         print("NEW k = {}".format(k))
#         max_probability = 0
#         best_deck = None
#         for i in range(1000):
#             deck = sample(blotkarz_deck, k)
#             pr = estimate_probability(tries, deck)
#             if pr > max_probability:
#                 print("We i = {}, have {} and deck = \n {}\n".format(i, pr ,deck))
#                 max_probability = pr
#                 best_deck = deck
#
#         print(max_probability, best_deck, compute_probability(best_deck))
# works but slow and gives maximum of 0.3-0.35 probability
# print(find_fine_deck(2000))

def find_fine_deck(order):
    for i in range(5,len(order)-5):
        print("for i = {} we have {}({}) and deck({}) {}".format(i, estimate_probability(10000,order[i:]), compute_probability(order[i:]), len(order[i:]),order[i:]))
