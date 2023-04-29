import util


class Transaction:
    def __init__(self, txn_hash, status, timestamp, from_account, to_account, block_num, value, gas, chain_id):
        self.txn_hash = txn_hash
        self.status = status
        self.timestamp = timestamp
        self.from_account = from_account
        self.to_account = to_account
        self.block_num = block_num
        self.value = value
        self.gas = gas
        self.chain_id = chain_id

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
        """

    def __eq__(self, other):
        return self.txn_hash == other.txn_hash and self.chain_id == other.chain_id

    def __hash__(self):
        return hash((self.txn_hash, self.chain_id))

