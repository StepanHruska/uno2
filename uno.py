import random

class Card:
    def __init__(self, color, value, wilds=None):
        self.color = color
        self.value = value
        self.wilds = wilds
    
    def __str__(self):
        return f"{self.color} {self.value} {self.special_ability}"
class player:
    def __init__(self, name, hand=None):
        self.name = name
        self.hand = []

def generate_hand_for_player(player, deck):  
    pass
    

def create_all_cards():
    deck = []
    colors = ['Red', 'Green', 'Blue', 'Yellow']
    values = list(range(10)) + ['Skip', 'Reverse', 'Draw Two']
    wilds = ['Wild', 'Draw Four']
    for color in colors:
        for value in values:
            cardValue = "{} {}".format(color,value)
            deck.append(cardValue)  
            if value != 0:
                deck.append(cardValue)
    for i in range (4):
        deck.append(wilds[0])
        deck.append(wilds[1])
    for cardPos in range(len(deck)):
        randPos = random.randint(0, 107)
        deck[cardPos], deck[randPos] = deck[randPos], deck[cardPos]
    print(deck)
    return deck