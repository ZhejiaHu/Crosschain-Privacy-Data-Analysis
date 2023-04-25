class Account:
    def __init__(self, address, balance, is_contract):
        self.address = address
        self.balance = balance
        self.is_contract = is_contract

    def __str__(self):
        return f"Account: address {self.address} | balance {self.balance} | is_smart_contract {self.is_contract}"

    def __eq__(self, other):
        return self.address == other.address

    def __hash__(self):
        return hash(self.address)
