import util


class Transaction:
    def __init__(self, txn_hash, status, timestamp, from_account, to_account, net, block_num, value, gas):
        self.txn_hash = txn_hash
        self.status = status
        self.timestamp = timestamp
        self.from_account = from_account
        self.to_account = to_account
        self.net = net
        self.block_num = block_num
        self.value = value
        self.gas = gas

    def __str__(self):
        return f"""Transaction:
        - Transaction hash: {self.txn_hash}
        - Status: {self.status}
        - Time stamp: {util.convert_linux_timestamp(self.timestamp)}
        - From account: {self.from_account}
        - To account: {self.to_account}
        - Net: {self.net}
        - Block number: {self.block_num}
        - ETH value: {self.value}
        - Gas: {self.gas}
        """

