import random

class Card:
    def __init__(self, color, value, wilds=None):
        self.color = color
        self.value = value
        self.wilds = wilds
    
    def is_playable(self, top_card):
        return (
            self.color == top_card.color or
            self.value == top_card.value or
            self.wilds in ['Wild', 'Wild+4']
        )
    def __str__(self):
        return f"{self.color} {self.value} {self.wilds}"

class Deck:
    def __init__(self, cards=None):
        self.cards = self._create_deck()
        random.shuffle(self.cards)

    def _create_deck(self):
        colors = ['Red', 'Yellow', 'Green', 'Blue']
        values = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, "Draw two", "Skip", "Reverse"]
        wilds = ["Wild", "Draw four"]
        deck = []

        for color in colors:
            deck.append(Card(color, '0'))  # každá barva má jednu 0
            for value in values[1:]:       # ostatní 2x
                deck.extend([Card(color, value), Card(color, value)])

        # Wild karty
        for i in range (4):
            deck.append(wilds[0])
            deck.append(wilds[1])

        return deck

    def draw(self, count=1):
        drawn = self.cards[:count]
        self.cards = self.cards[count:]
        return drawn

    def is_empty(self):
        return len(self.cards) == 0


class player:
    def __init__(self, name, hand=None):
        self.name = name
        self.hand = []

    def generate_hand_for_player(player, deck):
        player.hand = deck.draw(7)
        return player.hand

    def draw_cards(self, deck, count=1):
        self.hand.extend(deck.draw(count))

    def play_card(self, index):
        return self.hand.pop(index)

    def has_playable_card(self, top_card):
        return any(card.is_playable(top_card) for card in self.hand)

    def __str__(self):
        return f"{self.name}: {[str(card) for card in self.hand]}"

class Game:
    def __init__(self, player_names):
        self.deck = Deck()
        self.discard_pile = []
        self.players = [player(name) for name in player_names]
        self.current_player_index = 0
        self.direction = 1  # 1 = dopředu, -1 = dozadu
        self.setup_game()

    def setup_game(self):
        for player in self.players:
            player.draw_cards(self.deck, 7)
        # První karta
        first_card = self.deck.draw()[0]
        while first_card.color == 'wild':
            self.deck.cards.append(first_card)
            random.shuffle(self.deck.cards)
            first_card = self.deck.draw()[0]
        self.discard_pile.append(first_card)

    def current_player(self):
        return self.players[self.current_player_index]

    def next_player_index(self):
        return (self.current_player_index + self.direction) % len(self.players)

def play_turn(self):
    player = self.current_player()
    top_card = self.discard_pile[-1]
    print(f"\nTop card: {top_card}")
    print(player)

    playable_indices = [
        i for i, card in enumerate(player.hand) if card.is_playable_on(top_card)
    ]

    if not playable_indices:
        print(f"{player.name} has no playable card. Drawing a card...")
        player.draw_cards(self.deck)
        if player.hand[-1].is_playable_on(top_card):
            print(f"{player.name} can play drawn card: {player.hand[-1]}")
            play = input("Do you want to play it? (y/n): ").lower()
            if play == 'y':
                chosen_card = player.play_card(-1)
                self.discard_pile.append(chosen_card)
                self.resolve_special_card(chosen_card)
                return
    else:
        print("Playable cards:")
        for i in playable_indices:
            print(f"{i}: {player.hand[i]}")
        choice = int(input("Choose card index to play: "))
        chosen_card = player.play_card(choice)
        print(f"{player.name} played {chosen_card}")
        self.discard_pile.append(chosen_card)
        self.resolve_special_card(chosen_card)
        return

    # Pokud žádná karta nebyla zahraná, pokračuj k dalšímu hráči
    self.current_player_index = self.next_player_index()

    def is_game_over(self):
        return any(len(p.hand) == 0 for p in self.players)
    
def resolve_special_card(self, card):
    if card.value == 'skip':
        print("Next player is skipped!")
        self.current_player_index = self.next_player_index()
        self.current_player_index = self.next_player_index()

    elif card.value == 'reverse':
        print("Direction reversed!")
        self.direction *= -1
        if len(self.players) == 2:
            # reverse acts like skip in 2-player game
            self.current_player_index = self.next_player_index()

        self.current_player_index = self.next_player_index()

    elif card.value == 'draw2':
        next_index = self.next_player_index()
        next_player = self.players[next_index]
        print(f"{next_player.name} draws 2 cards and is skipped!")
        next_player.draw_cards(self.deck, 2)
        # Přeskočíme ho
        self.current_player_index = (next_index + self.direction) % len(self.players)

    elif card.value == 'wild':
        new_color = input("Choose a color (red, green, blue, yellow): ").lower()
        card.color = new_color
        self.current_player_index = self.next_player_index()

    elif card.value == 'wild_draw4':
        new_color = input("Choose a color (red, green, blue, yellow): ").lower()
        card.color = new_color
        next_index = self.next_player_index()
        next_player = self.players[next_index]
        print(f"{next_player.name} draws 4 cards and is skipped!")
        next_player.draw_cards(self.deck, 4)
        self.current_player_index = (next_index + self.direction) % len(self.players)

    else:
        self.current_player_index = self.next_player_index()
    
if __name__ == "__main__":
    game = Game(["Alice", "Bob"])

    while not game.is_game_over():
        game.play_turn()

    for player in game.players:
        if len(player.hand) == 0:
            print(f"\n🎉 {player.name} wins! 🎉")