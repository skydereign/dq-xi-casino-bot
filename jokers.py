#!/usr/bin/env python
# http://www.videopokerballer.com/strategy/jokers-wild/
import collections
import itertools
import logging
import sys

# h = Hearts, s = Spades, c = Clubs, d = Diamonds, T = Ten, s = Suited.
suites = ["h", "s", "c", "d"]

m = {"A": 1, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "T": 10, "J": 11, "Q": 12, "K": 13, "W": -1}

# joker is WW for parsing convenience
def parse_hand(string):
    l = map(lambda x: (m[x[0]], x[1]), string.split('-'))
    # print(l)
    return list(l)

def allcards(hand):
    v = list(filter(lambda x: x > 0, m.values()))
    return list(set(itertools.product(v, suites)).difference(set(hand)))

def flush(hand):
    if all(map(lambda x: x[1] == hand[0][1], hand)):
        return hand

def cards(hand):
    s = sorted(map(lambda x: x[0], hand))
    return s

def suitez(hand):
    s = sorted(map(lambda x: x[1], hand))
    return s

def royal(hand):
    s = cards(hand)
    if s == [1, 10, 11, 12, 13]:
        return hand

def straight(hand):
    s = cards(hand)
    
    if sorted(s) == list(range(min(s), max(s)+1)):
        return hand

    if 1 in s:
        low = s[1:] + [14]
        if sorted(low) == list(range(min(low), max(low)+1)):
            return hand

def suited(hand, cards):
    qjt = list(filter(lambda x: x[0] in cards, hand))
    for check in list(itertools.combinations(qjt, len(cards))):
        if flush(check):
            return check

# Pat Royal Flush 	800.0000 	Th-Jh-Qh-Kh-Ah
def pat_royal_flush(hand):
    return royal(hand) and flush(hand)

# Pat Straight Flush 	50.0000 	6h-7h-8h-9h-Th
def pat_straight_flush(hand):
    return straight(hand) and flush(hand)

# Four of a Kind 	23.7500 	6c-6s-6d-6h-9s
def four(hand):
    c = collections.Counter(cards(hand))
    if 4 in c.values():
        return list(filter(lambda x: c[x[0]] == 4, hand))

# Royal Flush Draw 	19.8958 	Th-Jh-Qh-Kh-4h
def rfd(hand):
    p = list(itertools.combinations(hand, 4))
    for combination in p:
        draws = allcards(combination)
        for i in draws:
            z = list(combination) + [i]
            if pat_royal_flush(z):
                return combination

# Pat Full House 	7.0000 	Ac-Ad-As-Js-Jc
def patfh(hand):
    c = collections.Counter(cards(hand)).values()
    if 3 in c and 2 in c:
        return hand

# Pat Flush 	5.0000 	Ac-Jc-6c-5c-4c
def patflush(hand):
    return flush(hand)

# Open Straight Flush Draw 	4.1667 	4c-5c-6c-7c-Th
def osfd(hand):
    p = list(itertools.combinations(hand, 4))
    for combination in p:
        draws = allcards(combination)
        for i in draws:
            z = list(combination) + [i]
            if straight(z) and flush(z):
                return combination


# Three of a Kind 	3.9362 	8c-8s-8d-9h-3d
def toak(hand):
    c = collections.Counter(cards(hand))
    if 3 in c.values():
        return list(filter(lambda x: c[x[0]] == 3, hand))

# Inside Straight Flush Draw 	3.1042 	Qs-Js-9s-8s-4c
# combined with above

# Pat Straight 	3.0000 	4c-5s-6h-7h-8h
def patstraight(hand):
    return straight(hand)

# Two Pair 	1.6250 	3c-3s-4d-4h-Ac
def tp(hand):
    c = collections.Counter(cards(hand))
    if len(list(filter(lambda x: x == 2, c.values()))) > 1:
        return list(filter(lambda x: c[x[0]] == 2, hand))

# Q-J-T suited 	1.4424 	Qh-Jh-Th-4d-3d
def qjts(hand):
    return suited(hand, [10, 11, 12])

# K-Q-Js, K-Q-Ts, K-J-Ts (w/ no Flush penalty*) 	1.4379 	Kc-Qc-Jc-8s-5s
def kqjskqtskjtsnfp(hand):
    for check in [[13, 12, 11], [13,12,10], [13,11,10]]:
        if suited(hand, check):
            x = suited(hand, check)
            suit = x[0][1]
            c = collections.Counter(suitez(hand))
            if c[suit] == 3:
                return x

