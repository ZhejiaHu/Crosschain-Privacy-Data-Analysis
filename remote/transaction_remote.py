from model import Transaction
from .setup import get_handler

handler = get_handler()


def parse_transaction_json(txn_json, status, net):
    return Transaction(txn_json["hash"], status, txn_json["timeStamp"], txn_json["from"], txn_json["to"], net, txn_json["timeStamp"], txn_json["value"], txn_json["gas"])


def get_transaction_from_transaction_hash(txn_hash):
    metadata, receipt = handler.get_transaction(txn_hash), handler.get_transaction_receipt(txn_hash)
    return Transaction(metadata.hash, receipt.status, handler.get_block(metadata.blockNumber).timestamp, metadata["from"], metadata.to, 1, metadata.blockNumber, metadata.value, metadata.gas)  # status is dummy for now
