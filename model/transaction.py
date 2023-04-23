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


