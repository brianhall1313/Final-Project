class Player:
    balance = 0
    name = 0


    def __init__(self, new_name, new_balance):
        self.name = new_name
        self.balance = new_balance
        self.hand = []

    def bet(self, amount):
        self.balance -= amount

    def payout(self, amount):
        self.balance += amount

    def save(self):
        return {"name": self.name, "balance": self.balance}

    def dealt(self, card):
        self.hand.append(card)

    def clear_hand(self):
        self.hand = []
