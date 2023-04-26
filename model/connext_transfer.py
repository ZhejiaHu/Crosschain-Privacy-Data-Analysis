from .transaction import Transaction


class ConnextTransfer:
    def __init__(self, transfer_id, origin_txn: Transaction, destination_txn: Transaction):
        self.transfer_id = transfer_id
        self.origin_txn = origin_txn
        self.destination_txn = destination_txn

    def __str__(self):
        return f"Context Transfer: {self.transfer_id}\n  Origin Transaction: {str(self.origin_txn)}\n  Source Transaction: {str(self.destination_txn)}"

    def __eq__(self, other):
        return self.transfer_id == other.transfer_id

    def __hash__(self):
        return hash(self.transfer_id)
