class Player:
    balance = 0
    name = 0

    def __init__(self, new_name, new_balance):
        self.name = new_name
        self.balance = new_balance

    def bet(self, amount):
        self.balance -= amount

    def payout(self, amount):
        self.balance += amount

    def save(self):
        return {"name": self.name, "balance": self.balance}
