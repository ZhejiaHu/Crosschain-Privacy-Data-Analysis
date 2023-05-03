from typing import List


class EventLog:
    def __init__(self, event_idx, contract_address, topics: List[str],  data: str, txn_hash, chain_id):
        self.event_idx = event_idx
        self.contract_address = contract_address
        self.topics: List[str] = topics
        self.data: str = data
        self.txn_hash = txn_hash
        self.chain_id = chain_id

    def __str__(self):
        return f"""Event Log:
                -- Event Index: {self.event_idx}
                -- Contract address: {self.contract_address}
                -- Topics: {self.topics}
                -- Data: {self.data}
                -- Transaction Hash: {self.txn_hash}
                -- Chain Id: {self.chain_id}
        
        """


class TypeDecoder:
    @staticmethod
    def decode():
        pass

