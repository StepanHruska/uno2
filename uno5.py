import random

# Základní třída pro všechny karty
class Card:
    def __init__(self, color, value):
        self.color = color  # červená, žlutá, zelená, modrá, None (pro černé karty)
        self.value = value  # číslo nebo speciální hodnota ('+2', 'Reverse', 'Skip', 'Wild', 'Wild+4')

    def is_playable(self, other_card):
        """Vrátí True, pokud kartu lze zahrát na základě barvy nebo hodnoty."""
        return self.color == other_card.color or self.value == other_card.value or self.color is None

    def __str__(self):
        return f"{self.color} {self.value}"

# Děděné třídy pro speciální karty
class ActionCard(Card):
    """Speciální karty jako +2, otočení, přeskočení."""
    pass

class WildCard(Card):
    """Karty bez barvy, které si vyžádají novou barvu."""
    def __init__(self, value):
        super().__init__(None, value)  # Žádná barva při vytvoření

# Třída balíčku karet
class Deck:
    def __init__(self):
        self.cards = []
        self.build()

    def build(self):
        """Vytvoří kompletní balíček UNO karet."""
        colors = ['Red', 'Yellow', 'Green', 'Blue']
        values = list(range(0, 10)) + ['+2', 'Reverse', 'Skip']

        for color in colors:
            for value in values:
                self.cards.append(Card(color, value))
                if value != 0:
                    self.cards.append(Card(color, value))  # 2x každá karta kromě 0

        for _ in range(4):
            self.cards.append(WildCard('Wild'))
            self.cards.append(WildCard('Wild+4'))

        random.shuffle(self.cards)

    def draw_card(self):
        """Vytáhne kartu z balíčku."""
        if not self.cards:
            return None
        return self.cards.pop()

# Třída hráče
class Player:
    def __init__(self, name, is_computer=False):
        self.name = name
        self.hand = []
        self.is_computer = is_computer

    def draw(self, deck, num=1):
        for _ in range(num):
            card = deck.draw_card()
            if card:
                self.hand.append(card)

    def play_card(self, card, current_card):
        if card in self.hand and card.is_playable(current_card):
            self.hand.remove(card)
            return card
        return None

    def has_playable_card(self, current_card):
        return any(card.is_playable(current_card) for card in self.hand)

# Třída pro správu hry
class Game:
    def __init__(self):
        self.deck = Deck()
        # Hráči jsou rovnou nastavení
        self.players = [
            Player("Player", is_computer=False),
            Player("Computer", is_computer=True)
        ]
        self.discard_pile = []
        self.current_player_idx = 0
        self.direction = 1

        self.start_game()
    
    def start_game(self):
        # Rozdání karet
        for player in self.players:
            player.draw(self.deck, 7)

        # Otočení první karty
        first_card = self.deck.draw_card()
        while isinstance(first_card, WildCard):
            self.deck.cards.insert(0, first_card)
            random.shuffle(self.deck.cards)
            first_card = self.deck.draw_card()

        self.discard_pile.append(first_card)

    def next_player(self):
        self.current_player_idx = (self.current_player_idx + self.direction) % len(self.players)

    def play_turn(self):
        player = self.players[self.current_player_idx]
        current_card = self.discard_pile[-1]

        print(f"\n{player.name}'s turn. Current card: {current_card}")

        if player.is_computer:
            # Automatické hraní počítače
            playable_cards = [card for card in player.hand if card.is_playable(current_card)]

            if playable_cards:
                card_to_play = playable_cards[0]
                print(f"{player.name} plays {card_to_play}")
                played_card = player.play_card(card_to_play, current_card)
                self.discard_pile.append(played_card)

                if played_card.value == 'Reverse':
                    self.direction *= -1
                elif played_card.value == 'Skip':
                    self.next_player()
                elif played_card.value == '+2':
                    self.next_player()
                    self.players[self.current_player_idx].draw(self.deck, 2)
                elif played_card.value == 'Wild' or played_card.value == 'Wild+4':
                    chosen_color = random.choice(['Red', 'Yellow', 'Green', 'Blue'])
                    print(f"{player.name} chooses color {chosen_color}")
                    played_card.color = chosen_color
                    if played_card.value == 'Wild+4':
                        self.next_player()
                        self.players[self.current_player_idx].draw(self.deck, 4)

            else:
                print(f"{player.name} has no playable cards. Drawing a card.")
                player.draw(self.deck)

        else:
            # Tah lidského hráče (zůstává tak jak jsme upravili předtím)
            print(f"Your hand: ")
            for idx, card in enumerate(player.hand):
                print(f"{idx}: {card}")

            playable_indices = [idx for idx, card in enumerate(player.hand) if card.is_playable(current_card)]

            if playable_indices:
                print("\nPlayable cards:")
                for idx in playable_indices:
                    print(f"{idx}: {player.hand[idx]}")

                while True:
                    choice = input(f"Choose a card to play (index), or type 'draw' to draw a card: ")
                    if choice.lower() == 'draw':
                        player.draw(self.deck)
                        print(f"{player.name} draws a card.")
                        break
                    elif choice.isdigit() and int(choice) in playable_indices:
                        card_to_play = player.hand[int(choice)]
                        print(f"{player.name} plays {card_to_play}")
                        played_card = player.play_card(card_to_play, current_card)
                        self.discard_pile.append(played_card)

                        if played_card.value == 'Reverse':
                            self.direction *= -1
                        elif played_card.value == 'Skip':
                            self.next_player()
                        elif played_card.value == '+2':
                            self.next_player()
                            self.players[self.current_player_idx].draw(self.deck, 2)
                        elif played_card.value == 'Wild' or played_card.value == 'Wild+4':
                            chosen_color = self.choose_color(player)
                            print(f"{player.name} chooses color {chosen_color}")
                            played_card.color = chosen_color
                            if played_card.value == 'Wild+4':
                                self.next_player()
                                self.players[self.current_player_idx].draw(self.deck, 4)
                        break
                    else:
                        print("Invalid choice. Try again.")

            else:
                print(f"No playable cards. {player.name} must draw.")
                player.draw(self.deck)

        self.next_player()

    def choose_color(self, player):
        """Zeptá se hráče na volbu barvy při Wild kartě."""
        colors = ['Red', 'Yellow', 'Green', 'Blue']
        print(f"{player.name}, choose a color: {', '.join(colors)}")
        while True:
            choice = input("Enter color: ").capitalize()
            if choice in colors:
                return choice
            print("Invalid color. Please choose again.")

    def is_game_over(self):
        return any(len(player.hand) == 0 for player in self.players)

    def get_winner(self):
        for player in self.players:
            if len(player.hand) == 0:
                return player.name
        return None

# --- Spuštění hry ---
if __name__ == "__main__":
    game = Game()

    while not game.is_game_over():
        game.play_turn()

    print(f"\nGame over! Winner: {game.get_winner()}")