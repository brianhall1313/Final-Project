class Card:
    _suit = ""
    _rank = ""
    _value = 0

    def __init__(self, new_suit, new_value):
        self.suit = new_suit
        self.value = new_value
        self.rank = new_value

    def __str__(self):
        return f"{self.rank} of {self.suit}"

    @property
    def suit(self):
        return self._suit

    @suit.setter
    def suit(self, new_suit):
        match new_suit:
            case 0:
                self._suit = "♠"
            case 1:
                self._suit = "♣"
            case 2:
                self._suit = "♥"
            case 3:
                self._suit = "♦"

    @property
    def rank(self):
        return self._rank

    @rank.setter
    def rank(self, new_rank):
        match new_rank:
            case 13:
                self._rank = "King"
            case 12:
                self._rank = "Queen"
            case 11:
                self._rank = "Jack"
            case 1:
                self._rank = "Ace"
            case _:
                self._rank = str(new_rank)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        match new_value:
            case 11 | 12 | 13:
                self._value = 10
            case _:
                self._value = new_value