# High Pair (Jacks or Better) 	1.5405 	Ac-Ad-Js-8c-5h
def hpjob(hand):
    c = collections.Counter(cards(hand))
    for k, v in c.items():
        if v == 2 and k in [1, 11, 12, 13]:
            return list(filter(lambda x: x[0] == k, hand))

# Three to a Royal, A+K (w/ no St. or Fl. penalty*) 	1.4113 	Ac-Kc-Tc-Ts-5h
# note: skipping the penalties for this one (difference is marginal)
def ttarak(hand):
    p = list(itertools.combinations(hand, 3))
    for combination in p:
        draws = allcards(combination)
        for i in draws:
            for two_draws in itertools.combinations(draws, 2):
                z = list(combination) + list(two_draws)
                if royal(z) and flush(z):
                    return(combination)

# Pair of Aces or Kings 	1.3997 	Ac-As-8s-5h-2h
# this looks like a subset of high pair (jacks or better), so ignoring
# Three to a Royal, A+K (w/ 1 St. or Fl. penalty*) 	1.3989 	Ac-Kc-Tc-Js-5h
# combined with ttarak above

# K-Q-Js, K-Q-Ts, K-J-Ts (w/ 1 Flush penalty*) 	1.3945 	Kc-Qc-Jc-8c-5s
def kqjskqtskjtswfp(hand):
    for check in [[13, 12, 11], [13,12,10], [13,11,10]]:
        if suited(hand, check):
            x = suited(hand, check)
            suit = x[0][1]
            c = collections.Counter(suitez(hand))
            if c[suit] == 4:
                return x

# Three to a Royal, Ace High, no King 	1.3005 	Ac-Qc-Tc-5h-4h
# combined with ttarak above

# Four to a Flush 	1.0417 	Kh-8h-6h-3h-2s
def ftaf(hand):
    p = list(itertools.combinations(hand, 4))
    for combination in p:
        if flush(combination):
            return combination

# Three to a Straight Flush, Open, No St. Penalty 	0.7358 	4c-5c-6c-Th-9h
def ttsf(hand):
    p = list(itertools.combinations(hand, 3))
    for combination in p:
        draws = allcards(combination)
        for i in draws:
            for two_draws in itertools.combinations(draws, 2):
                z = list(combination) + list(two_draws)
                if straight(z) and flush(z):
                    return(combination)

# Low Pair (Twos through Queens) 	0.7314 	3c-3s-7h-9h-Jc
def lpttq(hand):
    c = collections.Counter(cards(hand))
    for k, v in c.items():
        if v == 2 and k in [2,3,4,5,6,7,8,9,10,11,12]:
            return list(filter(lambda x: x[0] == k, hand))

# 3 to a St. Flush, Open (w/ 1 or 2 St. Penalties*) 	0.7225 	3c-4c-5c-7s-8d
# combined

# K-Q-J-T 	0.6250 	Kc-Qs-Jc-Ts-2h
def kqjt(hand):
    f = list(filter(lambda x: x[0] in [10,11,12,13], hand))
    if len(f) >= 4:
        return f

# 3 to a St. Flush, One Gap 	0.6020 	4h-5h-7h-9c-Tc
# combined
# 3 to a St. Flush, 2 Gaps, 1 High Card 	0.6011 	8h-Th-Qh-9c-2s
# combined

# A-K suited 	0.5700 	Ac-Kc-9s-6s-2d
def aks(hand):
    return suited(hand, [1, 13])

# Four to a Straight, Open, 2345-9TJQ 	0.5625 	2c-3s-4c-5d-8s
def ftas(hand):
    p = list(itertools.combinations(hand, 4))
    for combination in p:
        draws = allcards(combination)
        for i in draws:
            z = list(combination) + [i]
            if straight(z):
                return combination

# Three to a St. Flush, 2 Gaps, 0 High Cards 	0.4876 	4c-6c-8c-9s-Js
# not implemented

# K-Qs, K-Js, K-Ts 	0.4694 	Kc-Qc-8s-6s-4h
def kqkjkts(hand):
    return suited(hand, [13,12]) or suited(hand, [13,11]) or suited(hand, [13,10])

# A-K offsuit 	0.4506 	Ac-Ks-9h-6h-3s
def akos(hand):
    aces = list(filter(lambda x: x[0] == 1, hand))
    kings = list(filter(lambda x: x[0] == 13, hand))
    if len(aces) == 1 and len(kings) == 1:
        for suit in map(lambda x: x[1], aces):
            if suit not in map(lambda x: x[1], kings):
                return aces + kings

