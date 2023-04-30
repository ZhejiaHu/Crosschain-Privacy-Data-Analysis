from model import Transaction
from requests import get
from .setup import get_handler
import util

handler = get_handler()
INTERNAL_TXN_HASH = "OxFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF"


def parse_transaction_json(txn_json, status, chain_id, not_internal=True):
    internal_txns = []
    if not_internal: internal_txns = get_internal_transaction_from_transaction_hash(txn_json["hash"] if not_internal else INTERNAL_TXN_HASH, chain_id)
    return Transaction(txn_json["hash"] if not_internal else INTERNAL_TXN_HASH, status, txn_json["timeStamp"], txn_json["from"], txn_json["to"], txn_json["timeStamp"], txn_json["value"], txn_json["gas"], chain_id, internal_txns)


def get_transaction_from_transaction_hash(txn_hash):
    metadata, receipt = handler.get_transaction(txn_hash), handler.get_transaction_receipt(txn_hash)
    return Transaction(metadata.hash, receipt.status, handler.get_block(metadata.blockNumber).timestamp, metadata["from"], metadata.to, 1, metadata.blockNumber, metadata.value, metadata.gas)  # status is dummy for now


def get_internal_transaction_from_transaction_hash(txn_hash, chain_id):
    query = util.QUERY_TXN_URL_TEMPLATE.format(util.CHAINSCAN_URL[chain_id], "txlistinternal", txn_hash, util.CHAINSCAN_API[chain_id])
    response = get(query)
    if response.status_code != 200 or not util.is_valid_data(response.json()): return []
    inter_txns = []
    for txn_json in response.json()["result"]: inter_txns.append(parse_transaction_json(txn_json, response.json()["status"], chain_id, not_internal=False))
    return inter_txns
