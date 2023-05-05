from enum import Enum
from model import EventLog, Contract

TokenType = Enum("TokenType", ["T20", "T721", "T1155"])


class TokenTransfer:
    def __init__(self, token_type, token_name, token_symbol, token_decimal, token_id, token_value, txn_hash, sender, receiver):
        self.token_type = token_type  # ERC20 or ERC721
        self.token_name = token_name  # ERC20
        self.token_symbol = token_symbol  # ERC20
        self.token_decimal = token_decimal  # ERC20
        self.token_id = token_id  # ERC721
        self.token_value = token_value # ERC20
        self.txn_hash = txn_hash  # ERC20 and ERC721
        self.sender = sender  # ERC20 and ERC721
        self.receiver = receiver  # ERC20 and ERC721

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



