class Account:
    def __init__(self, address, balance, is_contract, chain_id):
        self.address = address
        self.balance = balance
        self.is_contract = is_contract
        self.chain_id = chain_id

    def __str__(self):
        return f"Account: address {self.address} | balance {self.balance} | is_smart_contract {self.is_contract} | chain id {self.chain_id}"

    def __eq__(self, other):
        return self.address == other.address and self.chain_id == other.chain_id

    def __hash__(self):
        return hash((self.address, self.chain_id))