# note, example is wrong
# A-Qs, A-Js, A-Ts (w/ no flush penalty*) 	0.4472 	Ac-Qs-8s-5s-2h
def aqajats(hand):
    for check in [[1, 12], [1, 11], [1, 10]]:
        if suited(hand, check):
            x = suited(hand, check)
            suit = x[0][1]
            c = collections.Counter(suitez(hand))
            if c[suit] == 2:
                return x

# Ace or King 	0.4469 	Ac-9s-7h-4s-2d
def aok(hand):
    aok = list(filter(lambda x: x[0] == 1 or x[0] == 13, hand))
    if len(aok) > 0:
        return aok

# J-T suited 	0.3560 	Jc-Tc-7s-5h-2d
def jts(hand):
    return suited(hand, [10, 11])

# Q-J suited, Q-T suited 	0.3448 	Ac-Jc-7s-5h-2d
def qjsqts(hand):
    return suited(hand, [11,12]) or suited(hand, [10,12])

# NOTE: this naive implementation takes 20+s to run, and probably isn't worth
# the compute effort
# Two to a Straight Flush, Open, (w/ no penalty*) 	0.3324 	5c-6c-Ts-2d-Jd
def ttsfo(hand):
    p = list(itertools.combinations(hand, 2))
    for combination in p:
        draws = allcards(combination)
        for i in draws:
            for three_draws in itertools.combinations(draws, 3):
                z = list(combination) + list(three_draws)
                if pat_straight_flush(z):
                    if abs(combination[0][0] - combination[1][0]) == 1:
                        # open means contiguous
                        return combination

# Everything Else : Draw Five New Cards 	0.3598 	10s-8c-6d-4s-2h

# yikes
regular_methods = [pat_royal_flush, pat_straight_flush, four, rfd, patfh, patflush, osfd, toak, patstraight, tp, qjts, kqjskqtskjtsnfp, hpjob, ttarak, kqjskqtskjtswfp, ftaf, ttsf, lpttq, kqjt, aks, ftas, kqkjkts, akos, aqajats, aok, jts, qjsqts,
                   # ttsfo
]

# Pat Five of a Kind 	200.0000 	Tc-Td-Th-Ts-W
def pat_foak(hand):
    return ((4 in collections.Counter(cards(hand)).values()) and hand)

# Pat Joker Royal 	100..0000 	Tc-Jc-Qc-Kc-W
def pat_joker_royal(hand):
    p = list(itertools.combinations(hand, 4))
    for combination in p:
        draws = allcards(combination)
        for i in draws:
            z = list(combination) + [i]
            if royal(z):
                return combination

# Pat Straight Flush 	50.0000 	6c-7c-8c-9c-W
def pat_joker_sf(hand):
    p = list(itertools.combinations(hand, 4))
    for combination in p:
        if flush(combination):
            draws = allcards(combination)
            for i in draws:
                z = list(combination) + [i]
                if straight(z) and flush(z):
                    return combination

# Four of a Kind 	23.7500 	4c-4s-4d-W-Jc
def joker_foak(hand):
    return toak(hand)

# Pat Full House 	7.0000 	Ac-Ad-As-Js-W
def pat_joker_fh(hand):
    p = list(itertools.combinations(hand, 4))
    for combination in p:
        if flush(combination):
            draws = allcards(combination)
            for i in draws:
                z = list(combination) + [i]
                if patfh(z):
                    return combination

# Four to a Joker Royal 	6.1458 	Tc-Jc-Qc-W-2d
def joker_ftajr(hand):
    p = list(itertools.combinations(hand, 3))
    for combination in p:
        draws = allcards(combination)
        for i in draws:
            z = list(combination) + [i]
            if royal(z):
                return combination

# Four to a Straight Flush, Open, W345s-W9TJs 	5.9375 	4c-5c-6c-W-Js
def joker_ftasf(hand):
    p = list(itertools.combinations(hand, 3))
    for combination in p:
        draws = allcards(combination)
        for i in draws:
            z = list(combination) + [i]
            if straight(z) and flush(z):
                return combination

# Pat Flush 	5.0000 	Ac-Jc-6c-5c-W
def joker_pat_flush(hand):
    return flush(hand)

# Four to a Straight Flush, One Gap 	4.8125 	5c-W-8c-9c-Js
# combined
# Four to a Straight Flush, 2 Gaps, 1 Hi Card 	4.1042 	Jc-9c-7c-W-3h
# combined

# Three of a Kind 	3.9362 	8c-8s-W-9h-3d
def joker_toak(hand):
    return tp(hand)

# Four to a Straight Flush, 2 Gaps, 0 Hi Cards 	3.7292 	Tc-8c-6c-W-2h
# combined

# Pat Straight 	3.0000 	4c-5s-6h-7h-W
def joker_pat_straight(hand):
    return straight(hand)

