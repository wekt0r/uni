from collections import namedtuple, defaultdict
from random import sample
COLORS = ["♣","♦","♥", "♠"]
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

#def is_hand_pair(hand_numbers):
#we dont need to check for pairs - we know from pigeonhole principle that figurant has at least one pair, which is better than blotkarz's pair
#    return 2 in hand_numbers

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

colors = ["♣","♦","♥", "♠"]
figures = ["2","3","4","5","6","7","8","9","10","J","Q","K","A"]
deck = [Card(f,c) for f in figures for c in colors]
blotkarz_deck = deck[:-16]
figurant_deck = deck[-16:]

def estimate_probability(tries, b_deck=blotkarz_deck, f_deck=figurant_deck):
    return sum(1 for _ in range(tries) if compare_two_hands(sample(b_deck, 5), sample(f_deck,5)))/tries

estimate_probability(10000)
