from enum import Enum

TokenType = Enum("TokenType", ["T20", "T721", "T1155"])


class TokenTransfer:
    def __init__(self, token_type, token_name, token_symbol, token_decimal, token_id, token_value, txn_hash, sender, receiver):
        self.token_type = token_type
        self.token_name = token_name
        self.token_symbol = token_symbol
        self.token_decimal = token_decimal
        self.token_id = token_id
        self.token_value = token_value
        self.txn_hash = txn_hash
        self.sender = sender
        self.receiver = receiver

    def __str__(self):
        return f"""Token Transfer:
                -- Token type: {self.token_type}
                -- Token name: {self.token_name}
                -- Token symbol: {self.token_symbol}
                -- Token decimal: {self.token_decimal}
                -- Token id: {self.token_id}
                -- Token value: {self.token_value}
                -- Transaction involved: {self.txn_hash}
                -- Sender: {self.sender}
                -- Receiver: {self.receiver}
        """

    def __eq__(self, other):
        return self.txn_hash == other.txn_hash and self.sender == other.sender and self.receiver == other.receiver and (self.token_id == other.token_id if self.token_id is not None else True)

    def __hash__(self):
        return hash((self.txn_hash, self.sender, self.receiver, self.token_id))




