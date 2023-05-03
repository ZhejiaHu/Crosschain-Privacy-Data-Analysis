from typing import List
from model import TokenTransfer, EventLog
import util


class MethodInvocation:
    def __init__(self, txn_hash, contract_address, method_id, inputs):
        self.txn_hash = txn_hash
        self.contract_address = contract_address
        self.method_id = method_id
        self.inputs = inputs

    def __str__(self):
        return f"Method invoked: transaction hash {self.txn_hash} | contract_address {self.contract_address} | method id {self.method_id} | inputs {self.inputs}\n"


class Transaction:
    def __init__(self,
                 txn_hash, status, timestamp, from_account, to_account, block_num, value, gas, chain_id, block_id,
                 internal_txns=[],
                 method_invoked: MethodInvocation=None,
                 tokens_transferred: List[TokenTransfer]=[],
                 events_emitted: List[EventLog]=[]):
        if internal_txns is None:
            internal_txns = []
        self.txn_hash = txn_hash
        self.status = status
        self.timestamp = timestamp
        self.from_account = from_account
        self.to_account = to_account
        self.block_num = block_num
        self.value = value
        self.gas = gas
        self.chain_id = chain_id
        self.block_id = block_id
        self.internal_txns = internal_txns
        self.method_invoked = method_invoked
        self.tokens_transferred = tokens_transferred
        self.events_emitted = events_emitted

    def __str__(self):
        return f"""Transaction:
        - Transaction hash: {self.txn_hash}
        - Status: {self.status}
        - Time stamp: {util.convert_linux_timestamp(self.timestamp)}
        - From account: {self.from_account}
        - To account: {self.to_account}
        - Block number: {self.block_num}
        - ETH value: {self.value}
        - Gas: {self.gas}
        - Chain Id: {self.chain_id}
        - Block Id: {self.block_id}
        - Internation transactions: {[str(in_txn) for in_txn in self.internal_txns]}
        - Method invocation: {str(self.method_invoked)}
        - Tokens transferred: {[str(token) for token in self.tokens_transferred]}
        - Events emitted: {[str(event) for event in self.events_emitted]}
        """

    def __eq__(self, other):
        return self.txn_hash == other.txn_hash and self.chain_id == other.chain_id

    def __hash__(self):
        return hash((self.txn_hash, self.chain_id))
