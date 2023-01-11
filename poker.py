# Command: python poker.py
# Auther: Zikun Wang
# 2023

import random
import matplotlib.pyplot as plt
import numpy as np
import timeit

### Hand Checking

def reorder_cards(i_cards):
    cards = i_cards.copy()
    
    for i in range(len(cards)):
        for j in range(len(cards)-1, i, -1):
            if cards[j].size < cards[j-1].size:
                cards[j], cards[j-1] = cards[j-1], cards[j]
    return cards

def find_smallest_card(i_cards):
    cards = i_cards.copy()
    smallest = cards[0]
    for i in range(1, len(cards)):
        if cards[i].size < smallest.size:
            smallest = cards[i]
            
    return smallest

def check_one_pair(i_cards):
    cards = i_cards.copy()
    biggest_pair = []
    
    for i in range(len(cards) - 1):
        for j in range(i + 1, len(cards)):
            if cards[i].size == cards[j].size:
                if biggest_pair == [] or biggest_pair[0].size < cards[i].size:
                    biggest_pair = [cards[i], cards[j]]
                    
    if biggest_pair == []:
        return None
    
    return biggest_pair

def check_two_pair(i_cards):
    cards = i_cards.copy()
    pair_1 = check_one_pair(cards)
    if pair_1 == None: return None
    
    for card in pair_1:
        cards.remove(card)
        
    pair_2 = check_one_pair(cards)
    if pair_2 == None: return None
    
    return pair_1 + pair_2

def check_three_of_a_kind(i_cards):
    cards = i_cards.copy()
    sizes = {}
    
    for card in cards:
        if card.size not in sizes:
            sizes[card.size] = 1
        else:
            sizes[card.size] += 1
            
    biggest_size = 0
    
    for size in sizes:
        if sizes[size] == 3:
            biggest_size = max(biggest_size, size)
            
    if biggest_size == 0:
        return None
    
    result = [card for card in cards if card.size == biggest_size]
    return result

def check_straight(i_cards):
    cards = i_cards.copy()
    cards = reorder_cards(cards)

    had_size = []
    for card in cards:
        if card.size not in had_size:
            had_size += [card.size]
        else:
            cards.remove(card)

    straight = []
    for i in range(len(cards)-4):
        if cards[i].size == cards[i+1].size-1 and \
        cards[i].size == cards[i+2].size-2 and \
        cards[i].size == cards[i+3].size-3 and \
        cards[i].size == cards[i+4].size-4:
            if straight == []:
                straight = [cards[i], cards[i+1], cards[i+2], cards[i+3], cards[i+4]]
            elif cards[i+4].size > straight[-1].size:
                straight = [cards[i], cards[i+1], cards[i+2], cards[i+3], cards[i+4]]
                
    if straight == []: return None
    return straight

def check_flush(i_cards):
    cards = i_cards.copy()
    shape_count = {}
    
    for card in cards:
        if card.shape not in shape_count:
            shape_count[card.shape] = 1
        else:
            shape_count[card.shape] += 1
            
    target = None
    
    for shape in shape_count:
        if shape_count[shape] >= 5:
            target = shape
            
    if target == None: return None
    
    flush = []
    for card in cards:
        if card.shape == target:
            flush += [card]
    
    while len(flush) > 5:
        smallest = find_smallest_card(flush)
        flush.remove(smallest)
        
    return flush

def check_full_house(i_cards):
    cards = i_cards.copy()
    
    three = check_three_of_a_kind(cards)
    if three == None: 
        return None
    
    for card in three:
        cards.remove(card)
        
    two = check_one_pair(cards)
    if two == None:
        return None
    
    return three + two

def check_four_of_a_kind(i_cards):
    cards = i_cards.copy()
    sizes = {}
    
    for card in cards:
        if card.size not in sizes:
            sizes[card.size] = 1
        else:
            sizes[card.size] += 1
    
    for size in sizes:
        if sizes[size] == 4:
            return [card for card in cards if card.size == size]
    
    return None

def check_straight_flush(i_cards):
    cards = i_cards.copy()
    shape_count = {}
    
    for card in cards:
        if card.shape not in shape_count:
            shape_count[card.shape] = 1
        else:
            shape_count[card.shape] += 1
            
    target = None
    
    for shape in shape_count:
        if shape_count[shape] >= 5:
            target = shape
            
    if target == None: return None
    
    flush = []
    for card in cards:
        if card.shape == target:
            flush += [card]
    
    straight_flush = check_straight(flush)

    if straight_flush == None:
        return None

    return straight_flush
    