# Three to a Royal, King High 	2.0505 	Kc-Qc-W-2h-4c

# Four to a Flush, One or Two High Cards 	2.0208 	Jc-8c-6c-W-2s
# Three to a Royal, Jack High 	1.9317 	Jc-Tc-W-6h-2h
# Three to a Royal, Ace High 	1.9176 	Ac-Jc-W-8s-2h
# Three to a St. Flush, Open, W45s-W9Ts 	1.8670 	W-5c-6c-9s-Jd
# Three to a St. Flush, 3 Gaps, 1 Hi Card 	1.8059 	Jc-7c-W-4s-2d
# Three to a Royal, Queen High 	1.7934 	Qc-Tc-W-8s-2h
# 3 to a St. Flush, 1 Gap, 6-T Hi (w/ no penalty*) 	1.7287 	Tc-8c-W-7s-2s
# Joker and Ace (w/ no Flush penalty*) 	1.7148 	Ac-W-9s-6d-2h
# Joker and King (w/ no Flush penalty*) 	1.7050 	Kc-W-9s-6d-2h
# Joker and Ace (w/ One Flush penalty*) 	1.7021 	Ac-W-9s-6d-2c
# 3 to a St. Flush, 1 Gap, 6-T Hi (w/ 1 penalty*) 	1.6989 	Tc-8c-W-4c-2s
# Joker and K-Q-J, K-Q-T, K-J-T 	1.6875 	Kc-Qs-Jd-W-2h
# Joker and King (w/ One Flush penalty*) 	1.6839 	Kc-W-8d-6s-2c
# Three to a St. Flush, 1 Gap, 4, 5, or Jack High 	1.6809 	5c-3c-W-8s-9d
# 3 to a St. Flush, 2 Gaps, 6-J Hi (w/ no penalty*) 	1.5541 	Tc-7c-W-4h-2s
# Four to a Flush, no High Cards 	1.5417 	Qc-7c-2c-W-8s
# 3 to a St. Flush, 2 Gaps, 6-J Hi (w/ St. penalty*) 	1.5328 	Tc-7c-W-8s-2s
# Joker + 23s, 24s, 25s, Q9s 	1.5275 	2c-3c-W-8s-Jd
# Four to a Straight, Open, 6-T High 	1.5208 	Tc-9s-7d-W-4c
# Joker + 6/7/8 (w/ least penalty*) 	1.4952 	8c-W-4d-2h-Qd
# Joker + Ten (w/ no penalty*) 	1.4932 	Tc-W-5s-3d-2h
# Joker + 5/9 (w/ no penalty*) 	1.4926 	9c-W-4s-3d-2h
# Joker + Ten (w/ one penalty*) 	1.4720 	Tc-W-Js-4h-2d
# Joker + 5/9 (w/ one penalty*) 	1.4695 	9c-W-5s-3d-2h
# Joker + 9-T-J 	1.4583 	Jc-Ts-9d-W-4h
# Joker + Ten (w/ two or more penalties*) 	1.4514 	Tc-W-Js-7d-2h
# Joker + 5/9 (w/ two or more penalties*) 	1.4473 	9c-W-5s-3c-2h
# Joker + Jack (four different suits) 	1.4369 	Jc-W-6d-3s-2h
# Everything Else : Keep Joker and Draw Four 	1.4360 	W-6c-7d-2h-3s

joker_methods = [pat_foak]


def get_should_keep(hand):
    keepers = process_hand(hand)
    if keepers is None:
        return [False, False, False, False, False]

    should_keep = []
    
    for i in range(0, len(hand)):
        should_keep.append(hand[i] in keepers or hand[i][0] == -1) # should always keep a joker

    return should_keep

def process_hand(hand):
    methods = regular_methods
    if -1 in cards(hand):
        hand = list(filter(lambda x: x[0] > 0, hand))
        # print(hand)
        methods = joker_methods
        # instead of implementing the remainder of the joker strategies, use
        # software to enumerate them
        draws = allcards(hand)
        for i in draws:
            z = hand + [i]
            for method in regular_methods:
                a = method(z)
                if a:
                    logging.info('jokers choice,{}'.format(str(method)))
                    if i in a:
                        # print([x for x in a if x != i])
                        return [x for x in a if x != i]
                    else:
                        # print(a)
                        return a

    else:
        for method in methods:
            a = method(hand)
            if a:
                logging.info('jokers choice,{}'.format(str(method)))
                # print(a)
                return(a)
    

if __name__ == '__main__':
    # print(sys.argv[1])
    hand = process_hand(parse_hand(sys.argv[1]))
    print(get_should_keep(parse_hand(sys.argv[1])))
