class Account:
    def __init__(self, address, balance):
        self.address = address
        self.balance = balance

    def __str__(self):
        return f"Account: address {self.address} | balance {self.balance}"
