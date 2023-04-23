from model import Transaction


def parse_transaction_json(txn_json, status, net):
    return Transaction(txn_json["hash"], status, txn_json["timeStamp"], txn_json["from"], txn_json["to"], net, txn_json["timeStamp"], txn_json["value"], txn_json["gas"])