def check_royal_flush(i_cards):
    cards = i_cards.copy()
    straight_flush = check_straight_flush(cards)
    if straight_flush == None:
        return None
    if straight_flush[-1].size == 13:
        return straight_flush
    return None

def check_hand(i_cards):
    cards = i_cards.copy()
    best = None
    hand_type = None
    
    one_pair = check_one_pair(cards)
    two_pair = check_two_pair(cards)
    three_of_a_kind = check_three_of_a_kind(cards)
    straight = check_straight(cards)
    flush = check_flush(cards)
    full_house = check_full_house(cards)
    four_of_a_kind = check_four_of_a_kind(cards)
    straight_flush = check_straight_flush(cards)
    royal_flush = check_royal_flush(cards)
    
    if one_pair != None:
        best = one_pair
        hand_type = "One Pair"
        
    if two_pair != None:
        best = two_pair
        hand_type = "Two Pair"
        
    if three_of_a_kind != None:
        best = three_of_a_kind
        hand_type = "Three of a Kind"
        
    if straight != None:
        best = straight
        hand_type = "Straight"
        
    if flush != None:
        best = flush
        hand_type = "Flush"
    
    if full_house != None:
        best = full_house
        hand_type = "Full House"
        
    if four_of_a_kind != None:
        best = four_of_a_kind
        hand_type = "Four of a Kind"
        
    if straight_flush != None:
        best = straight_flush
        hand_type = "Straight Flush"
        
    return best, hand_type

class Deck():
    def __init__(self):
        self.cards = self.create_cards()

    def create_cards(self):
        cards = []
        shapes = ["♠", "♡", "♢", "♣"]
        sizes = list(range(1, 14))
        for shape in shapes:
            for size in sizes:
                cards += [Card(shape, size)]
        return cards

    def shuffle(self):
        random.shuffle(self.cards)
        
    def reset(self):
        self.cards = self.create_cards()

    def __repr__(self):
        return self.cards

class Card():
    def __init__(self, shape, size):
        self.size = size
        self.shape = shape

    def __repr__(self):
        big_cards = ["J", "Q", "K"]
        if self.size in [11, 12, 13]:
            size = big_cards[self.size - 11]
        else:
            size = self.size
        return self.shape + str(size)

class Player():
    def __init__(self, name):
        self.name = name
        self.cards = []
        self.hand = []
        self.hand_type = ""

    def draw_card(self, deck):
        self.cards += [deck.cards.pop()]
        
    def reset(self):
        self.cards = []
        self.hand = []
        self.hand_type = ""
        
    def check(self, dealer):
        cards = self.cards + dealer.cards
        
        
    def __repr__(self):
        cards = ""
        for card in self.cards:
            cards += str(card) + " "
        if cards == "": cards = "No cards."
        r = "Name: " + self.name
        for i in range(10 - len(self.name)):
            r += " "
        r += "| Cards: " + cards
        return r
        
class Dealer():
    def __init__(self):
        self.name = "Dealer"
        self.cards = []
        
    def draw_card(self, deck):
        self.cards += [deck.cards.pop()]
        
    def reset(self):
        self.cards = []
        
    def __repr__(self):
        cards = ""
        for card in self.cards:
            cards += str(card) + " "
        if cards == "": cards = "No cards."
        r = "Name: " + self.name
        for i in range(10 - len(self.name)):
            r += " "
        r += "| Cards: " + cards
        return r
        
class Game():
    def __init__(self, names):
        self.deck = Deck()
        self.dealer = Dealer()
        self.players = []
        self.hands = {}
        for name in names:
            self.players += [Player(name)]
            self.hands[name] = []
            
    def send_cards(self):
        self.deck.shuffle()
        
        # Dealer draw cards
        for i in range(5):
            self.dealer.draw_card(self.deck)
        
        # Player draw cards
        for player in self.players:
            for i in range(2):
                player.draw_card(self.deck)
                
    def reset(self):
        self.deck.reset()
        self.dealer.reset()
        self.hands = {}
        for player in self.players:
            player.reset()
            self.hands[name] = []
            
    def check_hands(self):
        for player in self.players:
            hand, hand_type = check_hand(player.cards + self.dealer.cards)
            player.hand = hand
            player.hand_type = hand_type
            
    def __repr__(self):
        r = ""
        r += f"Player Count: {len(self.players)}\n"
        r += f"{self.dealer}\n"
        for player in self.players:
            r += f"{player} "
            if player.hand_type != None:
                r += f" {player.hand_type} "
                for card in player.hand:
                    r += f"{card} "
            r += "\n"
            
        return r

players = ["Alice", "Bob", "Cart"]
game = Game(players)
game.send_cards()
game.check_hands()
print(game)


