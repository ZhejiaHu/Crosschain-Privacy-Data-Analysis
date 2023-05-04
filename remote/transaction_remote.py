from model import Transaction, MethodInvocation, TokenTransfer, TokenType, EventLog
from requests import get
from remote.setup import get_handler
from threading import Thread
import util

handler = get_handler()
INTERNAL_TXN_HASH = "OxFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF"


def parse_transaction_json(txn_json, status, chain_id, not_internal=True):
    internal_txns = get_internal_transaction_from_transaction_hash(txn_json["hash"] if not_internal else INTERNAL_TXN_HASH, chain_id) if not_internal else []
    method_called = MethodInvocation(txn_json["hash"], txn_json["to"], txn_json["methodId"], txn_json["input"]) if "methodId" in txn_json.keys() and txn_json["methodId"] != "0x" else None
    # tokens = get_token_swap_from_transaction_hash(txn_json["hash"], txn_json["blockNumber"], txn_json["from"], chain_id, TokenType.T20) if not_internal else [] + \
    events_emitted = get_event_log_from_transaction_hash(txn_json["hash"], chain_id)
    return Transaction(txn_json["hash"] if not_internal else INTERNAL_TXN_HASH, status,
                       txn_json["timeStamp"],
                       txn_json["from"],
                       txn_json["to"],
                       txn_json["value"],
                       txn_json["gas"],
                       chain_id,
                       txn_json["blockNumber"],
                       internal_txns=internal_txns,
                       method_invoked=method_called,
                       events_emitted=events_emitted)


def get_transaction_from_transaction_hash(txn_hash, chain_id):
    print(f"Currently getting transaction {txn_hash}.")
    metadata, receipt = handler.get_transaction(txn_hash), handler.get_transaction_receipt(txn_hash)
    return Transaction(txn_hash,
                       receipt.status,
                       handler.get_block(metadata.blockNumber).timestamp,
                       metadata["from"],
                       metadata.to,
                       metadata.blockNumber,
                       metadata.value,
                       metadata.gas,
                       chain_id,
                       internal_txns=get_internal_transaction_from_transaction_hash(metadata.hash, chain_id),
                       events_emitted=get_event_log_from_transaction_hash(txn_hash, chain_id))


def get_internal_transaction_from_transaction_hash(txn_hash, chain_id):
    query = util.QUERY_TXN_URL_TEMPLATE.format(util.CHAINSCAN_URL[int(chain_id)], "txlistinternal", txn_hash, util.CHAINSCAN_API[int(chain_id)])
    response = get(query)
    if response.status_code != 200 or not util.is_valid_data(response.json()): return []
    inter_txns = []
    for txn_json in response.json()["result"]: inter_txns.append(parse_transaction_json(txn_json, response.json()["status"], chain_id, not_internal=False))
    return inter_txns


def get_token_swap_from_transaction_hash(txn_hash, block_num, initial_account, chain_id, token_type: TokenType):
    account_visited = set()

    def depth_first_search(from_account):
        account_visited.add(from_account)
        action = "tokentx" if token_type == TokenType.T20 else "tokennfttx"
        query = util.QUERY_ACCOUNT_URL_TEMPLATE.format(util.CHAINSCAN_URL[chain_id], action, from_account, util.CHAINSCAN_API[chain_id]) + util.QUERY_INFO.format(block_num, block_num)
        response = get(query)
        if response.status_code != 200 or not util.is_valid_data(response.json()): return []
        map_to_token_receiver = lambda jsn: (TokenTransfer(token_type, jsn["tokenName"], jsn["tokenSymbol"], jsn["tokenDecimal"], jsn["tokenID"] if "tokenID" in jsn else None, jsn["value"] if "value" in jsn else None, txn_hash, jsn["from"], jsn["to"]), jsn["to"])
        filter_token = lambda jsn: jsn["hash"] == txn_hash
        current_token_transfers_ = list(map(map_to_token_receiver, filter(filter_token, response.json()["result"])))
        current_token_transfers, receivers = list(map(lambda tr: tr[0], current_token_transfers_)), set(map(lambda tr: tr[1], current_token_transfers_))
        for receiver in receivers:
            if receiver in account_visited: continue
            current_token_transfers.extend(depth_first_search(receiver))
        return current_token_transfers
    return set(depth_first_search(initial_account))


def get_transactions_from_latest_block(chain_id):
    latest_txn_hashes = handler.get_block(handler.get_block_number())["transactions"][:50]
    print(len(latest_txn_hashes))
    return list(map(lambda th: get_transaction_from_transaction_hash(th.hex(), chain_id), latest_txn_hashes))


def get_event_log_from_transaction_hash(txn_hash, chain_id):
    logs = handler.get_transaction_receipt(txn_hash).logs
    return list(map(lambda log: EventLog(log["logIndex"], log["address"], list(map(lambda hx: hx.hex(), log["topics"])), log["data"].hex(), txn_hash, chain_id), logs))

