import card
import random


class Deck:
    def __init__(self, num_of_decks=1):
        self.deck = []
        self.build_deck(num_of_decks)

    def __str__(self):
        s = ""
        for c in self.deck:
            s += str(c) + "\n"
        return s

    def build_deck(self, num_of_decks):
        for _ in range(num_of_decks):
            for suit in range(4):
                for value in range(1, 14):
                    new_card = card.Card(suit, value)
                    self.deck.append(new_card)

    def test_print(self):
        for view_card in self.deck:
            print(view_card)

    def shuffle(self):
        random.shuffle(self.deck)

    def deal_card(self):
        return self.deck.pop()
